import csv
import json
import requests
import os, math

API_KEY = ''
PASSWORD = ''
SHOP_NAME = ''

shop_url = "https://%s:%s@%s.myshopify.com/admin/" % (API_KEY, PASSWORD, SHOP_NAME)

params = {'limit': 250}

count = requests.get(shop_url + '/products/count.json').json().get('count')
print(count)
pages = math.ceil(count/250)
num = 0


#next = solditems.headers['Link']
#next = next.replace('"', '')
#next = next.replace('>; rel=next', '')
#next = next.replace('<', '')

#print(next)

f = csv.writer(open("test.csv", "w"))

f.writerow(["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Variant Barcode", "Image Src", "Image Position", "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Google Shopping / Google Product Category", "Google Shopping / Gender", "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / AdWords Grouping", "Google Shopping / AdWords Labels", "Google Shopping / Condition", "Google Shopping / Custom Product", "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2", "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4", "Variant Image", "Variant Weight Unit", "Variant Tax Code", "Cost per item"])
for page in range(1, pages+1):

	solditems = requests.get(shop_url + '/admin/products.json',params={'page': page, **params})
	x = solditems.json()

	for item in x["products"]:
		for d in item["variants"]:
			price = d["price"]
			sku = d["sku"]
			grams = d["grams"]
			inventory_quantity = d["inventory_quantity"]
	
		for e in item["images"]:
			image = e["src"]
		
		f.writerow([item["handle"],item["title"],"",item["vendor"],item["product_type"],item["tags"],"","","","","","","",sku,grams,"shopify",inventory_quantity,"deny","manual",price,"","TRUE","TRUE","",image,"1","","False"])
	num += 1