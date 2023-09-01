import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    to_sort = []
    cur = frappe.get_doc("Delivery Trip", docname)
    for i in cur.table:
        to_sort.append(i.distance)

    # frappe.msgprint(str(sorted(to_sort)))

    for i,a in sorted(to_sort):
        frappe.msgprint(i + ": : " + a)

