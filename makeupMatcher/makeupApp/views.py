from django.shortcuts import render
from makeupApp.models import Product
from .forms import imgForm
from .models import imgModel

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
    return render(request, 'results.html')

def home_view(request):
    context = {}
    if request.method == "POST":
        form = imgForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("img_field")
            obj = imgModel.objects.create(
                                 title = name,
                                 img = img
                                 )
            obj.save()
            print(obj)
    else:
        form = imgForm()
    context['form']= form
    return render(request, 'index.html', context)
