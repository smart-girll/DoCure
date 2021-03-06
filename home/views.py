from multiprocessing import context
from site import USER_BASE
from token import RBRACE
# from tkinter.font import names
# from tkinter.tix import Form
from urllib import request
from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from matplotlib.pyplot import rcdefaults, text
from numpy import delete
from platformdirs import Path
# from DoCure.settings import EMAIL_HOST_USER

from django.contrib.auth.forms import AuthenticationForm
# from django.core.mail import send_mail

from .forms  import  ConfirmDoctors, NewUserForm,DoctorForm,ConfirmForm,EditProfile,CommentForm,EditProfileDoctor, UploadForm, ConfirmUrineForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.decorators import login_required

import re
# import requests
import pdfplumber
import pandas as pd
import os
import pytesseract
from PIL import Image
from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator

from django.core.files.storage import default_storage
from itertools import chain
 

import random
import datetime
import time

import requests
url = "https://app.nanonets.com/api/v2/OCR/Models/"
payload = {}
response = requests.request("GET", url, data = payload, auth=('bORDKfw8l-5-ulI1jCxmrFBQpiUHvgQP', ''))

# Create your views here.
from .models import *


def home(request):
    name=request.user.username or None
    # if request.user.is_authenticated:
    #         return redirect('home')
    # else:
    # messages.clear()
    return render(request,'HtmlFiles/home.html',{'name':name})
def allreports(request):
    name=request.user.username or None
    # if request.user.is_authenticated:
    #         return redirect('home')
    # else:
    return render(request,'HtmlFiles/allreports.html',{'name':name})

def homebefore(request):
    if  'ConfirmDoctor_id' in request.session:
        
         return redirect('viewPatients')
    
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request,'HtmlFiles/homebefore.html')

def Doctorhome(request):
            name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
            return render(request,'HtmlFiles/Doctorhome.html',{'name':name})
def Comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
                form.save()
    form = CommentForm()
    return render(request,context={'forms':form} ,template_name='HtmlFiles/docDashboard.html')
    
        
from django.db.models import CharField, Value

def viewDoctor(request):
    context={}
    
    name=request.user.username or None
    user=request.user
    d1 = ConfirmDoctor.objects.all()

    for doc in d1:
        if(ViewDoctor.objects.filter(user=user, doctor=doc).exists()):
            d=ViewDoctor.objects.get(user=user, doctor=doc)
            doc.status = d.status
        else:
            doc.status = 0
    
   
    # for d in d1:
    #     print(d.status)
    
    return render(request,'HtmlFiles/viewDoctor.html',context={'name':name,'d1':d1})
def Doctorregister(request):
    if  'ConfirmDoctor_id' in request.session:
        
         return redirect('viewPatients')
    else:
        if request.method == "POST":
            form = DoctorForm(request.POST)
            if form.is_valid():
                # password = make_password(request.data['password'])
                # subject = 'Welcome to Docure'
                # message = 'You have Successfully Signed up into our WebApp You can go and Login to our App'
                # recepient = str(form['email'].value())
                # send_mail(subject, message, EMAIL_HOST_USER,
                #               [recepient], fail_silently=False)
                form.save()
                # login(request, user)
                messages.success(request, "Registration successful." )
            
                return redirect("Doctorlogin")

            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = DoctorForm()
        return render(request,context={'register_form':form} ,template_name='HtmlFiles/Doctorregister.html')
def about(request):
	return render(request,'HtmlFiles/about.html')

def urineDashboard(request,rid):
    context={}
    user=request.user or None
    name=request.user.username or None
    all_Urine_reports= Urine.objects.get(user=request.user, id=rid)
    return render(request,'HtmlFiles/urineDashboard.html',context={'name':name,'all_report':all_Urine_reports})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                        # subject = 'Welcome to Docure'
                        # message = 'You have Successfully Signed up into our WebApp You can go and Login to our App '
                        # recepient = str(form['email'].value())
                        # send_mail(subject, message, EMAIL_HOST_USER,
                        #         [recepient], fail_silently=False)
                        user = form.save()
                        login(request, user)
                        messages.success(request, "Registration successful.")

                        return redirect("login")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
        return render(request, context={'register_form': form}, template_name='HtmlFiles/register.html')


	

def extract(text):
    wbc_re = re.compile(r'(.*[Ll]eu[ck]ocyte\D*|.*WBC\D*|.*White Blood Cell\D*) ([\d,.]+) ')
    rbc_re = re.compile(r'(.*[eE]rythrocyte\D*|.*[r,R][b,B][c,C]\D*|.*[Rr]ed [Bb]lood [Cb]ell\D*|.*[Rr]ed [Cc]ell [Cc]ount\D*) ([\d,.]+) ')
    hgb_re = re.compile(r'(.*[Hh][a]*emoglobin\D*) ([\d,.]+) ')
    pcv_re = re.compile(r'(.*[Pp]acked [Cc]ell [Vv]olume\D*|.*[pP][cC][vV]\D*|.*[Hh][a]*ematocrit\D*) ([\d,.%]+) ')
    mcv_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Vv]olume\D*|.*[mM][cC][vV]\D*|.*[Mm]ean [Cc]ell [Vv]olume\D*) ([\d,.]+) ')
    mch_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Hh]b\D*|.*[mM][cC][hH]\D*) ([\d,.]+) ')
    mchc_re = re.compile(r'(.*[Mm]ean [Cc]ell [Hh]b Conc\D*|.*[mM][cC][hH][cC]\D*|.*[Mm]ean [Cc]ell [Hh]b[\.]* [Cc]onc\D*) ([\d,.]+) ')
    rcd_re = re.compile(r'(.*[Rr]ed [Cc]ell [Dd]ist\D*|.*[Rr][cC][Dd]\D*|.*[Rr][Dd][Ww]\D*) ([\d,.]+) ')
    pc_re = re.compile(r'(.*[Pp]la[Ee]*telet[s]* [Cc]ount\D*|.*[Pp]la[Ee]*telet[s]*\D*) ([\d,.]+) ')
    mpv_re = re.compile(r'(.*[Mm]ean Pla[eE]*telet [Vv]olume\D*|.*[Mm][Pp][Vv]\D*) ([\d,.]+) ')
