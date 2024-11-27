from django.contrib import admin
from django.urls import path
from Home import views


urlpatterns = [
        path("", views.index, name='home' ),
        path("about",views.about,name='about'),
        path("contact",views.contact,name='contact'),
        path("login",views.login,name='login'),
        path("signin",views.signin,name='signin')
]