import csv
import json
import requests
import os

# Environment variables
if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

url = 'https://' + os.getenv('SHOPIFY_URL') + '.myshopify.com/admin/api/2020-01/'

params = {'limit': 250}
page_number = 1
count = requests.get(url + 'products/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Products: #{count}".format(count=count))

products = requests.get(url + 'products.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("products.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position", "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category", "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels", "Google Shopping / Condition", "Google Shopping / Custom Product", "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4", "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item"])

while products:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = products.json()
		for item in x["products"]:
			for d in item["variants"]:
				price = d["price"]
				sku = d["sku"]
				grams = d["grams"]
				inventory_quantity = d["inventory_quantity"]
			
			if len(item["images"]) == 0:
				image = ""
			
			for e in item["images"]:
				image = e["src"]
			f.writerow([item["handle"],item["title"],"",item["vendor"],item["product_type"],item["tags"],"","","","","","","",sku,grams,"shopify",inventory_quantity,"deny","manual",price,"","TRUE","TRUE","",image,"1","","False"])

		products = products.links['next']['url']
		products = requests.get(products,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		products = ""

	page_number += 1