from django.shortcuts import render
from makeupApp.models import Product
from django.core.files.storage import FileSystemStorage
from makeupApp.utils.color_correction import CorrectImage
from makeupApp.matches import Match
from makeupApp.forms import InputForm
from django.http import HttpResponse
import re
import os
from PIL import Image

brandChoices = Product.getBrands()

def index(request):
    # CorrectImage('../makeupMatcher/media/figure3.jpg')
    if request.method == 'POST':
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        request.session['raw_image_url'] = file_url[1:]
        correct_url = CorrectImage('../makeupMatcher/', file_url)
        if correct_url == "": # image could not be corrected 
            correct_url = '/media/empty.jpg' # insert empty image
        request.session['image_url'] = correct_url
        # with the file url read the image
        return render(request, 'index.html', {'file_url' : correct_url})
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def corrected(request):
    # get the corrected picture and pass it in the context
    file_url = request.session['image_url']
    context = {
        'file_url' : "../" + file_url,
    }
    return render(request, 'corrected.html', context)

def picker(request):
    coords_s = request.META['QUERY_STRING']
    coords = [0,0]
    if (coords_s != ""): coords = list(map(int, re.findall(r'\d+', coords_s)))
    file_url = request.session['image_url']
    im = Image.open('../makeupMatcher/' + file_url).load()
    color = im[coords[0], coords[1]]
    context = {
        'x': coords[0],
        'y': coords[1],
        'r': color[0],
        'g': color[1],
        'b': color[2],
        'file_url' : '../' + file_url,
    }
    
    return render(request, 'picker.html', context)

def test(request):
    m = Match(197, 140, 133)
    query_results = m.getMatchesKNearest(20, brandName='Lancome')
    print(len(query_results))
    context = {
        'query_results':query_results,
    
    }
    return render(request, 'picker.html', context)



def results(request):
    #delete the images after the resutls page
    delete_images(request)
    match_results = Match(240, 184, 160)

    context = {
        'match_results':match_results.getMatchesKNearest(100),
    }
    context['form'] = InputForm()

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            priceL = request.POST.get('priceL')
            priceM = request.POST.get('priceM')
            brandidx = request.POST.get('brandName')
            print("Brand Idx: ", brandidx)
            brandName = brandChoices[int(brandidx)]
            print("Brand Name: ", brandName)
            if not priceL:
                priceL = 0
            if not priceM:
                priceM = float('inf')
            if not brandName:
                brandName = ""

            context = {
                    'match_results':match_results.getMatchesKNearest(100, priceL, priceM, brandName),
                }
            
            context['form'] = InputForm(request.POST)
    return render(request, 'results.html', context)

def delete_images(request):
    ''' Delete the pictures of user when browser is closed '''

    # delete the raw user image
    if 'raw_image_url' in request.session:
        if os.path.exists(request.session['raw_image_url']):
            os.remove(request.session['raw_image_url'])
    #check for corrected image  and delete it
    if 'image_url' in request.session:
        if os.path.exists(request.session['image_url']):
            os.remove(request.session['image_url'])
    return HttpResponse('SUCCESS FROM PYTHON')
