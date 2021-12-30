from django import forms
import  datetime
from attendance.models import Attendance, AttendanceDetail
from employees.models import Employee
from django.forms.models import inlineformset_factory
from dbmaster.models import SalaryPeriod

class AttendanceCreateForm(forms.ModelForm):  
      class Meta:
            model = Attendance
            fields=['year','month']
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)           
            self.fields['month'].initial = datetime.datetime.now().month
      id=forms.CharField(widget=forms.TextInput(attrs={
            'id':'id',
            'value':'',
            'size':'6',
            'autocomplete':'off',
      }),required=False)
      year=forms.ChoiceField(
          choices=SalaryPeriod.get_years,
         initial=0)
      month=forms.ChoiceField(
       choices=SalaryPeriod.get_months,
       required=False)
      
class  AttendanceUpdateForm(forms.ModelForm):
      class Meta:
            model = Attendance
            fields=['id','year','month']
      id=forms.CharField(widget=forms.TextInput(attrs={
      'id':'attn_id',
      'value':'',
      'autocomplete':'off',
      }),required=False)

      year=forms.ChoiceField(
          choices=SalaryPeriod.get_years,
         initial=0)

      month=forms.ChoiceField(
       choices=SalaryPeriod.get_months,
       required=False)
class AttendanceDetailsForm(forms.ModelForm):
      class Meta:
            model = AttendanceDetail
            fields=['employee_no','employee_name','days']
      employee_no=forms.ModelChoiceField(
                  queryset = Employee.objects.all(),
                  widget=forms.TextInput(attrs={
                  'size':6,
            'style':'text-align:center;',
            'class':'unique row-nav form-control-small select2'
      }))
      employee_name=forms.CharField(widget=forms.TextInput(attrs={
            'readonly':'readonly',
      }))     
      days=forms.DecimalField(widget=forms.TextInput(attrs={
            'class':'text-right row-nav',
            'onclick': 'this.select();',
             'size':6,             
            'pattern':'(?:1[0-9]|[0-9])(?:1[0-9]|[0-9])(?:\.[0-9])?',
            'autocomplete':'off'
      }),required=False)

AttendanceFormset=inlineformset_factory(Attendance,AttendanceDetail,extra=10,form=AttendanceDetailsForm)
