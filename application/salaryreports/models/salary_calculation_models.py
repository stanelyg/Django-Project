import functools
from collections import OrderedDict
from decimal import Decimal
from itertools import groupby
from multiprocessing import Pool, cpu_count
import datetime

from attendance.get_report_data import get_employee_attendance_details,rounddown
from attendance.models import  get_working_dates
from dbmaster.models import period_dates, round_half_up
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from employees.models import (Employee)
from salaryreports.models import (NhifDetail,Nhif,Nssfreferencetable,Payetable)



def get_attendance_infor(year,month,employee):
    attendance_data=get_employee_attendance_details(employee.employee_no,year,month)
    attendance_data['employee_no']=attendance_data['employee_no']
    attendance_data['pin_no']=employee.pin_no
    attendance_data['national_id']=employee.national_id 
    attendance_data['hours_in_month']=employee.work_hours_code.hours_in_month 
    return attendance_data

def get_payment_report(employee_data,year,month):
    rows=OrderedDict()
    total_array={}
    employee_count_array={}
    group_list=[]
    partial_multi = functools.partial(get_pay_calculation,year,month)
    with Pool(processes=cpu_count()-1) as pool:
        multi_data = pool.map(partial_multi,employee_data)
    loc_dept_total_array = {}
    value_keys = {
        # 'working_days':'Working Days',
        # 'worked_days':'Worked Days', 
        # 'no_of_holidays':'Holidays', 
        # 'leaves': 'Leaves',
        'basic_salary':'Basic Salary',
        'housing_amount':'Housing Amount',
        'absent_days':'Absent Days',
        'absent_amount':'Absent Amount',
        'gross_salary':'Gross Salary',
        'taxable_amount':'Taxable Amount',
        'paye_amount':'Paye Amount',
        'insurance_relief':'Insurance Relief',
        'nssf_amount':'Nssf Amount',
        'nhif_amount':'Nhif Amount',
        'total_deduction':'Total Deduction',
        'net_salary':'Net Salary',

    }
    dept_head = []
    dept_foot = []
    temp_dept_empno = None
    temp_dept_empno_last = None
    loc_dept_single = True
    for pay_data in multi_data:
        rows[pay_data['employee_no']]=pay_data
        total_array = get_total_payment(pay_data,value_keys,total_array)    
    return_data={}
    return_data['dept_employee_count'] = employee_count_array
    return_data['totals'] = dict(total_array)
    return_data['value_keys'] = value_keys      
    return {'rows':rows,'return_data':return_data}
def get_total_payment(pay_data,value_keys,total_array):
    for key in value_keys:
        if key in pay_data:
            if key in total_array:
                if pay_data[key]:
                    total_array[key] = Decimal(total_array[key])+ Decimal(pay_data[key])
            else:
                total_array.update({key:pay_data[key]})
    return total_array

def get_pay_calculation(year,month,employee):
    net_infor =pay_formular(year,month,employee)    
    return net_infor

