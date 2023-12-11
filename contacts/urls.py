from django.urls import path

from . import views

urlpatterns = [
  path('contact', views.contact, name='contact'),
  path('setTheTIme', views.setTheTIme, name='setTheTIme'),
  path('contact_status/<int:contact_id>/', views.change_status, name='contact_status'),
  path('change_status_cancel/<int:contact_id>/', views.change_status_cancel, name='change_status_cancel'),
  path('schedule', views.schedule, name='schedule'),
  path('all_schedule', views.all_schedule, name='all_schedule'), 
  path('realtor_all_schedule/<int:realtor_id>/', views.realtor_all_schedule, name='realtor_all_schedule'), 
] 