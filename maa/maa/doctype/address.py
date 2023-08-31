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
    check_distance = 0.0
    distance = 0.0
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    distance = (2 * r * asin(sqrt(a)))

    check_distance = frappe.db.get_single_value("MAA Distance Setting", "delivery_distance")
    if distance < check_distance:
        doc.in_range = 1
        doc.save()