from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class UserModel(AbstractUser):
    userProfile=models.ImageField(upload_to="user")
    type=models.CharField(max_length=20,default='#')
    password = models.CharField(max_length=150, default='#')


class book(models.Model):
    # Fields of the model
    name = models.CharField(max_length=200)
    mobilenum = models.IntegerField()
    email = models.TextField()
    date = models.DateTimeField()
    doctor = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    prescription = models.TextField(null=True, blank=True) 

class Category(models.Model):

    #fields of the model
    title = models.CharField(max_length = 200)
    description = models.TextField()


    #renames the instances of the model
    #with their title name
    def __str__(self):
        return self.title
    


# models.py
class OpenAIData(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class mcs1(models.Model):
    usid = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    a=models.TextField()
    b=models.TextField()
    c=models.TextField()
    d=models.TextField()
    e=models.TextField()
    f=models.TextField()
    g=models.TextField()
    h=models.TextField()
    i=models.TextField()
    j=models.TextField()

