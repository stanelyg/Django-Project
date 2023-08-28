from django.db import models

import datetime
import os
import json
from decimal import Decimal

from dbmaster.models import (WorkingHour,get_post_array)
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.urls import reverse

class Employee(models.Model):
      employee_no=models.AutoField(primary_key=True)
      first_name=models.CharField(max_length=100) 
      other_name=models.CharField(max_length=100)      
      national_id=models.CharField(max_length=11)      
      date_of_joining=models.DateField()
      date_of_leaving=models.DateField(blank=True,null=True)
      is_active=models.BooleanField(blank=True,null=True,default=True)     
      work_hours_code=models.ForeignKey(WorkingHour,on_delete=models.PROTECT)
      basic_salary=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
      house_allowance_rate=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
      housing_levy_rate=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
      pin_no=models.CharField(max_length=11,blank=True,null=True)
      nssf_no=models.CharField(max_length=11,blank=True,null=True)
      nhif_no=models.CharField(max_length=11,blank=True,null=True)
     


      class Meta:
            verbose_name_plural = "Employee"
            
            
      def get_absolute_url(self):
          return reverse('employees:employee-details',kwargs={'pk': self.pk})
    
    

def get_employees(request):         
      query = request.GET.get("term", "")
      emps = Employee.objects.filter(Q(employee_no__icontains=query)|Q(first_name__icontains=query)|Q(other_name__icontains=query),is_active=1).all()
      results = []
      for emp in emps:
            new_row={}
            new_row['label'] = str(emp.employee_no) + ' - '+emp.first_name +' '+emp.other_name
            new_row['value'] = emp.employee_no
            results.append(new_row)
            data = json.dumps(results)
      mimetype = "application/json"
      return HttpResponse(data, mimetype)

def get_emp_details(request):
      data = {'employee_name': [],'basic_salary':[]}
      q = request.GET.get("code", "")
      emp_details = Employee.objects.filter(employee_no=q)
      for emp in emp_details:
            data['employee_name'].append(emp.first_name +' '+emp.other_name)
            data['basic_salary'].append(emp.basic_salary)
      return JsonResponse(data, safe = True)

