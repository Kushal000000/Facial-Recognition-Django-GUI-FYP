from django.urls import path
from . import views
from .views import update_student_details

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-management/', views.student_management, name='student_management'),
    path('attendance-management/', views.attendance_management, name='attendance_management'),
    path('add-student/', views.add_student, name='add_student'),
    path('statistics/', views.statistics, name='statistics'),
    path('reports/', views.reports, name='reports'),
    path("update_student_details/", update_student_details, name="update_student_details"),
    
]
