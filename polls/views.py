from django.shortcuts import render,get_object_or_404
from django.http import Http404 , HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        #Return the last five published questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DeleteView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    mode = Question
    template_name = "polls/results.html"

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context={"question":question, "error_message":"You didnt select a choice"}
        return render(request,"polls/detail.html",context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results",args=(question_id)))


#1.Version der Funktionen
#
#def index(request):
#   latest_question_list = Question.objects.order_by("-pub_date")[:5]
#    context = {
#        "latest_question_list":latest_question_list,
#    }
#    return render(request , "polls/index.html",context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.objects.get(pk=question_id).DoesNotExist:
#         raise Http404(f"Question with id '{question_id}' does not exist")
#     return render(request , "polls/detail.html" ,{"question":question})

# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/results.html",{"question":question})