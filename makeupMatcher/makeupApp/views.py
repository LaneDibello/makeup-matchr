from django.shortcuts import render, redirect
from makeupApp.models import Product
from makeupApp.utils.color_correction import CorrectImage
from makeupApp.matches import Match
from makeupApp.forms import InputForm
from django.http import HttpResponse
import re, os
from PIL import Image, ExifTags
from io import BytesIO
import numpy as np
from base64 import b64encode, b64decode

brandChoices = Product.getBrands()

def index(request):
    if not request.method == 'POST':
        return render(request, 'index.html')
    
    img_raw = Image.open(request.FILES['image'])
    
    if img_raw.format == "JPEG":
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation' : break
        
        i_exif = img_raw._getexif()
        print(i_exif)
        if (i_exif is not None):
            exif=dict(i_exif.items())
            print(exif)
            print(orientation)
            if exif is None:
                print("Nonetype Exif")
            elif (orientation in exif) and (exif[orientation] == 3) : 
                img_raw=img_raw.rotate(180, expand=True)
            elif (orientation in exif) and (exif[orientation] == 6) : 
                img_raw=img_raw.rotate(270, expand=True)
            elif (orientation in exif) and (exif[orientation] == 8) : 
                img_raw=img_raw.rotate(90, expand=True)
            

    img_raw = img_raw.convert('RGB')
    width, height = img_raw.size
    height = int(400 * (height/width))
    img_raw = img_raw.resize((400, height))
    img = CorrectImage(img_raw)

    # Use raw image if color correction fails
    if not img:
        img = img_raw
    
    # Convert the image to base64
    img_buf = BytesIO()
    img.save(img_buf, format="JPEG")
    request.session['image'] = b64encode(img_buf.getvalue()).decode()

    return redirect('corrected')

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
    if (coords_s != ""): coords = list(map(int, re.findall(r'\d+', coords_s)))[-2:]

    img_b64 = request.session['image']
    # im = Image.open('../makeupMatcher/' + file_url).load()
    im = np.array(Image.open(BytesIO(b64decode(img_b64))))
    color = im[coords[1], coords[0]]
    context = {
        'x': coords[0],
        'y': coords[1],
        'r': int(color[0]),
        'g': int(color[1]),
        'b': int(color[2]),
        'img_b64' : img_b64,
    }
    
    # save the rgb values to make the query in the results page
    if request.method == "POST":
        request.session['color-values'] = {
            'r' : int(color[0]),
            'g' : int(color[1]),
            'b' : int(color[2]),
        }
        return redirect('results')
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
