from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse 
from event.models import Events 
from contacts.models import Contact
 
# Create your views here.
def index(request):  
    all_events = Contact.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'event/index.html',context)
 
def all_events(request):                                                                                                 
    all_events = Contact.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.listing.title,                                                                                         
            'id': "Appt-" + str(event.id),                                                                                              
            'start': event.contact_date.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.contact_date.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
