"""
URL configuration for zingmind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# # ]

# from django.contrib import admin
# from django.urls import path
# from django.contrib.auth import views
# from .views import login_view , home , reset_password, dashboard 
# from . import views 

# urlpatterns = [
#     path('login/', login_view, name="login"),
#     path('dashboard/', dashboard ,name= "dashboard"),
#     # path('profile/',profile)
    
#     path('password_reset_form/',reset_password, name="password_reset_form.html"),
    
#     path('password_reset_email/', reset_password, name="password_reset_email.html"),

#     path('reset_password_done/',reset_password, name="reset_password_done"),

#     path('reset_password_confirm/', reset_password, name="reset_password_confirm"),

#     path('employees/', dashboard, name="employees"),

#     path('', home, name=""),


# ]


from django.urls import path
from .views import login_view, home, reset_password, dashboard , employees_dashboard, logout_view , hr_dashboard
from . import views


urlpatterns = [
    path("", home, name="welcome"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("password_reset_form/", reset_password, name="password_reset_form"),
    path("employees_dashboard/",employees_dashboard, name="employees_dashboard"),
    path("hr_dashboard/" ,hr_dashboard, name="hr_dashboard"),
    path('logout/', logout_view, name="logout"),


    path("admin/employees/", views.manage_employees, name="manage_employees"),
    path("admin/employees/add/", views.add_employee, name="add_employee"),
    path("admin/employees/edit/<int:employee_id>/", views.edit_employee, name="edit_employee"),
    path("admin/employees/delete/<int:employee_id>/", views.delete_employee, name="delete_employee"),
    path("admin/attendance/", views.manage_attendance, name="manage_attendance"),
    path("admin/leave/", views.manage_leave, name="manage_leave"),
    path("admin/payroll/", views.manage_payroll, name="manage_payroll"),
    path("admin/reports/", views.manage_reports, name="manage_reports"),
    path("admin/settings/", views.manage_settings, name="manage_settings"),
 ]
