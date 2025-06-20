# Ecom-Tango
A centralised Django based tool to streamline tasks from multiple ecommerce seller platforms

## Overview
Ecom-Tango allows users to manage multiple ecommerce stores from a single dashboard. It supports integrating stores via API credentials, enabling operations like inventory management, order tracking, and more. Currently, it supports Amazon Seller Central and Shopify, with plans to add more platforms in the future.

## Prerequisites
Before installing Ecom-Tango, ensure you have the following:

- **Python**: Version 3.8 or higher
- **Git**: For cloning the repository
- **SQLite**: For the database
- **API Credentials**: Access to Amazon Seller Central SP-API and/or Shopify API tokens

# Installation and running
1. **Clone the Repository** : ```git clone "https://github.com/harilal766/Ecom-Tango"```
2. **Create a Virtual Environment** : ```python -m venv env```
3. **Activate the Virtual Environment** : ```env/scripts/activate```
4. **Install Dependencies**: : ```pip install -r requirements.txt```

5. **Set Up the Database**:

   - Ensure PostgreSQL is installed and running (or use SQLite for development).
   - Update the `DATABASES` setting in `Ecom-Tango/settings.py` with your database configuration. Example for sqlite:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite',
             'NAME': 'ecom_tango_db',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Run migrations:

     ```bash
     python manage.py migrate
     ```

6. **Run the Development Server**:

   ```bash 
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`.

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

### Dashboard Operations

Once a store is added, you can:

- View and manage orders.
- Sync inventory across platforms.
- Update product listings (e.g., prices, descriptions).
- Generate basic sales reports.

## Troubleshooting

- **API Errors**: Ensure your API credentials are correct and have the necessary permissions. Check the platform’s developer portal for error details.
- **Database Issues**: Verify your database is running and credentials in `settings.py` are correct. Run `python manage.py check` to diagnose issues.
- **Dependency Conflicts**: If `pip install` fails, ensure your Python version is compatible (3.8+). Try upgrading pip: `pip install --upgrade pip`.
- **Server Not Starting**: Check for errors in the terminal. Ensure no other process is using port 8000.

## Additional Resources

- Amazon SP API Documentation : https://developer-docs.amazon.com/sp-api/docs/welcome
- Shopify Admin API Documentation : https://shopify.dev/docs/api/admin-rest
- Django Documentation : https://docs.djangoproject.com/en/5.2/

For further assistance, open an issue on the GitHub repository.
