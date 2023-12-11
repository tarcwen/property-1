from django.contrib import admin
from django.urls import path
from . import views  
 
urlpatterns = [
    path('', views.index, name='eventIndex'), 
    path('all_events/', views.all_events, name='all_events'), 
]