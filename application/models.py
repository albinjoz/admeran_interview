from django.db import models

from django.contrib.auth.models import User as AuthUser
# Create your models here.

class Snippet (models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    created_user =  models.ForeignKey(AuthUser, on_delete = models.CASCADE)
    description = models.TextField(null=True, blank=True)

class Tag (models.Model):
    title = models.CharField(max_length=100, blank=True, null= True, unique=True)
    snippet = models.ForeignKey(Snippet, on_delete = models.CASCADE)
