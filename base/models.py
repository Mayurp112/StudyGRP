from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    #participent
    name=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        ordering=['-updated_at','-created_at']


    def __str__(self):
        return self.name
    

class message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField(max_length=200)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

