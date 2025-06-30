
## Adding Ecommerce Stores
Ecom-Tango allows you to connect and manage stores from supported platforms. Follow these steps to add a store:mdmd
# Working
- Initially, only Amazon seller central and Shopify are supported.
- To add stores of these services, user need to Register for their API.
- Ater getting the required credentials of it, it should be added to the site.
- To do this the option is selected and on the given form, 
the name of the store, platform and api credentials are given. 
- Submitting the form should add the store to the dashboard of the site and user should be able to 
perform the operations related to that store.
- To make this happen, the `models.py` module on the app made for each platform should have a class to store its credentials.
- These class should have attributes for logged user, api credentials, storename etc..

### Step 1: Obtain API Credentials
- **Amazon Seller Central**:
  - Register for Amazon Selling Partner API (SP-API) at Amazon Developer Portal.
  - Obtain SP-API credentials (e.g., `Client ID`, `Client Secret`, `Refresh Token`).
- **Shopify**:
  - Create a custom app in your Shopify store’s admin panel under **Apps &gt; Apps and sales channels &gt; Develop Apps**.
  - Generate an API key and secret. Ensure the app has permissions for required operations (e.g., read/write products, orders) by selecting required scopes.

### Step 2: Add a Store to Ecom-Tango

1. Log in to the Ecom-Tango dashboard at `http://localhost:8000`.
2. Navigate to the **Add Store** section.
3. Select the platform (Amazon or Shopify) from the dropdown menu.
4. Fill out the form with the following details:
   - **Store Name**: A unique name for your store (e.g., "My Amazon Store").
   - **Platform**: Amazon Seller Central or Shopify.
   - **API Credentials**: Enter the required credentials.
5. Submit the form to add the store to your dashboard.

Example form input for Shopify:

```
Store Name: My Shopify Store
Platform: Shopify
API Key: abc123xyz789
API Secret: def456uvw012
Storename: 2fj4faf-2
```

### Step 3: Verify and Use

- Once added, the store will appear on your dashboard.
- You can perform operations like viewing orders, syncing inventory, or updating product listings, depending on the platform’s API capabilities.

## How It Works

Ecom-Tango uses Django models to store and manage store credentials securely. Each platform (Amazon, Shopify) has a dedicated app within the Django project, with a `models.py` file defining the structure for storing credentials.

### Example Model Structure

Below is an example of how credentials are stored in `amazon/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class AmazonStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100, unique=True)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=200)
    referesh_token = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200,default = None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name
```

A similar structure exists for Shopify in `shopify/models.py`.