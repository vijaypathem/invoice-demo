from django.urls import path 
from .views import invoice_list_create, invoice_detail

urlpatterns = [
    path('invoices/',invoice_list_create,name='invoice_list_create'),
    path('invoices/<int:pk>/',invoice_detail,name='invoice_detail'),
]