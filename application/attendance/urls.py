from django.urls import include, path
from employees.models import get_employees,get_emp_details

from attendance.views import (AttendanceCreateView, AttendanceUpdateView,
                              copy_attendance, navigate_attendance,
                              search_attendance)

from . import views

app_name="attendance"
urlpatterns = [
    path('attendance-create/', AttendanceCreateView.as_view(), name = 'attendance-create'),
    path('<int:pk>/update',AttendanceUpdateView.as_view(),name='attendance-details'),
    path('nav-attendance/',views.navigate_attendance,name='nav-attendance'),
    path('search-attendance',views.search_attendance,name='search-attendance'),
    path('copy-attendance',views.copy_attendance,name='copy-attendance'),
        
    path('json/emps-autocomplete/',get_employees, name='emps-autocomplete'),
    path('json/emps-details/',get_emp_details, name='emps-details'),
]
