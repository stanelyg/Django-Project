import datetime

from dbmaster.models import (SalaryPeriod, check_open_month,
                             get_post_array, period_dates)
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from employees.models import Employee
from salaryreports.forms import MonthlyReportForm
from salaryreports.models import (get_pay_calculation,get_payment_report)


class MonthlyReportView(LoginRequiredMixin,ListView):
      form_class=MonthlyReportForm     
      template_name ='monthly_salary_report.html'
      def get_initial(self):
            initial_base={}
            initial_base['year']=(datetime.datetime.now().year ,self.request.GET.get('year'))[self.request.GET.get('year') is not None]
            initial_base['month']=(datetime.datetime.now().month,self.request.GET.get('month')) [self.request.GET.get('month') is not None]          
            return initial_base
      def get_queryset(self):
            year = self.request.GET.get('year')
            month = self.request.GET.get('month')
                   
            if year and month:
                period=period_dates(year,month) 
                queryset =Employee.objects.filter(Q(date_of_leaving__isnull=True)|Q(date_of_leaving__range=[period['from_date'],period['to_date']])|Q(date_of_leaving__gte=period['from_date']),date_of_joining__lte=period['to_date']).all()
            else:
                queryset =Employee.objects.none()
            form = self.form_class(initial=self.get_initial())
            data_array={}
            salary_data={}
            salary_data['form']=form
            if queryset:
               return_data=get_payment_report(queryset,year,month)
               salary_data['table']=return_data['rows']
               salary_data['return_data']=return_data['return_data']
            return salary_data





