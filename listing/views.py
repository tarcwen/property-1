from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from listing.forms import ListingForm  
from django.template import loader
from django.contrib import messages
from .models import Listing, Realtor
from listingview.models import ListingView
from mysite.utils import encrypt_id, decrypt_id
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from mysite.utils import get_geolocation_info

def index(request):
  encrypted_id = request.encrypted_id

  # listings = Listing.objects.order_by('-list_date').filter(is_published=True)
  # listings = Listing.objects.annotate(view_count=Count('listingview')).order_by('-view_count', '-list_date').filter(is_published=True)
  if request.user.groups.filter(name='customer').exists():
    fake_ip_address = '118.101.197.197'  # Replace with the desired fake IP address
    geolocation_info = get_geolocation_info(fake_ip_address)
    city_name = geolocation_info.city 

    # Query to get city-specific listings
    city_listings = Listing.objects.filter(city=city_name).annotate(view_count=Count('listingview')).order_by('-view_count', '-list_date')

    # Query to get remaining listings
    remaining_listings = Listing.objects.exclude(city=city_name).annotate(view_count=Count('listingview')).order_by('-view_count', '-list_date')

    # Combine city-specific listings and remaining listings
    listings = list(city_listings) + list(remaining_listings)
  else:
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings,
    'encrypted_id': encrypted_id,
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  encrypted_id = request.encrypted_id

  listing = get_object_or_404(Listing, pk=listing_id)
  hours_list = [f"{hour}:00" for hour in range(10, 19)]
  duration_list = [1, 2]
  if request.user.groups.filter(name='customer').exists():
      ListingView.objects.create(user=request.user, listing=listing)
  context = {
    'listing': listing,
    'encrypted_id': encrypted_id,
    'hours_list': hours_list,
    'duration_list': duration_list,
  }

  return render(request, 'listings/listing.html', context)

def search(request):
  encrypted_id = request.encrypted_id

  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET,
    'encrypted_id': encrypted_id,
  }

  return render(request, 'listings/search.html', context)

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def upscale_image(image):
    url = "https://ai-picture-upscaler.p.rapidapi.com/supersize-image"
    
    # Prepare the payload for the API request
    payload = {
        "sizeFactor": 2,
        "imageStyle": "default",
        "noiseCancellationFactor": 0
    }
    
    # Attach the image file to the payload
    files = {"image": (image.name, image.file.read(), image.content_type)}
    
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

def listingCreate(request):
    encrypted_id = request.encrypted_id
    current_user_id = decrypt_id(encrypted_id)

    try:
        realtor_instance = Realtor.objects.get(user_id=current_user_id)
        realtor_id = realtor_instance.id
    except Realtor.DoesNotExist:
        realtor_instance = None
        realtor_id = None

    if request.method == "POST":
        realtor_instance = Realtor.objects.get(user_id=current_user_id)
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            # Set the realtor field before saving the form
            form.instance.realtor = realtor_instance

            # Add watermark to the main photo
            form.instance.photo_main = apply_watermark_to_image(request.FILES['photo_main'],realtor_instance.name,realtor_instance.phone,realtor_instance.email)

            # Apply watermark to additional photos
            for i in range(1, 7):  # Assuming you have six additional photos
                photo_field_name = f'photo_{i}'
                if photo_field_name in request.FILES:
                    setattr(form.instance, photo_field_name, apply_watermark_to_image(request.FILES[photo_field_name],realtor_instance.name,realtor_instance.phone,realtor_instance.email))

            # Save the form
            form.save()

            messages.success(request, 'Listing Created')
            return redirect('realtors')
    else:
        form = ListingForm(initial={'realtor': realtor_instance})

    return render(request, 'listings/CreateListing.html', {"encrypted_id":encrypted_id,'form': form, 'realtor_id': realtor_id, 'realtor':realtor_instance})


from django.shortcuts import render
from django.http import HttpResponse
from .models import Listing
from .forms import CompareListingsForm

def compare_listings(request):
    encrypted_id = request.encrypted_id
    if request.method == 'POST':
        form = CompareListingsForm(request.POST)
        if form.is_valid():
            # Use the correct key: 'selected_listings' instead of 'selected_listing'
            selected_listings = form.cleaned_data['selected_listings']

            # Perform any additional processing based on the selected listings
            return render(request, 'listings/compare_listings.html', {'listings': selected_listings})
    else:
        form = CompareListingsForm()

    return render(request, 'listings/compare_listings.html', {'encrypted_id':encrypted_id,'form': form})