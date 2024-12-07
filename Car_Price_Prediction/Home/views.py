from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from Home.models import Contact,UserData
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from Home.helper import GETDATA
from django.contrib.auth.hashers import make_password,check_password

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    data_getter = GETDATA()
    context = data_getter.get_cars_data()

    if request.method == "POST":
        input_data = {
            'name': request.POST.get('car_brand'),  
            'year': request.POST.get('year'),
            'km': request.POST.get('km'),
            'fuel': request.POST.get('fuel_type'),  
            'seller_type': request.POST.get('seller_type'),  
            'transmission': request.POST.get('transmission'),  
            'owner': request.POST.get('owner'),  
            'mileage': request.POST.get('mileage'),
            'engine': request.POST.get('engine'),
            'max_power': request.POST.get('max_pow'),
            'seats': request.POST.get('seats'),
        }

        prediction = data_getter.get_prediction(input_data)
        print("=="*30)
        print("POST")
        print("=="*30)
        return JsonResponse(prediction)
    
    print("=="*30)
    print("GET")
    print("=="*30)

    return render(request, 'index.html', context)


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


def signupUser(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone=request.POST['phone']
        password = request.POST['passw']
        confirm_password = request.POST['confpass']

        if password==confirm_password:
            user = UserData(name=name, email=email, phone=phone, password=make_password(password))  
            user.save()
            # messages.success(request,"your data is submitted succefully.")
        return redirect('/login')
    
    return render(request, 'signup.html')


def loginUser(request):
    if request.method == "POST":
        user = authenticate(username = request.POST["username"], password = request.POST["password"])

        if user is None:
            return render(request, "login.html", { "error": "Something went wrong!" })
        else:
            return render(request, 'index.html')
    
    if request.method == "GET": 
        return render(request, "login.html")