from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.list import ListView
from salaryreports.forms import StatutoryReportForm
from salaryreports.models import get_pay_calculation
from collections import OrderedDict
from multiprocessing import Pool, cpu_count,Manager
import functools
from decimal import Decimal

from employees.models import Employee
from dbmaster.models import SalaryPeriod,Company,period_dates



def get_statutory_report(year,month,permanent,casual):
    nhif_data = OrderedDict()
    nssf_data = OrderedDict()
    nhif_total = 0
    total_income = 0
    nssf_total_member = 0
    nssf_total_employer = 0
    casual_employees=0
    permanent_employees=0
    permanent_salary_data={}
    casuals_salary_data={}
    for employee in permanent:
        data=get_statutory_mult_data(year,month,employee)
        if data['nssf_data']['member_nssf_amount']>0:
            permanent_employees+=1
            nssf_data[str(data['nssf_data']['employee_no'])+'p']=data['nssf_data']
            permanent_salary_data.update({data['nssf_data']['employee_no']:data['permanent_salary_data']})
            nssf_total_member += Decimal(data['nssf_data']['member_nssf_amount'])
            nssf_total_employer += Decimal(data['nssf_data']['employer_nssf_amount'])
            total_income += Decimal(data['nssf_data']['gross_salary'])
            #nhif-data
            nhif_data[str(data['nhif_data']['employee_no'])+'p'] =data['nhif_data']
            nhif_total += Decimal(data['nhif_data']['nhif_amount'])
    return_arry={
        'nhif_data':nhif_data,
        'nssf_data':nssf_data,
        'nhif_total':nhif_total,
        'total_income':total_income,
        'nssf_total_member':nssf_total_member,
        'nssf_total_employer':nssf_total_employer,
        'permanent_employees':permanent_employees,
        'casual_employees':casual_employees,
        'total_no_of_employee':permanent_employees+casual_employees,
        'permanent_salary_data':permanent_salary_data,
        'casual_salary_data':casuals_salary_data
        }

    return return_arry

def get_statutory_mult_data(year, month,employee):
            return_data = get_pay_calculation(year, month, employee)    
            nhif_data = {
                    'employee_no':return_data['employee_no'],                   
                    'first_name':return_data['first_name'],
                    'other_name':return_data['other_name'],
                    'national_id':employee.national_id,
                    'nhif_no':employee.nhif_no,
                    'nhif_amount':Decimal(return_data['nhif_amount'])
            }
            nssf_data= {
                    'employee_no':return_data['employee_no'],                   
                    'first_name':return_data['first_name'],
                    'other_name':return_data['other_name'],
                    'national_id':employee.national_id,
                    'pin_no':employee.pin_no,
                    'nssf_no':employee.nssf_no,
                    'member_nssf_amount':Decimal(return_data['nssf_amount']),
                    'employer_nssf_amount':round(Decimal(return_data['nssf_amount'])),
                    'gross_salary':Decimal(return_data['gross_salary']),
                    'total_contribution':Decimal(return_data['nssf_amount']) + Decimal(return_data['nssf_amount']) * Decimal(return_data['employee_contribution']),
                    'paye_amount':Decimal(return_data['paye_amount']),
                    'nita_deduction':0
            }
            return_data['nssf_amount']=nssf_data['member_nssf_amount']
            return_data['paye_amount']=nssf_data['paye_amount']
            return  {'nssf_data':nssf_data,'nhif_data':nhif_data,'permanent_salary_data':return_data}


