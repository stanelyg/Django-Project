from django import forms
import  datetime
from django.forms.models import inlineformset_factory
from dbmaster.models import SalaryPeriod


class MonthlyReportForm(forms.Form):
    year=forms.ChoiceField(
        choices=SalaryPeriod.get_years,
        initial=0)
    
    month=forms.ChoiceField(
    choices=SalaryPeriod.get_months,
    required=False)
class StatutoryReportForm(forms.Form):
    year = forms.ChoiceField(choices=(SalaryPeriod.get_years))
    month = forms.ChoiceField(choices=(SalaryPeriod.get_months))

class ItaxReportForm(forms.Form):
    year = forms.ChoiceField(choices=(SalaryPeriod.get_years))
    month = forms.ChoiceField(choices=(SalaryPeriod.get_months))
    
