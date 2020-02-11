import csv
import json
import requests
import math
import os

# Environment variables
if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

f = csv.writer(open("shipping-zones.csv", "w"))

s_shipping_zones = requests.get('https://' + os.getenv('SHOPIFY_API_KEY') + ':' + os.getenv('SHOPIFY_API_PASSWORD') + '@' + os.getenv('SHOPIFY_URL') + '.myshopify.com/admin/shipping_zones.json')
x = s_shipping_zones.json()
price = 0

for item in x["shipping_zones"]:
	f.writerow(["Country"])
	f.writerow(["-------"])
	f.writerow([item["name"]])
	f.writerow(["-------"])
	for y in item["countries"]:
		f.writerow(["Provinces"])
		f.writerow(["-------"])
		for z in y["provinces"]:
			f.writerow([z["name"]])
			for w in item["weight_based_shipping_rates"]:
				price = w["price"]
				
	f.writerow([price])
			
	f.writerow([])
	f.writerow([])