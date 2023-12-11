from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact, ContactBackup
from realtors.models import Realtor
from profileOTP.models import Profile
from django.urls import reverse_lazy
from accounts.forms import AccountForm, PasswrodChangingFrom  
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from mysite.utils import encrypt_id, decrypt_id
import pyotp
import qrcode
from django.http import HttpResponseBadRequest
import os
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Validate username length
    if len(username) <= 5:
      messages.error(request, 'Username must be at least 6 characters long')
      return redirect('register')
    
     # Validate password length and complexity
    try:
      validate_password(password)
    except ValidationError as e:
      messages.error(request, ', '.join(e.messages))
      return redirect('register')

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Create user
          user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
          
          totp = pyotp.TOTP(pyotp.random_base32())
          otp_secret = totp.secret

          totp_generate = pyotp.TOTP(otp_secret)
          otp_url = totp_generate.provisioning_uri(name=user.username, issuer_name='YourApp')

          # Generate a unique filename for the QR code image
          filename = f'qrcode_{user.username}.png'

          # Generate and save the QR code image
          image_path = generate_qrcode_image(otp_url, filename)

          

          # Create and associate OTP secret with the user
          profile = Profile.objects.create(user=user, otp_secret=otp_secret, qr_code_image=image_path)
          # Add user to the 'customer' group
          group = Group.objects.get(name='customer')
          user.groups.add(group)

          # Save changes
          user.save()
          profile.save()

          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')
  
def realtors_register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    phone = request.POST['phone']
    password = request.POST['password']
    password2 = request.POST['password2']
     # Validate username length
    if len(username) <= 5:
      messages.error(request, 'Username must be at least 6 characters long')
      return redirect('realtors_register')
    
     # Validate password length and complexity
    try:
      validate_password(password)
    except ValidationError as e:
      messages.error(request, ', '.join(e.messages))
      return redirect('realtors_register')

    # Validate phone number using regex
    phone_regex = re.compile(r'^0[0-9]{9,10}$')
    if not phone_regex.match(phone):
        messages.error(request, 'Phone number must start with "0" followed by 10 digits.')
        return redirect('realtors_register')

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('realtors_register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('realtors_register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          group = Group.objects.get(name='realtor')
          user.groups.add(group)
          user.save()
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')

          # Create a Realtor instance for the user
          realtor = Realtor(name=first_name + ' ' + last_name, phone=phone, email=email, user_id=user.id)
          realtor.save()

          totp = pyotp.TOTP(pyotp.random_base32())
          otp_secret = totp.secret
          totp_generate = pyotp.TOTP(otp_secret)
          otp_url = totp_generate.provisioning_uri(name=user.username, issuer_name='YourApp')

          # Generate a unique filename for the QR code image
          filename = f'qrcode_{user.username}.png'

          # Generate and save the QR code image
          image_path = generate_qrcode_image(otp_url, filename)
          # Create and associate OTP secret with the user
          profile = Profile.objects.create(user=user, otp_secret=otp_secret, qr_code_image=image_path)
          profile.save()

          messages.success(request, 'You are now registered and can log in as realtor')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('realtors_register')
  else:
    return render(request, 'accounts/realtors_register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
       # Check if the user has a PyOTP secret stored (you may need to adapt this part based on your user model)
      if hasattr(user, 'profile') and hasattr(user.profile, 'otp_secret'):
        # User has PyOTP secret, check OTP
        encrypted_id = encrypt_id(user.id) #get the user id and encrypt
        return redirect('display_qr_code', encrypted_id=encrypted_id)
      else:
        # admin
        auth.login(request, user)
        messages.success(request, 'You are now logged in')
        return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def generate_qrcode_image(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file in the media directory
    media_root = settings.MEDIA_ROOT
    image_path = os.path.join(media_root, 'qrcodes', filename)
    img.save(image_path)

    return image_path

def verify_otp(request, encrypted_id):
    decrypted_id = decrypt_id(encrypted_id)
    user = get_object_or_404(User, id=decrypted_id)
    if request.method == 'POST':
        
        otp_code = request.POST.get('otp_code')

        # Check if the OTP code is valid
        totp = pyotp.TOTP(user.profile.otp_secret)
        if totp.verify(otp_code):
            # Mark the QR code as scanned
            user.profile.is_qr_code_scanned = True
            user.profile.save()
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP code')
            return redirect('display_qr_code', encrypted_id=encrypted_id)
    else:
        return HttpResponseBadRequest('Invalid request method')

def display_qr_code(request, encrypted_id):
    decrypted_id = decrypt_id(encrypted_id)
    user = get_object_or_404(User, id=decrypted_id)

    if hasattr(user, 'profile') and hasattr(user.profile, 'otp_secret'):
        # Check if the QR code has already been scanned
        if user.profile.is_qr_code_scanned:
            messages.success(request, 'Qr code already scanned')
            scanned = user.profile.is_qr_code_scanned
            encrypted_id = encrypt_id(user.id)
            context = {
                'scanned' : scanned,
                'encrypted_id': encrypted_id,
            }
            return render(request, 'accounts/display_qr_code.html', context)

        image_path = user.profile.qr_code_image
        encrypted_id = encrypt_id(user.id)

        context = {
            'qr_code_img': image_path,
            'encrypted_id': encrypted_id,
        }

        return render(request, 'accounts/display_qr_code.html', context)

    return render(request, 'accounts/display_qr_code.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

def dashboard(request):
  encrypted_id = request.encrypted_id
  # Get the first user group
  user_group = request.user.groups.first()
  if user_group and user_group.name == 'customer':
    user_contacts = Contact.objects.order_by('-contact_date_start').filter(user_id=request.user.id)
    user_contact_backups = ContactBackup.objects.order_by('-backup_date').filter(user_id=request.user.id)
  elif user_group and user_group.name == 'realtor':
    realtor = get_object_or_404(Realtor, user_id=request.user.id)
    user_contacts = Contact.objects.order_by('-contact_date_start').filter(realtor_id=realtor)
    user_contact_backups = ContactBackup.objects.order_by('-backup_date').filter(realtor_id=realtor)
  else:
        # Handle other cases or set user_contacts to an empty queryset
        user_contacts = Contact.objects.none()
        user_contact_backups = ContactBackup.objects.none()

  context = {
    'contacts': user_contacts,
    'user_contact_backups': user_contact_backups,
    'encrypted_id': encrypted_id
  }
  
  return render(request, 'accounts/dashboard.html', context)

def selection(request):
  encrypted_id = request.encrypted_id
  context = {
        'encrypted_id': encrypted_id,
    }
  return render(request, 'accounts/selection.html', context)

def UpdateCustomerProfile(request, encrypted_id):
  
  decrypted_id = decrypt_id(encrypted_id)
  selectedUser = get_object_or_404(User, id=decrypted_id)
  form = AccountForm(instance=selectedUser)
  if request.method == 'POST':
      form = AccountForm(request.POST, instance=selectedUser)
      if form.is_valid():
          form.save()
          return redirect("dashboard")
        
  return render(request, 'accounts/customerProfile.html', {'form': form, 'encrypted_id': encrypted_id})

class PasswordsChangeView(PasswordChangeView):
  from_class = PasswrodChangingFrom
  success_url = reverse_lazy('login')