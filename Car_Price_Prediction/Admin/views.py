from django.shortcuts import render
from Home.helper import GETDATA
import os,csv
from django.contrib import messages
from pathlib import Path
from django.conf import settings
from Admin.decorators import admin_required

def admin_index(request):
    return render(request, 'admin_index.html')

@admin_required
def see_cars_data(request):
    data_getter = GETDATA()
    raw_context = data_getter.get_cars_data()

    # Prepare the data for the template
    car_data_list = []
    for car_id in raw_context['car_brands']:
        car_data_list.append({
            'car_id': car_id,
            'brand': raw_context['car_brands'].get(car_id, ""),
            'fuel_type': raw_context['fuel_types'].get(car_id, ""),
            'transmission': raw_context['transmissions'].get(car_id, ""),
            'owner': raw_context['owners'].get(car_id, ""),
            'seller_type': raw_context['seller_types'].get(car_id, ""),
            'engine': raw_context['engines'].get(car_id, ""),
            'max_power': raw_context['max_power'].get(car_id, ""),
            'seats': raw_context['seats'].get(car_id, ""),
        })

    context = {'car_data': car_data_list}
    return render(request, 'see_cars_data.html', context)



data_path = os.path.join(settings.BASE_DIR, 'Data', 'Cardetails.csv')

@admin_required
def add_new_car_data(request):
    if request.method == 'POST':
        data_getter = GETDATA()
        data = {
            'car_brand': request.POST.get('car_brand'),
            'year': int(request.POST.get('year')),
            'km': float(request.POST.get('km')),
            'fuel_type': request.POST.get('fuel_type'),
            'seller_type': request.POST.get('seller_type'),
            'transmission': request.POST.get('transmission'),
            'owner': request.POST.get('owner'),
            'mileage': float(request.POST.get('mileage')),
            'engine': float(request.POST.get('engine')),
            'max_pow': float(request.POST.get('max_pow')),
            'seats': int(request.POST.get('seats')),
        }

        with open(data_path, 'a', newline='') as csvfile:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)

        messages.success(request,"Car data added successfully!")
        return render(request, 'add_new_car_data.html')

    return render(request, 'add_new_car_data.html')