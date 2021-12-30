from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from employees.forms import EmployeeCreateForm,EmployeeUpdateForm
from employees.models import Employee
from dbmaster.models import navigate_model,get_post_array


# Create your views here.
class EmployeeCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    template_name='employee.html'
    form_class=EmployeeCreateForm
    success_message="Employee Added"
    
    def get_success_url(self):
             return reverse("employees:employee-details",kwargs={'pk':self.object.employee_no})
         
class EmployeeUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
      model=Employee
      template_name='employee_detail.html'
      success_message="Updated"
      form_class=EmployeeUpdateForm
      
      
def get_form(request):
      if request.POST:
            emp_id=get_post_array(request.POST.items(), dict())['employee_no']
            return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':emp_id}))
def navigate_form(request):
      if request.POST:
            nav_btn_data=get_post_array(request.POST.items(),dict())
            if nav_btn_data['nav-button']=='first':
                  query=Employee.objects.order_by('employee_no').first()
                  if query:
                        return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))
                  else:
                        return HttpResponseRedirect(reverse("employees:employee-create"))

            elif nav_btn_data['nav-button'] =='forward':
                  if nav_btn_data['employee_no']:
                              query=Employee.objects.filter(employee_no__gt=nav_btn_data['employee_no']).order_by('employee_no').first()
                              if query:
                                    return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))
                              else:
                                    query=Employee.objects.order_by('employee_no').first()
                                    return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))
                  else :
                        query=Employee.objects.order_by('employee_no').first()
                        if query:
                                   return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))
                        else:
                                   return HttpResponseRedirect(reverse("employees:employee-create"))

            elif nav_btn_data['nav-button'] =='backward':
                  if nav_btn_data['employee_no']:
                        query=Employee.objects.filter(employee_no__lt=nav_btn_data['employee_no']).order_by('employee_no').last()
                        if query:
                              return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))

                        else:
                              query=Employee.objects.order_by('employee_no').last()
                              return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))

                  else:
                        query=Employee.objects.order_by('employee_no').last()
                        if query:
                              return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))

                        else:
                               return HttpResponseRedirect(reverse("employees:employee-create"))
            elif  nav_btn_data['nav-button']=='last':
                  query=Employee.objects.order_by('employee_no').last()
                  if query:
                         return HttpResponseRedirect(reverse("employees:employee-details",kwargs={'pk':query.employee_no}))
                  else:
                         return HttpResponseRedirect(reverse("employees:employee-create"))
                   
