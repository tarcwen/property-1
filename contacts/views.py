from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact
from django.shortcuts import get_object_or_404, render
from .models import Listing, Realtor
from django.http import JsonResponse 
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.utils.html import escape

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_id = request.POST['realtor_id']
        realtor_email = request.POST['realtor_email']

        # Sanitize the message using Django's escape function before storing it
        message = escape(message)

        # Extracting the selected date, time, and duration from the request
        selected_date = datetime.strptime(request.POST['contact_date'], '%Y-%m-%d').date()
        selected_time = datetime.strptime(request.POST['time'], '%H:%M').time()
        duration_hours = int(request.POST['duration'])

        # Combining the selected date and time for contact_date_start
        contact_date_start = datetime.combine(selected_date, selected_time)

        # Calculating contact_date_end by adding the duration to contact_date_start
        contact_date_end = contact_date_start + timedelta(hours=duration_hours)

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listing/' + listing_id)

        contact_date_start = timezone.make_aware(contact_date_start)
        contact_date_end = timezone.make_aware(contact_date_end)

        conflicting_contacts = Contact.objects.filter(
        Q(realtor_id=realtor_id) &
        (
            Q(listing_id=listing_id) |
            (
                Q(contact_date_start__lte=contact_date_start, contact_date_end__gte=contact_date_end) |
                Q(contact_date_start__lt=contact_date_end, contact_date_end__gt=contact_date_start)
            )
        )
    )

        if conflicting_contacts.exists():
            messages.error(request, 'The selected time slot is not available')
            return redirect('/listing/' + listing_id)

        # Create new Contact instance
        contact = Contact(
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id,
            realtor_id=realtor_id,
            contact_date_start=contact_date_start,
            contact_date_end=contact_date_end
        )

        contact.save()

          # Send email
          # send_mail(
          #   'Property Listing Inquiry',
          #   'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
          #   'traversy.brad@gmail.com',
          #   [realtor_email, 'techguyinfo@gmail.com'],
          #   fail_silently=False
          # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listing/' + listing_id)

  
def setTheTIme(request):
  contact_id = request.POST['contact_id']
  selectedContact = get_object_or_404(Contact, id=contact_id)
  if request.method == 'POST':
    # Update the date and time field
    selectedContact.contact_date_start = request.POST.get('contact_date_start')  # Replace 'contact_datetime' with the actual field name
    selectedContact.contact_date_end = request.POST.get('contact_date_end')
    selectedContact.status = "Upcoming" 
    # Save the changes
    selectedContact.save()
    messages.success(request, 'Date and time has been submitted, Waiting Customer to comfirm')
    return redirect('dashboard')
  else:
    messages.error(request, 'Appoinment has not been setted')
    return redirect('dashboard')

def change_status(request, contact_id):
    # Assuming you have some way to identify the object, e.g., contact_id

    # Retrieve the object
    contact = get_object_or_404(Contact, id=contact_id)

    # Update the status
    contact.status = 'Complete'
    contact.save()

    return redirect('dashboard')

def change_status_cancel(request, contact_id):
    # Assuming you have some way to identify the object, e.g., contact_id

    # Retrieve the object
    contact = get_object_or_404(Contact, id=contact_id)

    # Update the status
    contact.status = 'Cancel'
    contact.save()

    return redirect('dashboard')

def schedule(request):  
    all_events = Contact.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'scheduling.html',context)
 
def all_schedule(request):                                                                                                 
    all_events = Contact.objects.all()                                                                                    
    out = []   
    target_time_zone = timezone.pytz.timezone('Asia/Kuala_Lumpur')                                                                                                          
    for event in all_events:  
         # Convert event.contact_date to the target time zone
        target_time_start = event.contact_date_start.astimezone(target_time_zone)
        target_time_end = event.contact_date_end.astimezone(target_time_zone)                                                                             
        out.append({                                                                                                     
            'title': event.listing.title,                                                                                         
            'id': "Appt-" + str(event.id),                                                                                              
            'start': target_time_start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': target_time_end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 

def realtor_all_schedule(request, realtor_id):                                                                                                 
    all_events = Contact.objects.filter(realtor_id=realtor_id)                                                                                   
    out = []   
    target_time_zone = timezone.pytz.timezone('Asia/Kuala_Lumpur')                                                                                                          
    for event in all_events:  
         # Convert event.contact_date to the target time zone
        target_time_start = event.contact_date_start.astimezone(target_time_zone)
        target_time_end = event.contact_date_end.astimezone(target_time_zone)                                                                             
        out.append({                                                                                                     
            'title': event.listing.title,                                                                                         
            'id': "Appt-" + str(event.id),                                                                                              
            'start': target_time_start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': target_time_end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 