# -*- coding: cp949 -*-
from django.http import HttpResponse

#for template
from django.shortcuts import render
from django.template import Context, loader
from stapp.models import *

def main_page(req):
    tpl = loader.get_template('main.html')
    ctx = Context({
    })
    html = tpl.render(ctx)
    return HttpResponse(html)




##로그인,로그아웃
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('login_user_id')
        password = request.POST.get('login_password')

        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in !"
            else:
                state = "Your account is not active, please contact the site admin"
        else:
            state = "Your username and/or password were incorrect"

    return HttpResponseRedirect('/administrator/')

def logout_user(request):
    logout(request)
    response = redirect('administrator.views.home')
    response.delete_cookie('user_location')
    return response
#########
