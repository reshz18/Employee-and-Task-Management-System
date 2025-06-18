from django import forms
from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_reason', 'from_date', 'to_date', 'place_of_visit', 'remarks']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['status']

from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['message']

from django import forms
from .models import DailyUpdate

class DailyUpdateForm(forms.ModelForm):
    class Meta:
        model = DailyUpdate
        fields = ['activity', 'description', 'daily_hours']

from django import forms
from .models import Salary

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['basic_salary', 'pf']


from django import forms
from .models import Employee

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email_address', 'phone', 'date_of_birth', 'gender', 'marital_status']

