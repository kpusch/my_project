from django.shortcuts import render

# Create your views here.

#전체 추가
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
#from stapp.forms import SignupForm
#from django.contrib.auth.decorators import login_required
#from qna.models import Question

def signup(request):
    """signup
    to register users
    """
    if request.method == "POST":
        userform = UserCreationForm(request.POST)
        #signupform = SignupForm(request.POST)
        #if signupform.is_valid():
        if userform.is_valid():
            #user = signupform.save(commit=False)
            #user.email = signupform.cleaned_data['email']
            #user.save()
            userform.save()

            return HttpResponseRedirect(
                reverse("signup_ok")
            )
    elif request.method == "GET":
        #signupform = SignupForm()
        userform = UserCreationForm()

    return render(request, "registration/signup.html", {
        #"signupform": signupform,
        "userform": userform,
    })

def about(request):
    return render(request, "about.html")

def home(request):
    return render(request, "index.html")

def question(request):
    return render(request, "question.html")
