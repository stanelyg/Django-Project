import datetime

from dbmaster.models import (SalaryPeriod, check_open_month,
                             get_post_array, period_dates)
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from decimal import Decimal
from django.shortcuts import render
from django.views.generic.list import ListView
from employees.models import Employee
from dbmaster.models import Company,round_half_up
from salaryreports.forms import MonthlyReportForm,StatutoryReportForm,ItaxReportForm,PayslipForm
from salaryreports.models import (get_pay_calculation,get_payment_report,get_statutory_report)


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

class StatutoryReportView(LoginRequiredMixin,ListView):
    form_class = StatutoryReportForm
    template_name = 'nssf_nhif_report.html'
    def get_initial(self):
        initial_base = {}
        initial_base['year']=(datetime.datetime.now().year ,self.request.GET.get('year'))[self.request.GET.get('year') is not None]
        initial_base['month']=(datetime.datetime.now().month,self.request.GET.get('month')) [self.request.GET.get('month') is not None]
        return initial_base

    def get_queryset(self):
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        if year and month:
            queryset =Employee.objects.filter(Q(date_of_leaving__isnull=True) | Q(date_of_leaving__range=[period_dates(year, month)['from_date'],period_dates(year, month)['to_date']])| Q(date_of_leaving__gte=period_dates(year, month)['from_date'])).all()
        else:
            queryset = Employee.objects.none()
        form = self.form_class(initial=(self.get_initial()))
        statutories_report_data = {}
        statutories_report_data['form'] = form
        casual_queryset=''
        if queryset:
            return_array=get_statutory_report(year,month,queryset,casual_queryset)
            statutories_report_data['nhif_table'] = return_array['nhif_data']
            statutories_report_data['nhif_total'] = return_array['nhif_total']
            statutories_report_data['nssf_table'] = return_array['nssf_data']
            statutories_report_data['total_income'] = return_array['total_income']
            statutories_report_data['nssf_total_member'] =return_array['nssf_total_member']
            statutories_report_data['nssf_total_employer'] =return_array['nssf_total_employer']
            statutories_report_data['nssf_total_records'] = len(return_array['nssf_data'])
            statutories_report_data['nssf_grand_total'] = Decimal(return_array['nssf_total_employer']) +  Decimal(return_array['nssf_total_member'])
        if Company.get_company_details():
            statutories_report_data['company_name'] = Company.get_company_details()['name']
            statutories_report_data['company_code'] = Company.get_company_details()['nhif_no']
            statutories_report_data['company_pin'] = Company.get_company_details()['pin_no']
            statutories_report_data['company_nssf_no'] = Company.get_company_details()['nssf_no']
        else:
            statutories_report_data['company_name'] = 'Update Company Details'
            statutories_report_data['company_code'] = 'Update Company Details'
            statutories_report_data['company_pin'] = 'Update Company Details'
            statutories_report_data['company_nssf_no'] = 'Update Company Details'
        statutories_report_data['contribution_month'] = month
        statutories_report_data['contribution_year'] = year
        return statutories_report_data
