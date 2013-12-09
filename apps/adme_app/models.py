import string
import random

from datetime import datetime    
from django.db import models
from django.contrib.auth.models import User
import socket
import smtplib
from email.MIMEText import MIMEText

class Target(models.Model):
    incoming_bitly = models.CharField(max_length=256)
    outgoing_bitly = models.CharField(max_length=256)
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
    name = models.CharField(max_length=64)
    dob = models.DateField(null=True)
    gender_male = models.NullBooleanField(null=True)
    confirmation_hash = models.CharField(max_length=64)
    def __unicode__(self):
        if self.name!='':
            return self.name
        else:
            return self.auth_user.email
    def send_confirmation_email(self):
        message = 'Thanks again for joining\n\nPlease hit this url either by clicking on it or copy-pasting it into your browser:\n'
        self.confirmation_hash = self.generate_confirmation_hash()
        confirmation_string = socket.gethostname() + '/u/' + self.confirmation_hash + '/confirm/'
        confirmation_url = '<a href="'
        confirmation_url += confirmation_string
        confirmation_url += '" >'
        confirmation_url += confirmation_string
        confirmation_url += '</a>'
        message += confirmation_url
        server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
        server.ehlo()
        server.starttls()
        server.ehlo()
        myusername = '' #Dont forget to put this back before doing any commits to github!!
        mysupersecretpassword = '' #Dont forget to put this back before doing any commits to github!!
        server.login(myusername,mysupersecretpassword)
        m = MIMEText(message)
        m['Subject'] = 'New User Confirmation'
        m['From'] = myusername
        m['To'] = self.auth_user.email
        server.sendmail(myusername,self.auth_user.email,m.as_string())
        server.close()  
    def generate_confirmation_hash(self):
        #TODO - A real hash instead of just the ID
        #key1 = self.auth_user.date_joined
        #key2 = datetime.now()
        #key3 = self.auth_user.email
        #conf_hash = somefunc(key1) + key2 + key3
        return str(self.auth_user.id)
    
    
    
    
    
    
    
    
    
class Contract(models.Model):
    target_url = models.CharField(max_length="32")
    def get_simple_stats(self):
        return str(self.link_set.count()) + ' links had ' + str(Click.objects.filter(link__contract__id=self.id).count()) + ' clicks on this contract.'   
    
class Link(models.Model):
    contract = models.ForeignKey(Contract, null=True, blank=True)
    short_form = models.CharField(max_length="32")
    #activated_by = models.ForeignKey(User, blank=True)
    activated_by = models.CharField(max_length="16")
        
        
class Click(models.Model):
    link = models.ForeignKey(Link)
    date_clicked = models.DateTimeField(auto_now_add=True)
    
    
    
    
    
    
    
    
    
    

    