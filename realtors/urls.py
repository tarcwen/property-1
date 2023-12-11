from django.urls import path

from . import views

urlpatterns = [
    path('', views.realtorsIndex, name='realtors'),
    path('ListingUploaded', views.realtorsUploaded, name='realtorsUploaded'),
    path('SelectedRealtors/<int:id>/', views.selectedRealtors, name='selectedRealtors'),
    path('<int:listing_id>', views.realtorsListing, name='realtorsListing'),
    path('UpdateListing/<int:listing_id>/', views.UpdateListing, name='UpdateListing'),
    path('DeleteListing/<int:listing_id>/', views.DeleteListing, name='DeleteListing'),
    path('UpdateProfile/<str:userID>/', views.UpdateProfile, name='UpdateProfile'),
    path('RealtorProfile/<str:id>/', views.realtorProfile, name='realtorProfile'),
]