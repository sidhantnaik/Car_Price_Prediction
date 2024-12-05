from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from Home.models import Contact
from Home.models import Signin
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from Home.helper import GETDATA


def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    
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

        prediction = data_getter.get_prediction(input_data)
        return JsonResponse(prediction)

    return render(request, 'index.html', context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

    return render(request, "login.html")

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
    messages.success(request,"ohh yeah !")
    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request,"your data is submitted succefully.")
    return render(request, "contact.html")

def logoutUser(request):
    logout(request)
    return redirect('/login')

