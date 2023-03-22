from django.shortcuts import render
from makeupApp.models import Product
from makeupApp.matches import Match

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def test(request):
    m = Match(197, 140, 133)
    query_results = m.getMatchesKNearest(20, brandName='Lancome')
    print(len(query_results))
    context = {
        'query_results':query_results,
    }
    return render(request, 'testing.html', context)

def results(request):
    query_results = Product.objects.all()[:10]
    context = {
        'query_results':query_results,
    }
    return render(request, 'results.html', context)
