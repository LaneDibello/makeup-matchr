from django.shortcuts import render
from makeupApp.models import Product
from makeupApp.matches import Match
from makeupApp.forms import InputForm

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
            brandName = request.POST.get('brandName')
            if priceL == '' and priceM == '' and brandName == '':
                context = {
                    'match_results':match_results.getMatchesKNearest(100),
                }
            elif priceL == '' and priceM == '' and brandName != '':
                context = {
                    'match_results':match_results.getMatchesKNearest(100, 0, float('inf'), brandName),
                }
            elif priceL != '' and priceM != '' and brandName == '':
                context = {
                    'match_results':match_results.getMatchesKNearest(100, priceL, priceM, ""),
                }
            else:
                context = {
                    'match_results':match_results.getMatchesKNearest(100, priceL, priceM, brandName),
                }
            context['form'] = InputForm(request.POST)
    return render(request, 'results.html', context)
