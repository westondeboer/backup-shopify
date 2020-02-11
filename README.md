# Shopify Backup
 This is a simple python backup for Shopify. With the separate tools it will backup the Products, Draft Orders, and Orders. 
  
Instead of using the web interface to backup the products, just use python. It will save it all locally where you want it to save. I am terrible at Python, this is my first time using it.  

Configure Shopify API credentials
Create a .env environment configuration file to hold your Shopify API credentials. You can get an API key by going to your Shopify admin dashboard and navigating to Apps -> Private apps -> Create private app. Call your app simply “Shopify backup” with all of the default settings, and you should get an API key and and Password. Set these in your .env file.

touch config.env
and in the file:

```
SHOPIFY_URL=your-store.myshopify.com
SHOPIFY_API_KEY=yourapikeylettersandnumbers
SHOPIFY_API_PASSWORD=yourapipasswordlettersandnumbers
```

Task List:
- [x] Draft Orders to csv
- [x] Orders to csv
- [x] Products to csv
- [x] Products Images Backup
- [x] Customers Backup
- [x] Gift Cards Backup
- [ ] Collections Backup
- [ ] Pages Backup
- [x] Theme Backup
- [ ] Store Policies Backup
- [ ] Shipping Zones Backup
- [x] Convert to new API
