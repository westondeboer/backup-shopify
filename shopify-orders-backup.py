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
count = requests.get(url + 'orders/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Orders: #{count}".format(count=count))

orders = requests.get(url + 'orders.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("orders.csv", "w"))

f.writerow(["Name","Email","Financial Status","Paid at","Fulfillment Status","Fulfilled at","Accepts Marketing","Currency",
"Subtotal",
"Shipping",
"Taxes",
"Total",
"Discount Code",
"Discount Amount",
"Shipping Method",
"Created at",
"Lineitem quantity",
"Lineitem name",
"Lineitem price",
"Lineitem compare at price",
"Lineitem sku",
"Lineitem requires shipping",
"Lineitem taxable",
"Lineitem fulfillment status",
"Billing Name",
"Billing Street",
"Billing Address1",
"Billing Address2",
"Billing Company",
"Billing City",
"Billing Zip",
"Billing Province",
"Billing Country",
"Billing Phone",
"Shipping Name",
"Shipping Street",
"Shipping Address1",
"Shipping Address2",
"Shipping Company",
"Shipping City",
"Shipping Zip",
"Shipping Province",
"Shipping Country",
"Shipping Phone",
"Notes",
"Note Attributes",
"Cancelled at",
"Payment Method",
"Payment Reference",
"Refunded Amount",
"Vendor",
"Outstanding Balance",
"Employee",
"Location",
"Device ID",
"Id",
"Tags",
"Risk Level",
"Source",
"Lineitem discount",
"Tax 1 Name",
"Tax 1 Value",
"Tax 2 Name",
"Tax 2 Value",
"Tax 3 Name",
"Tax 3 Value",
"Tax 4 Name",
"Tax 4 Value",
"Tax 5 Name",
"Tax 5 Value",
"Phone",
"Receipt Number",
])

while orders:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = orders.json()
		for item in x["orders"]:	
			order_num = 0
				
			for y in item["line_items"]:
					shipping_price = item["total_shipping_price_set"]["shop_money"]["amount"]
				
					fin = item["financial_status"]
						
					if order_num == 0:
								fin = item["financial_status"]
								paid_at = item["created_at"]
								full = item["fulfillment_status"]
								marketing = item["buyer_accepts_marketing"]
								curr = item["currency"]
								sub = item["subtotal_price"]
								total_tax = item["total_tax_set"]["shop_money"]["amount"]
								total_p = item["total_price"]
					else:
								fin = ""
								
					order_num += 1
						
					f.writerow(
				[item["name"],
				item["email"],
				fin,
				paid_at,
				full,
				"fulfilled at",
				marketing,
				curr,
				sub,
				shipping_price,
				total_tax,
				total_p,
				item["discount_codes"],
				item["total_discounts"],
				"Shipping Lines",
				"Created at",
				y["quantity"],
				y["name"],
				y["price"],
				"Lineitem compare at price",
				y["sku"],
				y["requires_shipping"],
				y["taxable"],
				y["fulfillment_status"],
				item["billing_address"]["first_name"] + ' ' + item["billing_address"]["last_name"],
				item["billing_address"]["address1"],
				item["billing_address"]["address1"],
				item["billing_address"]["address2"],
				item["billing_address"]["company"],
				item["billing_address"]["city"],
				item["billing_address"]["zip"],
				item["billing_address"]["province"],
				item["billing_address"]["country"],
				item["billing_address"]["phone"],
				#item["shipping_address"]["first_name"] + ' ' + item["shipping_address"]["last_name"],
				#item["shipping_address"]["address1"],
				#item["shipping_address"]["address1"],
				#item["shipping_address"]["address2"],
				#item["shipping_address"]["company"],
				#item["shipping_address"]["city"],
				#item["shipping_address"]["zip"],
				#item["shipping_address"]["province"],
				#item["shipping_address"]["country"],
				#item["shipping_address"]["phone"],
				item["note"],
				"Note Attributes",
				"Cancelled at",
				item["gateway"],
				"Payment Reference",
				"Refunded Amount",
				y["vendor"],
				"Outstanding Balance",
				"Employee",
				"Location",
				"Device ID",
				item["id"],
				item["tags"],
				"Risk Level",
				item["source_name"],
				"Lineitem discount",
				"Tax 1 Name",
				"Tax 1 Value",
				"Tax 2 Name",
				"Tax 2 Value",
				"Tax 3 Name",
				"Tax 3 Value",
				"Tax 4 Name",
				"Tax 4 Value",
				"Tax 5 Name",
				"Tax 5 Value",
				item["phone"],
				"Receipt",
					])
		orders = orders.links['next']['url']
		orders = requests.get(orders,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		orders = ""

	page_number += 1