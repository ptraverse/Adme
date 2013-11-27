import bitly_api
import socket
import sys
from datetime import datetime
    
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.utils import simplejson

from adme_app.models import Target

def auth_log_in(request):
    if request.method=='POST':
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../all-stats' )    
            else:
                return HttpResponseRedirect('../sign-up')
    else:
        return render(request,'login.html' )

def auth_log_out(request):
    logout(request)
    return HttpResponseRedirect('../')

def auth_sign_up(request):
    if request.method=='POST':
        # TODO: Use CSS3 in /templates/signup.html to validate the input
        email = request.POST.get("element_email","")
        password = request.POST.get("element_password","")
        u = User.objects.create_user(email,email,password)
        return HttpResponseRedirect('../new-target')
    else:
        return render(request,'signup.html', { "message": "There was a problem with your sign up, please try again."} )
    
def hello_world(request,word):
    if (word==''):
        word = 'World'
    return render(request, 'hello_world.html', { "word":word } )    

def new_target(request):
    return render(request, 'new_target.html' )

def create_target_json(request):
    if request.POST.has_key('client_response'):
        API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
        API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
        ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4" 
        b = bitly_api.Connection(access_token=ACCESS_TOKEN)
        x = request.POST.get('client_response','')                 
        y = b.shorten(uri=x)
        # y.new_hash           #if this is the first time this long_url was shortened by this user.
        # y.url                #the actual link that should be used,
        # y.hash               #a bitly identifier for long_url which is unique to the given account.
        # y.global_hash        #a bitly identifier for long_url which can be used to track aggregate stats across all bitly links that point to the same long_url
        # y.long_url           #an echo back of the longUrl request parameter.
          
        t = Target.objects.create()
        t.endpoint = y.get('url')
        t.user_created_id = request.user.id
        t.save()  
                       
        response_dict = {}                                         
        response_dict.update({'server_response': y })
        response_dict.update({'target_date_created': str(t.date_created) })                                                                  
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
