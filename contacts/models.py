from django.db import models
from datetime import datetime
from realtors.models import Realtor
from django.contrib.auth.models import User
from listing.models import Listing

class Contact(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  message = models.TextField(blank=True)
  status = models.CharField(max_length=100, default='Upcoming')
  contact_date_start = models.DateTimeField(blank=True)
  contact_date_end = models.DateTimeField(blank=True)
  realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  def __str__(self):
        return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

      # Check if status is 'done'
    if self.status.lower() == 'complete' or  self.status.lower() == 'cancel':
      # Create ContactRecord instance with booking date as contact_date_start
      ContactBackup.objects.create(
        listing =self.listing,
        appointment_id = self.id,
        name = self.name,
        email = self.email,
        phone = self.phone,
        message = self.message,
        status = self.status,
        contact_date_start = self.contact_date_start,
        contact_date_end = self.contact_date_end,
        realtor = self.realtor,
        user = self.user,
      )

      # Delete the original Contact instance
      self.delete()

class ContactBackup(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    appointment_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=100, default='Upcoming')
    contact_date_start = models.DateTimeField(blank=True)
    contact_date_end = models.DateTimeField(blank=True)
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    backup_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} - {self.backup_date}"