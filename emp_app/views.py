from .models import Employee, Role,Department,Task_manager
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Task_employee
from .models import Leave
from .forms import LeaveForm, LeaveApprovalForm
from .forms import DailyUpdateForm
from .models import DailyUpdate
# from django.shortcuts import render
# from .models import Task_manager
from django.http import JsonResponse
from .models import Announcement
from .forms import AnnouncementForm
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def all_emp(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)

from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Employee
from django.core.mail import send_mail
from django.conf import settings

def remove_emp(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == "POST":
        removal_reason = request.POST.get("removal_reason")
        explanation = request.POST.get("explanation")
        last_working_day = request.POST.get("last_working_day")
        supporting_doc = request.FILES.get("supporting_doc")  # File Upload Handling

        # OPTIONAL: Update Employee Status Instead of Deleting
        employee.status = "Inactive"
        employee.removal_reason = removal_reason
        employee.explanation = explanation
        employee.last_working_day = last_working_day

        if supporting_doc:
            employee.supporting_doc = supporting_doc  # Assuming a FileField in your Employee model

        employee.save()

        # OPTIONAL: Send Email Notification
        subject = f"Employee Removal Notification - {employee.first_name} {employee.last_name}"
        message = (
            f"{employee.first_name} {employee.last_name} has been removed.\n\n"
            f"Reason: {removal_reason}\n"
            f"Explanation: {explanation}\n"
            f"Last Working Day: {last_working_day}"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [employee.email_address])

        return JsonResponse({"success": True, "message": "Employee removed successfully"})

    return render(request, "remove_emp.html", {"employee": employee})



from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .models import Employee, Department, Role
from datetime import datetime
@login_required(login_url='login')
def add_emp(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')

    if request.method == 'POST':
        try:
            # Retrieve form data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email_address = request.POST['email_address']
            password = request.POST['password']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept_id = int(request.POST['dept'])
            role_id = int(request.POST['role'])
            status = request.POST['status']
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']
            marital_status = request.POST['marital_status']
            profile_photo = request.FILES.get('profile_photo')

            # Check if an employee with the same email already exists
            if Employee.objects.filter(email_address=email_address).exists():
                return JsonResponse({'success': False, 'message': 'An employee with this email address already exists.'})

            # Create and save the new employee
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept_id=dept_id,
                role_id=role_id,
                hire_date=datetime.now(),
                status=status,
                date_of_birth=date_of_birth,
                gender=gender,
                marital_status=marital_status,
                profile_photo=profile_photo
            )
            new_emp.set_password(password)  # Hash the password
            new_emp.save()

            # Return a JSON response with success message
            return JsonResponse({'success': True, 'message': 'Employee added successfully!'})
        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Missing field: {e}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'})

    elif request.method == 'GET':
        # Fetch departments and roles for the form dropdowns
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'add_emp.html', context)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
def filter_emp(request):
    return render(request, 'filter_emp.html')

# def task(request):
#     if request.method == 'POST':
#         task_name = request.POST['task_name']
#         task_description = request.POST['task_description']
#         task_start_date = request.POST['task_start_date']
#         task_end_date = request.POST['task_end_date']
#         task_priority = request.POST['task_priority']
#         task_status = request.POST['task_status']
#         assigned_to_id = request.POST['assigned_to']  # Employee ID from form

#         try:
#             assigned_to = Employee.objects.get(id=assigned_to_id)  # Fetch Employee object
#             new_task = Task_manager(
#                 task_name=task_name,
#                 task_description=task_description,
#                 task_start_date=task_start_date,
#                 task_end_date=task_end_date,
#                 task_priority=task_priority,
#                 task_status=task_status,
#                 assigned_to=assigned_to  # Pass Employee object
#             )
#             new_task.save()
#             return HttpResponse('Task added successfully')
#         except Employee.DoesNotExist:
#             return HttpResponse('Error: Employee not found')

#     elif request.method == 'GET':
#         emps = Employee.objects.all()
#         context = {
#             'emps': emps
#         }
#         print(context)
#         return render(request, 'task.html', context)
#     else:
#         return HttpResponse('Invalid request')
    
from django.shortcuts import render, HttpResponse
from .models import Employee, Task_manager
from datetime import datetime

from django.http import JsonResponse

