from django.contrib import admin

from .models import RealEstateItem


@admin.register(RealEstateItem)
class RealEstateItemAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "address", "created_by", "price")
