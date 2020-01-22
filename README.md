# backup shopify
 This is a simple backup for shopify. Products Backup Now.  

Instead of using the web interface to backup the products, just use python. Saves to a CSV File. 

Configure Shopify API credentials
Create a .env environment configuration file to hold your Shopify API credentials. You can get an API key by going to your Shopify admin dashboard and navigating to Apps -> Private apps -> Create private app. Call your app simply “Shopify backup” with all of the default settings, and you should get an API key and and Password. Set these in your .env file.

touch config.env
and in the file:

SHOPIFY_URL=your-store.myshopify.com
SHOPIFY_API_KEY=yourapikeylettersandnumbers
SHOPIFY_API_PASSWORD=yourapipasswordlettersandnumbers


Todo:
orders, customers, draft orders, theme files