def task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        task_start_date = request.POST['task_start_date']
        task_end_date = request.POST['task_end_date']
        task_priority = request.POST['task_priority']
        assigned_to_id = request.POST['assigned_to']

        try:
            assigned_to = Employee.objects.get(id=assigned_to_id)
            new_task = Task_manager(
                task_name=task_name,
                task_description=task_description,
                task_start_date=task_start_date,
                task_end_date=task_end_date,
                task_priority=task_priority,
                assigned_to=assigned_to
            )
            new_task.save()
            # Create a corresponding Task_employee entry
            Task_employee.objects.create(task=new_task)

            # Return a JSON response with success message
            return JsonResponse({'success': True, 'message': 'Task created successfully!'})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Error: Employee not found'})

    elif request.method == 'GET':
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        return render(request, 'task.html', context)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    


# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email_address')
#         password = request.POST.get('password')
#         user = authenticate(request, email_address=email, password=password)
#         if user:
#             login(request, user)
#             if user.status == 'Manager':
#                 return redirect('manager_dashboard')
#             else:
#                 return redirect('employee_dashboard')
#         else:
#             return HttpResponse('Invalid credentials')
#     return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        password = request.POST.get('password')
        user = authenticate(request, email_address=email, password=password)
        if user is not None:
            login(request, user)
            if user.status == 'Manager':
                return redirect('manager_dashboard')  # Redirect to dashboard
            else:
                return redirect('employee_dashboard')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Leave, Announcement

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Leave, Announcement

@login_required(login_url='login')
def manager_dashboard(request):
    if not request.user.is_authenticated or request.user.status != 'Manager':
        return redirect('login')

    # Fetch data for the dashboard
    total_employees = Employee.objects.count()
    on_leave_today = Leave.objects.filter(from_date__lte=timezone.now(), to_date__gte=timezone.now()).count()
    pending_leave_requests = Leave.objects.filter(status='Pending').count()  # Count pending leave requests
    announcements = Announcement.objects.all().order_by('-created_at')[:4]  # Latest 4 announcements

    context = {
        'total_employees': total_employees,
        'on_leave_today': on_leave_today,
        'pending_leave_requests': pending_leave_requests,  # Add pending leave requests to context
        'announcements': announcements,
    }
    return render(request, 'manager_dashboard.html', context)

@login_required(login_url='login')
def employee_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch tasks assigned to the logged-in employee
    tasks = Task_manager.objects.filter(assigned_to=request.user)

    # Calculate task counts based on Task_employee status
    tasks_completed = Task_employee.objects.filter(task__assigned_to=request.user, task_status="Completed").count()
    tasks_in_progress = Task_employee.objects.filter(task__assigned_to=request.user, task_status="In Progress").count()
    tasks_not_started = Task_employee.objects.filter(task__assigned_to=request.user, task_status="Not Started").count()

    # Fetch leave requests for the logged-in employee
    leaves = Leave.objects.filter(employee=request.user)

    # Fetch announcements (latest 4)
    announcements = Announcement.objects.all().order_by('-created_at')[:4]

    context = {
        'tasks': tasks,
        'tasks_completed': tasks_completed,
        'tasks_in_progress': tasks_in_progress,
        'tasks_not_started': tasks_not_started,
        'leaves': leaves,
        'announcements': announcements,
    }
    return render(request, 'employee_dashboard.html', context)

# from django.shortcuts import get_object_or_404, redirect
# from .models import Task_employee

# from django.shortcuts import get_object_or_404, redirect
# from .models import Task_employee

def update_task(request, task_id):
    task_employee = get_object_or_404(Task_employee, task_id=task_id)
    if request.method == 'POST':
        if 'save' in request.POST:
            # Update task status
            task_employee.task_status = request.POST['task_status']
            task_employee.save()
        elif 'submit' in request.POST:
            # Handle file upload and final submission
            if 'file' in request.FILES:
                task_employee.file = request.FILES['file']
            task_employee.task_status = "Completed"  # Automatically set status to "Completed" on submission
            task_employee.save()
        return redirect('employee_tasks')
    return render(request, 'employee_tasks.html', {'tasks': Task_manager.objects.filter(assigned_to=request.user)})



def view_tasks(request):
    tasks = Task_manager.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'view_tasks.html', context)

# from django.shortcuts import render
# from .models import Task_manager

