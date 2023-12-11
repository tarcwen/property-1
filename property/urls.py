from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from property.views import error_404, error_500

handler404 = 'property.views.error_404'
handler500 = 'property.views.error_500'

urlpatterns = [
    path('', include('mysite.urls')),
    path('admin/', admin.site.urls),
    path('contacts/', include('contacts.urls')),
    path('listing/', include('listing.urls')),
    path('accounts/', include('accounts.urls')),
    path('realtors/', include('realtors.urls')),
    path('rating/', include('rating.urls')),
    path('event/', include('event.urls')),
    path("django-check-seo/", include("django_check_seo.urls")),

]

# Include these lines once
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
