from django.http import JsonResponse
from django.shortcuts import render,redirect
from datetime import datetime
from Home.models import Contact
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from Home.helper import GETDATA
from django.contrib.auth.decorators import login_required
from Admin.forms import RegisterForm

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
    if request.user.is_authenticated:
        logout(request)
    return redirect("/login")


def signupUser(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Automatically log in the user after signup
                messages.success(request, "Account created successfully.")
                return redirect("home:login")  # Redirect to login page
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                form = RegisterForm(request.POST)  # Repopulate form with submitted data
    else:
        form = RegisterForm()

    return render(request, "signup.html", {'form': form})


def loginUser(request):
    if request.method == "POST":
        user = authenticate(username = request.POST["username"], password = request.POST["password"])

        if user is not None:
            return render(request, 'index.html')
    
    if request.method == "GET": 
        return render(request, "login.html")