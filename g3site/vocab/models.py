import datetime
from django.db import models
from django.utils import timezone

class Word(models.Model):
    word_text = models.CharField(max_length=50)
    def __str__(self):
        return self.word_text

class Mean(models.Model):
    mean_text = models.CharField(max_length=200)
    type_text = models.CharField(max_length=10)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    def __str__(self):
        return self.mean_text
