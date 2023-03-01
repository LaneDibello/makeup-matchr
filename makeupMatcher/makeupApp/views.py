from django.shortcuts import render
from makeupApp.models import Product

# Gutted by the old firebase stuff 
# This is just a test that grabs the test product from the table

def index(request):
        

        # Inserting Products:
        # p = Product(name='django import test', vendor='Test', red=60, blue=70, green=90, url='TEST URL', brand='brandname haha', colorcode='17C')
        # p.save()


        #Selecting Values Example:
        prod = Product.objects.get(name='django import test')
        context = {
            'name':prod.name,
            'vendor':prod.vendor,
            'brand':prod.brand,
            'url':prod.url,
            'red':prod.red,
            'green':prod.green,
            'blue':prod.blue,
        }
        return render(request, 'index.html', context)

        return None


