from django.db import models
import datetime
from django.db.models import Max, Min,Count
from dbmaster.models import round_half_up,period_dates
from decimal import Decimal

class PayeRelief(models.Model):
      effective_date=models.DateField()
      relief_amount=models.DecimalField(max_digits=12,decimal_places=2)
      class Meta:
            verbose_name_plural = "Paye Relief"
      def __str__(self):
            return str(self.effective_date)
class Payetable(models.Model):
      annual_gross=models.DecimalField(max_digits=16,decimal_places=4)
      min_gross=models.DecimalField(max_digits=16,decimal_places=4)
      max_gross=models.DecimalField(max_digits=16,decimal_places=4)
      tax_percentage=models.DecimalField(max_digits=5,decimal_places=2)
      payerelief=models.ForeignKey('PayeRelief',on_delete=models.PROTECT)


      class Meta:
            verbose_name_plural = "Paye Details"

      def get_paye_amount(taxable_amount,from_date):
          paye_array={}
          tax_amount=0
          paye_amount=0
          relief_amount=0
          tax_relief=PayeRelief.objects.filter(effective_date__lte=from_date).latest('effective_date','relief_amount','id')
          relief_amount+=tax_relief.relief_amount
          first_bracket_max=Payetable.objects.filter(payerelief=tax_relief.id).aggregate(Min('max_gross'))
          paye_array['paye_first_bracket_max']=first_bracket_max['max_gross__min']
          max_tax_percentage=Payetable.objects.filter(payerelief=tax_relief.id).aggregate(Max('tax_percentage'))
          paye_array['max_tax_percentage']=max_tax_percentage


          all_brackets=Payetable.objects.filter(payerelief=tax_relief.id).all().order_by('min_gross')
          for values in all_brackets:
                if taxable_amount>=values.max_gross:
                      tax_amount+=((values.max_gross-values.min_gross))*(values.tax_percentage/100)
                elif taxable_amount >values.min_gross and taxable_amount <=values.max_gross:
                      tax_amount+=(Decimal(taxable_amount)- Decimal(values.min_gross))*(values.tax_percentage/100)

          if tax_amount-relief_amount <0:
                  paye_array['tax_amount']=round_half_up(tax_amount,0)
                  paye_array['paye_amount']=0
                  paye_array['relief_amount']=round_half_up(relief_amount,0)
          else:
                  paye_array['tax_amount']=round_half_up(tax_amount,0)
                  paye_array['paye_amount']=round_half_up(tax_amount-relief_amount,0)
                  paye_array['relief_amount']=round_half_up(relief_amount,0)
          return paye_array


class Nhif(models.Model):
      effective_date=models.DateField()
      paye_relief_percentage=models.DecimalField(max_digits=5,decimal_places=2)
      class Meta:
            verbose_name_plural = "Nhif"
      def __str__(self):
            return str(self.effective_date)

class NhifDetail(models.Model):
      min_gross=models.DecimalField(max_digits=12,decimal_places=2)
      max_gross=models.DecimalField(max_digits=12,decimal_places=2)
      premium=models.DecimalField(max_digits=12,decimal_places=2)
      nhif=models.ForeignKey('Nhif',on_delete=models.PROTECT)

      def get_nhif_amount(gross_salary,from_date):
          rounded_gross=round_half_up(gross_salary,0)
          effective_id=Nhif.objects.filter(effective_date__lte=from_date).latest('id')
          queryset=NhifDetail.objects.filter(min_gross__lte=rounded_gross,max_gross__gte=rounded_gross,nhif=effective_id.id).values('premium')
          if queryset:
                return queryset[0]['premium']
          else:
                return 0



      def __str__(self):
            return str(self.nhif)


class Nssfreferencetable(models.Model):
      effective_date=models.DateField()
      tier_one_lower=models.DecimalField(max_digits=12,decimal_places=2)
      tier_one_upper=models.DecimalField(max_digits=12,decimal_places=2)
      tier_two_lower=models.DecimalField(max_digits=12,decimal_places=2)
      tier_two_upper=models.DecimalField(max_digits=12,decimal_places=2)
      percentage=models.DecimalField(max_digits=6,decimal_places=2)
      employee_contribution=models.DecimalField(max_digits=3,decimal_places=1)

      class Meta:
            verbose_name_plural = "Nssf Table"


      def get_nssf_amount(gross_salary,from_date):
            nssf_array={}
            nssf_array['tier_one']=0
            nssf_array['tier_two']=0
            nssf_array['nssf_amount']=0
            rounded_gross=round_half_up(gross_salary,0)
            queryset=Nssfreferencetable.objects.filter(effective_date__lte=from_date).values().latest('effective_date','tier_one_lower','tier_one_upper','tier_two_lower','tier_two_upper','percentage','employee_contribution')
            nssf_array['employee_contribution']=queryset['employee_contribution']
            if rounded_gross >=queryset['tier_one_lower'] and  rounded_gross < queryset['tier_one_upper']:
                  nssf_array['tier_one']+=round_half_up(Decimal(rounded_gross)* queryset['percentage']/100 ,0)
            else:
                  nssf_array['tier_one']=round_half_up(queryset['tier_one_upper']*(queryset['percentage']/100),0)
                  if rounded_gross > queryset['tier_two_lower'] and rounded_gross < queryset['tier_two_upper']:
                        nssf_array['tier_two'] = round_half_up((Decimal(rounded_gross)-queryset['tier_two_lower']) * (queryset['percentage']/100),0)
                  else:
                        nssf_array['tier_two'] = round_half_up((queryset['tier_two_upper']-queryset['tier_two_lower']) * (queryset['percentage']/100),0)
         
            nssf_array['nssf_amount']+=Decimal(nssf_array['tier_one']+  nssf_array['tier_two'])

            return nssf_array
      def __str__(self):
            return str(self.effective_date)


class OverTimeSetting(models.Model):
      effective_date=models.DateField()
      ot1_factor=models.DecimalField(max_digits=5,decimal_places=2)
      ot2_factor=models.DecimalField(max_digits=5,decimal_places=2)

      class Meta:
            verbose_name_plural='Over Time Settings'

      def __str__(self):
            return str(self.effective_date)







