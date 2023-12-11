from django.shortcuts import render, redirect
from customerCmd.models import CustomerCmd, Reply
from django.contrib import messages
from django.http import HttpResponse
from listing.choices import price_choices, bedroom_choices, state_choices
from listing.models import Listing
from realtors.models import Realtor
from django.shortcuts import render
from django.template import loader
from ipware import get_client_ip
from geopy.geocoders import Nominatim
from mysite.utils import get_geolocation_info
from django.contrib.auth import get_user_model
from mysite.utils import encrypt_id, decrypt_id
import pyotp
from django.utils.html import escape
from django.shortcuts import get_object_or_404, redirect, render

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    # listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    # print(len(listings),"+++++++++++++++++++++++++++++++++++++++++++++++")

    encrypted_id = request.encrypted_id

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'encrypted_id': encrypted_id
    }

    return render(request, 'pages/index.html', context)

def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')
    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    encrypted_id = request.encrypted_id

    context = {
        'realtors': realtors,
        'encrypted_id': encrypted_id,
        'mvp_realtors': mvp_realtors,
    }

    return render(request, 'pages/about.html', context)

def mortgage(request):
    encrypted_id = request.encrypted_id
        
    context = {
    'encrypted_id': encrypted_id,
    }
    return render(request, 'mortgage_calculator.html', context)

def buyvsrent(request):
    encrypted_id = request.encrypted_id
        
    context = {
    'encrypted_id': encrypted_id,
    }
    return render(request, 'buyvsrent.html', context)


def my_view(request):
    # user_ip = request.META.get('REMOTE_ADDR', '')
    # geolocation_info = get_geolocation_info(user_ip)

    fake_ip_address = '118.101.197.197'  # Replace with the desired fake IP address

    geolocation_info = get_geolocation_info(fake_ip_address)

    return render(request, 'database_info.html', {'geolocation_info': geolocation_info})

def space(request):
    encrypted_id = request.encrypted_id
    # Fetch all CustomerCmd instances from the database
    all_customercmds = CustomerCmd.objects.all()
    all_replies = Reply.objects.all()
    all_realtors = Realtor.objects.all()

    # Pass the data to the template context
    context = {
        'customerCmds': all_customercmds,
        'all_replies': all_replies,
        'all_realtors': all_realtors,
        'encrypted_id': encrypted_id,
    }

    return render(request, 'space.html', context)

def sendInquiry(request):
    if request.method == 'POST':
        command_text = request.POST.get('command_text')

        # Validate form data
        if not command_text:
            messages.error(request, 'Command text is required.')
            return redirect('space')  # Redirect to the same view if validation fails

        # Escape the command_text to prevent XSS
        command_text = escape(command_text)
        # Create a new CustomerCmd instance and save it to the database
        try:
            CustomerCmd.objects.create(user=request.user, command_text=command_text)
            messages.success(request, 'Inquiry Uploaded')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return redirect('space')

def reply(request):
    if request.method == 'POST':
        command_text_id = request.POST.get('user_command')
        reply_text = request.POST.get('reply_text')

        # Validate form data
        if not command_text_id or not reply_text:
            messages.error(request, 'Invalid reply data.')
            return redirect('space')  # Redirect to the 'space' view if validation fails

        # Retrieve the CustomerCmd instance based on the ID
        try:
            customer_cmd_instance = CustomerCmd.objects.get(pk=command_text_id)

            # Create a new reply instance and save it to the database
            Reply.objects.create(user=request.user, user_command=customer_cmd_instance, reply_text=reply_text)
            messages.success(request, 'Reply Successful')
        except CustomerCmd.DoesNotExist:
            messages.error(request, 'Invalid user command ID.')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return redirect('space')

def delete_command(request, command_id):
    command = get_object_or_404(CustomerCmd, id=command_id)

    # Check if the user is the author of the command
    if request.user == command.user:
        command.delete()
        messages.success(request, 'Command Deleted')

    return redirect('space')

def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Check if the user is the author of the command
    if request.user == reply.user:
        reply.delete()
        messages.success(request, 'Reply Deleted')

    return redirect('space')