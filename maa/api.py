import frappe
import json

@frappe.whitelist()
def get_distance_and_sort(doc, method):
    to_sort = []
    #Jethipura Address Log
    latitude = "23.7625575" #29.44671
    longitude = "72.9234269" #77.3515
    for a in doc.table:
        url = "https://api.distancematrix.ai/maps/api/distancematrix/json?origins='" + latitude + "+" + longitude + "&destinations=" + a.latitude + "+" + a.longitude + "&mode=driving&departure_time=now&key=bUNDH50AQXySHRt6qzMdirw8a8rkl"
        response = frappe.frappe.make_get_request(url)
        resp = json.load(response)
        a.distance = resp['rows']['0']['elements']['0']['distance']['text']
        a.estimated_delivery_time = resp['rows']['0']['elements']['0']['duration']['text']
        to_sort.append(a.distance)
        frappe.msgprint(a.estimated_delivery_time)
    i = 0
    for a in sorted(to_sort):
        i+=1
        # frappe.msgprint(str(i) + ": : " + str(a))
        for d in doc.table:
            if d.distance == a:
                d.idx = i

    cur.save()

    # def get_distance_and_sort(docname):
    
    # to_sort = []
    # cur = frappe.get_doc("Delivery Trip", docname)
    # for i in cur.table:
    #     to_sort.append(i.distance)

    # # frappe.msgprint(str(sorted(to_sort)))
    # i = 0
    # for a in sorted(to_sort):
    #     i+=1
    #     # frappe.msgprint(str(i) + ": : " + str(a))
    #     for d in cur.table:
    #         if d.distance == a:
    #             d.idx = i

    # cur.save()