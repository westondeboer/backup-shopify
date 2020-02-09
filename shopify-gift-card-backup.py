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
count = requests.get(url + 'gift_cards/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total Gift Cards: #{count}".format(count=count))

gift_cards = requests.get(url + 'gift_cards.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("gift_cards.csv", "w"))

f.writerow([
"Id",
"Last Characters",
"Customer Name",
"Email",
"Order Name",
"Created At",
"Expires On",
"Initial Value",
"Balance",
"Currency",
"Expired?",
"Enabled?",
"Disabled At",
"Note",
])


while gift_cards:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = gift_cards.json()
		for item in x["gift_cards"]:
	
			f.writerow([		
			item["id"],
			item["last_characters"],
			item["customer_id"],
			item["order_id"],
			item["created_at"],
			item["expires_on"],
			item["initial_value"],
			item["balance"],
			item["currency"],
			"",
			"",
			item["disabled_at"],
			item["note"],
			])
		gift_cards = gift_cards.links['next']['url']
		gift_cards = requests.get(gift_cards,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		gift_cards = ""

	page_number += 1

print("Done.")