from django.shortcuts import render
from makeupApp.models import Product
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.method == 'POST':
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'index.html', {'file_url' : file_url})
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
