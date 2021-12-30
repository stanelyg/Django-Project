from django.urls import include, path
from employees.models import get_employees

from employees.views import (EmployeeCreateView, EmployeeUpdateView, get_form,
                             navigate_form)

from . import views

app_name="employees"
urlpatterns = [
     path('employee-create/',EmployeeCreateView.as_view(),name='employee-create'),
     path('<int:pk>/update',EmployeeUpdateView.as_view(),name='employee-details'),
     path('nav-employees/',views.navigate_form,name='nav-employees'),
     path('get_form/',views.get_form, name='get_form'),
     path('json/emps-autocomplete/',get_employees, name='emps-autocomplete'),    
    
]
