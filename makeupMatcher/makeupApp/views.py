from django.shortcuts import render
from makeupApp.models import Product

# Gutted by the old firebase stuff 
# This is just a test that grabs the test product from the table

def index(request):
    return render(request, 'index.html')


