import time

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Employee , Timecalc , Leave
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#import datetime
from django.utils import timezone
from datetime import datetime
from fpdf import FPDF

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
        checkin = []
        breaks = []
        backtowork =[]
        checkout = []
        totalhours = 0
        totalbreakhours = 0
        y= Timecalc.objects.all()

        for i in y:
            if i.checkstate=='CHECK IN':
                checkin.append(i.time)
            elif i.checkstate=='BREAK':
                breaks.append(i.time)
            elif i.checkstate=='BACK TO WORK':
                backtowork.append(i.time)
            else:
                checkout.append(i.time)
        if len(breaks)>len(backtowork):
            rang = len(backtowork)
        else:
            rang = len(breaks)
        for i in range(0,rang):
            totalbreakhours += ((backtowork[i]-breaks[i]).seconds/3600)
        if len(checkin)>len(checkout):
            rang = len(checkout)
        else:
            rang = len(checkin)
        for i in range(0,rang):
            totalhours+= ((checkout[i]-checkin[i]).seconds/3600)
        print("totalbreakhours",totalbreakhours)
        print("totalhours", totalhours)
        totalbreakhours=round(totalbreakhours, 2)
        averageintime = totalhours-totalbreakhours
        averageintime = round(averageintime, 2)
        print("checkin",len(checkin))
        averagehours = averageintime/len(checkin)
        averagehours = round(averagehours, 2)
        return render(request,'dashboard.html',{'averageintime':averageintime,'totalbreakhours':totalbreakhours,'averagehours':averagehours})



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
        date = request.GET.get('date')# getting calender date from front end
        date_object = datetime.strptime(date, "%Y-%m-%d") # converting date into date object
        #print(">>>>>>>>>>",employee)
        if state == 'emp' or state== 'date' or state=='FULL DAY LEAVE' or state=='HALF DAY LEAVE':   #to solve emp saving error
            date = Timecalc.objects.filter(employee=employee)
            filtered_list = []
            for i in date:
                date = timezone.localtime(i.time).date()
                if date == date_object.date():
                    filtered_list.append(i)
            return render(request,'table.html',{'times':filtered_list})
        else:
            current_datetime = datetime.now()
            emp = Employee.objects.get(id=employee)
            Timecalc(employee=emp, time=current_datetime, checkstate=state).save()
            date = Timecalc.objects.filter(employee=employee)
            filtered_list = []
            for i in date:
                date = timezone.localtime(i.time).date()
                if date == date_object.date():
                    filtered_list.append(i)
            return render(request,'table.html',{'times':filtered_list})

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
        if y:
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
        else:
            ck_in_button = 0  # 1-disable 0-enable
            bk_work_button = 1
            ck_out_button = 1
            brk_button = 1
        return JsonResponse({"check_in":ck_in_button,"check_out":ck_out_button,"break":brk_button,"back_to_work":bk_work_button,})

@method_decorator(login_required,name='dispatch')
class Totaltiming(View):
    def get(self,request):
        time.sleep(0.1)
        employee = request.GET.get('user')
        date = request.GET.get('date')
        date_object = datetime.strptime(date, "%Y-%m-%d")
        #y = Timecalc.objects.filter(employee=employee)
        #total_hours =  (y[len(y) - 1].time - y[0].time).seconds/3600   #getting last and first time from queryset for total hours
        list_of_dates = []
        breaks = []
        back_to_works = []
        total_break_hours = 0
        date = Timecalc.objects.filter(employee=employee)
        for i in date:
            date = timezone.localtime(i.time).date()
            if date == date_object.date():
                list_of_dates.append(i)
        if list_of_dates==[]:
            total_hours = 0
            total_office_hours = 0
            return JsonResponse({"totalhours": total_hours, "in_office_hours": total_office_hours, })
        total_hours = (list_of_dates[len(list_of_dates) - 1].time - list_of_dates[0].time).seconds / 3600  #getting last and first time from queryset for total hours
        total_hours = round(total_hours, 2)
        for i in list_of_dates:
            if i.checkstate == 'BREAK':
                breaks.append(i)
            elif i.checkstate == 'BACK TO WORK':
                back_to_works.append(i)
        # to prevent list index error
        if len(breaks) > len(back_to_works):
            rang = len(back_to_works)
        else:
            rang = len(breaks)
        for i in range(0,rang):
            total_break_hours += ((back_to_works[i].time-breaks[i].time).seconds/3600)  #BACK TO WORK - BREAK
        total_office_hours = total_hours - total_break_hours
        total_office_hours = round(total_office_hours,2)
        return JsonResponse({"totalhours":total_hours,"in_office_hours":total_office_hours,})

