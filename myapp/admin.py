from django.contrib import admin

# Register your models here.
from .models import Invoice, InvoiceDetails

admin.site.register(Invoice)
admin.site.register(InvoiceDetails)