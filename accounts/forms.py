from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class AccountForm(forms.ModelForm):  
    class Meta:  
        model = User  
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
		}
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class':'form-control col-md-4 mb-3', 
                }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control col-md-4 mb-3', 
                }),
			'email': forms.TextInput(attrs={
                'class':'form-control col-md-4 mb-3', 
                }),
		} 

class PasswrodChangingFrom(PasswordChangeForm):  
    class Meta:  
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {
            'old_password': 'Old Password',
            'new_password1': 'New Password',
            'new_password2': 'Confirm Password',
		}
        widgets = {
            'old_password': forms.PasswordInput(attrs={
                'class':'form-control col-md-4 mb-3', 
                'type':'password',
                }),
            'new_password1': forms.PasswordInput(attrs={
                'class':'form-control col-md-4 mb-3',
                'type':'password', 
                }),
			'new_password2': forms.PasswordInput(attrs={
                'class':'form-control col-md-4 mb-3',
                'type':'password', 
                }),
		}   