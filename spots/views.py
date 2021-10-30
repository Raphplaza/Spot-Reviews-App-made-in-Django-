
from django.template import loader
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import get_object_or_404, render
from .models import SpotReview, SurfSpot
from .forms import NewSpotForm, NewSpotReviewForm

def index(request):
    surfspot_list = SurfSpot.objects.order_by('-pub_date')[:30]

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewSpotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_text = form.cleaned_data['new_spot']
            SurfSpot.objects.create(name=form_text,pub_date=timezone.now())
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('//')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewSpotForm()

    template = loader.get_template('spots/index.html')
    context = {
        'surfspot_list' : surfspot_list,
        'form': form
    }
    #return render(request, 'index.html',{'surf_spot_list':surf_spot_list})
    #return HttpResponse(template.render(context,request))
    return render(request, 'spots/index.html', context)


def detail(request, surfspot_id):
    spotname=SurfSpot.objects.get(pk=surfspot_id)
    surf_spot_review_list = spotname.spotreview_set.all() 

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewSpotReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_text = form.cleaned_data['new_spot_review']
            form_author = form.cleaned_data['author_name']
            SpotReview.objects.create(review_text=form_text,surfspot=SurfSpot.objects.get(pk=surfspot_id), author=form_author)
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('//')

    # if a GET (or any other method) we'll create a blank form
    else: form = NewSpotReviewForm()
    
    template = loader.get_template('spots/detail.html')
    context = {
        'surf_spot_review_list' : surf_spot_review_list,
        'form': form,
        'spotname':spotname,
        'surfspot_id':surfspot_id
    }
    return render(request, 'spots/detail.html', context)