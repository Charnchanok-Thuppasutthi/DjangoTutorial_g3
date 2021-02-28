from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Word ,Mean
from django.utils import timezone

class IndexView(generic.ListView):#แสดงหน้าแรก
    template_name = 'vocab/index.html'
    context_object_name = 'wordList'
    def get_queryset(self):
        return Word.objects.all()

class DetailView(generic.DetailView):#แสดหน้าคำศัพท์
    model = Word
    template_name = 'vocab/detail.html'
    def get_queryset(self):
        return Word.objects.all()

def addWordView(request):#แสดงหน้าเพิ่มคำศัพท์
    return render(request, 'vocab/addWord.html')

def submit(request):#เมื่อมีการกดคำเพิ่มศัพท์จะดูว่า คัพท์ซ้ำหรือไม่ ถ้าซ้ำจะความหมายใหม่ไปเลย แต่ถ้าไม่ซ่้ำจะสร้างคำศัพท์ใหม่
    word = request.POST.get("word")
    mean = request.POST.get("mean")
    text = request.POST.get("type")

    checkWord=Word.objects.filter(word_text=word).exists() #return Boolean

    if ( (word =="")or( mean  == "") ):
        return render(request, 'vocab/addWord.html', {
            'error_message2': "ข้อมูลไม่ครบ.",})

    elif (checkWord):
        word = Word.objects.filter(word_text=word)[0]
        checkMeaning = word.mean_set.all().filter(mean_text=mean).exists()

        if (checkMeaning):
            return render(request, 'vocab/addWord.html', {
                'error_message1': "มีความหมายนี้แล้ว จะไม่ทำการเพิ่มใหม่ ",})   
        else:
            newWord = Word.objects.filter(word_text=word)[0]
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

def search(request):#เมื่อมีการกดปุ่มค้นหาบนหน้าแรก จะดูว่ามีศัพท์ที่ตรงกับที่ค้นมั้ย ถ้าไม่มีจะแสดงคำที่มีพยัญชนะเหมือนกัน
    searchword = request.POST.get("searchBar_text")
    checkWord=Word.objects.filter(word_text=searchword).exists() 
    if (checkWord == False):
        if( Word.objects.filter(word_text__icontains=searchword).exists() ):
            context = {'wordList':Word.objects.filter(word_text__icontains=searchword)}
            return render(request, 'vocab/index.html', context )
        else:   
            return render(request, 'vocab/index.html', {
                'error_message1': "ไม่เจอคำศัพท์ที่ต้องการจะหา",})
    else:
        context = {'word':searchword}
        return render(request ,'vocab/index.html',context)

def delete(request ,word_id):
    word = Word.objects.all().filter(pk=word_id)        
    word.delete()  
    return render(request , 'vocab/index.html',{ 'wordList' : Word.objects.all()})

def editPage(request ,word_id):
    selected_word = get_object_or_404(Word,pk=word_id)
    return render(request, 'vocab/edit.html' , {'word': selected_word ,'mean': selected_word.mean_set.all()})

def delMean(request ,word_id ,mean_id):
    selected_word = Word.objects.get(pk=word_id)
    selected_mean = selected_word.mean_set.get(pk=mean_id)
    selected_mean.delete()
    return render(request,'vocab/edit.html',{'word':selected_word , 'mean':selected_word.mean_set.all()})

def resubmit(request ,word_id ):
    selected_word = Word.objects.get(pk=word_id)
    word_txt = request.POST.get("word")
    selected_word.word_text = word_txt
    selected_word.save() 
    print(selected_word.mean_set.all())
    for i in selected_word.mean_set.all(): 
        inputMean = request.POST.get(str(i.id))
        inputType = request.POST.get(str(i.id)+"type")
        
        if (inputType == None):
            i.mean_text = inputMean
        else:
            i.mean_text = inputMean
            i.type_text = inputType
        i.save()
    return render(request,'vocab/detail.html',{ 'word':selected_word , 'mean':selected_word.mean_set.all()})