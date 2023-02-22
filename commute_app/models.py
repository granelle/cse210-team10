from django.db import models

# Create your models here.

# Need to run these after adding any models:
# python3 manage.py makemigrations 
# python3 manage.py migrate

class Commute_Search(models.Model):
    start = models.TextField() # might need to be CharField?
    end = models.TextField()
    start_nick = models.CharField(max_length=50)
    end_nick = models.CharField(max_length=50)
    # add weights here later