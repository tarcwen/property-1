from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from rating.models import Rating
from django.contrib.auth.models import Group
from decimal import Decimal, InvalidOperation

# Create your views here.
def rating(request):
    if request.method == 'POST' and request.user.is_authenticated:
        rating_value_str = request.POST.get('ratingRadio')
        realtor_id = request.POST['realtorsID']
        rateBy_id = request.user.id

        # Check if the user is in the 'customer' group
        if request.user.groups.filter(name='customer').exists():
            # Check if the user has already rated the realtor
            if not Rating.objects.filter(rateBy_id=rateBy_id, realtor_id=realtor_id).exists():
                try:
                    # Convert the rating_value to a Decimal
                    rating_value = Decimal(rating_value_str)
                    rating = Rating(rating_value=rating_value, realtor_id=realtor_id, rateBy_id=rateBy_id)
                    rating.save()
                    messages.success(request, 'Thanks For Your Rating')
                    return redirect('/realtors/SelectedRealtors/'+realtor_id)
                except InvalidOperation:
                    messages.error(request, 'Invalid rating value. Please enter a valid number.')
            else:
                messages.error(request, 'You have already rated this realtor')
        else:
            messages.error(request, 'You do not have permission to rate realtors')

    return redirect('/realtors/SelectedRealtors/'+realtor_id)