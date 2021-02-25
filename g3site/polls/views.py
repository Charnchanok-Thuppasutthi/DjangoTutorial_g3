from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone

#admin
#pass 12
class IndexView(generic.ListView):#เมื่อมีการ request path polls/ จะทำการเรียกหน้า index.html
    template_name = 'polls/index.html'
    context_object_name = 'sorted_question_list'
            
    def get_queryset(self):
        return Question.objects.all().order_by('-allVote')

def menu(request):
    return render(request, 'polls/homepage.html')

class DetailView(generic.DetailView):#เมื่อมีการ request จากการกด Question จากหน้า index.html จะทำการเปิด detail.html
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):#ไปเรียกหน้า result.html ใน templates/polls มาแสดง
    model = Question
    template_name = 'polls/results.html'


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
        selected_choice.vote_set.create(vote_date=timezone.now())
        question.allVote +=1
        question.lastVote = timezone.now()
        question.save()
        selected_choice.votes += 1  #increase number of that vote
        selected_choice.lastVote = timezone.now()
        selected_choice.save()  #save modified attribute 
        return render(request , 'polls/results.html', {'question': question ,'choice_all': question.choice_set.all()} )

def sortingQuestion(request ):

    request_type1 = request.GET.get("Newest")
    request_type2 = request.GET.get("Oldest")
    request_type3 = request.GET.get("Most Votes")
    request_type4 = request.GET.get("Least Votes")
    request_type5 = request.GET.get("Latest Votes")

    if (request_type1 == "Sort By Newest"):
        context = {'sorted_question_list': Question.objects.all().order_by('-pub_date') }
        return render(request , "polls/index.html" ,context)

    elif (request_type2 == "Sort By Oldest"):
        context = {'sorted_question_list': Question.objects.all().order_by('pub_date') }
        return render(request , "polls/index.html" ,context)
    
    elif (request_type3 == "Sort By Most Votes"):
        context = {'sorted_question_list': Question.objects.all().order_by('-allVote')}
        return render(request , "polls/index.html" , context) 

    elif (request_type4 == "Sort By Least Votes"):
        context = {'sorted_question_list': Question.objects.all().order_by('allVote')}
        return render(request , "polls/index.html" , context) 

    elif (request_type5 == 'Sort By Latest Votes'):
        context = {'sorted_question_list': Question.objects.all().order_by('-lastVote')}
        return render(request , "polls/index.html" , context) 


def sortingVote(request ,question_id):
    question = get_object_or_404(Question, pk=question_id)

    request_type = request.GET.get("inputVoteMax")
    request_type2 = request.GET.get("inputDateLast")
    request_type3 = request.GET.get("inputVoteMin")
    request_type4 = request.GET.get("inputDateFirst")

    if (request_type == "Sort By MaxVote"):
        context = {'question': question ,'choice_all': question.choice_set.all().order_by('-votes')}
        return render(request , "polls/results.html" , context) 
    elif (request_type3 == "Sort By MinVote"):
        context = {'question': question ,'choice_all': question.choice_set.all().order_by('votes')}
        return render(request , "polls/results.html" , context) 

    elif (request_type2 == "Sort By LastVote"):
        context = {'question': question ,'choice_all': question.choice_set.all().order_by('-lastVote') }
        return render(request , "polls/results.html" ,context)
    elif (request_type4 == 'Sort By FirstDate'):
        context = {'question': question ,'choice_all': question.choice_set.all().order_by('lastVote') }
        return render(request , "polls/results.html" ,context)