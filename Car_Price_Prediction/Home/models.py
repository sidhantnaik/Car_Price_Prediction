from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    desc=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.name
    

    
#regisiter this in the admin.py

    
