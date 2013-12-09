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
from adme_app.models import Extended_User
from adme_app.models import Contract, Link, Click


def target_create_form(request):
    return render(request, 'create_target_form.html' )

def create_target(request):
    return render(request, 'create_target.html')

def show_target(request, target_id):
    t = Target.objects.get(id=target_id)
    return render(request, 'show_target.html', { "target":t })
    #todo change this so that it uses the startpoint bitly

def edit_target(request, target_id):
    t = Target.objects.get(id=target_id)
    return render(request, 'edit_target.html', { "target":t, "user":request.user })

def user_stats(request):
    user = User.objects.get(email=request.user)
    targetlist = Target.objects.all()
    #API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
    #API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
    #ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4" 
    #b = bitly_api.Connection(access_token=ACCESS_TOKEN)
    #for target in targetlist:
        #endpoint_bitly = b.expand(shortUrl=target.endpoint)
        #TODO Get this part working
        #target.endpoint_bitly_ghash = endpoint_bitly
    return render(request, 'user_stats.html', { "user":user, "targetlist":targetlist })

def auth_log_in(request):
    if request.method=='POST':
        username = request.POST.get("element_username","")
        password = request.POST.get("element_password","")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../all-stats' )    
            else:
                return render(request,'signup.html', { "message": "Not activated yet."} )
        else:
            return render(request,'signup.html', { "message": "Email not recognized. Why don't you sign up?"} )
    else:
        return render(request,'login.html' )

def auth_log_out(request):
    logout(request)
    return HttpResponseRedirect('../')

def auth_sign_up(request):
    if request.method=='POST':
        # TODO: Use CSS3 in /templates/signup.html to validate the input
        email = request.POST.get("element_email","")
        email_confirm = request.POST.get("element_email_confirm","")
        password = request.POST.get("element_password","")
        password_confirm = request.POST.get("element_password_confirm","")
        agree = request.POST.get("element_agree","")
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            return render(request,'signup.html', { "message": "Malformed Email"} )
        if len(password)<4:
            return render(request,'signup.html', { "message": "Password too short- 4 characters minimum."} )
        if (email!=email_confirm):
            return render(request,'signup.html', { "message": "Emails Mismatch"} )
        if (password!=password_confirm):
            return render(request,'signup.html', { "message": "Password Mismatch"} )
        if not (agree):
            return render(request,'signup.html', { "message": "I Agree Left Unchecked"} )
        else:
            #try:
            #    u = User.objects.create_user(email,email,password,is_active=0)
            #except:
            #    return render(request,'signup.html', { "message": "Email Already Taken"} )
            u = User.objects.create_user(email,email,password)
            u.is_active=0
            u.save()
            e = Extended_User.objects.create()
            e.auth_user_id = u.id
            e.save()        
            e.send_confirmation_email()
            return render(request,'confirm.html', { "user_email":email } )
    else:
        return render(request,'signup.html')

def auth_user_confirm(request,auth_user_id):
    #TODO Use the Hash instead of hte ID
    #Should the hash somehow encode the password also to do autologin after confirmation?
    auth_user = User.objects.get(id=auth_user_id)
    auth_user.is_active = True
    auth_user.save()
    email = auth_user.email
    return render(request,'confirm_thanks.html', { "email":email } )
    
    
def hello_world(request,word):
    if (word==''):
        word = 'World'
    return render(request, 'hello_world.html', { "word":word } )    

def  index(request):
    if (str(request.user)!="AnonymousUser"):
        return render(request, 'user_home.html', { "user":request.user })
    else:
        return render(request, 'index.html' )

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
        response_dict.update({'target_created_by': str(request.user) })                                                                                                                             
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')




def test_module(request):
        c = Contract.objects.create()
        l1 = Link.objects.create(short_form="wmnk/a",contract_id=c.id,activated_by=1)
        l2 = Link.objects.create(short_form="wmnk/b",contract_id=c.id,activated_by=2)
        c1 = Click.objects.create(link_id=l1.id)
        c2 = Click.objects.create(link_id=l2.id)
        c3 = Click.objects.create(link_id=l2.id)
        m = c.get_simple_stats()
        return render(request, 'echo_template.html', { "message":m } )
    

    