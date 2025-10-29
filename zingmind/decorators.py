from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.error(request, "You must log in first.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    """Restrict access to specific user roles"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_type = request.session.get("user_type")
            if not user_type:
                return redirect("login")
            if user_type not in roles:
                messages.error(request, "Access denied.")
                return redirect("login")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
