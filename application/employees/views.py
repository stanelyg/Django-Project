from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView


# Create your views here.
class EmployeeCreateView(LoginRequiredMixin,SuccessMessageMixin,TemplateView):
    template_name='employee.html'