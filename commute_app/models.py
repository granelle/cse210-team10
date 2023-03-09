from django.db import models

# Create your models here.
class Search(models.Model):
    startAdd = models.TextField() # might need to change type later
    startNick = models.CharField(max_length=500)
    targetAdd = models.TextField() # might need to change type later
    targetNick = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True) # automatically adds
    overallScore = models.DecimalField(max_digits = 5,decimal_places=2,default=-1)
    #drivingScore = commuteScore
    driveScore = models.DecimalField(max_digits = 5,decimal_places=2,default=-1)
    restScore = models.DecimalField(max_digits = 5,decimal_places=2,default=-1)
    hospScore = models.DecimalField(max_digits = 5,decimal_places=2,default=-1)
    groceryScore = models.DecimalField(max_digits = 5,decimal_places=2,default=-1)

    def __str__(self): # right now if database has same nickname, replacing with the newest value
        return self.startNick