def employee_tasks(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch active tasks assigned to the logged-in employee
    tasks = Task_manager.objects.filter(assigned_to=request.user, employee_task__task_status__in=["Not Started", "In Progress"])
    context = {
        'tasks': tasks
    }
    return render(request, 'employee_tasks.html', context)

# from django.shortcuts import render
# from .models import Task_manager, Task_employee
from datetime import date

def employee_progress(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch completed tasks (history)
    task_history = Task_manager.objects.filter(assigned_to=request.user, employee_task__task_status="Completed")

    # Calculate statistics
    total_tasks = Task_manager.objects.filter(assigned_to=request.user).count()
    tasks_completed_on_time = Task_manager.objects.filter(
        assigned_to=request.user,
        employee_task__task_status="Completed",
        task_end_date__gte=date.today()  # Tasks completed before or on the deadline
    ).count()
    tasks_submitted_late = Task_manager.objects.filter(
        assigned_to=request.user,
        employee_task__task_status="Completed",
        task_end_date__lt=date.today()  # Tasks completed after the deadline
    ).count()
    tasks_not_submitted = Task_manager.objects.filter(
        assigned_to=request.user,
        employee_task__task_status__in=["Not Started", "In Progress"]
    ).count()

    context = {
        'task_history': task_history,
        'total_tasks': total_tasks,
        'tasks_completed_on_time': tasks_completed_on_time,
        'tasks_submitted_late': tasks_submitted_late,
        'tasks_not_submitted': tasks_not_submitted,
    }
    return render(request, 'employee_progress.html', context)
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Leave
# from .forms import LeaveForm, LeaveApprovalForm

@login_required(login_url='login')
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            return redirect('leave_history')
    else:
        form = LeaveForm()
    return render(request, 'apply_leave.html', {'form': form})

@login_required(login_url='login')
def leave_history(request):
    leaves = Leave.objects.filter(employee=request.user)
    return render(request, 'leave_history.html', {'leaves': leaves})

@login_required(login_url='login')
def edit_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id, employee=request.user)
    if leave.status != 'Pending':
        return HttpResponse('You cannot edit this leave request.')
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_history')
    else:
        form = LeaveForm(instance=leave)
    return render(request, 'edit_leave.html', {'form': form})

from django.shortcuts import render
from .models import Leave

def manage_leaves(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')

    # Fetch only pending leave requests
    leaves = Leave.objects.filter(status='Pending')

    context = {
        'leaves': leaves,
    }
    return render(request, 'manage_leaves.html', context)

# from django.shortcuts import get_object_or_404, redirect
# from django.http import HttpResponse

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Leave
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def approve_leave(request, leave_id):
    if request.user.status != 'Manager':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Approved'
    leave.comments = request.POST.get('comments', '')
    leave.save()

    # Send email notification
    subject = 'Leave Request Approved'
    message = f'Your leave request from {leave.from_date} to {leave.to_date} has been approved.\n\nComments: {leave.comments}'
    recipient_email = leave.employee.email_address
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)

    return JsonResponse({'message': 'Leave approved', 'status': 'Approved'})

@login_required(login_url='login')
def reject_leave(request, leave_id):
    if request.user.status != 'Manager':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Rejected'
    leave.comments = request.POST.get('comments', '')
    leave.save()

    # Send email notification
    subject = 'Leave Request Rejected'
    message = f'Your leave request from {leave.from_date} to {leave.to_date} has been rejected.\n\nComments: {leave.comments}'
    recipient_email = leave.employee.email_address
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)

    return JsonResponse({'message': 'Leave rejected', 'status': 'Rejected'})



