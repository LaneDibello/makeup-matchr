from django.shortcuts import render
from makeupApp.models import Product
from django.core.files.storage import FileSystemStorage
from makeupApp.utils.color_correction import CorrectImage

def index(request):
    # CorrectImage('../makeupMatcher/media/figure3.jpg')
    if request.method == 'POST':
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        correct_url = CorrectImage('../makeupMatcher/', file_url)
        if correct_url == "": # image could not be corrected 
            correct_url = '/media/empty.jpg' # insert empty image
        # with the file url read the image
        return render(request, 'index.html', {'file_url' : correct_url})
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
