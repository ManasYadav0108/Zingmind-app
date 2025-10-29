# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class Admin(models.Model):
#     id = models.AutoField(primary_key=True)   
#     email = models.EmailField(max_length=255, unique=True)  
#     password = models.CharField(max_length=255)             

#     def __str__(self):
#         return self.email



# class Company(models.Model):
#     name = models.CharField(max_length=150)
#     address = models.TextField(blank=True, null=True)
#     contact_email = models.EmailField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Employees(models.Model):
#     full_name = models.CharField(max_length=150)
#     id = models.AutoField(primary_key=True)   
#     email = models.EmailField(max_length=255, unique=True)  
#     password = models.CharField(max_length=255)             
#     # profile_image = models.ImageField(upload_to="profile_images/", default="profile_images/default.png")
#     def __str__(self):
#         return self.email



# class Document(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="documents")
#     title = models.CharField(max_length=200)
#     file_path = models.FileField(upload_to="documents/")
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

from django.db import models


class Assets(models.Model):
    asset_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assets'


class Attendance(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    attendance_date = models.DateField(blank=True, null=True)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    work_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attendance'


class Departments(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departments'


class EmployeeAppraisals(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    appraisal_period = models.CharField(max_length=20, blank=True, null=True)
    self_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    manager_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    appraisal_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_appraisals'


class EmployeeAssets(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    asset = models.ForeignKey(Assets, models.DO_NOTHING, blank=True, null=True)
    issued_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    condition_on_return = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_assets'


class EmployeeBankDetails(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    ifsc = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    aadhar = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_bank_details'


class EmployeeContacts(models.Model):
    employee_code = models.OneToOneField('Employees', models.DO_NOTHING, db_column='employee_code', primary_key=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    alternate_no = models.CharField(max_length=15, blank=True, null=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    present_address = models.TextField(blank=True, null=True)
    emergency_contact_person = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_no = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_contacts'


class EmployeeGoals(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    goal_description = models.TextField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_goals'


class EmployeeLeaves(models.Model):
    employee_code = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    leave_type = models.ForeignKey('LeaveTypes', models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    applied_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_leaves'


class EmployeePersonalInfo(models.Model):
    employee_code = models.OneToOneField('Employees', models.DO_NOTHING, db_column='employee_code', primary_key=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    functional_area = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    work_history = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_personal_info'


class Employees(models.Model):
    employee_code = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Departments, models.DO_NOTHING, blank=True, null=True)
    reporting_manager = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    employment_type = models.CharField(max_length=50, blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    # is_active = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    doj = models.DateField(blank=True, null=True)
    date_of_leaving = models.DateField(blank=True, null=True)
    resignation_date = models.DateField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=8, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'employees'


class LeaveTypes(models.Model):
    leave_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leave_types'


class SalaryStructure(models.Model):
    employee_code = models.ForeignKey(Employees, models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    monthly_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    annual_ctc_without_bonus = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    annual_ctc_with_bonus = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    basic_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    telephone_reimbursement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    uniform_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bonus_eligible = models.IntegerField(blank=True, null=True)
    revision_month = models.CharField(max_length=20, blank=True, null=True)
    last_revision_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salary_structure'


class SalaryTransactions(models.Model):
    employee_code = models.ForeignKey(Employees, models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    month_year = models.CharField(max_length=10, blank=True, null=True)
    total_days = models.IntegerField(blank=True, null=True)
    working_days = models.IntegerField(blank=True, null=True)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tds = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    advance_deduction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    employee_pf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    esic = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    inhand_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    employer_epf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    employer_esic = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bonus_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salary_transactions'
