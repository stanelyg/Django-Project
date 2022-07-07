from django.urls import include, path
from . import views
from salaryreports.views import  MonthlyReportView,StatutoryReportView,ItaxReportView,EmployeePaySlipView,get_print_preview
app_name="salaryreports"
urlpatterns = [
    path('monthly-salary-report',MonthlyReportView.as_view(),name='monthly-salary-report'),
    path('nssf-nhif-report',StatutoryReportView.as_view(),name='nssf-nhif-report'),
    path('itax-report',ItaxReportView.as_view(),name="itax-report"),       
    path('payslip-print',EmployeePaySlipView.as_view(),name="payslip-print"),
    path('payslip-print-preview',get_print_preview,name="payslip-print-preview"),
    
]