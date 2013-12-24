import bitly_api
import socket
import sys
from datetime import datetime

#from ghost import Ghost
    
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.http import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.utils import simplejson

from adme_app.models import Target
from adme_app.models import Extended_User
from adme_app.models import Business, Contract, Link, Click

def is_valid(request, form):
    if form=='auth_sign_up':
        email = request.POST.get("element_email","")
        email_confirm = request.POST.get("element_email_confirm","")
        password = request.POST.get("element_password","")
        password_confirm = request.POST.get("element_password_confirm","")
        agree = request.POST.get("element_agree","")
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            return "Malformed Email"
        if len(password)<4:
            return "Password too short- 4 characters minimum."
        if (email!=email_confirm):
            return "Emails Mismatch" 
        if (password!=password_confirm):
            return "Password Mismatch" 
        if not (agree):
            return "I Agree Left Unchecked" 
        else:
            return True
    #else if form=='':
        #...
    else:
        return { "invalid": "No Form Name Specified" }

def target_create_form(request):
    return render(request, 'create_target_form.html' )

def create_target(request):
    return render(request, 'create_target.html')

def show_target(request, target_id):
    t = Target.objects.get(id=target_id)
    return render(request, 'show_target.html', { "target":t } )
    #todo change this so that it uses the startpoint bitly

def edit_target(request, target_id):
    t = Target.objects.get(id=target_id)
    return render(request, 'edit_target.html', { "target":t, "user":request.user } )

def user_stats(request):
    u = User.objects.get(email=request.user)
    ll = Link.objects.filter(activated_by=request.user.email)
    e = Extended_User.objects.get(auth_user=request.user.id)
    b = Business.objects.get(auth_user=request.user.id)        
    #API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
    #API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
    #ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4" 
    #b = bitly_api.Connection(access_token=ACCESS_TOKEN)
    #for target in targetlist:
        #endpoint_bitly = b.expand(shortUrl=target.endpoint)
        #TODO Get this part working
        #target.endpoint_bitly_ghash = endpoint_bitly
    return render(request, 'user_stats.html', { "user":u, "linklist":ll, "extended_user":e, "business":b } )

def auth_log_in(request):
    if request.method=='POST':
        username = request.POST.get("element_username","")
        password = request.POST.get("element_password","")
        user = authenticate(username=username, password=password)
        e = Extended_User.objects.get(auth_user = user.id)
        b = Business.objects.filter(auth_user = user.id)
        if user is not None:
            if user.is_active:
                API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
                API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
                ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4" 
                bitly = bitly_api.Connection(access_token=ACCESS_TOKEN)
                request.session['bitly'] = bitly
                login(request, user)
                return HttpResponseRedirect('../home')    
            else:
                return render(request,'signup.html', { "message": "Not activated yet."} )
        else:
            return render(request,'signup.html', { "message": "Email not recognized. Why don't you sign up?"} )
    else:
        return render(request,'login.html' )

def auth_log_out(request):
    logout(request)
    return HttpResponseRedirect('../')

def home(request):
    e = Extended_User.objects.filter(auth_user=request.user.id)
    b = Business.objects.filter(auth_user=request.user.id)
    if b:
        cl = Contract.objects.filter(created_by_business=b)
        for c in cl:
            print 'getting num activated links'
            c.num_activated_links = Link.objects.filter(contract=c).exclude(activated_by='').count()
            print c.num_activated_links
            c.num_clicks = c.get_num_clicks(request)   
            # c.num_remaining_links = 
        ll = Link.objects.filter(contract__in=cl).select_related
        return render(request, 'business_home.html', { "extended_user":e, "business":b, "linklist":ll, "contractlist":cl } )
    if e:
        return render(request, 'user_home.html', { "extended_user":e } )
    else:
        return HttpResponseRedirect('/')

