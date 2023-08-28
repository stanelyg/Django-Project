from dbmaster.models import WorkingHour
from django import forms
from employees.models import Employee
from django.forms.models import inlineformset_factory

class EmployeeCreateForm(forms.ModelForm):
        class Meta:
            model =Employee
            fields='__all__'      
        employee_no=forms.ModelChoiceField(
                    queryset = Employee.objects.all(),
                    widget=forms.TextInput(attrs={
                    'size':6,
                    'class':"form-control",
                    'placeholder':"Emp No",
                    'style':'text-align:center;'
            }),required=False)
        first_name= forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter First Name",                                                                 
                }),required=False)
        
        other_name= forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter Other Names ",                                                                 
                }),required=False)
        date_of_joining=forms.DateField(widget=forms.TextInput(attrs={
                    'id':'date_of_joining',
                    'value':'',
                    'autocomplete':'off',
                    'class':"form-control",
                    'type':'date',
                }))
        date_of_leaving=forms.DateField(widget=forms.TextInput(attrs={
                    'id':'date_of_leaving',
                    'value':'',
                    'class':"form-control",
                    'autocomplete':'off',
                    'type':'date',
                }),required=False)      
        work_hours_code=forms.ModelChoiceField(
                queryset=WorkingHour.objects.all().order_by('id'),
                empty_label='Select Working Hours',
                required=True,
            )
        basic_salary=forms.DecimalField(
                widget=forms.TextInput(attrs={
                    'id':'id_basic_salary',
                    'value':'',
                    'class':"form-control",                
                    'autocomplete':'off',
                }))
        house_allowance_rate=forms.DecimalField(
                widget=forms.TextInput(attrs={                   
                    'value':'',
                    'class':"form-control",                
                    'autocomplete':'off',
                }))
        housing_levy_rate=forms.DecimalField(
                widget=forms.TextInput(attrs={                   
                    'value':'',
                    'class':"form-control",                
                    'autocomplete':'off',
                }))
        national_id=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter National ID",                                                                 
                }))
        pin_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter PIN NO",                                                                 
                }))
        nssf_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter NSSF NO",                                                                 
                }))
        nhif_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter NHIF NO",                                                                 
                }))
        

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model =Employee
        fields='__all__'

    employee_no=forms.ModelChoiceField(
                queryset = Employee.objects.all(),
                widget=forms.TextInput(attrs={
                'size':6,
                'class':"form-control",
                'placeholder':"Emp No",
                'style':'text-align:center;'
        }),required=False)
      
      
    first_name= forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter First Name",                                                                 
                }),required=False)
        
    other_name= forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
                    'class':"form-control",
                    'placeholder':"Enter Other Names ",                                                                 
                }),required=False)
    date_of_joining=forms.DateField(widget=forms.TextInput(attrs={
            'id':'date_of_joining',
            'value':'',
            'autocomplete':'off',
            'class':"form-control",
            'type':'date',
        }))
    date_of_leaving=forms.DateField(widget=forms.TextInput(attrs={
            'id':'date_of_leaving',
            'value':'',
            'class':"form-control",
            'autocomplete':'off',
            'type':'date',
        }),required=False)      
    work_hours_code=forms.ModelChoiceField(
        queryset=WorkingHour.objects.all().order_by('id'),
        empty_label='Select Working Hours',
        required=True,
    )
    basic_salary=forms.DecimalField(
        widget=forms.TextInput(attrs={
            'id':'id_basic_salary',
            'value':'',
            'class':"form-control",                
            'autocomplete':'off',
        }))
    house_allowance_rate=forms.DecimalField(
                widget=forms.TextInput(attrs={                   
                    'value':'',
                    'class':"form-control",                
                    'autocomplete':'off',
                }))
    housing_levy_rate=forms.DecimalField(
                widget=forms.TextInput(attrs={                   
                    'value':'',
                    'class':"form-control",                
                    'autocomplete':'off',
                }))
    national_id=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
            'class':"form-control",
            'placeholder':"Enter National ID",                                                                 
        }))
    pin_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
            'class':"form-control",
            'placeholder':"Enter PIN NO",                                                                 
        }))
    nssf_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
            'class':"form-control",
            'placeholder':"Enter NSSF NO",                                                                 
        }))
    nhif_no=forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off',
            'class':"form-control",
            'placeholder':"Enter NHIF NO",                                                                 
        }))
      
