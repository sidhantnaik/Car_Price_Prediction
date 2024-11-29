from django.shortcuts import render,HttpResponse
from datetime import datetime
from Home.models import Contact
from Home.models import Signin
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from Home.helper import GETDATA

def index(request):
    data_getter = GETDATA()
    context = data_getter.get_cars_data()

    if request.method == "POST":
        input_data = {
            'name': request.POST.get('car_brand'),  
            'year': int(request.POST.get('year')),
            'km': float(request.POST.get('km')),
            'fuel': request.POST.get('fuel_type'),  
            'seller_type': request.POST.get('seller_type'),  
            'transmission': request.POST.get('transmission'),  
            'owner': request.POST.get('owner'),  
            'mileage': float(request.POST.get('mileage')),
            'engine': float(request.POST.get('engine')),
            'max_power': float(request.POST.get('max_pow')),
            'seats': int(request.POST.get('seats')),
        }

        context = data_getter.get_prediction(input_data)


    return render(request, 'index.html', context)



# def index(request):
#     if request.user.is_anonymous:
#         return redirect("/login")
    
    
#     return render(request,"index.html")

def login(request):
    if request.method=="POST":
        name = request.POST.get('name')
        passw = request.POST.get('passw')

        user=authenticate(username=name,password=passw)
        if user is not None:
            return redirect("/login")
        else:
            return render(request,"login.html")


def signin(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        passw = request.POST.get('passw')
        confpass=request.POST.get('confpass')
        
        if confpass==passw:
            signin = Signin(name=name, email=email, phone=phone,passw=passw)
            signin.save()
            messages.success(request,"Sign in succefully.")
        else:
            messages.warning(request,"unable to Sign in. ")

    return render(request, "signin.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        passw = request.POST.get('passw')
        contact = Contact(name=name, email=email, phone=phone, passw=passw, date=datetime.today())
        contact.save()
        messages.success(request,"your data is submitted succefully.")
    return render(request, "contact.html")

def logout(request):
    logout()
    return render(request,'index.html')

