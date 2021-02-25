import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):#this table have question text , published date 
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    lastVote = models.DateTimeField('lastVote')
    allVote = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):#this table have choice text ,vote number and linked to Question table
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    lastVote = models.DateTimeField('lastVote')
    def __str__(self):
        return self.choice_text

class Vote(models.Model):#this table have voted date and linked to Choice table
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    vote_date = models.DateTimeField('voted date')
    def __str__(self):
        return str(self.vote_date)
