from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Word ,Mean
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'vocab/index.html'
    context_object_name = 'word_list'
    def get_queryset(self):
        return Word.objects.all()

class DetailView(generic.DetailView):
    model = Word
    template_name = 'vocab/detail.html'
    def get_queryset(self):
        return Word.objects.all()

def addWordView(request):
    return render(request, 'vocab/addWord.html')

def submit(request):
    word = request.POST.get("word")
    mean = request.POST.get("mean")
    text = request.POST.get("type")

    checkWord=Word.objects.filter(word_text=word).exists() #return Boolean

    if ( (word =="")or( mean  == "") ):
        return render(request, 'vocab/addWord.html', {
            'error_message2': "ข้อมูลไม่ครบ.",})
    elif (checkWord == True):
        newWord = Word.objects.filter(word_text=word)[0]
        print(newWord)
        newWord.mean_set.create( mean_text = mean , type_text = text)
        newWord.save()

        return render(request, 'vocab/addWord.html', {
             'error_message1': "มีคำศัพท์นี้แล้ว และได้เพิ่มความหมายไปแล้ว ",})
    
    elif (word and mean  != ""):
        newWord = Word(word_text = word)
        newWord.save()
        newWord.mean_set.create( mean_text = mean , type_text = text)
        newWord.save()

    return render(request , 'vocab/addWord.html' )