def export_leaves(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')

    # Get filter parameters from the request
    status_filter = request.GET.get('status')
    employee_filter = request.GET.get('employee')

    # Filter leaves based on the parameters
    leaves = Leave.objects.all()
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    if employee_filter:
        leaves = leaves.filter(employee_first_name_icontains=employee_filter)

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leaves.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Employee Name', 'Leave Reason', 'From Date', 'To Date', 'Place of Visit', 'Status'])

    for leave in leaves:
        writer.writerow([
            leave.employee.id,
            f"{leave.employee.first_name} {leave.employee.last_name}",
            leave.leave_reason,
            leave.from_date,
            leave.to_date,
            leave.place_of_visit,
            leave.status,
        ])

    return response

from openpyxl import Workbook
from django.http import HttpResponse

def export_leaves_excel(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')

    # Get filter parameters from the request
    status_filter = request.GET.get('status')
    employee_filter = request.GET.get('employee')

    # Filter leaves based on the parameters
    leaves = Leave.objects.all()
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    if employee_filter:
        leaves = leaves.filter(employee_first_name_icontains=employee_filter)

    # Create Excel workbook and worksheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Leaves'

    # Add headers
    headers = ['Employee ID', 'Employee Name', 'Leave Reason', 'From Date', 'To Date', 'Place of Visit', 'Status']
    worksheet.append(headers)

    # Add data rows
    for leave in leaves:
        worksheet.append([
            leave.employee.id,
            f"{leave.employee.first_name} {leave.employee.last_name}",
            leave.leave_reason,
            leave.from_date,
            leave.to_date,
            leave.place_of_visit,
            leave.status,
        ])

    # Create HTTP response with Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="leaves.xlsx"'
    workbook.save(response)

    return response


# from .models import Leave

def leave_calendar(request):
    leaves = Leave.objects.all()  # Show all leaves
    events = []
    for leave in leaves:
        if leave.status == 'Approved':
            color = '#28a745'  # Green for approved
        elif leave.status == 'Pending':
            color = '#ffc107'  # Yellow for pending
        else:
            color = '#dc3545'  # Red for rejected

        events.append({
            'title': f"{leave.employee.first_name} {leave.employee.last_name} - {leave.leave_reason}",
            'start': leave.from_date.isoformat(),
            'end': leave.to_date.isoformat(),
            'color': color,
        })
    return JsonResponse(events, safe=False)

from django.shortcuts import render, redirect
from .models import Attendance, Employee
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from django.utils import timezone

@login_required(login_url='login')
def mark_attendance(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    
    if request.method == 'POST':
        employee_id = request.POST['employee']
        date = request.POST['date']
        status = request.POST['status']
        
        employee = Employee.objects.get(id=employee_id)
        Attendance.objects.create(employee=employee, date=date, status=status)
        return HttpResponse('Attendance marked successfully')
    
    employees = Employee.objects.all()
    return render(request, 'mark_attendance.html', {'employees': employees})

@login_required(login_url='login')
def view_attendance(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    
    attendances = Attendance.objects.all()
    return render(request, 'view_attendance.html', {'attendances': attendances})

@login_required(login_url='login')
def employee_attendance(request):
    if request.user.status != 'Employee':
        return HttpResponse('You are not authorized to access this page.')
    
    attendances = Attendance.objects.filter(employee=request.user)
    total_slots = attendances.count()
    present_slots = attendances.filter(status='Present').count()
    absent_slots = attendances.filter(status='Absent').count()
    attendance_percentage = (present_slots / total_slots * 100) if total_slots > 0 else 0
    
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Status'])
        
        for attendance in attendances:
            writer.writerow([attendance.date, attendance.status])
        
        return response
    
    return render(request, 'employee_attendance.html', {
        'total_slots': total_slots,
        'present_slots': present_slots,
        'absent_slots': absent_slots,
        'attendance_percentage': attendance_percentage
    })


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def send_announcement(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect('manager_dashboard')
    else:
        form = AnnouncementForm()
    return render(request, 'send_announcement.html', {'form': form})


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def delete_announcement(request, announcement_id):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.delete()
    return redirect('manager_dashboard')


# from django.shortcuts import render

def chat_room(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import DailyUpdateForm
# from .models import DailyUpdate

@login_required(login_url='login')
def submit_daily_update(request):
    if request.method == 'POST':
        form = DailyUpdateForm(request.POST)
        if form.is_valid():
            daily_update = form.save(commit=False)
            daily_update.employee = request.user
            daily_update.save()
            return redirect('employee_dashboard')
    else:
        form = DailyUpdateForm()
    return render(request, 'submit_daily_update.html', {'form': form})


@login_required(login_url='login')
def view_employee_updates(request):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    employees = Employee.objects.all()
    return render(request, 'view_employee_updates.html', {'employees': employees})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyUpdateForm
from .models import DailyUpdate

@login_required(login_url='login')
def submit_daily_update(request):
    if request.method == 'POST':
        form = DailyUpdateForm(request.POST)
        if form.is_valid():
            daily_update = form.save(commit=False)
            daily_update.employee = request.user
            daily_update.save()
            return redirect('employee_dashboard')
    else:
        form = DailyUpdateForm()
    return render(request, 'submit_daily_update.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DailyUpdate, Employee

@login_required(login_url='login')
def employee_daily_updates(request, employee_id):
    if request.user.status != 'Manager':
        return HttpResponse('You are not authorized to access this page.')
    employee = get_object_or_404(Employee, id=employee_id)
    updates = DailyUpdate.objects.filter(employee=employee).order_by('-date')
    return render(request, 'employee_daily_updates.html', {'employee': employee, 'updates': updates})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid

@login_required(login_url='login')  # Ensure only logged-in users can access the meeting
def create_meet(request):
    """Generates a unique meeting ID and redirects to the meeting page."""
    meeting_id = str(uuid.uuid4())[:8]  # Generate a short random ID
    return redirect(f"/meet/{meeting_id}/")

@login_required(login_url='login')  # Ensure only logged-in users can access the meeting
def meet_page(request, meeting_id):
    """Renders the meeting page with Jitsi integration."""
    return render(request, "meet.html", {"meeting_id": meeting_id, "user": request.user})

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile_view(request):
    employee = request.user  # Get the logged-in user
    context = {
        'employee': employee
    }
    return render(request, 'profile.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee

from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee

from django.shortcuts import render
from .models import Employee

def remove_emp_list(request):
    employees = Employee.objects.all()  # Fetch all employees
    return render(request, 'remove_emp_list.html', {'employees': employees})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee  # Import your Employee model

def remove_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    employee.delete()
    return redirect('employee_list') 



from django.shortcuts import render
from .models import Employee

@login_required
def assign_salary(request):
    if not request.user.is_staff:  # Ensure only managers/admins can access
        return redirect('employee_dashboard')  # Redirect employees elsewhere
    employees = Employee.objects.all()
    print(employees)
    return render(request, 'assign_salary.html', {'employees': employees})

# emp_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Salary, Employee
from .forms import SalaryForm

@login_required
def salary_list(request):
    if not request.user.is_staff:  # Ensure only managers/admins can access
        return redirect('employee_dashboard')  # Redirect employees elsewhere
    salaries = Salary.objects.all()
    return render(request, 'salary_list.html', {'salaries': salaries})

# @login_required

def add_salary(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            salary.employee = employee
            salary.save()
            return redirect('salary_list')
    else:
        form = SalaryForm()
    return render(request, 'add_salary.html', {'form': form, 'employee': employee})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Salary, Employee

@login_required
def employee_salary(request):
    salary = Salary.objects.filter(employee=request.user).first()
    if not salary:
        # Handle the case where no salary record exists for the employee
        return render(request, 'employee_salary.html', {'salary': None})
    return render(request, 'employee_salary.html', {'salary': salary})

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Salary

@login_required
def download_salary_report(request):
    salary = Salary.objects.filter(employee=request.user).first()
    
    if not salary:
        return HttpResponse("No salary record found.", status=404)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salary_report.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Salary Report for {salary.employee.first_name}")
    p.drawString(100, 780, f"Basic Salary: {salary.basic_salary}")
    p.drawString(100, 760, f"Provident Fund (PF): {salary.pf}")
    p.drawString(100, 740, f"On-Hand Salary: {salary.on_hand_salary}")
    
    p.showPage()
    p.save()
    return response

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeEditForm

def is_manager(user):
    return user.is_authenticated and user.status == 'Manager'

@login_required
@user_passes_test(is_manager)
def edit_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('edit_employee_list')  # Redirect back to employee list after saving
    else:
        form = EmployeeEditForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee

def is_manager(user):
    return user.is_authenticated and user.status == 'Manager'  # Ensure this matches your model

@login_required
@user_passes_test(is_manager)
def edit_employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'edit_employee_list.html', {'employees': employees})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee

def is_manager(user):
    return user.is_authenticated and user.status == 'Manager'

@login_required
@user_passes_test(is_manager)
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        employee.delete()
        return redirect('edit_employee_list')  # Redirect back to employee list after deletion

    return render(request, 'emp_app/delete_employee.html', {'employee': employee})

@login_required
def profile_view(request):
    if request.user.status == "Manager":
        return render(request, "profile.html", {"user": request.user})
    else:
        return render(request, "employee_profile.html", {"user": request.user})
