# Copyright (c) 2023, InshaSiS Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MAACoinsTransaction(Document):
	# pass

	def after_insert(self):
		if self.transaction_type == 'Credit':
			coin_wallet = frappe.db.get_value('MAA Coins Wallet',{'name':self.coins_wallet},'coins')
			frappe.msgprint(str(coin_wallet))
			sum_coin = int(coin_wallet) + int(self.transaction_coins) 
			# Update Coins in MAA Coins coin_wallet
			frappe.db.set_value('MAA Coins Wallet', self.coins_wallet, {
				'coins': sum_coin
			})
			# Update Coins in Customer
			frappe.db.set_value('Customer', self.customer, {
				'total_coins': sum_coin
			})
			# frappe.msgprint("Coins Credit Sucessfull {0}".format(self.coins_wallet))
		else:
			coin_wallet = frappe.db.get_value('MAA Coins Wallet',{'name':self.coins_wallet},'coins')
			sum_coin = int(coin_wallet) - int(self.transaction_coins) 
			# Update Coins in MAA Coins coin_wallet
			frappe.db.set_value('MAA Coins Wallet', self.coins_wallet, {
				'coins': sum_coin
			})

			# Update Coins in Customer
			frappe.db.set_value('Customer', self.customer, {
				'total_coins': sum_coin
			})
			# frappe.msgprint("Coins Debit Sucessfull {0}".format(self.coins_wallet))
