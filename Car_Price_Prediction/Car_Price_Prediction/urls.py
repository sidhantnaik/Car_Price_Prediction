from django.contrib import admin
from django.urls import path,include

admin.site.site_header="Car Price Prediction Admin"
admin.site.site_title="Admin Portal"
admin.site.index_title="Welcome to Car Price Prediction Admin"

urlpatterns = [
    path('', include('Home.urls')),
    path('custom_admin/', include(('Admin.urls', 'Admin'), namespace='custom_admin')),
    path('admin/', admin.site.urls),
]