def pay_formular(year,month,employee):    
    full_array={}
    employee_no=employee.employee_no
    salary_dates=period_dates(year,month)
    from_date=period_dates(year,month)['from_date']
    to_date=period_dates(year,month)['to_date']  
    attendance_data=get_attendance_infor(year, month,employee)
    full_array=attendance_data
    #for the purpose of simple closing of the salay
    full_array['year']=year
    full_array['month']=month
    full_array['basic_daily_rate']=round_half_up(attendance_data['basic_salary']/attendance_data['working_days'],2)
    # full_array['hourly_rate']=round_half_up(attendance_data['basic_salary']/attendance_data['hours_in_month'],2)
    house_mount=get_housing_amount(employee_no,attendance_data['basic_salary'],attendance_data['house_allowance_rate'])
    full_array['housing_amount']=house_mount['housing_amount']  
    full_array['gross_daily_rate']=round_half_up((attendance_data['basic_salary']+ Decimal(house_mount['housing_amount']))/attendance_data['working_days'],2)    
    full_array['absent_amount']=get_absent_amount(full_array['gross_daily_rate'],attendance_data['absent_days'])
    full_array['tax_excemption']=0
    full_array['arrears_amount']=0
    full_array['notice_pay_amount']=0
    full_array['notice_recovery_amount']=0
    full_array['severance_amount']=0
    full_array['directors_fee']=0
    full_array['leave_encashed_days']=0
    full_array['leave_encashed_amount']=0

    
    
    gross_salary_value=round_half_up(
                                    attendance_data['basic_salary']
                                    + Decimal(full_array['housing_amount'])
                                    - Decimal(full_array['absent_amount']),0)

    full_array['gross_salary']=(gross_salary_value,0) [gross_salary_value<2]
    taxable_array={ 
            'tax_excemption':Decimal(full_array['tax_excemption']),
    }
    statutory_data=statutory_master(employee,year,month,full_array['gross_salary'],taxable_array)    
    full_array['statutory_data']=statutory_data
    #to replaced by statutory_master
    nssf_array=statutory_data['nssf_array']
    full_array['nssf_amount']=nssf_array['nssf_amount']
    full_array['employee_contribution']=nssf_array['employee_contribution']
        #to replaced by statutory_master
    full_array['nhif_amount']=statutory_data['nhif_amount']

    full_array['taxable_amount']=Decimal(round_half_up(
                        Decimal(full_array['gross_salary'])
                    - Decimal(full_array['nssf_amount']),0))
    #to replaced by statutory_master
    paye_array=statutory_data['paye_array']
    full_array['insurance_relief']=get_insurance_policy_relief(employee_no,year,month,statutory_data['nhif_amount'])
    #effected in the month of march -(Decimal(full_array['over_time_one_amount']) + Decimal(full_array['over_time_two_amount']) +  Decimal(full_array['bonus_amount']))
    negate_overtime_bonus=Decimal(full_array['taxable_amount'])
    if paye_array['paye_first_bracket_max'] > negate_overtime_bonus:
        full_array['tax_amount']=paye_array['tax_amount']
        full_array['paye_amount']=0
        full_array['relief_amount']=paye_array['relief_amount']
    else:
        full_array['tax_amount']=paye_array['tax_amount']
        full_array['paye_amount']=paye_array['paye_amount']
        full_array['paye_amount']-=Decimal(full_array['insurance_relief'])
        full_array['relief_amount']=paye_array['relief_amount']
    full_array['total_deduction']=round_half_up(
                            Decimal(full_array['paye_amount'])
                        + Decimal(full_array['nhif_amount'])
                        + Decimal(full_array['nssf_amount'])                      
                        ,0)
    full_array['net_salary']=Decimal(full_array['gross_salary'])- Decimal(full_array['total_deduction'])
    return full_array




def get_housing_amount(employee_no,basic_salary,house_allowance_rate):
    return_array={}
    return_array['housing_amount']=0
    return_array['housing_amount']+=round_half_up(basic_salary*(house_allowance_rate/100),2)

    return return_array


def get_ot1_amount(hourly_rate,ot1_hours,factor):
    return round(Decimal(hourly_rate)* Decimal(ot1_hours)*factor,2)

def get_ot2_amount(hourly_rate,ot2_hours,factor):
    return round(Decimal(hourly_rate)*Decimal(ot2_hours)* factor,2)

def get_absent_amount(daily_rate,absent_days):
    return Decimal(round_half_up(Decimal(daily_rate) * Decimal(absent_days),0))


def get_employee_rates(employee_no,basic_salary,house_allowance_rate,from_date,to_date):
      rates_details={}
      housing_array=get_housing_amount(employee_no,basic_salary,house_allowance_rate)
      working_days=get_working_dates(from_date,to_date,employee_no)
      rates_details['gross_daily_rate']=Decimal(round_half_up((basic_salary+Decimal(housing_array['housing_amount']))/len(working_days['workingdays']),2))
      rates_details['basic_daily_rate']=Decimal(round_half_up(basic_salary/len(working_days['workingdays']),2))
      rates_details['hourly_rate']=Decimal(round_half_up((rates_details['gross_daily_rate']/8),2))
      return rates_details

def get_insurance_policy_relief(employee_no,year,month,nhif_amount):
            paye_relief_amount=0
            from_date=period_dates(year,month)['from_date']
            to_date=period_dates(year,month)['to_date']
            from_date=datetime.datetime.strftime(from_date,'%Y-%m-%d')
            # Add NHIF to Relief
            nhif_queryset=Nhif.objects.filter(effective_date__lte=from_date).all().order_by('-effective_date')
            if nhif_queryset:
                  nhif_relief=nhif_queryset[0]
                  paye_relief_amount=rounddown(nhif_amount*nhif_relief.paye_relief_percentage/100,1)
            return paye_relief_amount


def statutory_master(employee,year,month,gross_salary,taxable_array):
    return_array={}
    taxable_amount=0
    from_date=period_dates(year,month)['from_date']
    to_date=period_dates(year,month)['to_date']
    nssf_array=Nssfreferencetable.get_nssf_amount(gross_salary,from_date)
    return_array['nhif_amount']=NhifDetail.get_nhif_amount(gross_salary,from_date)
    taxable_amount=Decimal(round_half_up(
                        Decimal(gross_salary)
                        - Decimal(nssf_array['nssf_amount'])
    ))
    paye_array=Payetable.get_paye_amount(taxable_amount,from_date)
    paye_array['paye_amount']=Decimal(paye_array['paye_amount'])
    return_array['nssf_array']=nssf_array
    return_array['paye_array']=paye_array
    return return_array


 


