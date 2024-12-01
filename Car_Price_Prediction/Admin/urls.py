from django.contrib import admin
from django.urls import path
from Admin import views


urlpatterns = [
        path("", admin.site.urls, name='adminHome' ),
        path("showdata",views.showData,name='showCarsData'),
        path("addCar",views.addCar,name='addNewCar'),
]