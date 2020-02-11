import os
import requests
from os.path import basename
from urllib.request import urlopen  

# Environment variables
if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

url = 'https://' + os.getenv('SHOPIFY_URL') + '.myshopify.com/admin/api/2020-01/'

params = {'limit': 250}
page_number = 1

themes = requests.get(url + 'themes.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

os.makedirs('shopify_themes', exist_ok=True)

while themes:
	print("Processing page: #{page_number}".format(page_number=page_number))
	try:
		x = themes.json()
		for x in x["themes"]:
			
			# Try to make folder if it already exists it will skip
			try:				
				# Creats the Directory
				os.makedirs('shopify_themes/' + x["name"], exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/assets', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/layout', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/snippets', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/config', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/locales', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/sections', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/templates', exist_ok=True)
				os.makedirs('shopify_themes/' + x["name"] + '/templates/customers', exist_ok=True)

			# Directory already Exists so do nothing
			except OSError:
				# directory already exists
				pass
				
			asset_id = x["id"]

			# now get the assets list for this theme
			assets = requests.get(url + 'themes/' + str(asset_id) + '/assets.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
			y = assets.json()
			for z in y["assets"]:
				if z["content_type"] == "text/x-liquid":
					file_name = z["key"]
					files = requests.get(url + 'themes/' + str(asset_id) + '/assets.json?asset[key]=' + file_name,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
					w = files.json()
					text = w["asset"]["value"]
					file = open('shopify_themes/' + x["name"] + "/" + file_name,"w")
					file.write(text)
							
		themes = themes.links['next']['url']
		themes = requests.get(themes,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))
		
	except KeyError:
   		themes = ""

	page_number += 1