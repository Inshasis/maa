import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    cur = frappe.get_doc("Delivery Trip", docname)
    for item in sorted(cur.table, key=lambda x:x["distance"]):
        frappe.msgprint(item)
