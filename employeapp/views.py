import time

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Employee , Timecalc
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.utils import timezone

class Home(View):
    def get(self, request):
        return render(request,'login.html')

class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)                                               #login##
            return redirect ('/dashboard')
        else:
            messages.error(request, "INVALID LOGIN DETAILS")
            return render(request, 'login.html')



@method_decorator(login_required,name='dispatch')
class Dashboard(View):
    def get(self, request):                                        #dashboard##
        return render(request,'dashboard.html')



@method_decorator(login_required,name='dispatch')
class Users(View):
    def get(self, request):                                  ##employee list###
        y = Employee.objects.all()
        return render(request,'employeelist.html',{'employees':y})


@method_decorator(login_required,name='dispatch')
class Addemployee(View):
    def get(self,request):
        return render(request,'addemployee.html')            ## add employee page view ##



def logout_request(request):
    logout(request)
    return redirect("employeapp:home")


@method_decorator(login_required,name='dispatch')
class Saveemployee(View):
    def post(self,request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')                       ## saving employee###
        role = request.POST.get('role')
        password = request.POST.get('password')
        try:
            Employee(firstname=firstname,lastname=lastname,email=email,role=role,password=password).save()
            messages.success(request, "EMPLOYEE CREATED")
            return render(request,'addemployee.html')
        except IntegrityError:
            messages.error(request,'EMAIL ALREADY EXISTS')
            return render(request, 'addemployee.html')

@method_decorator(login_required,name='dispatch')
class Employeeattendence(View):                                      ## to display attendence page
    def get(self,request):
        y=Employee.objects.all()
        return render(request,'employeeattendence.html',{'employees':y})

@method_decorator(login_required,name='dispatch')
class Savingtime(View):
    def get(self,request):
        employee = request.GET.get('user') #getting userid
        state = request.GET.get('id')    #getting checkstate           ## saving time with selected employee
        if state == 'emp':   #to solve emp saving error
            y = Timecalc.objects.filter(employee=employee)
            return render(request,'table.html',{'times':y})
        else:
            current_datetime = datetime.datetime.now()
            emp=Employee.objects.get(id=employee)
            Timecalc(employee=emp,time=current_datetime,checkstate=state).save()
            y = Timecalc.objects.filter(employee=employee)  ## to show saved table
            return render(request,'table.html',{'times':y})

@method_decorator(login_required,name='dispatch')
class Buttonstate(View):                                      ## to check button state
    def get(self,request):
        ck_in_button = ''
        ck_out_button = ''
        bk_work_button = ''
        brk_button = ''
        time.sleep(0.1)     ## syncing frontend with backend
        employee = request.GET.get('user')
        y = Timecalc.objects.filter(employee=employee)
        ck_state = y[len(y)-1].checkstate  # getting last button checkstate
        if ck_state == "CHECK IN":
            ck_in_button = 1  #1-disable 0-enable
            bk_work_button = 0
            ck_out_button = 0
            brk_button = 0
        elif ck_state == 'BREAK':
            ck_in_button = 1
            bk_work_button = 0
            ck_out_button = 0
            brk_button = 1
        elif ck_state == 'BACK TO WORK':
            bk_work_button = 1
            ck_in_button = 1
            brk_button = 0
            ck_out_button = 0
        elif ck_state == 'CHECK OUT':
            bk_work_button = 1
            ck_in_button = 0
            brk_button = 1
            ck_out_button = 1
        return JsonResponse({"check_in":ck_in_button,"check_out":ck_out_button,"break":brk_button,"back_to_work":bk_work_button,})

@method_decorator(login_required,name='dispatch')
class Totaltiming(View):
    def get(self,request):
        time.sleep(0.1)
        employee = request.GET.get('user')
        y = Timecalc.objects.filter(employee=employee)
        total_hours =  (y[len(y) - 1].time - y[0].time).seconds/3600   #getting last and first time from queryset
        prev_time = y[0].time
        for i in y:
            localized_time = timezone.localtime(i.time)
            print("disp",(localized_time-prev_time).seconds)
            prev_time = localized_time
        total_hours=round(total_hours, 2)
        print(">>>",total_hours)
        return JsonResponse({"totalhours":total_hours})




