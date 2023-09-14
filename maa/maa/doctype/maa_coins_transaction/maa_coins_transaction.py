# Copyright (c) 2023, InshaSiS Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class MAACoinsTransaction(Document):
	# pass

	def before_insert(self):
		if self.transaction_type == "Debit":
			check = frappe.db.get_value("MAA Coins Wallet", {'name':self.coins_wallet}, 'coins')
			if check <= 0:
				frappe.throw("Coins not Enough for this transaction!")
	def after_insert(self):
		coin_wallet = frappe.db.get_value('MAA Coins Wallet',{'name':self.coins_wallet},'coins')
		if self.transaction_type == 'Credit':
			sum_coin = int(coin_wallet) + int(self.transaction_coins) 
		elif self.transaction_type == 'Debit':
			update_used_coins(self)
			sum_coin = int(coin_wallet) - int(self.transaction_coins) 
			
		# Update Coins in MAA Coins coin_wallet
		frappe.db.set_value('MAA Coins Wallet', self.coins_wallet, {
			'coins': sum_coin
		})
		# Update Coins in Customer
		frappe.db.set_value('Customer', self.customer, {
			'total_coins': sum_coin
		})
		

def update_used_coins(self):
	if self.transaction_type == "Debit":
		credit = frappe.db.get_all("MAA Coins Transaction", filters={"coins_wallet": self.coins_wallet, "transaction_type": "Credit", "coins_status":"Valid", "coins_used": 0}, fields=["*"])
		to_be_debited = self.transaction_coins
		if credit:
			credit.reverse()
			for c in credit:
				doc = frappe.get_doc("MAA Coins Transaction", c.name)
				if to_be_debited > 0:
					if to_be_debited >= doc.unused_coins:
						doc.unused_coins = int(0)
						doc.coins_used = 1
						to_be_debited -= doc.transaction_coins
					else:
						doc.unused_coins = doc.unused_coins - to_be_debited
						to_be_debited = int(0)

					self.append("coins_transaction", {
						"maa_coins_transaction": doc.name,
						"transaction_type": doc.transaction_type,
						"transaction_coins": doc.transaction_coins,
						"debited_coins": doc.transaction_coins - doc.unused_coins
					})
				else:
					break
				doc.save()
			self.save()

def check_expiry_date():	
	coins_tran = frappe.db.get_all("MAA Coins Transaction",filters={},fields=["*"])
	for tran in coins_tran:
		doc = frappe.get_doc("MAA Coins Transaction",tran.name)
		if str(doc.coins_expiration_date) == str(frappe.utils.today()) and str(doc.coins_status) == "Valid":
			frappe.msgprint("Expired")
			doc.coins_status = "Expired"
			doc.save()
			doc = frappe.get_doc("MAA Coins Transaction",tran.name)
			if not doc.coins_used:
				debit_entry = frappe.get_doc({
					"doctype": "MAA Coins Transaction",
					"coins_wallet": doc.coins_wallet,
					"transaction_type": "Debit",
					"transaction_method": "Credit/Debit by Admin",
					"transaction_coins": int(doc.unused_coins),
					"transaction_date": nowdate(),
					"reference_doctype": "MAA Coins Transaction",
					"reference_docname": doc.name
				})
				debit_entry.insert()
				