# def auth_sign_up(request):
#     if request.method=='POST':
#         email = request.POST.get("element_email","")
#         email_confirm = request.POST.get("element_email_confirm","")
#         password = request.POST.get("element_password","")
#         password_confirm = request.POST.get("element_password_confirm","")
#         agree = request.POST.get("element_agree","")
#         try:
#             valid = is_valid(request, 'auth_sign_up')
#             if valid:
#                 u = User.objects.create_user(email,email,password)
#                 u.is_active=0
#                 u.save()
#                 e = Extended_User.objects.create()
#                 e.auth_user_id = u.id
#                 e.save()        
#                 #e.send_confirmation_email()
#                 return render(request,'confirm.html', { "user_email":email } )
#             else:
#                 m = valid
#                 return render(request,'signup.html', { "message":m } )
#         except IntegrityError, e:
#             m ="""
#             Error
#             
#             IntegrityError
# 
#             Some Lazy Programmer hasn't figured out what to do if this happens. 
#             (But he's guessing you tried to register with an email that already exists...)
#             
#             """
#             return render(request,'echo_template.html', { "message":m } )
#     else:
#         return render(request,'signup.html')

def auth_sign_up(request):
    if request.method=='POST':
        email = request.POST.get("element_email","")
        email_confirm = request.POST.get("element_email_confirm","")
        password = request.POST.get("element_password","")
        password_confirm = request.POST.get("element_password_confirm","")
        agree = request.POST.get("element_agree","")
        valid = is_valid(request, 'auth_sign_up')
        if valid:
            u = User.objects.create_user(email,email,password)
            u.is_active=0
            u.save()
            e = Extended_User.objects.create()
            e.auth_user_id = u.id
            e.save()        
            #e.send_confirmation_email()
            return render(request,'confirm.html', { "user_email":email } )
        else:
            m = valid
            return render(request,'signup.html', { "message":m } )
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

def index(request):
    if (str(request.user)!="AnonymousUser"):
        e = Extended_User.objects.get(auth_user=request.user.id)
        b = Business.objects.filter(auth_user=request.user.id)
        if b:
            return render(request, 'user_home.html', { "user":request.user, "extended_user":e, "business":b } )
        else:
            return render(request, 'user_home.html', { "user":request.user, "extended_user":e } )
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
    domain = request.get_host()
    m = domain
    return render(request, 'echo_template.html', { "message":m } )

def contract_create(request):
    if request.user:
        e = Extended_User.objects.get(auth_user=request.user.id)        
        b = Business.objects.filter(auth_user=request.user.id)
        if b:
            return render(request, 'contract_create_form.html', { "user":request.user, "extended_user":e, "business":b } )
        else:
            return render(request, 'user_home.html', { "user":request.user,  "business":b } )
    return render(request, 'contract_create_form.html' , { "business":b, "extended_user":e } )

def contract_create_action(request):
    if request.method=='POST':
        target_url = request.POST.get("element_target_url","")        
        payout_clicks_required = request.POST.get("element_payout_clicks_required","")
        payout_description = request.POST.get("element_payout_description","")
        expiry_date = request.POST.get("element_expiry_date","")
        expiry_amount = request.POST.get("element_expiry_amount","")
        initial_num_links = request.POST.get("element_initial_num_links","")
        #todo - put the validation into is_valid()
        if is_valid(request, 'contract_create_action'):
            b = Business.objects.get(auth_user=request.user.id)
            assert b            
            c = Contract.objects.create(created_by_business=b)            
            c.target_url = target_url     
            c.payout_clicks_required = payout_clicks_required 
            c.payout_description = payout_description 
            c.expiry_date = expiry_date 
            c.expiry_amount = expiry_amount 
            c.save()
            linklist = []
            for i in range(1,int(initial_num_links)+1):
                l = Link.objects.create()
                l.contract_id = c.id
                API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
                API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
                ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4" 
                b = bitly_api.Connection(access_token=ACCESS_TOKEN)                             
                domain = request.get_host()
                long_url = 'http://' + domain + '/link/' + str(c.id) + '-' + str(l.id)
                y = b.shorten(uri=long_url)
                l.short_form = y['url']       
                l.bitly_hash = y['hash']
                l.bitly_long_url = y['long_url']    
                l.save()
                linklist.append(l)
            m = c.interpret_string()
            #todo - add more message
            return HttpResponseRedirect('/business/contracts/')
            #return render(request, 'contract_links_div.html', {"message":m, "linklist":linklist } )
        else:
            return render(request, '/contract-create/')

