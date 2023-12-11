from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from listing.models import Listing
from listing.forms import ListingForm  
from realtors.forms import RealtorForm  
from realtors.models import Realtor
from rating.models import Rating
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.template.defaultfilters import floatformat
from django.contrib.auth import get_user_model
from mysite.utils import encrypt_id, decrypt_id

# Create your views here.
def realtorsIndex(request):
    realtor = Realtor.objects.get(user_id=request.user.id)
    # Get the current user (assuming they are logged in)
    user = request.user

    # Encode the user ID
    encrypted_id = encrypt_id(user.id)
    #display 3 only
    listings = Listing.objects.order_by('-list_date').filter(is_published=True, realtor__id = realtor.id)[:3]
    # listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    # print(len(listings),"+++++++++++++++++++++++++++++++++++++++++++++++")s

    context = {
        'listings': listings,
        'encrypted_id': encrypted_id,
    }
    return render(request, 'realtors/index.html', context)

def realtorsUploaded(request):
  realtor = Realtor.objects.get(user_id=request.user.id)
  listings = Listing.objects.order_by('-list_date').filter(is_published=True, realtor__id = realtor.id)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'realtors/realtorsListingAll.html', context)

def selectedRealtors(request, id):
  encrypted_id = request.encrypted_id
  realtor = Realtor.objects.get(id=id)
  listings = Listing.objects.order_by('-list_date').filter(is_published=True, realtor__id = realtor.id)
  total_listing = listings.count()
  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  # Assuming you have a user instance
  user = User.objects.get(id=request.user.id)

  # Get the first user group (if any)
  isCustomer = user.groups.filter(name='customer').exists
  
  # Get the rating
  realtor_rating = Rating.objects.filter(realtor__id = realtor.id)
  
  # get the average
  average_rating = realtor_rating.aggregate(avg_rating=Avg('rating_value'))['avg_rating']
  if average_rating is None:
    average_rating = 0.0
  # rount the decimal
  average_rating = float(floatformat(average_rating, 1))
  

  # Classify the rating
  classification = 'Neutral' if average_rating < 4 else 'Excellent'



  context = {
    'listings': paged_listings,
    'realtors':realtor,
    'isCustomer':isCustomer,
    'total_listing':total_listing,
    'average_rating':average_rating,
    'classification':classification,
    'encrypted_id':encrypted_id,
  }

  return render(request, 'realtors/realtorsListingAll.html', context)

def realtorsListing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'realtors/realtorsListing.html', context)

##realtor/views
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import requests
import hashlib

