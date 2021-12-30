from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin,TemplateView):
    template_name="layouts/home.html"
    