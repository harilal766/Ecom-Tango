from django.shortcuts import render

# Create your views here.
class ShopifyBase:
    def __init__(self,shopify_credentials:dict):
        self.sh_creds = shopify_credentials

class ShopifyOrders(ShopifyBase):
    def __init__(self, shopify_credentials):
        super().__init__(shopify_credentials)
        
    def find_potential_returns(self):
        orders = {}
        try:
            pass
        except Exception as e:
            print(e)
        finally:
            return orders

"""
list out order address and other details in a homepage, 
try to find the common pattern between potential returns
"""