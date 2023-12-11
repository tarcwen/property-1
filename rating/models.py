from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from realtors.models import Realtor

class Rating(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
    rateBy = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_value = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    rated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name