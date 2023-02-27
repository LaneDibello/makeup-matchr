import firebase_admin
from firebase_admin import db
import os
from typing import Dict, Optional, List

# Find Credentials relative to the calling script
cred_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Grab crednetials from the provided private key
cred_obj = firebase_admin.credentials.Certificate(cred_path)

# Connect
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://makeup-matchr-default-rtdb.firebaseio.com'
	})


def pushProduct(prod: dict):
    """
    Takes a Dictionary representing a product to be pushed to the database
    (While necessarily there's no set schema these products need to follow, here's a suggestion below)
        - Name: a string representing the product name
        - URL: the URL of the Vendor product page
        - Vendor: a string representing the vendor of this product
        - Red: single byte red value
        - Green: single byte green value
        - Blue: single byte blue value
    """
    db.reference('Products').push().set(prod) # pushes a new Products into the product listing wiht a unique ID and sets it's data to the provided product data


def getProductByName(name: str) -> Optional[Dict[str, str]]:
    """
    Finds the first product with the provided name in the products table
        `name`: The 'Name' parameter from the database 
    Returns a dictionaries represnting all the first product with this name
    """
    ref = db.reference('Products') # Get reference to Products Collection
    products = ref.order_by_child('Name').equal_to(name).limit_to_first(1).get() # Indexing by the 'Name' attribute, grab the first product with this name
    if len(products) < 1: return None # if there were none return None
    return list(products.values())[0] # Restructure the OrderedDict as a list of values, and grab the first


def getProductByUID(uid: str) -> Optional[Dict[str, str]]:
    """
    THIS IS LESS USEFUL UNDER OUR CURRENT SCHEMA, MOSTLY FOR DEBUG PURPOSES
    Retrieves a single product from the Database using its UID.
        `uid`: The UID of the product to retrieve.
    Returns A dictionary representing the product, or None if the product does not exist.
    """
    ref = db.reference('Products')
    product_ref = ref.child(uid)
    product = product_ref.get()
    if product is None:
        return None
    product['UID'] = uid
    return product

def getProductsByQuery():
    pass


# TEST SECTION - DELETE ME
# pushProduct(
# {
#   "Blue": 255,
#   "Green": 0,
#   "Name": "test2",
#   "Red": 0,
#   "URL": "https://www.test.com/",
#   "Vendor": "cosmetics inc"
# })
prod = getProductByName('test2')
print(prod)