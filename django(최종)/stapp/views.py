

# Create your views here.

#전체 추가
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from stapp.forms import SignupForm, PostForm
#from stapp.forms import SignupForm
from django.contrib.auth.decorators import login_required
from stapp.models import Question  #Question 모델 가져옴

def signup(request):
    """signup
    to register users
    """
    if request.method == "POST":
        signupform = SignupForm(request.POST)
        #signupform = SignupForm(request.POST)
        if signupform.is_valid():
            user = signupform.save(commit=False)
            user.email = signupform.cleaned_data['email']
            user.save()
            #userform.save()

            return HttpResponseRedirect(
                reverse("signup_ok")
            )
    elif request.method == "GET":
        signupform = SignupForm()
        #userform = UserCreationForm()

    return render(request, "registration/signup.html", {
        "signupform": signupform,
        #"userform": userform,
    })

def home(request):   
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def question(request, question_id=0):
    """
    viewing the question
    """
    if int(question_id) == 0:
        HttpResponseRedirect(reverse('home'))

    q = get_object_or_404(Question, id=question_id)

    return render(request, "question.html", {
        'question': q,
    })

@login_required   #글쓰기 로그인 된 후에 가능하게
def post(request):
    """
    posting questions
    """
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.user = request.user
            post.save()

            return HttpResponseRedirect(reverse('home'))

    elif request.method == "GET":
        postform = PostForm()

    return render(request, "post.html", {
        'postform': postform,
    })
