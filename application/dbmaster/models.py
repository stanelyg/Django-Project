from django.db import models
from decimal import Decimal ,ROUND_HALF_UP
import  datetime,calendar

from django.contrib.auth.models import User
# Create your models here.

class Holiday(models.Model):
      year=models.CharField(max_length=4)

      class Meta:
            verbose_name_plural="Public Holiday "

      def __str__(self):
           return self.year

class HolidayDetail(models.Model):
      holiday_date=models.DateField()
      holiday_name=models.CharField(max_length=100)   
      year=models.ForeignKey('Holiday',on_delete=models.PROTECT)

      class Meta:
           verbose_name_plural="Holiday Dates"

      def __str__(self):
           return str(self.holiday_date) +'  '+ self.holiday_name


class SalaryYear(models.Model):
      year=models.CharField(max_length=4)

      def __str__(self):
           return self.year
class SalaryPeriod(models.Model):
     year = models.ForeignKey("SalaryYear", on_delete=models.CASCADE)
     month=models.PositiveSmallIntegerField()
     active =models.BooleanField(default=0)

     class Meta:
          verbose_name_plural="Salary Dates"

     def get_years():
          years=[]
          for choice in SalaryYear.objects.all().distinct().order_by('year'):
                         years.append((choice.year,choice.year))
          return years
     def get_months():
          month_names = ['January','February','March','April','May','June', 'July','August','September','October','November','December']
          months=[(i+1 ,month_names[i]) for i in range(12)]
          return months

     def get_months_submit():
          month_names = ['January','February','March','April','May','June', 'July','August','September','October','November','December']
          current_month = datetime.datetime.now().month - 1
          months=[(('','Select Month'))]
          months.extend([(i+1 ,month_names[i]) for i in range(12)])
          return months
     def __str__(self):
          return str(self.year) +'  '+ str(self.year)
def check_open_month(year,month):   
     query=SalaryPeriod.objects.filter(year__year=year,month=month,active=1).count()
     if query >0 :
        return True
     else:
        return False
def period_dates(year,month):
    return {'from_date':datetime.date(year,month,1),'to_date':datetime.date(year,month,calendar.monthlen(year, month))}
    
class WorkingHour(models.Model):
      work_hour_name=models.CharField(max_length=100)
      normal_hour=models.CharField(max_length=2)
      sun=models.CharField(max_length=2)
      mon=models.CharField(max_length=2)
      tue=models.CharField(max_length=2)
      wed=models.CharField(max_length=2)
      thu=models.CharField(max_length=2)
      fri=models.CharField(max_length=2)
      sat =models.CharField(max_length=2)
      class Meta:
            verbose_name_plural = "Working Hours"

      def __str__(self):
                return self.work_hour_name
    
    
def navigate_model(nav_btn_data,data_model):
     if nav_btn_data['nav-button']=='first':
               query=data_model.objects.order_by('id').first()
               if query:
                    return query.id
               else:
                    return None
     elif nav_btn_data['nav-button'] =='forward':
               if nav_btn_data['id']:
                         query=data_model.objects.filter(id__gt=nav_btn_data['id']).order_by('id').first()
                         if query:
                              return query.id
                         else:
                              query=data_model.objects.order_by('id').first()
                              return query.id
               else :
                    query=data_model.objects.order_by('id').first()
                    if query:
                              return query.id
                    else:
                              return None
     elif nav_btn_data['nav-button'] =='backward':
          if nav_btn_data['id']:
               query=data_model.objects.filter(id__lt=nav_btn_data['id']).order_by('id').last()
               if query:
                    return query.id
               else:
                    query=data_model.objects.order_by('id').last()
                    return query.id
          else:
               query=data_model.objects.order_by('id').last()
               if query:
                    return query.id
               else:
                    return None
     elif  nav_btn_data['nav-button']=='last':
               query=data_model.objects.order_by('id').last()
               if query:
                    return query.id
               else:
                    return None


def get_post_array(tup, di):
    di = dict(tup)
    return di
