from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('CreateListing', views.listingCreate, name="CreateListing"),
    path('compare_listings/', views.compare_listings, name='compare_listings'), 

]