from django.urls import include, path
from . import  views
from dbmaster.views import HomeView

app_name="dbmaster"
urlpatterns = [
     path('',HomeView.as_view(),name='home'),
         
]