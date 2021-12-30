from django.contrib import messages
from datetime import datetime,timedelta
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from dateutil.relativedelta import relativedelta

from django.forms.models import inlineformset_factory

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView,View

from attendance.forms import (AttendanceCreateForm, AttendanceDetailsForm,
                              AttendanceUpdateForm,AttendanceFormset)
from attendance.models import Attendance, AttendanceDetail
from dbmaster.models import  get_post_array, navigate_model,check_open_month


class AttendanceCreateView(LoginRequiredMixin,CreateView):
      form_class=AttendanceCreateForm
      permission_required='attendance.add_attendance'
      template_name='attendance.html'
      attendance_details_form_set= AttendanceFormset
      def get_context_data(self,**kwargs):
            data = super().get_context_data(**kwargs)
            if self.request.method == 'POST':
                data["details"] = self.attendance_details_form_set(self.request.POST)
            else:
                data["details"] = self.attendance_details_form_set()
            return data

      def form_valid(self, form):
            context = self.get_context_data()
            details = context["details"]
            if check_open_month(self.request.POST['year'],self.request.POST['month']):
                id=check_duplicates('',self.request.POST['year'],self.request.POST['month'])
                if id:
                    messages.success(self.request, 'Duplicates not allowed')
                    return HttpResponseRedirect(reverse("attendance:attendance-details",kwargs={'pk':id}))
                else:
                    if details.is_valid():
                        self.object = form.save()
                        details.instance = self.object
                        details.save()
                        messages.success(self.request, 'Attendance Added')
                    else:
                        messages.warning(self.request, "Attendance Couldn't be added")
                    return super().form_valid(form)
            else:
                    messages.warning(self.request, 'No Add Period Locked')
                    return self.render_to_response(self.get_context_data(form=form))


      def get_success_url(self):
             return reverse("attendance:attendance-details",kwargs={'pk':self.object.id})


class AttendanceUpdateView(LoginRequiredMixin,UpdateView):
      model = Attendance
      form_class=AttendanceUpdateForm
      template_name='attendance_details.html'
      attendance_details_form_set= AttendanceFormset
      def get_context_data(self,**kwargs):
                data = super().get_context_data(**kwargs)
                if self.request.method == 'POST':
                       data["details"] = self.attendance_details_form_set(self.request.POST,instance=self.object)
                else:
                        data["details"] = self.attendance_details_form_set(instance=self.object)
                return data
      def form_valid(self, form):
                context = self.get_context_data()
                details = context["details"]
                if  check_open_month(self.request.POST['year'],self.request.POST['month']):
                    id=check_duplicates(self.request.POST['id'],self.request.POST['year'],self.request.POST['month'])
                    if id:
                        messages.success(self.request, 'Duplicates not allowed')
                        return HttpResponseRedirect(reverse("attendance:attendance-details",kwargs={'pk':id}))
                    else:
                        self.object = form.save()
                        if details.is_valid():
                            messages.success(self.request, 'Well Done!  Attendance Updated')
                            details.instance = self.object
                            details.save()
                        else:
                            messages.warning(self.request, "Ooh No! Attendance Couldn't be updated")
                        return super().form_valid(form)
                else:
                    messages.warning(self.request, 'No Update Period Locked')
                    return self.render_to_response(self.get_context_data(form=form))

      def get_success_url(self):
             return reverse("attendance:attendance-details",kwargs={'pk':self.kwargs['pk']})


def navigate_attendance(request):
    if request.POST:
              nav_btn_data=get_post_array(request.POST.items(),dict())
              id=navigate_model(nav_btn_data,Attendance)
              if id:
                    return HttpResponseRedirect(reverse("attendance:attendance-details",kwargs={'pk':id}))
              else:
                     return HttpResponseRedirect(reverse("attendance:attendance-create"))


def search_attendance(request):
    if request.POST:
              array=get_post_array(request.POST.items(),dict())
              if array['id']:
                    querset=Attendance.objects.filter(id=array['id']).values('id')
                    if querset:
                        return HttpResponseRedirect(reverse("attendance:attendance-details",kwargs={'pk':querset[0]['id']}))
                    else:
                        messages.warning(request,"Serial Number not Found")
                        return HttpResponseRedirect(reverse("attendance:attendance-create"))
              elif array['id']=='' and array['year'] and array['month']:
                   querset=Attendance.objects.filter(year=array['year'],month=array['month']).values('id')
                   if querset:
                         return HttpResponseRedirect(reverse("attendance:attendance-details",kwargs={'pk':querset[0]['id']}))
                   else:
                        messages.warning(request,"Attendance not Found")
                        return HttpResponseRedirect(reverse("attendance:attendance-create"))
              else:
                        messages.warning(request,"No search Criteria Given")
                        return HttpResponseRedirect(reverse("attendance:attendance-create"))

def check_duplicates(id,year,month):
    if id :
       querset=Attendance.objects.exclude(id=id).filter(year=year,month=month).values('id')
    else:
       querset=Attendance.objects.filter(year=year,month=month).values('id')
    if querset:
        return querset[0]['id']
    else:
        return False



def copy_attendance(request):
    initial={}
    if request.POST:
            array=get_post_array(request.POST.items(),dict())
            if array['id']:
                initial['month']=(int(array['month']) +1,1)[int(array['month']) +1==13]           
                initial['year']=(array['year'],int(array['year']) + 1)[int(array['month']) +1==13]    
                form=AttendanceCreateForm(initial=initial)
                data=[{
                    'employee_name':row.employee_name,               
                    'employee_no':row.employee_no,
                    'days':''
                } for row in AttendanceDetail.objects.filter(attendance=array['id']).all()]
                formset=AttendanceFormset(initial=data)
            return render(request,'attendance.html' ,{'form':form,'details':formset})

