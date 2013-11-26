from django.db import models
from django.contrib.auth.models import User
import string
import random
from datetime import datetime    

class Target(models.Model):
    startpoint = models.ForeignKey(Bitly)
    endpoint = models.ForeignKey(Bitly)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    #image_file
    user_created = models.ForeignKey(User, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
class Bitly(models.Model):
    hash = models.CharField(max_length=16)
    ghash = models.CharField(max_length=16)
    