def business_contracts(request):
    e = Extended_User.objects.get(auth_user=request.user.id)
    b = Business.objects.get(auth_user=request.user.id)
    cl = Contract.objects.filter(created_by_business=b)
    for contract in cl:
        contract.num_clicks = contract.get_num_clicks()
        print(contract.num_clicks)
        print('foo')
        contract.payout_clicks_remaining = contract.payout_clicks_required - contract.num_clicks
        print(contract.payout_clicks_remaining)
        print('bar')
    return render(request, 'business_contracts.html', { "business":b, "contractlist":cl, "extended_user":e } )

def contract_clicks(request,contract_id):
    e = Extended_User.objects.get(auth_user=request.user.id)
    c = Contract.objects.get(id=contract_id)
    contract_b = Business.objects.get(id=c.created_by_business.id)
    user_b = Business.objects.get(auth_user=request.user.id)
    if contract_b == user_b: 
        #cl = Click.objects.filter()
        #nwo use the bitly stuff
        return render(request, 'contract_clicks.html', { "contract":c, "extended_user":e, "clicklist":cl, "business":user_b } )
    else:
        return render(request, 'echo_template', {"message":'Error: You dont have permission to see details of this contract' } )
    

#ghost = Ghost() 
#page, extra_resources = ghost.open("http://google.com")
#m = []
#for e in (extra_resources):
#    m.append(str(e))
#return render(request, 'echo_template.html', {"message":m } )
#assert page.http_status==200 and 'jeanphix' in ghost.content
        
        
def view_link(request,contract_id,link_id):
    l = Link.objects.get(id=link_id)
    if l.activated_by=='':         
        return link_activate(request,link_id)
    else:
        c = Contract.objects.get(id=contract_id)
        final_url = c.target_url
        return HttpResponseRedirect( final_url )
    return render(request, 'echo_template.html', { "message":'fukc!' } )
        
def link_activate(request,link_id):
    l = Link.objects.get(id=link_id)
    c = Contract.objects.get(id=l.contract_id)    
    return render(request, 'inactive_link.html', {"link":l, "contract":c } )
    
def link_activate_action(request):    
    if request.method=='POST':
        #todo - put the validation into is_valid()
        activation_email = request.POST.get("element_activation_email","")
        link_id = request.POST.get("element_link_id","")
        l = Link.objects.get(id=link_id)
        l.activated_by = str(activation_email)
        l.save()
        c = Contract.objects.get(id=l.contract_id)
        b = Business.objects.get(id=c.created_by_business_id)
        return render(request, 'link_activated.html', { "link":l, "contract":c, "contract_business":b } )
    else:
        m = 'no post error!'
        return render(request, 'echo_template.html', { "message":m} )
  
@login_required
def contract_links(request, contract_id):        
    e = Extended_User.objects.get(auth_user=request.user.id)
    c = Contract.objects.get(id=contract_id)
    b = Business.objects.get(auth_user=request.user.id)
    ll = Link.objects.filter(contract=c.id)
    llc = Link.objects.filter(contract=c.id).count()
    print llc
    for l in ll:
        print l
        l.num_clicks = l.get_num_clicks(request) 
    return render(request, 'contract_links.html', { "linklist":ll, "extended_user":e, "contract":c, "business":b } )

def business_signup_action(request):
    if request.method=='POST':
        email = request.POST.get("element_b_email","")        
        email_confirm = request.POST.get("element_b_email_confirm","")
        password = request.POST.get("element_b_password","")
        password_confirm = request.POST.get("element_b_password_confirm","")
        name = request.POST.get("element_b_name","")
        phone = request.POST.get("element_b_phone","")
        person = request.POST.get("element_b_person","")
        address = request.POST.get("element_b_address","")
        agree = request.POST.get("element_b_agree","")
        #todo - put the validation into is_valid()
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
            #create auth user
            u = User.objects.create_user(email,email,password)
            u.is_active=0
            u.save()
            #create extended user
            e = Extended_User.objects.create()
            e.auth_user_id = u.id
            e.save()        
            #create business
            b = Business.objects.create()
            b.auth_user_id =  u.id
            b.name = name 
            b.contact_person =  person
            b.contact_phone = phone 
            b.address = address
            b.save()
            #e.send_confirmation_email()
            m = 'New Business Created ' + str(b.id) + ' and ' + str(b.contact_person)
            return render(request, 'welcome.html', { "business":b, "extended_user":e } )
    else:
        return render(request, 'echo_template.html', { "message":m } )