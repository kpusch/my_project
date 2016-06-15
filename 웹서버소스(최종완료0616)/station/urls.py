from django.conf.urls import *
from django.contrib import admin
from stapp import main_views
from stapp.forms import LoginForm  
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^stapp/$', main_views.main_page), 
    url(r'^admin/', admin.site.urls),               #관리자페이지

    url(r'^signup/$', 'stapp.views.signup', name='signup'), #회원가입
    url(r'^signup_ok/$', TemplateView.as_view(              #회원가입완료
        template_name='registration/signup_ok.html'), name='signup_ok'), #name='signup_ok'
    url(r'^$', 'stapp.views.home', name='home'),
    url(r'^about/$', 'stapp.views.about', name='about'),
    url(r'^q/$', 'stapp.views.question', name='question'),
    url(r'^post/$', 'stapp.views.post', name='post'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'authentication_form': LoginForm
        }, name='login_url'), #name='login_url'
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
           'next_page': '/login/',}, name='logout_url'),   #name='logout_url'
    url(r'^question/(?P<question_id>[0-9]+)/$',
        'stapp.views.question', name='view_question'
    ),
    url(r'^summernote/', include('django_summernote.urls')),
] 
