from django.db import models

# Create your models here.
class Search(models.Model):
    startAdd = models.TextField() # might need to change type later
    startNick = models.CharField(max_length=500)
    targetAdd = models.TextField() # might need to change type later
    targetNick = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True) # automatically adds

    def __str__(self): # right now if database has same nickname, replacing with the newest value
        return self.startNick

