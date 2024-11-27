from django.shortcuts import render,HttpResponse
from datetime import datetime
from Home.models import Contact
from Home.models import Signin
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login




def index(request):

        from django.shortcuts import render
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        import os
        from django.conf import settings

        # Load and preprocess the data

        # file_path = os.path.join(settings.BASE_DIR, "Car_Price_Prediction", "Data", "Cardetails.csv")
        cars_data = pd.read_csv(r"D:\myProject\ML Project\Car_Price_Prediction\Data\Cardetails.csv")
        cars_data.drop(columns=["torque"], inplace=True)
        cars_data.dropna(inplace=True)
        cars_data.drop_duplicates(inplace=True)

       

        def get_first_string(firt_string):
            firt_string=firt_string.split(' ')[0]
            return firt_string.strip(' ')

        def get_first_value(value):
            value=value.split(' ')[0]
            value=value.strip()
            if value=='':
                value=0
            return float(value)

        cars_data['name']=cars_data['name'].apply(get_first_string)
        cars_data['mileage']=cars_data['mileage'].apply(get_first_value)
        cars_data['max_power']=cars_data['max_power'].apply(get_first_value)
        cars_data['engine']=cars_data['engine'].apply(get_first_value)


        # Extract unique values for dropdowns
        car_brands = cars_data['name'].unique()
        fuel_types = cars_data['fuel'].unique()
        transmissions = cars_data['transmission'].unique() 
        owners = cars_data['owner'].unique()
        engines = cars_data['engine'].unique()
        seller_type=cars_data['seller_type'].unique()
        max_power=cars_data['max_power'].unique()
        seats=cars_data['seats'].unique()
        


        arr=np.arange(1,32)

        cars_data['name'].replace(cars_data['name'].unique(),arr,inplace=True)
        cars_data['transmission'].replace(['Manual', 'Automatic'],[1,2],inplace=True)
        cars_data['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'],[1,2,3],inplace=True)
        cars_data['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'],[1,2,3,4],inplace=True)
        cars_data['owner'].replace(cars_data['owner'].unique(),[1,2,3,4,5],inplace=True)



        input_data = cars_data.drop(columns=['selling_price'])
        output_data = cars_data['selling_price']
        x_train, x_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2, random_state=2)

        model = RandomForestRegressor()
        model.fit(x_train, y_train)

        # Pass the dropdown data to the template
        context = {
            'car_brands': car_brands,
            'fuel_types': fuel_types,
            'transmissions': transmissions,
            'owners': owners,
            'engines': engines,
            'seller_type':seller_type,
            'max_power':max_power,
            'seats':seats,
            }
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