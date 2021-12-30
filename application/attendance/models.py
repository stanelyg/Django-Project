import datetime
from datetime import date, timedelta
from decimal import Decimal
from dbmaster.models import (WorkingHour)
from django.db import models
from django.db.models import Q
from employees.models import Employee

class Attendance(models.Model):    
    year=models.CharField(max_length=4)
    month=models.CharField(max_length=2)
class AttendanceDetail(models.Model):
    employee_name=models.CharField('EmpName',max_length=100)  
    days=models.DecimalField('Total Hours',max_digits=3,decimal_places=1,null=True,default=0)
    employee_no=models.ForeignKey(Employee,on_delete=models.PROTECT)
    attendance=models.ForeignKey('Attendance',on_delete=models.PROTECT)
  
