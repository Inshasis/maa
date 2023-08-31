import frappe
from math import cos, asin, sqrt, pi


def validate(doc,method):
    distance(doc)

def distance(doc):
    lat2 = 29.451550
    lon2 = 77.316391
    lat1 = float(doc.latitude)
    lon1 = float(doc.longitude)
    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    frappe.msgprint("CALLED")
    frappe.msgprint(str(2 * r * asin(sqrt(a))))
    # return 2 * r * asin(sqrt(a))