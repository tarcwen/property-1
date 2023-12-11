from django import forms  
from listing.models import Listing
from django.core.exceptions import ValidationError
import os  
from django.core.validators import FileExtensionValidator

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
        raise ValidationError("Only .png, .jpg,and .jpeg files are allowed.")

class ListingForm(forms.ModelForm):  
    class Meta:  
        model = Listing  
        fields = ('realtor', 'title', 'address','city','state','zipcode', 'description','price','bedrooms','bathrooms','garage', 'sqft','lot_size', 'photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6')
        labels = {
            'realtor': 'Realtor',
            'title': 'Title',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
            'description': 'Description',    
            'price': 'Price',    
            'bedrooms': 'Number of Bedrooms',    
            'bathrooms': 'Number of Bathrooms',    
            'garage': 'Garage',    
            'sqft': 'Square Footage',        
            'lot_size': 'Lot Size',
            'photo_main': 'Main Photo',
            'photo_1': 'Photo 1',
            'photo_2': 'Photo 2',
            'photo_3': 'Photo 3',
            'photo_4': 'Photo 4',
            'photo_5': 'Photo 5',
            'photo_6': 'Photo 6',
		}
        widgets = {
            'realtor': forms.TextInput(attrs={
                'class':'form-control col-md-6 mb-3', 
                'placeholder':'Realtor',
                'hidden' : True,
                }),
            'title': forms.TextInput(attrs={
                'class':'form-control  mb-3', 
                'placeholder':'Place your listing name here',
                'required': True,
                
                }),
			'address': forms.TextInput(attrs={
                'class':'form-control  mb-3', 
                'placeholder':'Address',
                'required': True,
                }),
			'city': forms.TextInput(attrs={
                'class':'form-control  mb-3',  
                'placeholder':'City',
                'required': True,
                }),
			'state': forms.TextInput(attrs={
                'class':'form-control mb-3', 
                'placeholder':'State',
                'required': True,
                }),
			'zipcode': forms.TextInput(attrs={
                'class':'form-control mb-3', 
                'placeholder':'Zipcode',
                'required': True,
                }),
			'description': forms.Textarea(attrs={
                'class':'form-control mb-3', 
                'placeholder':'Description',
                'required': True,
                }),
            'price': forms.TextInput(attrs={
                'class':'form-control mb-3', 
                'placeholder':'Price',
                'required': True,
                }),	
            'bedrooms': forms.TextInput(attrs={
                'class':'form-control mb-3',  
                'placeholder':'Bedrooms',
                'required': True,
                }),
            'bathrooms': forms.TextInput(attrs={
                'class':'form-control mb-3', 
                'placeholder':'Bathrooms',
                'required': True,
                }),	
            'garage': forms.TextInput(attrs={
                'class':'form-control mb-3',  
                'placeholder':'Garage',
                'required': True,
                }),	
            'sqft': forms.TextInput(attrs={
                'class':'form-control mb-3',  
                'placeholder':'Sqft',
                'required': True,
                }),		
            'lot_size': forms.TextInput(attrs={
                'class':'form-control mb-3',  
                'placeholder':'Lot Size',
                'required': True,
                }),
            'photo_main': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_1': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_2': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_3': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_4': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_5': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
            'photo_6': forms.FileInput(attrs={
                'class':'form-control mb-3', 
                }),
		} 
    photo_main = forms.FileField(
        required=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
        ],
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    def clean_photo_main(self):
        photo_main = self.cleaned_data.get('photo_main')
        validate_image_extension(photo_main)
        return photo_main

    def clean_photo_1(self):
        photo_1 = self.cleaned_data.get('photo_1')
        validate_image_extension(photo_1)
        return photo_1

    def clean_photo_2(self):
        photo_2 = self.cleaned_data.get('photo_2')
        validate_image_extension(photo_2)
        return photo_2

    def clean_photo_3(self):
        photo_3 = self.cleaned_data.get('photo_3')
        validate_image_extension(photo_3)
        return photo_3

    def clean_photo_4(self):
        photo_4 = self.cleaned_data.get('photo_4')
        validate_image_extension(photo_4)
        return photo_4

    def clean_photo_5(self):
        photo_5 = self.cleaned_data.get('photo_5')
        validate_image_extension(photo_5)
        return photo_5

    def clean_photo_6(self):
        photo_6 = self.cleaned_data.get('photo_6')
        validate_image_extension(photo_6)
        return photo_6
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')

        # Check if the value contains only digits
        if not zipcode.isdigit():
            raise ValidationError("Zipcode must contain only numbers.")

        return zipcode

class CompareListingsForm(forms.Form):
    selected_listings = forms.ModelMultipleChoiceField(
        queryset=Listing.objects.filter(is_published=True),
        widget=forms.CheckboxSelectMultiple
    )
