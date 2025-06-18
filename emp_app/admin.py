from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Role, Department, Task_manager

class CustomUserAdmin(UserAdmin):
    # Define fields to be used in the admin add/edit forms
    fieldsets = (
        (None, {'fields': ('email_address', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'dept', 'role', 'status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Define fields to be used in the admin add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_address', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    # Define fields to be displayed in the admin list view
    list_display = ('email_address', 'first_name', 'last_name', 'is_staff')
    # Define fields to be used for searching in the admin
    search_fields = ('email_address', 'first_name', 'last_name')
    # Define fields to be used for ordering in the admin
    ordering = ('email_address',)

# Register the Employee model with the custom admin class
admin.site.register(Employee, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Task_manager)