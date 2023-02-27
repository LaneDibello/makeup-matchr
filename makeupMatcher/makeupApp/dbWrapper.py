from firebase_admin import db

'''
Takes a Dictionary representing a product to be pushed to the database
(While necessarily there's no set schema these products need to follow, here's a suggestion below)
    - Name: a string representing the product name
    - URL: the URL of the Vendor product page
    - Vendor: a string representing the vendor of this product
    - Red: single byte red value
    - Green: single byte green value
    - Blue: single byte blue value
'''
def pushProduct(prod: dict):
    pass

'''
Finds the product with the following name in the products table
'''
def getProductByName(name: str):
    pass

'''
Finds the product with the following UID value in the products table
'''
def getProductByUID(uid: int):
    pass
