import os
import requests
from os.path import basename
from urllib.request import urlopen  

# todo: If image already exists do nothing

# Environment variables 
if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

# Setup the API url
url = 'https://' + os.getenv('SHOPIFY_URL') + '.myshopify.com/admin/api/2020-01/'

# Don't know if we need this or not
params = {'limit': 250}

# Counts the amount of products
count = requests.get(url + 'products/count.json',auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD'))).json().get('count')

# Prints out the amount of products
print("Total Products: #{count}".format(count=count))

# Get initial JSON from Shopify API
products = requests.get(url + 'products.json',params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

# While there are products look thought this
while products:
	
	# If there are products left do the loop
	try:
		
		# Converts the JSON so python can read it
		x = products.json()
		
		# The JSON is listed under "products"
		for item in x["products"]:
			
			# This is the directory name we are going to use later
			directory = item["title"]
			
			# Try to make folder if it already exists it will skip
			try:
				
				# Creats the Directory
				os.makedirs('shopify_images/'+ directory)

			# Directory already Exists so do nothing
			except FileExistsError:
				# directory already exists
				pass
			
			# for image variants
			for e in item["images"]:
			
				# Setup image name and remove unnecessary objects from the url
				image = e["src"].partition("?")[0]
				
				# request the image
				response = requests.get(image)
				
				# grabs the filename from the url
				f_name = basename(response.url)
				
				# with the image write it into the correct directory
				with open("shopify_images/"+ directory + "/" + f_name, 'wb') as f:
					f.write(response.content)
		
		# get json for the next page
		products = products.links['next']['url']
		
		# convert the json to use in the while products: loop
		products = requests.get(products,params={**params},auth=(os.getenv('SHOPIFY_API_KEY'), os.getenv('SHOPIFY_API_PASSWORD')))

	#if no more items default products to nothing so loop ends
	except KeyError:
   		products = ""