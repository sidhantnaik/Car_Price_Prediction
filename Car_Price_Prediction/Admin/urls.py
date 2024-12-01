from django.urls import path
from . import views



app_name = 'custom_admin'


urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('see_cars_data/', views.see_cars_data, name='see_cars_data'),
    path('add_new_car_data/', views.add_new_car_data, name='add_new_car_data'),
]