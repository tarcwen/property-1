from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from realtors.models import Realtor
import os

def validate_image_extension(value):
    """
    Validate that the uploaded file has a valid image extension.
    """
    if value is None:
        # Handle the case where the field is not required and is left empty
        return

    valid_extensions = ['.png', '.jpg', '.jpeg']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only .png, .jpg, and .jpeg files are allowed.")

class RealtorForm(forms.ModelForm):
    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'Phone No.'
        }),
        validators=[
            # Add a RegexValidator for phone number validation
            RegexValidator(
                regex=r'^0[0-9]{9,10}$',
                message='Phone number must start with "0" followed by 10 digits.'
            ),
        ],
    )

    email = forms.CharField(
        label='E-mail',
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'example@gmail.com'
        }),
        validators=[EmailValidator(message='Enter a valid email address.')]
    )

    class Meta:
        model = Realtor
        fields = ('name', 'description', 'phone', 'email', 'photo')
        labels = {
            'name': 'Name',
            'description': 'Description',
            'phone': 'Phone',
            'email': 'E-mail',
            'photo': 'Photo',
		}
        widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'This will be your username'
        }),
        'description': forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'General information'
        }),
        'phone': forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'Phone No.'
        }),
        'email': forms.TextInput(attrs={
            'class': 'form-control col-md-8 mb-3',
            'placeholder': 'example@gmail.com'
        }),
        'photo': forms.FileInput(attrs={
            'class': 'form-control col-md-8 mb-3',
        }),
    }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        validate_image_extension(photo)
        return photo
