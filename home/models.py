# from asyncio.windows_events import NULL
from distutils.command.upload import upload
import email
from enum import unique
from pyexpat import model
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



from django.forms import ModelForm, NullBooleanField, PasswordInput
from django.forms.fields import ImageField

from datetime import datetime

# Create your models here.

class User(AbstractUser):
    gender=models.CharField(choices=[('Male','Male'),('Female','Female')],max_length=15)
    height=models.IntegerField(null=False, default=0)
    weight=models.IntegerField(null=False, default=0)
    date=models.DateField(null=False,default=datetime.now())
    def __str__(self):
        return self.last_name + " " + self.first_name 
    class Meta:  
        db_table = "User"  
        
from django.core.validators import RegexValidator
class Doctor(models.Model):
    username=models.CharField(max_length=100)
    Surname=models.CharField(max_length=100)
    email=models.CharField(max_length=250,unique=True)
    phone_number = models.CharField(max_length=17,blank=False, unique=True) # Validators should be a list
    Specialization=models.CharField(choices=[('Orthopedics','Orthopedics'),(' Internal Medicine',' Internal Medicine'),('Obstetrics and Gynecology','Obstetrics and Gynecology'),('Dermatology','Dermatology'),('Pediatrics','Pediatrics'),('General Surgery','General Surgery'),('Radiology','Radiology'),('Ophthalmology','Ophthalmology'),(' Family Medicine',' Family Medicine'),('ENT','ENT')],max_length=500)
    gender=models.CharField(choices=[('Male','Male'),('Female','Female')],max_length=15)
    USERNAME_FIELD = 'username'
    
class ConfirmDoctor(models.Model):
    username=models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

       
class ViewDoctor(models.Model):
     user=models.ForeignKey(User, on_delete=models.CASCADE)
     doctor=models.ForeignKey(ConfirmDoctor, on_delete=models.CASCADE)
     status = models.IntegerField(null=False, default=0)


class Cbc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rbc = models.FloatField(null=True,blank=True,default=None,max_length=150)
    wbc = models.FloatField(blank=True,default=None,null=True,max_length=150)
    pc = models.FloatField(null=True,blank=True,default=None,max_length=25)
    hgb = models.FloatField(null=True,blank=True,default=None,max_length=150)
    rcd= models.FloatField(null=True,blank=True,default=None,max_length=150)
    mchc = models.FloatField(null=True,blank=True,default=None,max_length=150)
    mpv = models.FloatField(null=True,blank=True,default=None,max_length=150)
    pcv = models.FloatField(null=True,blank=True,default=None,max_length=150)
    mcv = models.FloatField(null=True,blank=True,default=None,max_length=150)
    name= models.CharField(max_length=150,null=True,blank=False)
    password=models.CharField(max_length=150,null=True,blank=True)
    date = models.DateTimeField(default=datetime.now())
    image = models.ImageField(default=None, null=True)
    file = models.FileField(default=None, null=True)
    rbc_enc = models.BinaryField(default=None, null=True, editable=True)
    wbc_enc = models.BinaryField(default=None, null=True, editable=True)
    pc_enc = models.BinaryField(default=None, null=True, editable=True)
    hgb_enc = models.BinaryField(default=None, null=True, editable=True)
    rcd_enc = models.BinaryField(default=None, null=True, editable=True)
    mchc_enc = models.BinaryField(default=None, null=True, editable=True)
    mpv_enc = models.BinaryField(default=None, null=True, editable=True)
    pcv_enc = models.BinaryField(default=None, null=True, editable=True)
    mcv_enc = models.BinaryField(default=None, null=True, editable=True)
   

class tempFileStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(default=None, null=True)


class  Comments(models.Model):
     user=models.ForeignKey(User, on_delete=models.CASCADE)
     doctor=models.ForeignKey(ConfirmDoctor, on_delete=models.CASCADE)
     report = models.ForeignKey(Cbc, on_delete=models.CASCADE)
     field_name = models.TextField(max_length=500)
    

class FileStore(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default=None, null=True)
    file = models.FileField(default=None, null=True)
    date = models.DateTimeField(default=datetime.now())

class Urine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=150,null=True,blank=False)
    date = models.DateTimeField(default=datetime.now())
    image = models.ImageField(default=None, null=True)
    file = models.FileField(default=None, null=True)
    glucose = models.CharField(max_length=150,default=None ,null=True,blank=False)
    ketones = models.CharField(max_length=150,default=None ,null=True,blank=False)
    reaction = models.CharField(max_length=150,default=None ,null=True,blank=False)
    sg = models.FloatField(null=True,blank=True,default=None,max_length=150)
    uro = models.CharField(max_length=150,default=None ,null=True,blank=False)