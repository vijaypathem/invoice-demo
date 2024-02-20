from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Invoice, InvoiceDetails
from .serializers import InvoiceSerializer, InvoiceDetailsSerializer


class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date' : '2024-02-20',
            'customer_name' : 'Test Customer'
        }
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_detail_data = {
            'invoice' : self.invoice,
            'description': 'Test Description',
            'quantity' : 2,
            'unit_price':10.0,
            'price':20.0
        }
        self.invoice_detail = InvoiceDetails.objects.create(**self.invoice_detail_data)

    def test_create_invoice(self):
        url = reverse('invoice_list_create')
        data = {
            'date': '2024-02-21',
            'customer_name' : 'New Customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_read_invoice_list(self):
        url = reverse('invoice_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['customer_name'],self.invoice_data['customer_name'])

    def test_read_invoice_detail(self):
        url = reverse('invoice_detail',args=[self.invoice.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'],self.invoice_data['customer_name'])

    def test_update_invoice(self):
        url = reverse('invoice_detail',args=[self.invoice.id])
        updated_data = {
            'date':'2024-02-22',
            'customer_name': 'Updated Customer'
        }
        response = self.client.put(url,updated_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.customer_name,updated_data['customer_name'])

    def test_delete_invoice(self):
        url = reverse('invoice_detail',args=[self.invoice.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(),0)



class InvoiceDetailAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date': '2024-02-20',
            'customer_name':'Test Customer'
        }
        self.invoice = Invoice.objects.create(**self.invoice_data)
        self.invoice_detail_data = {
            'invoice':self.invoice,
            'description':'Test Description',
            'quantity':2,
            'unit_price':10.0,
            'price':20.0
        }
        self.invoice_detail = InvoiceDetails.objects.create(**self.invoice_detail_data)

    def test_create_invoice_detail(self):
        url = reverse('invoice_list_create')
        data = {
            'date':'2024-02-21',
            'customer_name':'New Customer',
            'details':[
                {
                    'description':'Test Description',
                    'quantity':2,
                    'unit_price':10.0,
                    'price':20.0
                }
            ]
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetails.objects.count(),1)

    def test_read_invoice_detail_list(self):
        url = reverse('invoice_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(len(response.data[0]['details']),1)
        self.assertEqual(response.data[0]['details'][0]['description'],self.invoice_detail_data['description'])

    def test_update_invoice_detail(self):
        url = reverse('invoice_detail',args=[self.invoice_detail.id])
        updated_data = {
            'date' : '2024-02-22',
            'customer_name':'Updated Customer',
            'details':[
                {
                'description':'Updated Description',
                'quantity':3,
                'unit_price':15.0,
                'price':45.0
                }
            ]
        }
        response = self.client.put(url,updated_data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.invoice_detail.refresh_from_db()
        #self.assertEqual(self.invoice_detail.description, updated_data['details'][0]['description'])

    def test_delete_invoice_detail(self):
        url = reverse('invoice_detail',args=[self.invoice.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetails.objects.count(),0)