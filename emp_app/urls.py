from django.contrib import admin
from django.urls import path, include
from . import views
from .views import chat_room, create_meet, meet_page
from .views import salary_list, add_salary, employee_salary
from .views import salary_list, add_salary, employee_salary, download_salary_report, assign_salary
from .views import edit_employee_list, edit_employee, delete_employee

urlpatterns = [
    # General Routes
    path('', views.index, name="index"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),

    # Employee Management
    path('all_emp/', views.all_emp, name="all_emp"),
    path('add_emp/', views.add_emp, name="add_emp"),
    path('remove_emp_list/', views.remove_emp_list, name="remove_emp_list"),  # Page to select employee for removal
    path('remove_emp/<int:emp_id>/', views.remove_emp, name="remove_emp"),    # Remove specific employee
    path('filter_emp/', views.filter_emp, name="filter_emp"),

    # Dashboard Routes
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Task Management
    path('task/', views.task, name='task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('view_tasks/', views.view_tasks, name='view_tasks'),
    path('employee_tasks/', views.employee_tasks, name='employee_tasks'),
    path('employee_progress/', views.employee_progress, name='employee_progress'),

    # Leave Management
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('leave_history/', views.leave_history, name='leave_history'),
    path('edit_leave/<int:leave_id>/', views.edit_leave, name='edit_leave'),
    path('manage_leaves/', views.manage_leaves, name='manage_leaves'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('export_leaves/', views.export_leaves, name='export_leaves'),
    path('export_leaves_excel/', views.export_leaves_excel, name='export_leaves_excel'),
    path('leave_calendar/', views.leave_calendar, name='leave_calendar'),

    # Attendance Management
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('employee_attendance/', views.employee_attendance, name='employee_attendance'),

    # Announcements
    path('send_announcement/', views.send_announcement, name='send_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),

    # Chat & Meetings
    path("chat/<str:room_name>/", chat_room, name="chat_room"),
    path("chat_room/", views.chat_room, name='chat_room'),
    path("create-meet/", create_meet, name="create_meet"),  # Create Meeting Room
    path("meet/<str:meeting_id>/", meet_page, name="meet_page"),  # Meeting Page

    # Daily Updates
    path('submit_daily_update/', views.submit_daily_update, name='submit_daily_update'),
    path('view_employee_updates/', views.view_employee_updates, name='view_employee_updates'),
    path('employee_daily_updates/<int:employee_id>/', views.employee_daily_updates, name='employee_daily_updates'),

    #salary
    path('salaries/', salary_list, name='salary_list'),
    path('salaries/add/<int:employee_id>/', add_salary, name='add_salary'),
    path('salary/', employee_salary, name='employee_salary'),
    path('salary/download/', download_salary_report, name='download_salary_report'),
    path('assign_salary/', assign_salary, name='assign_salary'),

    #edit 
    path('edit_employee_list/', edit_employee_list, name='edit_employee_list'),
    path('edit_employee/<int:emp_id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:emp_id>/', delete_employee, name='delete_employee'),

]
