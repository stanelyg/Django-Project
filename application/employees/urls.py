from django.urls import include, path
from . import  views
from employees.views import EmployeeCreateView

app_name="employees"
urlpatterns = [
     path('employee-create/',EmployeeCreateView.as_view(),name='employee-create'),
    
    
]