class ItaxReportView(LoginRequiredMixin,ListView):
    form_class = ItaxReportForm
    template_name = 'itax_report.html'
    def get_initial(self):
        initial_base = {}
        initial_base['year']=(datetime.datetime.now().year ,self.request.GET.get('year'))[self.request.GET.get('year') is not None]
        initial_base['month']=(datetime.datetime.now().month,self.request.GET.get('month')) [self.request.GET.get('month') is not None]
        return initial_base
    def get_queryset(self):
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        itax_report_data={}
        form = self.form_class(initial=(self.get_initial()))
        itax_report_data['form'] = form
        if year and month:
            period=period_dates(year,month)
        return_arry={}
        total_paye_amount=0
        if year and month:
            queryset =Employee.objects.filter(Q(date_of_leaving__isnull=True) | Q(date_of_leaving__range=[period_dates(year, month)['from_date'],period_dates(year, month)['to_date']])| Q(date_of_leaving__gte=period_dates(year, month)['from_date'])).all()
        else:
            queryset = Employee.objects.none()
        casual_queryset=''
        salary_data=get_statutory_report(year,month,queryset,casual_queryset)
        for key ,values in salary_data['permanent_salary_data'].items():
            total_paye_amount+=values['paye_amount']
            if key not in return_arry:
                temp_other_all_amt =-Decimal(values['absent_amount']) + Decimal(values['arrears_amount']) + Decimal(values['notice_pay_amount']) - Decimal(values['notice_recovery_amount']) + Decimal(values['severance_amount']) + Decimal(values['directors_fee'])
                temp_gross_not_rounded = Decimal(values['basic_salary']) + Decimal(values['housing_amount']) + Decimal(temp_other_all_amt)
                temp_rounding=Decimal(temp_gross_not_rounded) - Decimal(round_half_up(temp_gross_not_rounded,0))
                return_arry[str(key)+'p']={
                'pin_no':values['pin_no'],
                'employee_name':values['employee_name'],
                'type_of_employee':'Primary Employee',
                'basic_salary':values['basic_salary'],
                'housing_amount':values['housing_amount'],
                'directors_fee':values['directors_fee'],
                'leave_encashed_amount':values['leave_encashed_amount'],
                'over_time_allowance':0,
                'other_allowance':0 + (temp_other_all_amt-temp_rounding),
                'vehicle_benefit':0,
                'other_benefit_amount':0,
                'house_quota':0,
                'nssf_amount':Decimal(values['nssf_amount']),
                'rent_recovered':(values['basic_salary']*(values['house_allowance_rate']/100)),
                'permissible_limit':'',
                'mortgage_interest':0,
                'paye_relief':values['relief_amount'],
                'paye_amount':values['paye_amount'],
                'insurance_relief':values['insurance_relief'],
                }
        itax_report_data['table']=return_arry
        itax_report_data['paye_total']=total_paye_amount
        return itax_report_data

class EmployeePaySlipView(LoginRequiredMixin,ListView):
        form_class=PayslipForm
        template_name ='payslips/employee_pay_slip_form.html'
        def get(self, request,**kwargs):
                form = self.form_class(initial=self.get_initial())
                return render(request,self.template_name, {'form': form})
        def get_initial(self):
                initial_base={}
                initial_base['year']=(datetime.datetime.now().year ,self.request.GET.get('year'))[self.request.GET.get('year') is not None]
                initial_base['month']=(datetime.datetime.now().month,self.request.GET.get('month')) [self.request.GET.get('month') is not None]
                return initial_base
            
def get_print_preview(request):
    form=PayslipForm()
    template_name ='payslips/employee_pay_slip_form.html'
    context = {"form": form}
    if request.POST:
        initial_base={}
        initial_base['year']=request.POST.get('year')
        initial_base['month']=request.POST.get('month') 
        form =PayslipForm(initial=initial_base)
        year = request.POST.get('year')
        month = request.POST.get('month')
        period=period_dates(year,month)
        if year and month:
            queryset =Employee.objects.filter(Q(date_of_leaving__isnull=True)|Q(date_of_leaving__range=[period['from_date'],period['to_date']])|Q(date_of_leaving__gte=period['from_date']),date_of_joining__lte=period['to_date']).all().order_by('first_name')
        else:
                queryset =Employee.objects.none()
        context = {"form": form}
        earnings_array={}
        deductions_array={}
        extra_advances={}
        per_page_array={}
        final_array={}
        data_count=0         
        if queryset:
            for employee in queryset:
                data_count=data_count+1
                for x in range(1,3):
                    per_page_array.update({str(employee.employee_no)+''+str(x):get_pay_calculation(year=year,month=month,employee=employee)})
                final_array.update({data_count:per_page_array})
                per_page_array={}
            context['year']=year
            context['month']=datetime.date(1900, int(month), 1).strftime('%B')
            context['data']=final_array       
            context['type']=1               
    return render(request, template_name, context)
        
        
        
        



