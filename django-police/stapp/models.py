from django.db import models

from django.contrib.auth.models import User #추

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    


######추가
"""class Question(models.Model):
    ""question
    when a user posts questions
    ""
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __unicode__(self):
        return u"{0}".format(self.title)"""
##