#     neu_re = re.compile(r'([Nn]eutrophils) ([\d,.]+) ')
#     lym_re = re.compile(r'(.*[Ll]ymphocyte.*) ([\d,.]+) ')
#     mon_re = re.compile(r'(.*[Mm]onocyte.*) ([\d,.]+) ')
#     eos_re = re.compile(r'(.*[Ee]osinophils.*) ([\d,.]+) ')
#     bas_re = re.compile(r'(.*[Bb]asophils.*) ([\d,.]+) ')
   
    flag = 0
   
    wbc = wbc_re.search(text)
    if(wbc != None):
        wbc = wbc_re.search(text).group(2)
        wbc = float(wbc.replace(',',''))     
    elif(wbc==None):
            wbc = 0.0000000000000
            flag += 1
       
    rbc = rbc_re.search(text)
    if(rbc != None):
        rbc = rbc_re.search(text).group(2)
        rbc = float(rbc.replace(',',''))
        
    elif(rbc==None):
            rbc = 0.0000000000000
            flag += 1
       
    hgb = hgb_re.search(text)
    if(hgb != None):
        hgb = hgb_re.search(text).group(2)
        hgb = float(hgb.replace(',',''))
       
    elif(hgb==None):
            hgb = 0.0000000000000
            flag += 1
       
    pcv = pcv_re.search(text)
    if(pcv != None):
        pcv = pcv_re.search(text).group(2)
        pcv = pcv.replace('%','')
        pcv = pcv.replace(',','')
        pcv = float(pcv)
    elif(pcv==None):
            pcv = 0.0000000000000
            flag += 1
       
    mcv = mcv_re.search(text)
    if(mcv != None):
        mcv = mcv_re.search(text).group(2)
        mcv = float(mcv.replace(',',''))
    elif(mcv==None):
            mcv = 0.0000000000000
            flag += 1
       
    mch = mch_re.search(text)
    if(mch != None):
        mch = mch_re.search(text).group(2)
        mch = float(mch.replace(',',''))
    elif(mch==None):
            mch = 0.0000000000000
            flag += 1
       
    mchc = mchc_re.search(text)
    if(mchc != None):
        mchc = mchc_re.search(text).group(2)
        mchc = float(mchc.replace(',',''))
    elif(mchc==None):
            mchc = 0.0000000000000
            flag += 1
       
    rcd = rcd_re.search(text)
    if(rcd != None):
        rcd = rcd_re.search(text).group(2)
        rcd = float(rcd.replace(',',''))
    elif(rcd==None):
            rcd = 0.0000000000000
            flag += 1
       
    pc = pc_re.search(text)
    if(pc != None):
        pc = pc_re.search(text).group(2)
        pc = float(pc.replace(',',''))
        
    elif(pc==None):
            pc = 0.0000000000000
            flag += 1
       
    mpv = mpv_re.search(text)
    if(mpv != None):
        mpv = mpv_re.search(text).group(2)
        mpv = float(mpv.replace(',',''))
    elif(mpv==None):
            mpv = 0.0000000000000
            flag += 1
       
#     if(flag > 5):
#         print("Could not find values. Please check if the correct report is uploaded.")
#     else:
    print("Leukocyte count: ", wbc)
    print("Red Blood Cell count: ", rbc)
    print("Haemoglobin Count: ", hgb)
    print("Packed Cell Volume: "+ str(pcv) +"%")
    print("Mean Cell Volume: ", mcv)
    print("Mean Corpuscular Hb Conc.: ", mchc)
    print("Red Cell Dist.: ", rcd)
    print("Platelet Count: ", pc)
    print("Mean Platelet Volume: ", mpv)

    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv

        

    	

def GetInfo(path,filepassword):
    cbc = path
    

  
    with pdfplumber.open(cbc, password=filepassword) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = extract(text)
    
    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv
   




