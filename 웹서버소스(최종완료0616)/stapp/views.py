# Create your views here.
from django.shortcuts import render, get_object_or_404   #404 에러 부르는 모듈
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from stapp.forms import SignupForm, PostForm   #stapp 내부의 forms.py 파일에서 함수 import
from django.contrib.auth.decorators import login_required #로그인 된 후에 실행 가능하게 하는 모듈
from stapp.models import Question  #Question 모델 가져옴

def signup(request):            #함수 추가(회원가입)
    """signup
    to register users
    """
    if request.method == "POST":
        signupform = SignupForm(request.POST)
        
        if signupform.is_valid():
            user = signupform.save(commit=False)
            user.email = signupform.cleaned_data['email']
            user.save()             #DB에 저장
            
            return HttpResponseRedirect(
                reverse("signup_ok")
            )
    elif request.method == "GET":
        signupform = SignupForm()
        

    return render(request, "registration/signup.html", {
        "signupform": signupform,
        
    })

def home(request):              #함수 추가
    return render(request, "index.html")    #index.html 호출

def about(request):             #함수 추가
    return render(request, "about.html")    #about.html 호출

def question(request, question_id=0):   #함수 추가
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
            post.save()         #글쓴내용 DB에 저장 

            return HttpResponseRedirect(reverse('home'))

    elif request.method == "GET":
        postform = PostForm()

    return render(request, "post.html", {   #post.html 호출
        'postform': postform,
    })
