import frappe

@frappe.whitelist()
def sort_delivery_order(docname):
    to_sort = []
    cur = frappe.get_doc("Delivery Trip", docname)
    for i in cur.table:
        to_sort.append(i.distance)

    # frappe.msgprint(str(sorted(to_sort)))
    i = 0
    for a in sorted(to_sort):
        i+=1
        # frappe.msgprint(str(i) + ": : " + str(a))
        for d in cur.table:
            if d.distance == a:
                d.idx = i

    cur.save()