import datetime
import functools
import math
from collections import OrderedDict
from decimal import Decimal
from multiprocessing import Pool, cpu_count
from dbmaster.models import SalaryPeriod, WorkingHour,period_dates
from django.db.models import Min, Sum
from employees.models import Employee

from attendance.models import (Attendance, AttendanceDetail,get_all_date, get_date_hours, get_date_status,
                               get_public_holidays)


def get_daily_data(emp_no,year,month):
    salary_dates=period_dates(year,month)
    from_date=salary_dates['from_date']
    to_date=salary_dates['to_date']
    attendance_array={}
    attendance_array['leaves']=0
    attendance_array['worked_days']=0
    attendance_array['no_of_holidays']=0
    attendance_array['total_hours_worked']=0    
    emp_data=Employee.objects.filter(employee_no=emp_no).all()
    emp_details=emp_data[0]
    attendance_array['emp_details']=emp_data
    all_dates=get_all_date(from_date,to_date)
    holidays=get_public_holidays(from_date,to_date)
    all_dates_hours=get_date_hours(all_dates,holidays,emp_details.work_hours_code_id)
    dates_status=get_date_status(all_dates_hours)
    holiday_dates=[]
    
    for dates in holidays:
            holiday_dates.append(dates)
    
    attendance_array['all_dates_hours']=all_dates_hours
    attendance_array['all_dates']=all_dates
    attendance_array['holiday']=holiday_dates
    
    if 'workingdays' in dates_status:
        attendance_array['working_days']=dates_status['workingdays']
    else:
        attendance_array['working_days']=[]
    attendance_array['attendance_details']=get_attendance_query(emp_no,year,month)
    return attendance_array

def get_attendance_query(employee_no,year,month):
    attendance_array={}
    attndetails=AttendanceDetail.objects.filter(attendance__year=year,attendance__month=month,employee_no=employee_no,days__gte=0.0).values('attendance__year','attendance__month').annotate(leaves=Sum('leaves'),days=Sum('days'))
    for detail in attndetails:
        attendance_array[detail['attendance__year']+detail['attendance__month']]=detail
    return attendance_array


def get_employee_attendance_details(employee_no,year,month):
    rows = {}
    rows['worked_days']=0
    rows['no_of_holidays']=0
    rows['leaves']=0
    rows['absent_days']=0
    data=get_daily_data(employee_no,year,month)
    # print(data)
    rows['working_days']=len(data['working_days'])
    for row in data['emp_details']:
        rows['employee_no']=row.employee_no
        rows['employee_name']=row.employee_name
        rows['national_id']=row.national_id      
        rows['basic_salary']=row.basic_salary
        if data['attendance_details']:
                rows['leaves']+=data['attendance_details'][str(year)+str(month)]["leaves"]
                rows['worked_days'] +=Decimal(data['attendance_details'][str(year)+str(month)]["days"])
                rows['absent_days'] =rows['working_days']- (Decimal(rows['leaves'])+ Decimal(rows['worked_days']))                            
                if data['holiday']:
                    rows['no_of_holidays']+=len(data['holiday'])
        else:
            if data['holiday']:
                    rows['no_of_holidays']+=len(data['holiday'])
            rows['absent_days'] =rows['working_days']- (Decimal(rows['leaves'])+ Decimal(rows['worked_days']))  
    return rows


def get_monthly_report(employee_data,year,month):   
    attendance_totals={}
    attendance_data = OrderedDict()
    attendance_totals['sum_paid_leaves']=0
    attendance_totals['sum_worked_days']=0
    attendance_totals['dict_length']=0
    attendance_totals['sum_holidays']=0
    attendance_totals['sum_absent_days']=0

    partial_multi = functools.partial(get_monthly_data_multi, year, month)
    with Pool(processes=cpu_count()-1) as pool:
        multi_data = pool.map(partial_multi, employee_data)
    for data in multi_data:
        attendance_data[data['employee_no']] =data
        attendance_totals['sum_paid_leaves']+=Decimal(data['leaves'])
        attendance_totals['sum_worked_days']+=Decimal(data['worked_days'])
        attendance_totals['sum_holidays']+=Decimal(data['no_of_holidays'])
        attendance_totals['sum_absent_days']+=Decimal(data['absent_days'])
    return {'rows':attendance_data,'totals':attendance_totals}

def get_monthly_data_multi(year, month,employee):   
    attendance_data=get_employee_attendance_details(employee.employee_no,year,month)
    return attendance_data
def rounddown(value,nearrest):
    	return math.floor(Decimal(value)/Decimal(nearrest))*nearrest;

def round_leave(value,factor):
    return round(Decimal(value)/Decimal(factor))*factor
