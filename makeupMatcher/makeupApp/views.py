from django.shortcuts import render
from makeupApp.models import Product
from makeupApp.matches import Match

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
    match_results = Match(240, 184, 160)
    context = {
        'match_results':match_results.getMatchesKNearest(100),
    }
    return render(request, 'results.html', context)
