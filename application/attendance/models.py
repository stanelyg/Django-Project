import datetime
from datetime import date, timedelta
from decimal import Decimal
from dbmaster.models import (WorkingHour,HolidayDetail)
from django.db import models
from django.db.models import Q
from employees.models import Employee

class Attendance(models.Model):    
    year=models.CharField(max_length=4)
    month=models.CharField(max_length=2)
class AttendanceDetail(models.Model):
    employee_name=models.CharField('EmpName',max_length=100)  
    days=models.DecimalField('Total Hours',max_digits=3,decimal_places=1,null=True,default=0)
    leaves=models.DecimalField('Leaves',max_digits=3,decimal_places=1,null=True,default=0)
    employee_no=models.ForeignKey(Employee,on_delete=models.PROTECT)
    attendance=models.ForeignKey('Attendance',on_delete=models.PROTECT)
  


def get_all_date(from_date,to_date):
    date_array=[]
    from_date=datetime.datetime.strptime(str(from_date),'%Y-%m-%d')
    to_date =datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    ''' Create date'''
    start_date = date(from_date.year,from_date.month,from_date.day)
    end_date = date(to_date.year,to_date.month,to_date.day)
    delta = end_date - start_date
    for i in range(delta.days + 1):
        dates = start_date + timedelta(days=i)
        date_array.append(dates)
    return date_array

def get_working_dates(from_date,to_date,emp_id):
    emp_details=Employee.objects.filter(employee_no=emp_id).values('work_hours_code')
    all_dates =get_all_date(from_date,to_date)
    holidays =get_public_holidays(from_date,to_date)
    date_hours=get_date_hours(all_dates,holidays,emp_details[0]['work_hours_code'])
    datestatus=get_date_status(date_hours)
    return datestatus
def get_date_hours(all_dates,holiday_dates,workhrscode):
    dateshrs={}
    for dat in all_dates:
        dateshrs[dat]=Decimal(WorkingHour.objects.filter(id=workhrscode).values()[0][str.lower(dat.strftime('%a'))])
    for dat in holiday_dates:
        dateshrs[dat]=0
    return dateshrs
def get_date_status(datehrs):
    datearr={}
    datewklist=[]
    daterdlist=[]
    for key ,hours in datehrs.items():
        if hours and int(hours) > 0:
           datewklist.append(key)
           datearr['workingdays']=datewklist
        else:
           daterdlist.append(key)
           datearr['restingdays']=daterdlist
    return datearr

def get_public_holidays(from_date,to_date):
    pholiday_array=[]
    queryset=HolidayDetail.objects.filter(holiday_date__range=[from_date,to_date]).order_by('holiday_date')
    for holiday in queryset:
        pholiday_array.append(holiday.holiday_date)
    return pholiday_array
  
