import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    cur = frappe.get_doc("Delivery Trip", docname)
    frappe.msgprint(cur)

    for i, item in enumerate(sorted(cur.table._range, key=lambda item: item.distance), start=1):
        item.idx = i
        frappe.msgprint(i)
