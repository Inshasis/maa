# Copyright (c) 2023, InshaSiS Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import formatdate, get_datetime, getdate, nowdate, add_days


def validate(doc,method = None):
	if doc.status == "Completed":
		exist = frappe.db.get_value("MAA Coins Transaction", {"transaction_type":"Credit", "reference_doctype":"Order", "reference_docname":doc.name}, "name")
		expiry_in_days = 0
		if not exist:
			cashback_percentage = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type": "Percentage"},"cashback_percentage")
			max_cashback_on_percentage = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type": "Percentage"},"max_coins_to_be_given")
			max_cashback_on_amount = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type": "Amount"},"max_coins_to_be_given")
			cashback_amount = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type":"Amount"},"up_front_amount")
			
			referred_customer = frappe.get_doc("Customer", doc.customer_id)
			coin_wallet_acc_referred = frappe.db.get_value('MAA Coins Wallet',{'customer': referred_customer.name},'name')
			if cashback_percentage or cashback_amount:
				if cashback_percentage:
					expiry_in_days = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type": "Percentage"},"expiry_in_days")
					cashback_multiplyer = cashback_percentage * 0.01
					cashback_coins = cashback_multiplyer * float(doc.total_mrp)
					if cashback_coins > max_cashback_on_percentage:
						cashback_coins = max_cashback_on_percentage
				else:
					expiry_in_days = frappe.db.get_value("MAA Coins Settings", {"status":"Enable","min_order_value":["<=",doc.total_mrp],"max_order_value":[">=", doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date],"cashback_type": "Amount"},"expiry_in_days")
					cashback_multiplyer = cashback_amount * 0.01
					cashback_coins = cashback_multiplyer * float(doc.total_mrp)
					if cashback_coins > max_cashback_on_amount:
						cashback_coins = max_cashback_on_amount

					
				cashback_coins_added = frappe.get_doc({
					"doctype": "MAA Coins Transaction",
						"coins_wallet": coin_wallet_acc_referred,
						"transaction_type": "Credit",
						"transaction_method": "Settle in Order",
						"transaction_coins": int(cashback_coins),
						"unused_coins": int(cashback_coins),
						"transaction_date": nowdate(),
						"coins_expiration_date": frappe.utils.add_days(frappe.utils.getdate(nowdate()),expiry_in_days),
						"reference_doctype": "Order",
						"reference_docname": doc.name
					})
				cashback_coins_added.insert()
				# cashback_coins_added.save()
				frappe.msgprint("Cashback Coins Added!")

			if referred_customer.referred_by:
				percent_of_order = frappe.db.get_value("Refer and Earn Setting",{"disable":0,"is_order_first_delivered_order":1,"min_order_value":["<=",doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date]},"percentage_of_order_value")
				refer_expiry_in_days = frappe.db.get_value("Refer and Earn Setting",{"disable":0,"is_order_first_delivered_order":1,"min_order_value":["<=",doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date]},"expiry_in_days")
				# upfront_amount = frappe.db.get_value("Refer and Earn Setting",{"disable":0,"is_order_first_delivered_order":1,"min_order_value":["<=",doc.total_mrp],"valid_from":["<=",doc.order_date], "valid_to":[">=",doc.order_date]},"upfront_amount")
				if percent_of_order:
					referred_customer = frappe.get_doc("Customer", doc.customer_id)
					if not referred_customer.first_order_redeemed:
						referred_customer.first_order_redeemed = 1
						referred_customer.save()
						referred_by = frappe.get_doc("Customer", referred_customer.referred_by)
						coin_wallet_acc = frappe.db.get_value('MAA Coins Wallet',{'customer': referred_by.name},'name')
						multiplyer = percent_of_order * 0.01
						coins = multiplyer * float(doc.total_mrp)
						coins_added = frappe.get_doc({
							"doctype": "MAA Coins Transaction",
							"coins_wallet": coin_wallet_acc,
							"transaction_type": "Credit",
							"transaction_method": "Refer&Earn",
							"transaction_coins": int(coins),
							"unused_coins": int(coins),
							"transaction_date": nowdate(),
							"coins_expiration_date": frappe.utils.add_days(frappe.utils.getdate(nowdate()),refer_expiry_in_days),
							"reference_doctype": "Order",
							"reference_docname": doc.name
							})
						coins_added.insert()
						# coins_added.save()
						frappe.msgprint("Referral Points Added!")
					
