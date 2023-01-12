from django.db import models
from django_extensions.db.models import TimeStampedModel

from users.models import BaseUser


class RealEstateItem(TimeStampedModel):
    """
    RealEstateItem model
    """
    description = models.TextField(blank=True, default='')
    address = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, verbose_name="owner of Item"
    )

    class Meta:
        ordering = ["created"]