@method_decorator(login_required,name='dispatch')
class Leavings(View):
    def get(self,request):
        employee = request.GET.get('user')
        leavetype = request.GET.get('id')
        time = request.GET.get('time')
        date = request.GET.get('date')
        emp = Employee.objects.get(id=employee)
        current_datetime = datetime.now()
        if  leavetype != 'date' and leavetype != 'emp' and leavetype != 'BACK TO WORK' and leavetype !='CHECK IN' and leavetype != 'CHECK OUT' and leavetype !='BREAK':
            Leave(employee=emp,leavetype=leavetype,system_time=current_datetime,full_day_or_half_day_date_or_late_comming_or_early_logout_time=date).save()   # saving leave type with employee
        return HttpResponse("success")


@method_decorator(login_required,name='dispatch')
class Reports(View):
    def get(self,request):
        employee = request.GET.get('user')
        fromdate = request.GET.get('fromdate')
        todate = request.GET.get('todate')
        if employee != None and employee != None and fromdate != None and todate != None and employee !='Select Employee':
            from_date_object = datetime.strptime(fromdate, "%Y-%m-%d")                  ### report page on table
            to_date_object = datetime.strptime(todate, "%Y-%m-%d")
            checkin=[]
            checkout=[]
            breaks=[]
            backtowork=[]
            filter=Timecalc.objects.filter(employee=employee,time__range=[from_date_object,to_date_object])
            for i in filter:
                if i.checkstate=='CHECK IN':
                    checkin.append(i.time)
                elif i.checkstate=='CHECK OUT':
                    checkout.pop()
                    checkout.append(i.time)
                    checkin.pop()

                elif i.checkstate=='BREAK':
                    breaks.append(i.time)
                elif i.checkstate=='BACK TO WORK':
                    backtowork.append(i.time)
                    checkin.append("")
                    checkout.append("")
            z=zip(checkin,breaks,backtowork,checkout)
            return render(request,'table2.html',{'filtered':filter,'times':z})
        return render(request, 'table2.html')


@method_decorator(login_required,name='dispatch')
class Reportsemployee(View):                 ## rendering report page
    def get(self,request):
        y = Employee.objects.all()
        return render(request, 'report.html', {'employees': y})




'''class Report(View):
    def get(self, request):
        sales = [
            {"month": "JANUARY", "attendence": "100%"},
            {"month": "FEBRUARY", "attendence": "80%"},
            {"month": "MARCH", "attendence": "65%"},
            {"month": "APRIL", "attendence": "65%"},
            {"month": "MAY", "attendence": "65%"},
            {"month": "JUNE", "attendence": "65%"},
            {"month": "JULY", "attendence": "65%"},
            {"month": "AUGUST", "attendence": "65%"},
            {"month": "SEPTEMBER", "attendence": "65%"},
            {"month": "OCTOBER", "attendence": "65%"},
            {"month": "NOVEMBER", "attendence": "65%"},
            {"month": "DECEMBER", "attendence": "65%"},
        ]
        name = 'Kevin'
        current_datetime = str(datetime.now())
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        #pdf.image(name='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOebxopOqyWxbjIVqkoRlZH5Sv2tD-iFeU3P5ZMiQ8uqqRy_CDkg85NQBATWuJvCSLkcc&usqp=CAU', x=20, y=70, w=100, h=50, type='', link='')
        pdf.set_font('courier', 'B', 16)
        pdf.cell(40, 10,'CODESVERA INFOTECH', 0, 1)
        pdf.cell(40, 10, current_datetime, 0, 1)
        pdf.cell(40, 10, 'EMPLOYEE REPORT',0,1)
        pdf.cell(40, 10, '',0,1)
        pdf.cell(40, 10, name, 0, 1)
        pdf.cell(40, 10, '', 0, 1)
        pdf.cell(200, 8, f"{'MONTH'.ljust(30)} {'ATTENDENCE'.rjust(20)}", 0, 1)
        pdf.line(10, 30, 190, 30)
        pdf.line(10, 38, 190, 38)
        for line in sales:
            pdf.cell(200, 8, f"{line['month'].ljust(30)} {line['attendence'].rjust(20)}", 0, 1)

        pdf.output('tuto1.pdf', 'F')
        return FileResponse(open('tuto1.pdf', 'rb'), as_attachment=False, content_type='application/pdf')'''










