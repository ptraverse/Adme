from django.db import models
from django.contrib.auth.models import User
import string
import random
from datetime import datetime    

class Target(models.Model):
    startpoint = models.CharField(max_length=256)
    endpoint = models.CharField(max_length=256)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    #image_file
    user_created = models.ForeignKey(User, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    #def create_target(self, endpoint, user):
    #    target = self.create(endpoint=endpoint, user_created=user)
    #    return target
    
class Extended_User(models.Model):
    auth_user = models.ForeignKey(User, blank=True, null=True)
    activated_date = models.DateTimeField(null=True)
    name = models.CharField(max_length=64)
    dob = models.DateField(null=True)
    gender_male = models.NullBooleanField(null=True)
    def __unicode__(self):
        return self.name