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

brandChoices = Product.getBrands() # Grab a the list of brands targetted in the database for the filter drop down

def index(request):
    '''
    Generates the necessary elements for the main `index.html` page\n
    This primarily includes Image upload and handling, as well as passing to the color correction method
    '''
    if not request.method == 'POST':
        return render(request, 'index.html')
    
    img_raw = Image.open(request.FILES['image'])
    
    if img_raw.format == "JPEG":
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation' : break
        
        i_exif = img_raw._getexif()
        if (i_exif is not None):
            exif=dict(i_exif.items())
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
    height = int(300 * (height/width))
    img_raw = img_raw.resize((300, height))
    img = CorrectImage(img_raw)

    # Use raw image if color correction fails
    if not img:
        img = img_raw
    
    # Convert the image to base64
    img_buf = BytesIO()
    img.save(img_buf, format="JPEG")
    request.session['image'] = b64encode(img_buf.getvalue()).decode()

    return redirect('picker')

def corrected(request):
    '''
    Passes the color corrected image into the `corrected.html` page
    '''
    # get the corrected picture and pass it in the context
    img = request.session['image']
    context = {
        'img_b64' : img,
    }

    return render(request, 'corrected.html', context)

def picker(request):
    '''
    Passes the color corrected image into the `picker.html` page\n
    Obtains the selected image coordinates from the ismap element, and passes the associated color to the page.
    '''
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
        #'x': coords[0],
        #'y': coords[1],
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
    '''
    Passes the selected color into the `results.html` page\n
    Grabs 100 nearest matches to the provided color \n
    Handles posted filtering specs from the forms, and filters results with these options\n
    '''
    MATCHES = 10
    if not 'color-values' in request.session: # if there is no color chosen redirect to picker
        return redirect('picker')
    
    color = request.session['color-values']
    match_results = Match(color['r'], color['g'] , color['b'])
    # match_results = Match(240, 184, 160) This is the testing result

    context = {
        'match_results':match_results.getMatchesKNearest(MATCHES),
    }

    context['form'] = InputForm()

    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            if 'reset' in request.POST:
                priceL = 0
                priceM = 0
                brand_idx = 0
            else:
                priceL = form.data['priceL']
                priceM = form.data['priceM']
                brand_idx = form.data['brandName']
            
            if not priceL:
                priceL = 0

            if not priceM:
                priceM = float('inf')

            if not brand_idx:
                brand_idx = 0

            brandName = brandChoices[int(brand_idx)]

            context = {
                'match_results': match_results.getMatchesKNearest(MATCHES, priceL, priceM, brandName),
            }
            
            if 'reset' in request.POST:
                context['form'] = InputForm()
            else:
                context['form'] = InputForm(request.POST)
    
    return render(request, 'results.html', context)

