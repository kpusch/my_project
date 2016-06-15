from django.contrib import admin
from stapp.models import Person  #추

from stapp.models import Question  #추가
# Register your models here.

admin.site.register(Person) #추가
admin.site.register(Question)  #추
