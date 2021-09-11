from django.db import models


class Word_in_texts(models.Model):
    word = models.CharField(max_length=50)
    quantity = models.IntegerField()
