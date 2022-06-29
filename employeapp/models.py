from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    user = None
    email = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=50,blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Employee(models.Model):
    firstname = models.CharField(max_length=50,blank=True,null=True)
    lastname = models.CharField(max_length=50,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True,unique=True)
    role = models.CharField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.firstname


class Timecalc(models.Model):
    checkstate = models.CharField(max_length=15,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.time}  --- {self.checkstate}'

class Leave(models.Model):
    full_day_or_half_day_date_or_late_comming_or_early_logout_time = models.CharField(max_length=12,blank=True,null=True)
    leavetype = models.CharField(max_length=15,blank=True,null=True)
    system_time = models.DateTimeField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)








