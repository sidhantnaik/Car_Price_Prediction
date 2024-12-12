# Home/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from functools import wraps
from django.shortcuts import render,redirect


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to the default admin login page with next parameter
            login_url = reverse_lazy('admin:login')
            redirect_url = f"{login_url}?next={request.path}"
            return redirect(redirect_url)
    return _wrapped_view
