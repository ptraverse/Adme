import bitly_api
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
    
    
    
    
class Business(models.Model):
    auth_user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length="64")
    contact_person = models.CharField(max_length="64")
    contact_phone = models.CharField(max_length="12")
    address = models.CharField(max_length="64")    
    
    
class Contract(models.Model):
    target_url = models.CharField(max_length="32")
    payout_clicks_required = models.CharField(max_length="32")
    payout_description = models.CharField(max_length="128")
    expiry_date = models.CharField(max_length="32")
    expiry_amount = models.CharField(max_length="32")
    created_by_business = models.ForeignKey(Business)
    def get_simple_stats(self):
        return str(self.link_set.count()) + ' links had ' + str(Click.objects.filter(link__contract__id=self.id).count()) + ' clicks on this contract.'   
    def interpret_string(self):
        interpret_string = 'company x promises to give '
        interpret_string += str(self.payout_description)
        interpret_string += ' for every ' 
        interpret_string += str(self.payout_clicks_required)
        interpret_string += ' clicks that provide a redirect to '
        interpret_string += str(self.target_url)
        interpret_string += ', up to the maximum total amount of '
        interpret_string += str(self.expiry_amount)
        interpret_string += '$, with the contract expiring '
        interpret_string += str(self.expiry_date)
        interpret_string += '.'
        return  interpret_string
    def get_num_clicks(self,request):
        ll = Link.objects.filter(contract=self)
        counter = 0
        for link in ll:
            counter += link.get_num_clicks(request)
        return counter
        
class Link(models.Model):
    contract = models.ForeignKey(Contract, null=True, blank=True)
    short_form = models.CharField(max_length="254")
    #activated_by = models.ForeignKey(User, blank=True)
    activated_by = models.CharField(max_length="64")
    bitly_hash = models.CharField(max_length="16")
    bitly_long_url = models.CharField(max_length="64")
    def get_num_clicks(self, request):
        global bitly
        print 'getting num clicks'
        bitly = request.session['bitly']
        bitly_response = bitly.clicks(shortUrl=self.short_form)
        print 'got num clicks'
        return bitly_response[0]['user_clicks']
        
class Click(models.Model):
    link = models.ForeignKey(Link)
    date_clicked = models.DateTimeField(auto_now_add=True)
    
     
    
    
    
    
    
    
    
    

    