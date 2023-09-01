import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    to_sort = []
    cur = frappe.get_doc("Delivery Trip", docname)
    for i in cur.table:
        to_sort.append(i.distance)

    frappe.msgprint(str(to_sort))

    # for i, item in enumerate(sorted(cur.table, key=lambda item: item.distance), start=1):
    #     item.idx = i
    #     frappe.msgprint(i)
