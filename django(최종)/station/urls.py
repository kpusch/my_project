from django.conf.urls import *
from django.contrib import admin
#admin.autodiscover()
from stapp import main_views
from stapp.forms import LoginForm  #6
#from stapp import views
#from login import views

############
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^stapp/$', main_views.main_page),
    url(r'^admin/', admin.site.urls),
    #(r'^search/(?P<mode>[a-z,A-Z]+)/(?P<keyword>\S+)/Page(?P<page>\d+)/$', search_views.BlogSearchPage),
    #(r'^search/(?P<mode>[a-z,A-Z]+)/(?P<keyword>\S+)/$', search_views.BlogSearchPage),

    #url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'c:\\project\\station\\stapp\\images'}),
    #url(r'^administrator/login/$', 'administrator.views.login_user'),
    #url(r'^administrator/logout/$', 'administrator.views.logout_user'),

    #로그인 추가
    #url(r'^$', 'django.contrib.auth.views.login'),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^login/$', views.logout_page),
    #url(r'^logout/$', logout_page),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    #url(r'^register/$', register),
    #url(r'^register/success/$', register_success),
    #url(r'^home/$', home),

    ###########


    ##slidshar

    url(r'^signup/$', 'stapp.views.signup', name='signup'),
    url(r'^signup_ok/$', TemplateView.as_view(
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
    #url(r'^$', 'stapp.views.home'),
] 
