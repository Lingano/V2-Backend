from django.contrib import admin
from .models import Company

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'economic_sector')
    list_filter = ('country_of_origin', 'economic_sector')
    search_fields = ('name', 'description')
    ordering = ('name',)
