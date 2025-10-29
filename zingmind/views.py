# from django.shortcuts import render, redirect 
# from .models import Employees
# from django.contrib.auth.decorators import login_required

# def login_view(request):
#     msg = ""
#     if request.method == "POST":
#         em = request.POST.get("email")
#         pwd = request.POST.get("password")

        
#         adminuser = Employees.objects.filter(email=em, password=pwd).first()
#         if adminuser:
#             print("valid admin==========================")
#             return render(request, "dashboard.html")

        
#         empuser = Employees.objects.filter(email=em, password=pwd).first()
#         if empuser:
#             print("valid employee=====")
            
#             return render(request, "employees_dashboard.html", {"employee": empuser})

        
#         msg = "Invalid email or password"
#     return render(request, "login.html", {"msg": msg})


# def home(request):
#     return render(request, "welcome.html")


# def reset_password(request):
#     return render(request, "password_reset_form.html")

# @login_required
# def dashboard(request):
#     return render(request, "dashboard.html")

# @login_required
# def employees_dashboard(request):
#     return render(request, "employees_dashboard.html")


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import check_password
# from .models import Employees


# def login_view(request):
#     msg = ""
#     if request.method == "POST":
#         em = request.POST.get("email")
#         pwd = request.POST.get("password")

#         try:
#             user = Employees.objects.get(email=em)  
#         except Employees.DoesNotExist:
#             messages.error(request, "Invalid email or password")
#             return render(request, "login.html", {"msg": msg})

    
#         if check_password(pwd, user.password):
            
#             request.session["employee_id"] = user.id
#             request.session["user_type"] = user.user_type

#             if user.user_type == "Admin":
#                 print("valid admin==========================")
#                 return render("dashboard")

#             elif user.user_type == "Employee":
#                 print("valid employee=====")
#                 return render("employees_dashboard")

#         else:
#             messages.error(request, "Invalid email or password")

#     return render(request, "login.html", {"msg": msg})


# def home(request):
#     return render(request, "welcome.html")


# def reset_password(request):
#     return render(request, "password_reset_form.html")


# # @login_required
# def dashboard(request):
#     return render(request, "dashboard.html")


# # @login_required
# def employees_dashboard(request):
#     emp_id = request.session.get("employee_id")
#     emp = Employees.objects.filter(id=emp_id).first()
#     return render(request, "employees_dashboard.html", {"employee": emp})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Employees, Attendance, EmployeeLeaves, SalaryTransactions, Departments, EmployeePersonalInfo, EmployeeContacts
from .decorators import login_required_custom, role_required
from django.contrib.auth.hashers import check_password, make_password

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employees

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import Employees

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Employees.objects.get(email=email)
        except Employees.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")

        # If you are storing plain passwords (not recommended):
        if user.password == password:
            if not user.is_active:
                messages.error(request, "Your account is inactive. Please contact admin.")
                return render(request, "login.html")

            # Set session variables
            request.session["user_id"] = user.id
            request.session["user_type"] = user.user_type

            # Redirect based on user type
            if user.user_type == "Admin":
                return redirect("dashboard")
            elif user.user_type == "HR":
                return redirect("/hr_dashboard/")
            else:
                return redirect("employees_dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")

    return render(request, "login.html")




@login_required_custom
@role_required("Admin")
def dashboard(request):
    user_id = request.session["user_id"]
    admin_user = Employees.objects.filter(id=user_id).first()

    total_employees = Employees.objects.count()
    total_departments = Departments.objects.count()
    total_attendance = Attendance.objects.count()

    return render(request, "dashboard.html", {
        "AdminUser": admin_user,
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_attendance": total_attendance,
    })


@login_required_custom
@role_required("HR")
def hr_dashboard(request):
    user_id = request.session["user_id"]
    total_employee = Employees.objects.filter(is_active=True).count()
    total_attendance = Attendance.objects.filter(attendance_date__month=timezone.now().month).count()
    pending_leaves = EmployeeLeaves.objects.filter(status="Pending").count()

    return render(request, "hr_dashboard.html", {
        "total_employee": total_employee,
        "total_attendance": total_attendance,
        "pending_leaves": pending_leaves,
    })


@login_required_custom
@role_required("Employee")
def employees_dashboard(request):
    user_id = request.session["user_id"]
    emp = get_object_or_404(Employees, id=user_id)

    personal_info = EmployeePersonalInfo.objects.filter(employee_code=emp).first()
    contacts = EmployeeContacts.objects.filter(employee_code=emp).first()
    department = emp.department

    attendance = Attendance.objects.filter(employee_code=emp).order_by('-attendance_date')[:10]
    leaves = EmployeeLeaves.objects.filter(employee_code=emp).order_by('-applied_date')[:5]
    payrolls = SalaryTransactions.objects.filter(employee_code=emp).order_by('-id')[:5]

    context = {
        "employee": emp,
        "employee_personal_info": personal_info,
        "employee_contacts": contacts,
        "department": department,
        "attendance": attendance,
        "employee_leaves": leaves,
        "salary_transactions": payrolls,
    }
    return render(request, "employees_dashboard.html", context)

    
