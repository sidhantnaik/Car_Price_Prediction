from django.urls import path
from Home import views
from django.contrib.auth import views as auth_views
from Admin.forms import LoginForm

app_name = 'home'

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path(
        "login", 
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
            extra_context={'next': '/'}
        ),
        name='login'
    ),
    path("signup", views.signupUser, name='signup'),
    path("logout", views.logoutUser, name='logout'),
]