def ViewPatients(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    

    current_patients = User.objects.filter(viewdoctor__doctor=doc, viewdoctor__status=2)
    pending_patients = User.objects.filter(viewdoctor__doctor=doc, viewdoctor__status=1)

    return render(request,'HtmlFiles/viewPatients.html',context={'curr':current_patients,'name':name,'pend':pending_patients})

def removeDoctor(request, doc_id):
    print(doc_id)
    doc = ConfirmDoctor.objects.get(viewdoctor__id=doc_id)
    print(doc.username)
    user=request.user or None
    print(user)
    print(doc)
    v = ViewDoctor.objects.get(user=user, doctor=doc)
    v.delete()

    return redirect("userProfile")
def pendingReq(request, user_id, ar):
    user = User.objects.get(id=user_id)
    print(user)
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    if(ar==1):
        a = ViewDoctor.objects.get(user=user, doctor=doc)
        a.status = 2
        a.save()
    elif(ar==0):
        a = ViewDoctor.objects.get(user=user, doctor=doc)
        a.status = 3
        a.save()
    return redirect("viewPatients")

def removePatient(request, user_id):
    user = User.objects.get(id=user_id)
    print(user)
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    a = ViewDoctor.objects.get(user=user, doctor=doc)
    a.delete()
    return redirect("viewPatients")

def docRequest(request, doc_id):
    print(doc_id)
    doc = ConfirmDoctor.objects.get(id=doc_id)
    user=request.user or None
    print(user)
    print(doc)
    v = ViewDoctor(user=user, doctor=doc, status=1)
    
    print(v)
    v.save()
    name=request.user.username or None
    d1= ConfirmDoctor.objects.all()
    return redirect("viewDoctor")

def GetInfoOCR(path):
    cbc = path.name
    url = 'https://app.nanonets.com/api/v2/OCR/Model/5fdf8b64-fa8e-4c90-9102-15e7eeb961e4/LabelFile/?async=false'    
    data = {'file': open('media/'+cbc, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('bORDKfw8l-5-ulI1jCxmrFBQpiUHvgQP', ''), files=data)
    text=response.text.replace('\\n',' ')
    # pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    # text = pytesseract.image_to_string(Image.open(cbc))
    print(text)
    rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv= extract(text)
    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv
    



def upload(request):
    name=request.user.username or None
    context = {}    
    request.session["confirm_id"] = 1
    return render(request, 'HtmlFiles/upload.html',context= {'name':name})


def fileData(request):
    # print(request.session["confirm_id"])
   
    if "confirm_id" in request.session:
    
        context = {}
        rbc_final = 0
        wbc_final = 0
        pc_final = 0
        hgb_final = 0
        rcd_final = 0
        mchc_final = 0
        mpv_final = 0
        pcv_final = 0
        mcv_final = 0
        if request.method == 'POST':

            try:
                uploaded_file = request.FILES['document']
                for f in request.FILES.getlist('document'): 
                   
                    uploaded_file = f
                    
            except Exception as e:
                messages.error(request,'No file is uploaded.')
                return redirect('upload')
            else:
                for f in request.FILES.getlist('document'): 
                  
                    uploaded_file = f
                    print(uploaded_file)
                  
                    namess=request.POST.get('reportname')
                    filepassword=request.POST.get('password')
                    print(filepassword)
                    fs = FileSystemStorage()
                    name = fs.save(uploaded_file.name, uploaded_file)
                    context['url'] = fs.url(name)
                    if(namess != ""):
                        file_name = namess
                    else:
                        file_name = uploaded_file.name

                    if(uploaded_file.name.endswith(".pdf")):
                        try:
                            rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfo(uploaded_file,filepassword)
                            print(rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv)
                        except Exception as e:
                            messages.error(request,'Password is wrong')
                            return redirect('upload')
                        else:
                            if(rbc_final == 0):
                                rbc_final = rbc
                            if(wbc_final == 0):
                                wbc_final = wbc
                            if(pc_final == 0):
                                pc_final = pc
                            if(hgb_final == 0):
                                hgb_final = hgb
                            if(rcd_final == 0):
                                rcd_final = rcd
                            if(mchc_final == 0):
                                mchc_final = mchc
                            if(mpv_final == 0):
                                mpv_final = mpv
                            if(pcv_final == 0):
                                pcv_final = pcv
                            if(mcv_final == 0):
                                mcv_final = mcv
                            
                            initial = {'rbc': rbc_final,
                                    'wbc': wbc_final,
                                    'pc': pc_final,
                                    'hgb': hgb_final,
                                    'rcd': rcd_final,
                                    'mchc': mchc_final,
                                    'mpv': mpv_final,
                                    'pcv': pcv_final,
                                    'mcv': mcv_final,
                                    'name':file_name,
                                    'file':uploaded_file,
                                    }

                            request.session["file_name"] = uploaded_file.name
                        
                        
                            form = ConfirmForm(initial=initial)
                            # cbc.save()
                            context = {
                                'form': form,
                                'file_name': file_name,
                                # 'confirm_id': request.session["confirm_id"]
                            }
                            
                        
                    elif(uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
                        print(uploaded_file)
                        rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfoOCR(uploaded_file)
                        user = request.user.get_username()

                        if(rbc_final == 0):
                            rbc_final = rbc
                        if(wbc_final == 0):
                            wbc_final = wbc
                        if(pc_final == 0):
                            pc_final = pc
                        if(hgb_final == 0):
                            hgb_final = hgb
                        if(rcd_final == 0):
                            rcd_final = rcd
                        if(mchc_final == 0):
                            mchc_final = mchc
                        if(mpv_final == 0):
                            mpv_final = mpv
                        if(pcv_final == 0):
                            pcv_final = pcv
                        if(mcv_final == 0):
                            mcv_final = mcv
                    
                        initial = {'rbc': rbc_final,
                                'wbc': wbc_final,
                                'pc': pc_final,
                                'hgb': hgb_final,
                                'rcd': rcd_final,
                                'mchc': mchc_final,
                                'mpv': mpv_final,
                                'pcv': pcv_final,
                                'mcv': mcv_final,
                                'name':file_name,
                                'file':uploaded_file,
                                }

                        request.session["file_name"] = uploaded_file.name
                        print(request.session["file_name"])
                        form = ConfirmForm(initial=initial)
                        context = {
                            'form': form
                        }
                    else:
                        messages.error(request,'Please upload .png, .jpg or .pdf file.')

            return render(request, 'HtmlFiles/confirmForm.html', context)
    else:
        return redirect('viewmyreports')

    # return redirect('FILE')
            
import environ
env = environ.Env()
environ.Env.read_env()

key: bytes = bytes(env('KEY'),'ascii')
# print(key)
# print(type(key))
from cryptography.fernet import Fernet
# key = b'nMkhkaca8wdcK9NDPKmNCFOggEp0OwfPOqLl3BhpyHI='
f = Fernet(key)

def confirmForm(request):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():  
            s = Cbc()
            obj = form.save(commit=False)
            s.user = request.user
            file_name = request.session["file_name"]
            # f = default_storage.open(file_name, 'r')
            if(file_name.lower().endswith(('.png', '.jpg', '.jpeg'))):
                s.image = file_name
            elif(file_name.lower().endswith(('.pdf'))):
                s.file = file_name
            s.name = form.cleaned_data.get('name')

            rbc = form.cleaned_data.get('rbc')
            if(rbc != None):
                
                stringBytes = bytes(str(rbc),'UTF-8')
                token = f.encrypt(stringBytes)
                s.rbc_enc = token

            wbc = form.cleaned_data.get('wbc')
            if(wbc != None):
              
                stringBytes = bytes(str(wbc),'UTF-8')
                token = f.encrypt(stringBytes)
                s.wbc_enc = token

            pc = form.cleaned_data.get('pc')
            if(pc != None):
              
                stringBytes = bytes(str(pc),'UTF-8')
                token = f.encrypt(stringBytes)
                s.pc_enc = token

            hgb = form.cleaned_data.get('hgb')
            if(hgb != None):
               
                stringBytes = bytes(str(hgb),'UTF-8')
                token = f.encrypt(stringBytes)
                s.hgb_enc = token

            rcd = form.cleaned_data.get('rcd')
            if(rcd != None):
               
                stringBytes = bytes(str(rcd),'UTF-8')
                token = f.encrypt(stringBytes)
                s.rcd_enc = token

            mchc = form.cleaned_data.get('mchc')
            if(mchc != None):
               
                stringBytes = bytes(str(mchc),'UTF-8')
                token = f.encrypt(stringBytes)
                s.mchc_enc = token

            mpv = form.cleaned_data.get('mpv')
            if(mpv != None):
               
                stringBytes = bytes(str(mpv),'UTF-8')
                token = f.encrypt(stringBytes)
                s.mpv_enc = token

            pcv = form.cleaned_data.get('pcv')
            if(pcv != None):
               
                stringBytes = bytes(str(pcv),'UTF-8')
                token = f.encrypt(stringBytes)
                s.pcv_enc = token

            mcv = form.cleaned_data.get('mcv')
            if(mcv != None):
              
                stringBytes = bytes(str(mcv),'UTF-8')
                token = f.encrypt(stringBytes)
                s.mcv_enc = token
            
            s.save()
            # obj.rbc_enc = token
            # obj.save()
            del request.session['confirm_id']

    return redirect('viewmyreports')

   
def getJsonData(request):
    data= {
        "sales":100,
        "customers":10,
    }
    return JsonResponse(data)

def dashboard(request,rid):
    context={}
    name=request.user.username or None
  
    all_reports= Cbc.objects.get(user=request.user, id=rid)
    all_comments = Comments.objects.filter(user=request.user, report=all_reports)
    print(all_reports.wbc_enc)
    wbc = float(f.decrypt(all_reports.wbc_enc))
    print(wbc)

    all_reports.wbc = float(f.decrypt(all_reports.wbc_enc))
    if(all_reports.wbc>=1 and all_reports.wbc<100):
        all_reports.wbc *= 1000
    elif(all_reports.wbc>=100 and all_reports.wbc<1000):
        all_reports.wbc *= 10
    
    all_reports.rbc = float(f.decrypt(all_reports.rbc_enc))
    if(all_reports.rbc>=100 and all_reports.rbc<1000):
        all_reports.rbc /= 100
    elif(all_reports.rbc>=1000 and all_reports.rbc<10000):
        all_reports.rbc /= 1000

       
    all_reports.hgb = float(f.decrypt(all_reports.hgb_enc))
    if(all_reports.hgb>=100 and all_reports.hgb<1000):
        all_reports.hgb /= 10
    elif(all_reports.hgb>=1000 and all_reports.hgb<10000):
        all_reports.hgb /= 100
       
       
       
    all_reports.pc = float(f.decrypt(all_reports.pc_enc))
    if(all_reports.pc>=1 and all_reports.pc<10):
        all_reports.pc *= 1000000
    elif(all_reports.pc>=10 and all_reports.pc<100):
        all_reports.pc *= 100000
    elif(all_reports.pc>=100 and all_reports.pc<1000):
        all_reports.pc *= 10000
    elif(all_reports.pc>=1000 and all_reports.pc<10000):
        all_reports.pc *= 1000
    elif(all_reports.pc>=10000 and all_reports.pc<100000):
        all_reports.pc *= 100
    elif(all_reports.pc>=100000 and all_reports.pc<1000000):
        all_reports.pc *= 10
    
    if(all_reports.rcd_enc != None):
        all_reports.rcd = float(f.decrypt(all_reports.rcd_enc))
    
    if(all_reports.mchc_enc != None):
        all_reports.mchc = float(f.decrypt(all_reports.mchc_enc))

    if(all_reports.mpv_enc != None):
        all_reports.mpv = float(f.decrypt(all_reports.mpv_enc))

    if(all_reports.pcv_enc != None):
        all_reports.pcv = float(f.decrypt(all_reports.pcv_enc))

    if(all_reports.mcv_enc != None):
        all_reports.mcv = float(f.decrypt(all_reports.mcv_enc))
    

    labels = []
    data = []
    labels1 = []
    data1 = []
    print(type(rid))
    cbc = Cbc.objects.filter(user=request.user,date__range=["1947-01-01", all_reports.date]).order_by('date')
    for c in cbc:
        d=c.date.date()
        wbc = float(f.decrypt(c.wbc_enc))
        if(wbc>=1 and wbc<100):
            wbc *= 1000
        elif(wbc>=100 and wbc<1000):
            wbc *= 10
        if wbc>0.0:
            labels.append(str(d))
            data.append(wbc)
    for c in cbc:
        d=c.date.date()
        rbc = float(f.decrypt(c.rbc_enc))
        if(rbc>=100 and rbc<1000):
            rbc /= 100
        elif(rbc>=1000 and rbc<10000):
            all_reports.rbc /= 1000
        if rbc>0.0:
            labels1.append(str(d))
            data1.append(rbc)

    # print(labels)
    # print(data)
    # print(labels1)
    # print(data1)

    # print(all_reports.file.path)
    return render(request,'HtmlFiles/dashboard.html',context={'name':name,'all_report':all_reports, 'all_comments':all_comments, 'labels':labels, 'data':data,'labels1':labels1, 'data1':data1})



def docDashboard(request, rid):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    form = CommentForm()
    request.session['rid']=rid
    user_id=request.session['user_id']
    user = User.objects.get(id =user_id)
   
    all_reports= Cbc.objects.get(id=rid)
    print(all_reports.wbc_enc)
    wbc = float(f.decrypt(all_reports.wbc_enc))
    print(wbc)

    all_reports.wbc = float(f.decrypt(all_reports.wbc_enc))
    if(all_reports.wbc>=1 and all_reports.wbc<100):
        all_reports.wbc *= 1000
    elif(all_reports.wbc>=100 and all_reports.wbc<1000):
        all_reports.wbc *= 10
    
    all_reports.rbc = float(f.decrypt(all_reports.rbc_enc))
    if(all_reports.rbc>=100 and all_reports.rbc<1000):
        all_reports.rbc /= 100
    elif(all_reports.rbc>=1000 and all_reports.rbc<10000):
        all_reports.rbc /= 1000

       
    all_reports.hgb = float(f.decrypt(all_reports.hgb_enc))
    if(all_reports.hgb>=100 and all_reports.hgb<1000):
        all_reports.hgb /= 10
    elif(all_reports.hgb>=1000 and all_reports.hgb<10000):
        all_reports.hgb /= 100
       
       
       
    all_reports.pc = float(f.decrypt(all_reports.pc_enc))
    if(all_reports.pc>=1 and all_reports.pc<10):
        all_reports.pc *= 1000000
    elif(all_reports.pc>=10 and all_reports.pc<100):
        all_reports.pc *= 100000
    elif(all_reports.pc>=100 and all_reports.pc<1000):
        all_reports.pc *= 10000
    elif(all_reports.pc>=1000 and all_reports.pc<10000):
        all_reports.pc *= 1000
    elif(all_reports.pc>=10000 and all_reports.pc<100000):
        all_reports.pc *= 100
    elif(all_reports.pc>=100000 and all_reports.pc<1000000):
        all_reports.pc *= 10
    
    if(all_reports.rcd_enc != None):
        all_reports.rcd = float(f.decrypt(all_reports.rcd_enc))
    
    if(all_reports.mchc_enc != None):
        all_reports.mchc = float(f.decrypt(all_reports.mchc_enc))

    if(all_reports.mpv_enc != None):
        all_reports.mpv = float(f.decrypt(all_reports.mpv_enc))

    if(all_reports.pcv_enc != None):
        all_reports.pcv = float(f.decrypt(all_reports.pcv_enc))

    if(all_reports.mcv_enc != None):
        all_reports.mcv = float(f.decrypt(all_reports.mcv_enc))
    




    all_reports.wbc = float(f.decrypt(all_reports.wbc_enc))
    if(all_reports.wbc>=1 and all_reports.wbc<100):
        all_reports.wbc *= 1000
    elif(all_reports.wbc>=100 and all_reports.wbc<1000):
        all_reports.wbc *= 10
    
    all_reports.rbc = float(f.decrypt(all_reports.rbc_enc))
    if(all_reports.rbc>=100 and all_reports.rbc<1000):
        all_reports.rbc /= 100
    elif(all_reports.rbc>=1000 and all_reports.rbc<10000):
        all_reports.rbc /= 1000

       
    all_reports.hgb = float(f.decrypt(all_reports.hgb_enc))
    if(all_reports.hgb>=100 and all_reports.hgb<1000):
        all_reports.hgb /= 10
    elif(all_reports.hgb>=1000 and all_reports.hgb<10000):
        all_reports.hgb /= 100
       
       
       
    all_reports.pc = float(f.decrypt(all_reports.pc_enc))
    if(all_reports.pc>=1 and all_reports.pc<10):
        all_reports.pc *= 1000000
    elif(all_reports.pc>=10 and all_reports.pc<100):
        all_reports.pc *= 100000
    elif(all_reports.pc>=100 and all_reports.pc<1000):
        all_reports.pc *= 10000
    elif(all_reports.pc>=1000 and all_reports.pc<10000):
        all_reports.pc *= 1000
    elif(all_reports.pc>=10000 and all_reports.pc<100000):
        all_reports.pc *= 100
    elif(all_reports.pc>=100000 and all_reports.pc<1000000):
        pc *= 10
    
    if(all_reports.rcd_enc != None):
        all_reports.rcd = float(f.decrypt(all_reports.rcd_enc))
    
    if(all_reports.mchc_enc != None):
        all_reports.mchc = float(f.decrypt(all_reports.mchc_enc))

    if(all_reports.mpv_enc != None):
        all_reports.mpv = float(f.decrypt(all_reports.mpv_enc))

    if(all_reports.pcv_enc != None):
        all_reports.pcv = float(f.decrypt(all_reports.pcv_enc))

    if(all_reports.mcv_enc != None):
        all_reports.mcv = float(f.decrypt(all_reports.mcv_enc))

    labels = []
    data = []
    labels1 = []
    data1 = []
    print(type(rid))
    cbc = Cbc.objects.filter(user=user,date__range=["1947-01-01", all_reports.date]).order_by('date')
    for c in cbc:
        d=c.date.date()
        wbc = float(f.decrypt(c.wbc_enc))
        if(wbc>=1 and wbc<100):
            wbc *= 1000
        elif(wbc>=100 and wbc<1000):
            wbc *= 10
        if wbc>0.0:
            labels.append(str(d))
            data.append(wbc)
    for c in cbc:
        d=c.date.date()
        rbc = float(f.decrypt(c.rbc_enc))
        if(rbc>=100 and rbc<1000):
            rbc /= 100
        elif(rbc>=1000 and rbc<10000):
            all_reports.rbc /= 1000
        if rbc>0.0:
            labels1.append(str(d))
            data1.append(rbc)

    return render(request,'HtmlFiles/docDashboard.html',context={'all_report':all_reports, 'form':form,'name':name,'labels':labels, 'data':data,'labels1':labels1, 'data1':data1})

def redocDashboard(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    rid=request.session['rid']
    form = CommentForm()
    all_reports= Cbc.objects.get(id=rid)
    user_id=request.session['user_id']
    user = User.objects.get(id =user_id)
    print(all_reports.wbc_enc)
    wbc = float(f.decrypt(all_reports.wbc_enc))
    print(wbc)

    all_reports.wbc = float(f.decrypt(all_reports.wbc_enc))
    if(all_reports.wbc>=1 and all_reports.wbc<100):
        all_reports.wbc *= 1000
    elif(all_reports.wbc>=100 and all_reports.wbc<1000):
        all_reports.wbc *= 10
    
    all_reports.rbc = float(f.decrypt(all_reports.rbc_enc))
    if(all_reports.rbc>=100 and all_reports.rbc<1000):
        all_reports.rbc /= 100
    elif(all_reports.rbc>=1000 and all_reports.rbc<10000):
        all_reports.rbc /= 1000

       
    all_reports.hgb = float(f.decrypt(all_reports.hgb_enc))
    if(all_reports.hgb>=100 and all_reports.hgb<1000):
        all_reports.hgb /= 10
    elif(all_reports.hgb>=1000 and all_reports.hgb<10000):
        all_reports.hgb /= 100
       
       
       
    all_reports.pc = float(f.decrypt(all_reports.pc_enc))
    if(all_reports.pc>=1 and all_reports.pc<10):
        all_reports.pc *= 1000000
    elif(all_reports.pc>=10 and all_reports.pc<100):
        all_reports.pc *= 100000
    elif(all_reports.pc>=100 and all_reports.pc<1000):
        all_reports.pc *= 10000
    elif(all_reports.pc>=1000 and all_reports.pc<10000):
        all_reports.pc *= 1000
    elif(all_reports.pc>=10000 and all_reports.pc<100000):
        all_reports.pc *= 100
    elif(all_reports.pc>=100000 and all_reports.pc<1000000):
        all_reports.pc *= 10
    
    if(all_reports.rcd_enc != None):
        all_reports.rcd = float(f.decrypt(all_reports.rcd_enc))
    
    if(all_reports.mchc_enc != None):
        all_reports.mchc = float(f.decrypt(all_reports.mchc_enc))

    if(all_reports.mpv_enc != None):
        all_reports.mpv = float(f.decrypt(all_reports.mpv_enc))

    if(all_reports.pcv_enc != None):
        all_reports.pcv = float(f.decrypt(all_reports.pcv_enc))

    if(all_reports.mcv_enc != None):
        all_reports.mcv = float(f.decrypt(all_reports.mcv_enc))

    labels = []
    data = []
    labels1 = []
    data1 = []
    print(type(rid))
    cbc = Cbc.objects.filter(user=user,date__range=["1947-01-01", all_reports.date]).order_by('date')
    for c in cbc:
        d=c.date.date()
        wbc = float(f.decrypt(c.wbc_enc))
        if(wbc>=1 and wbc<100):
            wbc *= 1000
        elif(wbc>=100 and wbc<1000):
            wbc *= 10
        if wbc>0.0:
            labels.append(str(d))
            data.append(wbc)
    for c in cbc:
        d=c.date.date()
        rbc = float(f.decrypt(c.rbc_enc))
        if(rbc>=100 and rbc<1000):
            rbc /= 100
        elif(rbc>=1000 and rbc<10000):
            all_reports.rbc /= 1000
        if rbc>0.0:
            labels1.append(str(d))
            data1.append(rbc)

    return render(request,'HtmlFiles/docDashboard.html',context={'all_report':all_reports, 'name':name, 'form':form, 'labels':labels, 'data':data,'labels1':labels1, 'data1':data1})


def addComment(request):
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():  
            obj = form.save(commit=False)
            obj.doctor = doc
            user=User.objects.get(id=request.session['user_id'])
            obj.user = user
            print(user)
            report=Cbc.objects.get(id=request.session['rid'])
            obj.report=report
            obj.save()
            print('e')
    return redirect('redocDashboard')

# def addAnotherFile(request):
# from admin import download_csv
# #     report = Cbc.objects.last()
# def getCsv(request):
#     data = download_csv(ModelAdmin, request, Cbc.objects.all())

#     return HttpResponse (data, content_type='text/csv')


def Doctorlogin(request):
    if  'ConfirmDoctor_id' in request.session:
        
         return redirect('viewPatients')
    else:
        if request.method == 'POST':
                username = request.POST.get('name')
                password =request.POST.get('password') 
                



                # user = ConfirmDoctor.objects.filter(username=username,password=password).exists()
                # request.session['ConfirmDoctoR']='9555'
                if (ConfirmDoctor.objects.filter(username=username,password=password).exists()):
                        # login(request, user)
                        user = ConfirmDoctor.objects.get(username=username,password=password)
                        request.session['ConfirmDoctor_id']=user.id
                        # request.session['ConfirmDoctoR']='123'
                        return redirect('viewPatients')
                else:
                        messages.error(request,'username or password not correct')
                        return render(request, 'HtmlFiles/Doctorlogin.html')

	
                        
        
        return render(request, 'HtmlFiles/Doctorlogin.html')
        
def doctorProfile(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    context={}
    print(request.session['ConfirmDoctor_id'])
    confirm_doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    all_docs= Doctor.objects.get(confirmdoctor = confirm_doc)  
    return render(request,'HtmlFiles/doctorProfile.html',context={'all_docs':all_docs,'name':name})

def dgetEditProfile(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    confirm_doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    instance = Doctor.objects.get(confirmdoctor = confirm_doc)
    form = EditProfileDoctor(instance=instance)

    return render(request,'HtmlFiles/dEditProfile.html',context={'form':form,'name':name})

def dedituProfile(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    confirm_doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    form = ConfirmDoctors(instance=confirm_doc)

    return render(request,'HtmlFiles/deditu.html',context={'form':form,'name':name})

def deditu(request):
     if request.method == "POST":
        doc_id=request.session['ConfirmDoctor_id']
        confirm_doc = ConfirmDoctor.objects.get(id=doc_id)
        editform = ConfirmDoctors(request.POST,instance= confirm_doc)
        if editform.is_valid():
            editform.save()
        return redirect('doctorProfile')	
def dEditProfile(request):   
    if request.method == "POST":
        doc_id=request.session['ConfirmDoctor_id']
        confirm_doc = ConfirmDoctor.objects.get(id=doc_id)
        instance = Doctor.objects.get(confirmdoctor = confirm_doc)
        editform = EditProfileDoctor(request.POST, instance = instance)
        if editform.is_valid():
            editform.save()
        return redirect('doctorProfile')	
def Doctorlogout_view(request):
		del request.session['ConfirmDoctor_id']
		messages.info(request, "You have successfully logged out.") 
		return redirect("Doctorlogin")

def docViewReports(request, user_id):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    user = User.objects.get(id =user_id)
    request.session['user_id']=user_id
    all_reports= Cbc.objects.filter(user=user).order_by("-date") #.filter(user=request.user)
    return render(request,'HtmlFiles/docviewreports.html',context={'posts':all_reports,'name':name})

def reports(request):
    if 'confirm_id' in request.session:
        del request.session['confirm_id']
    user=request.user or None
    name=request.user.username or None
    all_reports= Cbc.objects.filter(user=user).order_by('-date')  #.filter(user=request.user)
    all_Urine_reports= Urine.objects.filter(user=user).order_by('-date') 
    result_list = sorted(
        chain(all_reports, all_Urine_reports),
        key=lambda data: data.date, reverse=True)
    print(result_list)
    p = Paginator(result_list, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    for i in page_obj.object_list:
        i.type = i.__class__.__name__
    return render(request,'HtmlFiles/viewmyreports.html',context={'posts':result_list,'name':name, 'page_obj':page_obj})

def deleteReport(request, rid):

    report = Cbc.objects.get(id=rid)
    print(report.name)
    report.delete()

    user=request.user or None
    name=request.user.username or None
    all_reports= Cbc.objects.filter(user=user).order_by('-date')  #.filter(user=request.user)
    return redirect('viewmyreports')




def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        if request.method == 'POST':
            username = request.POST.get('name')
            password =request.POST.get('password') 
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                        login(request, user)
                        
                        return redirect('home')
            else:
                        messages.error(request,'username or password not correct')

        return render(request, 'HtmlFiles/login.html')
        

def logout_view(request):
		logout(request)
		messages.info(request, "You have successfully logged out.") 
		return redirect("login")

def getEditProfile(request):
    user=request.user.id or None
    instance = User.objects.get(id = user)
    form = EditProfile(instance=instance)

    return render(request,'HtmlFiles/editProfile.html',context={'form':form})
def userProfile(request):
    context={}

    name=request.user.username or None
    all_users= User.objects.get(pk = request.user.pk)  
    user = request.user
    all_doctors = ViewDoctor.objects.filter(user=user, status=2)
    print()
    return render(request,'HtmlFiles/userProfile.html',context={'name':name,'all_users':all_users, 'all_doctors':all_doctors})

def editProfile(request):   
    if request.method == "POST":
        user=request.user.id or None
        instance = User.objects.get(id = user)
        editform = EditProfile(request.POST, instance = instance)
        if editform.is_valid():
            editform.save()
            return redirect('userProfile')

	

def password_reset_request(request):
                                if request.method == "POST":
                                    password_reset_form = PasswordResetForm(request.POST)
                                    if password_reset_form.is_valid():
                                        data = password_reset_form.cleaned_data['email']
                                        associated_users = User.objects.filter(Q(email=data))
                                        associated_userss = Doctor.objects.filter(Q(email=data))
                                        if associated_users.exists():
                                            for user in associated_users:
                                                subject = "Password Reset Requested"
                                                email_template_name = "HtmlFiles/password_reset_email.txt"
                                                c = {
                                                "email":user.email,
                                                'domain':'127.0.0.1:8000',
                                                'site_name': 'Website',
                                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                "user": user,
                                                'token': default_token_generator.make_token(user),
                                                'protocol': 'http',
                                                }
                                                email = render_to_string(email_template_name, c)
                                                try:
                                                    send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                                                except BadHeaderError:
                                                    return HttpResponse('Invalid header found.')
                                                return redirect ("/password_reset/done/")
                                        if associated_userss.exists():
                                            for user in associated_userss:
                                                subject = "Password Reset Requested"
                                                email_template_name = "HtmlFiles/password_reset_email.txt"
                                                c = {
                                                "email":user.email,
                                                'domain':'127.0.0.1:8000',
                                                'site_name': 'Website',
                                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                "user": user,
                                                'token': default_token_generator.make_token(user),
                                                'protocol': 'http',
                                                }
                                                email = render_to_string(email_template_name, c)
                                                try:
                                                    send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                                                except BadHeaderError:
                                                    return HttpResponse('Invalid header found.')
                                                return redirect ("/password_reset/done/")
                                password_reset_form = PasswordResetForm()
                                return render(request=request, template_name="HtmlFiles/password_reset.html", context={"password_reset_form":password_reset_form})


def fileUpload(request):
    name=request.user.username or None
    context = {}    
    # form = UploadForm()
    return render(request, 'HtmlFiles/FileUpload.html', {'name':name})

def fileStorage(request):
    if request.method == 'POST':
            try:
                uploaded_file = request.FILES['document']   
            except Exception as e:
                messages.error(request,'No file is uploaded.')
                return redirect('fileUpload')
            else:
                namess=request.POST.get('reportname')
                # filepassword=request.POST.get('password')
                # print(filepassword)
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name, uploaded_file)
                if(namess != ""):
                    file_name = namess
                else:
                    file_name = uploaded_file.name
                obj = FileStore(user=request.user)
                if(uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg'))): 
                    obj.image = uploaded_file
                else:
                    obj.file = uploaded_file
                obj.save()
                return redirect('viewmyreports')



def getPDFText(file, password):
    with pdfplumber.open(file, password=password) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    return text

def getImageText(uploaded_file):
    cbc = uploaded_file.name
    url = 'https://app.nanonets.com/api/v2/OCR/Model/5fdf8b64-fa8e-4c90-9102-15e7eeb961e4/LabelFile/?async=false'    
    data = {'file': open('media/'+cbc, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('bORDKfw8l-5-ulI1jCxmrFBQpiUHvgQP', ''), files=data)
    text=response.text.replace('\\n',' ')
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  #enter your path here
    # text = pytesseract.image_to_string(Image.open(cbc))

    return text
                        
def UrineFile(request):
    name=request.user.username or None
    context = {}    
    # form = UploadForm()
    request.session["confirm_id"] = 1
    return render(request, 'HtmlFiles/UrineFile.html', {'name':name})

def extractUrine(text):
    glucose_re = re.compile(r'(.*[gG]lucose\W*)(\w+)')
    glucose = glucose_re.search(text)
    if (glucose != None):
        glu = glucose[2]
    else:
        glu = None
        
    ketones_re = re.compile(r'(.*[kK]etones\W*)(\w+)')
    ketones = ketones_re.search(text)
    if (ketones != None):
        ket = ketones[2]
    else:
        ket = None
        
    reaction_re = re.compile(r'(.*[rR]eaction.*|.*pH\W*)(\w+)')
    reaction = reaction_re.search(text)
    if (reaction != None):
        reac = reaction[2]
    else:
        reac = None
    
    sg_re = re.compile(r'(.*[Ss]pecific\D*)([\d,.]+)')
    sg = sg_re.search(text)
    if (reaction != None):
        sg = sg[2]
    else:
        sg = None
        
    uro_re = re.compile(r'(.*[uU]robilinogen\W*)(\w+)')
    uro = uro_re.search(text)
    if (uro != None):
        uro = uro[2]
    else:
        uro = None
    
    return glu, ket, reac, sg, uro


def UrineFileData(request):
    if "confirm_id" in request.session:
    
        context = {}
        
        glu = ''
        if request.method == 'POST':

            try:
                uploaded_file = request.FILES['document']
                for f in request.FILES.getlist('document'): 
                    print("-----------------------------------------------------------------------------")
                    uploaded_file = f
                    print(uploaded_file)
                    print("-----------------------------------------------------------------------------")
                
            except Exception as e:
                messages.error(request,'No file is uploaded.')
                return redirect('UrineFile')
            else:
                for f in request.FILES.getlist('document'): 
                    print("-----------------------------------------------------------------------------")
                    uploaded_file = f
                    print(uploaded_file)
                    print("-----------------------------------------------------------------------------")
                    namess=request.POST.get('reportname')
                    filepassword=request.POST.get('password')
                    print(filepassword)
                    fs = FileSystemStorage()
                    name = fs.save(uploaded_file.name, uploaded_file)
                    context['url'] = fs.url(name)
                    if(namess != ""):
                        file_name = namess
                    else:
                        file_name = uploaded_file.name

                    if(uploaded_file.name.endswith(".pdf")):
                        try:
                            text = getPDFText(uploaded_file,filepassword)
                            print(text)
                            glu, ket, reac, sg, uro = extractUrine(text)
                        except Exception as e:
                            messages.error(request,'Password is wrong')
                            return redirect('UrineFile')
                        else:
                         
                            if(glu == ''):
                                glu = glu
                            if(ket == ''):
                                ket = ket
                            if(reac == ''):
                                reac = reac
                            if(sg == None):
                                sg = sg
                            if(uro == ''):
                                uro = uro
                            
                            initial = {
                                    'glucose': glu,
                                    'ketones': ket,
                                    'reaction': reac,
                                    'sg': sg,
                                    'uro': uro,
                                    'name':file_name,
                                    'file':uploaded_file,
                                    }

                            request.session["urine_file_name"] = uploaded_file.name
                        
                        
                            form = ConfirmUrineForm(initial=initial)
                            # cbc.save()
                            context = {
                                'form': form,
                                'file_name': file_name,
                                # 'confirm_id': request.session["confirm_id"]
                            }
                            
                        
                    elif(uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
                        text = getImageText(uploaded_file)
                        print(text)
                        glu, ket, reac, sg, uro  = extractUrine(text)
                        user = request.user.get_username()
                        if(glu == ''):
                            glu = glu
                        if(ket == ''):
                            ket = ket
                        if(reac == ''):
                            reac = reac
                        if(sg == None):
                            sg = sg
                        if(uro == ''):
                            uro = uro
                        
                        initial = {
                                'glucose': glu,
                                'ketones': ket,
                                'reaction': reac,
                                'sg': sg,
                                'uro': uro,
                                'name':file_name,
                                'file':uploaded_file,
                                }

                        request.session["urine_file_name"] = uploaded_file.name
                    
                    
                        form = ConfirmUrineForm(initial=initial)
                     
                        context = {
                            'form': form,
                            'file_name': file_name,
                            # 'confirm_id': request.session["confirm_id"]
                        }
                    else:
                        messages.error(request,'Please upload .png, .jpg or .pdf file.')

            return render(request, 'HtmlFiles/confirmUrineForm.html', context)
    else:
        print("yessss")
        return redirect('viewmyreports')

def confirmUrineForm(request):
    if request.method == 'POST':
        form = ConfirmUrineForm(request.POST)
        if form.is_valid():  
            obj = form.save(commit=False)
            file_name = request.session["urine_file_name"]
            if(file_name.lower().endswith(('.png', '.jpg', '.jpeg'))):
                obj.image = file_name
            elif(file_name.lower().endswith(('.pdf'))):
                obj.file = file_name
            obj.user = request.user
            obj.save()
            print('e')
    return redirect('viewmyreports')

def deleteUrineReport(request, rid):

    report = Urine.objects.get(id=rid)
    print(report.name)
    report.delete()

    user=request.user or None
    name=request.user.username or None
    return redirect('viewmyreports')