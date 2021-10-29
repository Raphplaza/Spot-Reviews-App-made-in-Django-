from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, response
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import SurfSpot
2

#Index view using generic
"""
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        ""Return the last five published questions""
        #filter future questions:

        return SpotName.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
"""


"""
class DetailView(generic.DetailView):
    model=SpotName
    template_name='polls/detail.html'

    def get_queryset(self):
        #excludes future questions   lte=less than equal
        return SpotName.objects.filter(pub_date__lte=timezone.now())
"""

class ResultsView(generic.DetailView):
    model=SurfSpot
    template='polls/results.html'


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import SpotReview, SurfSpot

def vote(request, question_id):
    question = get_object_or_404(SurfSpot, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, SpotReview.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NewSpotForm

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

    template = loader.get_template('polls/index.html')
    context = {
        'surfspot_list' : surfspot_list,
        'form': form
    }
    #return render(request, 'index.html',{'surf_spot_list':surf_spot_list})
    #return HttpResponse(template.render(context,request))
    return render(request, 'polls/index.html', context)



#from django.http import Http404
#from django.shortcuts import render

#def detail(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')

    return render(request, 'polls/detail.html', {'question':question})

#A shortcut: get_object_or_404()
from django.shortcuts import get_object_or_404, render
from .forms import NewSpotReviewForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SpotReview

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
    
    template = loader.get_template('polls/detail.html')
    context = {
        'surf_spot_review_list' : surf_spot_review_list,
        'form': form,
        'spotname':spotname,
        'surfspot_id':surfspot_id
    }

    return render(request, 'polls/detail.html', context)
