from django.shortcuts import render
from makeupApp.models import Product
import re
from PIL import Image

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def test(request):
    coords_s = request.META['QUERY_STRING']
    coords = [0,0]
    coords = list(map(int, re.findall(r'\d+', coords_s)))
    im = Image.open('DELETE_ME.jpg').load()
    color = im[coords[0], coords[1]]
    context = {
        'x': coords[0],
        'y': coords[1],
        'r': color[0],
        'g': color[1],
        'b': color[2],
    }

    return render(request, 'testing.html', context)

def results(request):
    query_results = Product.objects.all()[:10]
    context = {
        'query_results':query_results,
    }
    return render(request, 'results.html', context)
