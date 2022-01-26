from django.urls import include, path
from employees.models import get_employees,get_emp_details

from attendance.views import (AttendanceCreateView, AttendanceUpdateView,
                              copy_attendance, navigate_attendance,
                              search_attendance,MonthlyReportView,get_report_data)

from . import views

app_name="attendance"
urlpatterns = [
    path('attendance-create/', AttendanceCreateView.as_view(), name = 'attendance-create'),
    path('<int:pk>/update',AttendanceUpdateView.as_view(),name='attendance-details'),
    path('nav-attendance/',views.navigate_attendance,name='nav-attendance'),
    path('search-attendance',views.search_attendance,name='search-attendance'),
    path('copy-attendance',views.copy_attendance,name='copy-attendance'),
    
    path('monthly-report',MonthlyReportView.as_view(),name='monthly-report'),
    path('attendance-data',views.get_report_data,name='attendance-data'),

        
    path('json/emps-autocomplete/',get_employees, name='emps-autocomplete'),
    path('json/emps-details/',get_emp_details, name='emps-details'),
]
