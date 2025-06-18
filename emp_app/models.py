from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime
# from django.db import models
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

# class EmployeeManager(BaseUserManager):
#     def create_user(self, email_address, password=None, **extra_fields):
#         if not email_address:
#             raise ValueError('Email is required!')
#         email_address = self.normalize_email(email_address)
#         user = self.model(email_address=email_address, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email_address, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         # Ensure a default department exists or assign one manually
#         if 'dept' not in extra_fields or not extra_fields['dept']:
#             default_dept, created = Department.objects.get_or_create(name="Admin", location="Head Office")
#             extra_fields['dept'] = default_dept  # Assign the department object

#         return self.create_user(email_address, password, **extra_fields)
class EmployeeManager(BaseUserManager):
    def create_user(self, email_address, password=None, **extra_fields):
        if not email_address:
            raise ValueError("Email is required!")
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Default Department
        if "dept" not in extra_fields or not extra_fields["dept"]:
            default_dept, _ = Department.objects.get_or_create(name="Admin", location="Head Office")
            extra_fields["dept"] = default_dept  

        # Default Role
        if "role" not in extra_fields or not extra_fields["role"]:
            default_role, _ = Role.objects.get_or_create(name="Administrator")
            extra_fields["role"] = default_role  

        # Default Personal Details
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "User")
        extra_fields.setdefault("phone", 0000000000)  # Integer, not string
        extra_fields.setdefault("salary", 0)
        extra_fields.setdefault("bonus", 0)
        extra_fields.setdefault("hire_date", datetime.date.today())

        return self.create_user(email_address, password, **extra_fields)


# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# import datetime
# from django.utils import timezone

class Employee(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=10, choices=[('Manager', 'Manager'), ('Employee', 'Employee')], default='Employee')
    email_address = models.EmailField(unique=True, default="temp@example.com")
    password = models.CharField(max_length=100, default="defaultpassword123")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # New fields
    date_of_birth = models.DateField(default=datetime.date(2004, 1, 1))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.png')

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = EmployeeManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

# from django.db import models
# from .models import Employee

class Task_manager(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    task_name = models.CharField(max_length=100, null=False)
    task_description = models.TextField()
    task_start_date = models.DateField()
    task_end_date = models.DateField()
    task_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name

class Task_employee(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    task = models.OneToOneField(Task_manager, on_delete=models.CASCADE, related_name='employee_task')
    task_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Not Started')
    file = models.FileField(upload_to='task_files/', blank=True, null=True)  # Files will be uploaded to media/task_files/

    def __str__(self):
        return f"{self.task.task_name} - {self.task_status}"
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Leave(models.Model):
    LEAVE_REASONS = [
        ('Holiday', 'Holiday'),
        ('Medical Leave', 'Medical Leave'),
        ('Other', 'Other'),
        ('Personal Reason', 'Personal Reason'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=50, choices=LEAVE_REASONS)
    from_date = models.DateField()
    to_date = models.DateField()
    place_of_visit = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.leave_reason}"
    
from django.db import models
from .models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def _str_(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date} - {self.status}"
    



class Announcement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Announcement by {self.created_by.first_name} on {self.created_at}"
    
from django.conf import settings
from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chat_rooms")

    def __str__(self):
        return self.name if self.name else f"ChatRoom {self.id}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}..."


from django.db import models
from django.utils import timezone

class DailyUpdate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    activity = models.CharField(max_length=255)
    description = models.TextField()
    daily_hours = models.IntegerField()

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

    def weekly_hours(self):
        start_of_week = self.date - timezone.timedelta(days=self.date.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        weekly_updates = DailyUpdate.objects.filter(
            employee=self.employee,
            date__range=[start_of_week, end_of_week]
        )
        return sum(update.daily_hours for update in weekly_updates)
    

from django.db import models
from django.contrib.auth import get_user_model
from .models import Employee

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salaries")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    pf = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Provident Fund
    on_hand_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate on-hand salary after PF deduction
        self.on_hand_salary = self.basic_salary - self.pf
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - {self.on_hand_salary}"
