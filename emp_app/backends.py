from django.contrib.auth.backends import BaseBackend
from .models import Employee

class EmployeeBackend(BaseBackend):
    def authenticate(self, request, email_address=None, password=None):
        try:
            user = Employee.objects.get(email_address=email_address)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None