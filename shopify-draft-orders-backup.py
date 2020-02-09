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
count = requests.get(url + 'draft_orders/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Draft Orders: #{count}".format(count=count))

draft_orders = requests.get(url + 'draft_orders.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("draft-orders.csv", "w"))

f.writerow(["Name",
"ID",
"Email",
"Status",
"Currency",
"Discount Amount",
"Subtotal",
"Shipping",
"Taxes",
"Taxes Included",
"Total",
"Shipping Method",
"Custom Shipping",
"Total Weight",
"Created At",
"Item Quantity",
"Item name",
"Item price",
"Item Total Discount",
"Item Total Price",
"Lineitem sku",
"Lineitem requires shipping",
"Lineitem taxable",
"Vendor",
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
"Invoice Sent At",
"Complete At",
"Order ID",
"Notes",
"Note Attributes",
"Tags",
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
])

while draft_orders:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = draft_orders.json()
	
		for item in x["draft_orders"]:
				
			order_num = 0
				
			for y in item["line_items"]:
					taxnum = 0
				
					if item["shipping_line"] is not None:
						shipping_price = item["shipping_line"]["price"]
						shipping_title = item["shipping_line"]["title"]
						shipping_custo = item["shipping_line"]["custom"]
					else:
						shipping_price = ""
						shipping_title = ""
						shipping_custo = ""
				
					fin = item["status"]
				
					l = list(y["tax_lines"])
					taxnum = len(l)
				
					if order_num == 0 and item["note_attributes"]:
						note_attribute = item["note_attributes"]
					else:
						note_attribute = None
				
					grams = 0
					if order_num == 0:
						for g in item["line_items"]:
							grams += g["grams"]
					else:
						grams = None
				
					if(taxnum > 0):
						if order_num == 0:
							tax_1_n = y["tax_lines"][0]["title"]
							tax_1_v = y["tax_lines"][0]["rate"]
							tax_1_v = round(float(item["subtotal_price"]) * float(tax_1_v),2)
						else:
							tax_1_n = ""
							tax_1_v = ""
				
						## Tax Rate and Name 2
						if order_num == 0 and taxnum > 1:
							tax_2_n = y["tax_lines"][1]["title"]
							tax_2_v = y["tax_lines"][1]["rate"]
							tax_2_v = round(float(item["subtotal_price"]) * float(tax_2_v),2)
						else:
							tax_2_n = ""
							tax_2_v = ""
					
						## Tax Rate and Name 3
						if order_num == 0 and taxnum > 2:
							tax_3_n = y["tax_lines"][2]["title"]
							tax_3_v = y["tax_lines"][2]["rate"]
							tax_3_v = round(float(item["subtotal_price"]) * float(tax_3_v),2)
						else:
							tax_3_n = ""
							tax_3_v = ""
					
						## Tax Rate and Name 4
						if order_num == 0 and taxnum > 3:
							tax_4_n = y["tax_lines"][3]["title"]
							tax_4_v = y["tax_lines"][3]["rate"]
							tax_4_v = round(float(item["subtotal_price"]) * float(tax_4_v),2)
						else:
							tax_4_n = ""
							tax_4_v = ""
					
						## Tax Rate and Name 5
						if order_num == 0 and taxnum > 4:
							tax_5_n = y["tax_lines"][4]["title"]
							tax_5_v = y["tax_lines"][4]["rate"]
							tax_5_v = round(float(item["subtotal_price"]) * float(tax_5_v),2)
						else:
							tax_5_n = ""
							tax_5_v = ""
					else:
						tax_1_n = ""
						tax_1_v = ""
						tax_2_n = ""
						tax_2_v = ""
						tax_3_n = ""
						tax_3_v = ""
						tax_4_n = ""
						tax_4_v = ""
						tax_5_n = ""
						tax_5_v = ""
					
					
				
					if order_num == 0:
								fin = item["status"]
								paid_at = item["created_at"]
								curr = item["currency"]
								sub = item["subtotal_price"]
								total_tax = item["total_tax"]
								total_p = item["total_price"]
								o_id = item["id"]
								taxes_inc = item["taxes_included"]
								o_tags = item["tags"]
								
					else:
								fin = ""
								o_id = ""
								sub = ""
								total_tax = ""
								taxes_inc = ""
								total_p = ""
								o_tags = ""
				
					if y["applied_discount"]:
						applied_disc = y["applied_discount"]["amount"]
					else:
						applied_disc = "0"
				
					total_price = float(y["price"]) - float(applied_disc)
				
					if item["completed_at"] is not None and order_num == 0:
						completed_at = item["completed_at"]
					else:
						completed_at = ""
					
					if item["invoice_sent_at"] is not None and order_num == 0:
						sent_at = item["invoice_sent_at"]
					else:
						sent_at = ""
				
					if item["billing_address"] and order_num == 0:
						b_address_n = item["billing_address"]["name"]
						b_address_1 = item["billing_address"]["address1"]
						b_address_2 = item["billing_address"]["address2"]
						b_comp		= item["billing_address"]["company"]
						b_city		= item["billing_address"]["city"]
						b_zip		= item["billing_address"]["zip"]
						b_province	= item["billing_address"]["province"]
						b_country	= item["billing_address"]["country"]
						b_phone		= item["billing_address"]["phone"]
					else:
						b_address	= ""
						b_address_n = ""
						b_address_1 = ""
						b_address_2 = ""
						b_comp		= ""
						b_city		= ""
						b_zip		= ""
						b_province	= ""
						b_country	= ""
						b_phone		= ""
				
					if item["shipping_address"] and order_num == 0:
						s_name		= item["shipping_address"]["name"]
						s_address_n = item["shipping_address"]["name"]
						s_address_1 = item["shipping_address"]["address1"]
						s_address_2 = item["shipping_address"]["address2"]
						s_comp		= item["shipping_address"]["company"]
						s_city		= item["shipping_address"]["city"]
						s_zip		= item["shipping_address"]["zip"]
						s_province	= item["shipping_address"]["province"]
						s_country	= item["shipping_address"]["country"]
						s_phone		= item["shipping_address"]["phone"]
					else:
						s_name		= ""
						s_address_n = ""
						s_address_1 = ""
						s_address_2 = ""
						s_comp		= ""
						s_city		= ""
						s_zip		= ""
						s_province	= ""
						s_country	= ""
						s_phone		= ""
					
					order_num += 1
						
					f.writerow(
				[item["name"],
				o_id,
				item["email"],
				fin,
				curr,
				applied_disc,
				sub,
				shipping_price,
				total_tax,
				taxes_inc,
				total_p,
				shipping_title,
				shipping_custo,
				grams,
				item["created_at"],
				y["quantity"],
				y["name"],
				y["price"],
				applied_disc,
				total_price,
				y["sku"],
				y["requires_shipping"],
				y["taxable"],
				y["vendor"],
				b_address_n,
				b_address_1,
				b_address_1,
				b_address_2,
				b_comp,
				b_city,
				b_zip,
				b_province,
				b_country,
				b_phone,
				s_name,
				s_address_1,
				s_address_1,
				s_address_2,
				s_comp,
				s_city,
				s_zip,
				s_province,
				s_country,
				s_phone,
				sent_at,
				completed_at,
				item["order_id"],
				item["note"],
				note_attribute,
				o_tags,
				tax_1_n,
				tax_1_v,
				tax_2_n,
				tax_2_v,
				tax_3_n,
				tax_3_v,
				tax_4_n,
				tax_4_v,
				tax_5_n,
				tax_5_v,
					])
					
		draft_orders = draft_orders.links['next']['url']
		draft_orders = requests.get(draft_orders,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		draft_orders = ""

	page_number += 1