from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name ='index'),
    path('about',views.about,name ='about'),
    path('mortgage',views.mortgage,name ='mortgage'),
    path('buyvsrent',views.buyvsrent,name ='buyvsrent'),
    path('my_view',views.my_view,name ='my_view'),
    path('space',views.space,name ='space'),
    path('sendInquiry',views.sendInquiry,name ='sendInquiry'),
    path('delete_command/<int:command_id>/', views.delete_command, name='delete_command'),
    path('delete_reply/<int:command_id>/', views.delete_reply, name='delete_reply'),
    path('reply',views.reply,name ='reply'),
]