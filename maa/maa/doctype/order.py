# Copyright (c) 2023, InshaSiS Technologies and contributors
# For license information, please see license.txt

import frappe


def validate(doc,method = None):
	if doc.status == "Completed":
		percent_of_order = frappe.db.get_value("Refer and Earn Setting",{"is_order_first_delivered_order":1,"min_order_value":["<=",doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date]},"percentage_of_order_value")
		referred_customer = frappe.get_doc("Customer", doc.customer_id)
		if not referred_customer.first_order_redeemed:
			referred_by = frappe.get_doc("Customer", referred_customer.referred_by)
			coin_wallet_acc = frappe.db.get_value('MAA Coins Wallet',{'customer': referred_by.name},'name')
			multiplyer = percent_of_order * 0.01
			coins = multiplyer * float(doc.total_mrp)
			frappe.msgprint(coin_wallet_acc)
			coins_added = frappe.get_doc({
				"doctype": "MAA Coins Transaction",
				"coins_wallet": coin_wallet_acc,
				"transaction_type": "Credit",
				"transaction_method": "Refer&Earn",
				"transaction_coins": int(coins),
				"reference_doctype": "Order",
				"reference_docname": doc.name
				})
			coins_added.insert()
			coins_added.save()
			frappe.msgprint("Referral Points Added!")
			referred_customer.first_order_redeemed = 1
			referred_customer.save()


# def validate(doc,method):
# 	if doc.delivery_mode == "Delivery":
# 		ref_code = frappe.db.get_value('Customer',doc.customer_id,'enter_referred_code')
# 		if ref_code:
# 			cust_name = frappe.db.get_value('Customer', {'enter_referred_code': ref_code}, 'referred_by')
# 			coin_wallet_acc = frappe.db.get_value('MAA Coins Wallet',{'customer': cust_name},'name')
# 			maa_coins_transaction = frappe.get_doc({
# 			"doctype": "MAA Coins Transaction",
# 			"coins_wallet": coin_wallet_acc,
# 			"transaction_type": "Credit",
# 			"transaction_method": "Refer&Earn",
# 			"transaction_coins": 10,
# 			"reference_doctype": "Order",
# 			"reference_docname": doc.name,
# 			})
# 			maa_coins_transaction.insert()
# 			maa_coins_transaction.save()
# 			frappe.msgprint("Coin Transfer Succesfully!")
# 		else:
# 			frappe.msgprint("Please Add Referr By In Customer")

	
	
	# frappe.msgprint("Create Coin Wallet Account")
		
