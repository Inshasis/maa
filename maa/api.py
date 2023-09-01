import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    cur = frappe.get_doc("Delivery Trip", docname)
    print(str(cur.table))

    for i, item in enumerate(sorted(cur.table, key=lambda item: item.distance), start=1):
        item.idx = i
        frappe.msgprint(i)
