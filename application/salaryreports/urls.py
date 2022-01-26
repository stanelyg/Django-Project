from django.urls import include, path
from . import views
from salaryreports.views import  MonthlyReportView
app_name="salaryreports"
urlpatterns = [
    path('monthly-salary-report',MonthlyReportView.as_view(),name='monthly-salary-report'),
    #  path('employee-create/',EmployeeCreateView.as_view(),name='employee-create'),
    #  path('<int:pk>/update',EmployeeUpdateView.as_view(),name='employee-details'),
    #  path('nav-employees/',views.navigate_form,name='nav-employees'),
    #  path('get_form/',views.get_form, name='get_form'),
    #  path('json/emps-autocomplete/',get_employees, name='emps-autocomplete'),    
    
]