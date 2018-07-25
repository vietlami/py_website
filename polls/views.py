# 引用函数
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# 引入model
from .models import Choice, Question


def index(request):
    # 找到所有的question对象
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 找到选择的选项
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 返回投票页
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "您没有选择选项",
        })
    else:
        # 投票成功
        selected_choice.votes += 1
        selected_choice.save()
        # 返回结果页
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))