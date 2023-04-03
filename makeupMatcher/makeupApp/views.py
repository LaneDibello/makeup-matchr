from django.shortcuts import render, redirect
from makeupApp.models import Product
from django.core.files.storage import FileSystemStorage
from makeupApp.utils.color_correction import CorrectImage
from makeupApp.matches import Match
from makeupApp.forms import InputForm
from django.http import HttpResponse
import re, os
from PIL import Image
from io import BytesIO
import numpy as np
from base64 import b64encode, b64decode

brandChoices = Product.getBrands()

def index(request):
    if not request.method == 'POST':
        return render(request, 'index.html')
    
    img_raw = Image.open(request.FILES['image']).convert('RGB') 
    img = CorrectImage(img_raw)

    # Use raw image if color correction fails
    if not img:
        img = img_raw
    
    # Convert the image to base64
    img_buf = BytesIO()
    img.save(img_buf, format="JPEG")
    request.session['image'] = b64encode(img_buf.getvalue()).decode()

    return redirect('corrected')

def about(request):
    return render(request, 'about.html')

def corrected(request):
    # get the corrected picture and pass it in the context
    img = request.session['image']
    context = {
        'img_b64' : img,
    }

    return render(request, 'corrected.html', context)

def picker(request):
    if not 'image' in request.session: # if there is no image redirect to index page
        return redirect('index')

    coords_s = request.META['QUERY_STRING']
    coords = [0,0]
    if (coords_s != ""): coords = list(map(int, re.findall(r'\d+', coords_s)))

    img_b64 = request.session['image']
    # im = Image.open('../makeupMatcher/' + file_url).load()
    im = np.array(Image.open(BytesIO(b64decode(img_b64))))
    color = im[coords[0], coords[1]]
    context = {
        'x': coords[0],
        'y': coords[1],
        'r': color[0],
        'g': color[1],
        'b': color[2],
        'img_b64' : img_b64,
    }
    
    # save the rgb values to make the query in the results page
    if request.method == "POST":
        request.session['color-values'] = {
            'r' : color[0],
            'g' : color[1],
            'b' : color[2],
        }
        return redirect('results')
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
    #delete the images after the results page
    delete_images(request)

    if not 'color-values' in request.session: # if there is no color chosen redirect to picker
        return redirect('picker')
    
    color = request.session['color-values']
    match_results = Match(color['r'], color['g'] , color['b'])
    # match_results = Match(240, 184, 160) This is the testing result

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

    # delete the raw user image
    if 'raw_image_url' in request.session:
        if os.path.exists(request.session['raw_image_url']):
            os.remove(request.session['raw_image_url'])
    #check for corrected image  and delete it
    if 'image_url' in request.session:
        if os.path.exists(request.session['image_url']):
            os.remove(request.session['image_url'])
    return HttpResponse('SUCCESS FROM PYTHON')