def upscale_image(image):
    url = "https://ai-picture-upscaler.p.rapidapi.com/supersize-image"
    
    # Prepare the payload for the API request
    payload = {
        "sizeFactor": 2,
        "imageStyle": "default",
        "noiseCancellationFactor": 0
    }
    
    # Attach the image file to the payload
    files = {"image": (image.name, image.file.read())}
    
    # Set the headers
    headers = {
        "X-RapidAPI-Key": "2acd3092e3mshd966f3cfe06c348p1c40abjsn5ab65ff310c0",
        "X-RapidAPI-Host": "ai-picture-upscaler.p.rapidapi.com"
    }

    # Make the API request to upscale the image
    response = requests.post(url, data=payload, headers=headers, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the upscaled image from the response
        upscaled_image_data = response.content
        return Image.open(BytesIO(upscaled_image_data))
    else:
        # If the API request fails, return None
        return None

def apply_watermark_to_image(image, realtor_name, realtor_phone, realtor_email):
    # Upscale the image using the API
    upscaled_image = upscale_image(image)

    if upscaled_image:
        # Create a drawing object
        draw = ImageDraw.Draw(upscaled_image)

        # Add watermark text
        watermark_text = f"RealEstate\n{realtor_name}\nPhone: {realtor_phone}\nEmail: {realtor_email}"
        font = ImageFont.load_default()
        draw.text((10, 10), watermark_text, fill=(255, 255, 255), font=font)

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        upscaled_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Create an InMemoryUploadedFile from the buffer
        watermarked_image = InMemoryUploadedFile(
            buffer, None, image.name, 'image/png', buffer.tell(), None
        )

        return watermarked_image
    else:
        # Return the original image if the upscaling fails
        return image



def UpdateListing(request, listing_id):

    selectedListing = get_object_or_404(Listing, id=listing_id)
    form = ListingForm(instance=selectedListing)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=selectedListing)

        if form.is_valid():
            realtor_instance = Realtor.objects.get(user_id=decrypt_id(request.encrypted_id))

            # Save the form data
            listing = form.save()

            # Apply watermark to the uploaded images
            if form.cleaned_data['photo_main'] and form.cleaned_data['photo_main'] != selectedListing.photo_main:
                listing.photo_main = apply_watermark_to_image(listing.photo_main,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_1'] and form.cleaned_data['photo_1'] != selectedListing.photo_1:
                listing.photo_1 = apply_watermark_to_image(listing.photo_1,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_2'] and form.cleaned_data['photo_2'] != selectedListing.photo_2:
                listing.photo_2 = apply_watermark_to_image(listing.photo_2,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_3'] and form.cleaned_data['photo_3'] != selectedListing.photo_3:
                listing.photo_3 = apply_watermark_to_image(listing.photo_3,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_4'] and form.cleaned_data['photo_4'] != selectedListing.photo_4:
                listing.photo_4 = apply_watermark_to_image(listing.photo_4,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_5'] and form.cleaned_data['photo_5'] != selectedListing.photo_5:
                listing.photo_5 = apply_watermark_to_image(listing.photo_5,realtor_instance.name,realtor_instance.phone,realtor_instance.email)
            if form.cleaned_data['photo_6'] and form.cleaned_data['photo_6'] != selectedListing.photo_6:
                listing.photo_6 = apply_watermark_to_image(listing.photo_6,realtor_instance.name,realtor_instance.phone,realtor_instance.email)

            # Save the listing with watermarked images
            listing.save()

            return redirect("realtors")

    return render(request, 'listings/updateListing.html', {'form': form})

def DeleteListing(request, listing_id):
  selectedListing = Listing.objects.get(id=listing_id)
  selectedListing.delete()
  return HttpResponseRedirect(reverse('realtors'))

def UpdateProfile(request, userID):
  decrypted_id = decrypt_id(userID)
  selectedUser = get_object_or_404(Realtor, user_id=decrypted_id)
  form = RealtorForm(instance=selectedUser)
  if request.method == 'POST':
      form = RealtorForm(request.POST, request.FILES, instance=selectedUser)
      if form.is_valid():
          form.save()
          return redirect("realtors")
        
  return render(request, 'realtors/profile.html', {'form': form})

def realtorProfile(request, id):
  decrypted_id = decrypt_id(id)

  realtor = get_object_or_404(Realtor, user_id=decrypted_id)
  listings = Listing.objects.order_by('-list_date').filter(is_published=True, realtor__id = realtor.id)
  total_listing = listings.count()

  # Assuming you have a user instance
  user = User.objects.get(id=request.user.id)

  # Get the first user group (if any)
  isCustomer = user.groups.filter(name='customer').exists
  
  # Get the rating
  realtor_rating = Rating.objects.filter(realtor__id = realtor.id)
  
  # get the average
  average_rating = realtor_rating.aggregate(avg_rating=Avg('rating_value'))['avg_rating']
  if average_rating is None:
    average_rating = 0.0
  # rount the decimal
  average_rating = float(floatformat(average_rating, 1))
  

  # Classify the rating
  classification = 'Neutral' if average_rating < 4 else 'Excellent'

  #encrypted id
  encrypted_id = encrypt_id(user.id)

  context = {
    'realtors':realtor,
    'isCustomer':isCustomer,
    'total_listing':total_listing,
    'average_rating':average_rating,
    'classification':classification,
    'encrypted_id': encrypted_id,
  }


  return render(request, 'realtors/realtorProfile.html', context)