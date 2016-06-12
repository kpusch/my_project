# -*- coding: cp949 -*-
from django.http import HttpResponse

##login,logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.contrib.auth.forms import UserCreationForm
from qna.forms import SignupForm

#for template 다른거
from django.template import Context, loader

def main_page(req):
    tpl = loader.get_template('main.html')
    ctx = Context({
    })
    html = tpl.render(ctx)
    return HttpResponse(html)
###################

##login slideshare
def signup(request);
    """signup
    to register users
    """
    if request.method == "POST":
        #userform = UserCreationForm(request.POST)
        signupform = SignupForm(request.POST)
        if userform.is_valid():
            user = signupform.save(commit=False)
            user.email = signupform.cleaned_data['email']
            #userform.save()
            user.save()
            
            return HttpResponseRedirect(
                reverse("signup_ok")
            )
        elif request.method == "GET":
            #userform = UserCreationForm()
             signupform = SignupForm()
             
        return render(request, "registration/signup.html",{
            "signupform": signupform,   #user => signup
        })
#####
