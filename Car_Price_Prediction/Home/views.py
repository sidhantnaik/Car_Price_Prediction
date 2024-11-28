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
    flag = 1
    context = {}

    data_getter = GETDATA()  
    context = data_getter.get_cars_data()
    if flag == 2:
        flag = 2
          
    else:
        if request.method=="POST":
            car_brand = request.POST.get('car_brand')
            year = request.POST.get('year')
            km = request.POST.get('km')
            fuel_type = request.POST.get('fuel_type')
            seller_type = request.POST.get('seller_type')
            transmission = request.POST.get('transmission')
            owner = request.POST.get('owner')
            mileage = request.POST.get('mileage')
            engine = request.POST.get('engine')
            max_pow = request.POST.get('max_pow')
            seats = request.POST.get('seats')
            
            context = data_getter.get_prediction()  
            
            # car_brand,year,km,fuel_type,seller_type,transmission,owner,mileage,engine,max_pow,seats

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



# contact = Contact(car_brand=car_brand, year=year, km=km, fuel_type=fuel_type, seller_type=seller_type,transmission=transmission,owner=owner,mileage=mileage,engine=engine,max_pow=max_pow,seats=seats)
#             contact.save()