from django.shortcuts import render, redirect
from django.shortcuts import render
from login.models import Student
from login.forms import StudentForm
from .models import AttendanceLog
from django.db.models import Q
from datetime import datetime
from django.db import connections
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import csv
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import mysql.connector

# Admin Dashboard View
def admin_dashboard(request):
    students = Student.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'students': students})

# Student Management with Filters
def student_management(request):
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date', '')  
    section_filter = request.GET.get('section', '')  

    queryset = AttendanceLog.objects.using('iot_db').all()

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            queryset = queryset.filter(date__date=date_obj.date())  
        except ValueError:
            pass  

    if section_filter:
        queryset = queryset.filter(section=section_filter)  

    sections = AttendanceLog.objects.using('iot_db').values_list('section', flat=True).distinct()

    if 'clear' in request.GET:
        return render(request, 'admin_panel/student_management.html', {
            'students': AttendanceLog.objects.using('iot_db').all(),
            'sections': sections,
        })

    return render(request, 'admin_panel/student_management.html', {
        'students': queryset,
        'sections': sections,
    })

# Add Student View
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_management')
    else:
        form = StudentForm()
    return render(request, 'admin_panel/add_student.html', {'form': form})

# Statistics View
def statistics(request):
    with connections['iot_db'].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM attendance_logs")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM attendance_logs WHERE gender = 'Male'")
        male = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM attendance_logs WHERE gender = 'Female'")
        female = cursor.fetchone()[0]

        context = {
            'total_students': total,
            'male_students': male,
            'female_students': female,
        }

    return render(request, 'admin_panel/statistics.html', context)

# Reports View with Filter + Export
def reports(request):
    section = request.GET.get('section', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    export_format = request.GET.get('export', '')

    query = "SELECT * FROM attendance_logs WHERE 1=1"
    params = []

    if section:
        query += " AND section = %s"
        params.append(section)
    if start_date:
        query += " AND DATE(time_of_entry) >= %s"
        params.append(start_date)
    if end_date:
        query += " AND DATE(time_of_entry) <= %s"
        params.append(end_date)

    with connections['iot_db'].cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        logs = [dict(zip(columns, row)) for row in rows]

    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['S.N.', 'Name', 'Student ID', 'Section', 'Gender', 'Time of Entry'])
        for i, log in enumerate(logs, start=1):
            time_str = log['time_of_entry'].strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                i,
                log['name'],
                f"'{log['student_id']}",  # Preserve leading zeros
                log['section'],
                log['gender'],
                time_str
            ])
        return response

    elif export_format == 'pdf':
        template = get_template("admin_panel/reports_pdf_template.html")
        html = template.render({"data": logs})
        result = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'
        return response

    return render(request, "admin_panel/reports.html", {
        "data": logs,
        "selected_section": section,
        "start_date": start_date,
        "end_date": end_date,
    })



def attendance_management(request):
    return render(request, 'admin_panel/attendance_management.html')

@csrf_exempt
def update_student_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")

            if not student_id:
                return JsonResponse({"status": "error", "message": "Student ID is required"}, status=400)

            conn = mysql.connector.connect(
                host="192.168.1.85",
                user="attendance_user",
                password="Kushal_01",
                database="attendance_system"
            )
            cursor = conn.cursor()

            fields = []
            values = []

            for field in ["phone", "email", "father_name", "mother_name", "enrollment_date"]:
                if data.get(field):
                    fields.append(f"{field} = %s")
                    values.append(data[field])

            if fields:
                update_query = f"UPDATE students SET {', '.join(fields)} WHERE student_id = %s"
                values.append(student_id)
                cursor.execute(update_query, values)
                conn.commit()

                return JsonResponse({"status": "success", "message": "Student details updated successfully"})
            else:
                return JsonResponse({"status": "info", "message": "No fields provided to update"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
