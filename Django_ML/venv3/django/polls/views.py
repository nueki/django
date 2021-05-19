from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import pandas as pd

from polls.modules import gantt
from polls.modules import iris

from polls.forms import irisInput

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def chart(request):
    graph_html = gantt.get_graph_html()

    context = {
        'graph_html': graph_html
    }
    return render(request, 'polls/gantt.html', context)


def chart2(request):
    if request.method == 'POST':
        form = irisInput.IrisInputForm(request.POST)
    else:
        form = irisInput.IrisInputForm()

    input = None
    if form.is_valid():
        input = form.cleaned_data['input']
    result = iris.get_graph_html_virginica(input)

    context = {
        'graph_html_virginica': result['plot_fig'],
        'form': form,
        'prediction': result['prediction'],
        'coefficients': result['params'][0],
        'mean_squared_error': result['params'][1],
        'r2score': result['params'][2]
    }
    return render(request, 'polls/iris.html', context)
