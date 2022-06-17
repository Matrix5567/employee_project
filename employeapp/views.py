from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class Home(View):
    def get(self, request):
        return render(request,'login.html')

class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect ('/dashboard')
        else:
            messages.error(request, "INVALID LOGIN DETAILS")
            return render(request, 'login.html')

class Dashboard(View):
    def get(self, request):
        return render(request,'dashboard.html')

class Users(View):
    def get(self, request):                                ##employee list###
        return render(request,'employeelist.html')

class Addemployee(View):
    def get(self,request):
        return render(request,'addemployee.html')            ##createemployee##



def logout_request(request):
    logout(request)
    return redirect("employeapp:home")

