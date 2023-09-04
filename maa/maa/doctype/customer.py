# Copyright (c) 2023, InshaSiS Technologies and contributors
# For license information, please see license.txt

import frappe

def validate(doc,method):
    maa_coins_wallet = frappe.get_doc({
		"doctype": "MAA Coins Wallet",
		"customer": doc.name,
		"coins": 0,
		
	})
    maa_coins_wallet.save()
    frappe.msgprint("Create Coin Wallet Account")
		
