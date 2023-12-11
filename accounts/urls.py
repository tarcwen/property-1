from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Fix: Added a slash after 'login'
    path('register/', views.register, name='register'),
    path('realtors_register/', views.realtors_register, name='realtors_register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('selection/', views.selection, name='selection'),
    path('display_qr_code/<str:encrypted_id>/', views.display_qr_code, name='display_qr_code'),
    path('verify_otp/<str:encrypted_id>/', views.verify_otp, name='verify_otp'),
    path('customerProfile/<str:encrypted_id>/', views.UpdateCustomerProfile, name='UpdateCustomerProfile'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change-password.html'), name='password-change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]