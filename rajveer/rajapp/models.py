
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Employee(models.Model):
       
        name = models.CharField(max_length=100)
        designation = models.CharField(max_length=100)

class Product(models.Model):
       
        product_name = models.CharField(max_length=100)
        desc = models.CharField(max_length= 100)
        emp = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name="emp")

class PhoneOTP(models.Model):
        email = models.CharField(max_length=100)
        otp = models.IntegerField(default =1)
        password =models.IntegerField(default = 1)

class UserOtp(models.Model):
        otp = models.CharField(max_length=100)
        key = models.OneToOneField(User,on_delete=models.CASCADE,related_name = "key")

