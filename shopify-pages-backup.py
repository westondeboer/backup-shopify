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
count = requests.get(url + 'pages/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

print("Total pages: #{count}".format(count=count))

pages = requests.get(url + 'pages.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("pages.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)"])

while pages:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = pages.json()
		for item in x["pages"]:
			print(item["title"])

			f.writerow([item["handle"],item["title"],item["body_html"]])

		pages = pages.links['next']['url']
		pages = requests.get(pages,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		pages = ""

	page_number += 1