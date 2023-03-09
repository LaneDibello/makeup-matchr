from django.shortcuts import render
from makeupApp.models import Product

# Gutted by the old firebase stuff 
# This is just a test that grabs the test product from the table

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def test(request):
    query_results = Product.objects.all()[:20]
    context = {
        'query_results':query_results,
    }
    return render(request, 'testing.html', context)

def results(request):
    query_results = Product.objects.all()[:20]
    context = {
        'query_results':query_results,
    }
    return render(request, 'results.html', context)
