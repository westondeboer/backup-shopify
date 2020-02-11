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

policies = requests.get(url + 'policies.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

f = csv.writer(open("policies.csv", "w"))
f.writerow(["Handle", "Title", "Body (HTML)"])

while policies:
	try:
		x = policies.json()
		for item in x["policies"]:
			print(item["title"])

			f.writerow([item["handle"],item["title"],item["body"]])

		policies = policies.links['next']['url']
		policies = requests.get(policies,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		policies = ""

	page_number += 1