from django.shortcuts import render
from Home.helper import GETDATA

def admin_index(request):
    return render(request, 'admin_index.html')

def see_cars_data(request):
    data_getter = GETDATA()
    context = data_getter.get_cars_data()
    return render(request, 'see_cars_data.html', context)

def add_new_car_data(request):
    if request.method == 'POST':
        data_getter = GETDATA()
        data_getter.add_new_car(request.POST)
        return render(request, 'add_new_car_data.html', {'message': 'Car data added successfully!'})
    return render(request, 'add_new_car_data.html')