def home(request):
    return render(request, "welcome.html")


def reset_password(request):
    return render(request, "password_reset_form.html")

@login_required_custom
@role_required("Admin")
def manage_employees(request):
    employees = Employees.objects.all() 
    return render(request, "admin/manage_employees.html", {"employees": employees})

@login_required_custom
@role_required("Admin")
def add_employee(request):
    departments = Departments.objects.all()
    if request.method == "POST":
        emp = Employees(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            role=request.POST.get("role"),
            password=make_password(request.POST.get("password")),  
            department=Departments.objects.get(pk=request.POST.get("department")) if request.POST.get("department") else None,
            is_active=request.POST.get("status") == "Active",
            created_date=timezone.now(),
            created_by=request.session.get("user_id"),
            )
        emp.save()
        messages.success(request, f"{emp.name} added successfully.")
        return redirect("manage_employees")
    return render(request, "admin/add_employee.html", {"departments": departments})

@login_required_custom
@role_required("Admin")
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employees, id=employee_id)
    departments = Departments.objects.all()

    if request.method == "POST":
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.role = request.POST.get("role")

        departments = request.POST.get("department")
        employee.is_active = True if request.POST.get("status") == "Active" else False
        employee.save()
        employee.updated_date = timezone.now()
        employee.updated_by = request.session.get("user_id")

        messages.success(request, f"{employee.name}'s details updated successfully.")
        return redirect("manage_employees")

    return render(request, "admin/edit_employee.html", {
        "employee": employee,
        "departments": departments
    })

@login_required_custom
@role_required("Admin")
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employees, id=employee_id)
    employee.delete()
    messages.success(request, f"{employee.name} deleted successfully.")
    return redirect("manage_employees")

@login_required_custom
@role_required("Admin")
# Attendance management
def manage_attendance(request):
    attendance = Attendance.objects.all().order_by("-attendance_date")
    return render(request, "admin/manage_attendance.html", {"attendance": attendance})

@login_required_custom
@role_required("Admin")
# Leave management
def manage_leave(request):
    leaves = EmployeeLeaves.objects.all().order_by("-applied_date")
    return render(request, "admin/manage_leave.html", {"leaves": leaves})

@login_required_custom
@role_required("Admin")
# Payroll management
def manage_payroll(request):
    payrolls = SalaryTransactions.objects.all().order_by("-id")
    return render(request, "admin/manage_payroll.html", {"payrolls": payrolls})

@login_required_custom
@role_required("Admin")
# Reports section
def manage_reports(request):
    return render(request, "admin/manage_reports.html")

@login_required_custom
@role_required("Admin")
# Settings section
def manage_settings(request):
    return render(request, "admin/manage_settings.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out securely.")
    return redirect("login")




# from django.contrib.auth.hashers import check_password, make_password

# def login_view(request):
#     msg = ""
#     if request.method == "POST":
#         em = request.POST.get("email")
#         pwd = request.POST.get("password")

#         try:
#             user = Employees.objects.get(email=em)
#         except Employees.DoesNotExist:
#             return render(request, "login.html", {"msg": "Invalid email or password"})

#         # Check password (works for plain or hashed passwords)
#         if user.password == pwd or check_password(pwd, user.password):
#             # Save user session
#             request.session["employee_id"] = user.id
#             request.session["user_type"] = user.user_type

#             # Redirect based on user_type
#             if user.user_type and user.user_type.lower() == "admin":
#                 return redirect("dashboard")
#             else:
#                 return redirect("employees_dashboard")
#         else:
#             msg = "Invalid email or password"

#     return render(request, "login.html", {"msg": msg})





# @login_required
# def dashboard(request):
#     admin_id = request.session.get("employee_id")
#     admin_user = Employees.objects.filter(id=admin_id).first()
#     return render(request, "dashboard.html", {"AdminUser": admin_user})


# @login_required
# def employees_dashboard(request):
#     emp_id = request.session.get("employee_id")
#     emp = Employees.objects.filter(id=emp_id).first()

#     # Attendance last 10 days
#     attendance = Attendance.objects.filter(EmployeeID=emp.employee_id).order_by('-AttendanceDate')[:10]

#     # Leave last 5
#     leaves = EmployeeLeaves.objects.filter(EmployeeID=emp.employee_id).order_by('-AppliedDate')[:5]

#     # Payroll last 5
#     payrolls = SalaryTransactions.objects.filter(EmployeeID=emp.employee_id).order_by('-ID')[:5]

#     context = {
#         "employee": emp,
#         "attendance": attendance,
#         "leaves": leaves,
#         "payrolls": payrolls,
#         # "tasks": [], "performance": {}, "documents": [], "notifications": []

#     }
#     return render(request, "employees_dashboard.html", context)

# def home(request):
#     return render(request, "welcome.html")


# def reset_password(request):
#     return render(request, "password_reset_form.html")
