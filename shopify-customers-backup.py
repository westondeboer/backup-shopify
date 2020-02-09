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
count = requests.get(url + 'customers/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Customers: #{count}".format(count=count))

customers = requests.get(url + 'customers.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("customers.csv", "w"))

f.writerow([
"First Name",
"Last Name",
"Email",
"Company",
"Address1",
"Address2",
"City",
"Province",
"Province Code",
"Country",
"Country Code",
"Zip",
"Phone",
"Accepts Marketing",
"Total Spent",
"Total Orders",
"Tags",
"Note",
"Tax Exempt",
])


while customers:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = customers.json()

		for item in x["customers"]:
	
			for a in item["addresses"]:
				company = a["company"]
		
			f.writerow([		
		item["first_name"],
		item["last_name"],
		item["email"],
		a["company"],
		a["address1"],
		a["address2"],
		a["city"],
		a["province"],
		a["province_code"],
		a["country"],
		a["country_code"],
		a["zip"],
		a["phone"],
		item["marketing_opt_in_level"],
		item["total_spent"],
		item["orders_count"],
		item["tags"],
		item["note"],
		item["tax_exempt"],
			])
			
		customers = customers.links['next']['url']
		customers = requests.get(customers,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		products = ""

	page_number += 1