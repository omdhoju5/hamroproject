from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db import connection
from django.utils import timezone

# Create your models here.

from Stock.models import Item


class Invoice(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    comment = models.TextField()
    issued_by = models.CharField(max_length=100)
    subtotal = models.FloatField()
    additional_charge = models.FloatField()
    total = models.FloatField()
    created_at = models.DateField(editable=False)
    updated_at = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Invoice, self).save(*args, **kwargs)

    def validate_data(self,invoice_data):
        for k,v in invoice_data.items():
            if (v == ''):
                raise EmptyValueException({"error_message": "Please enter all the values properly"})

        return

    @staticmethod
    def save_invoice(invoice_data,invoice=None):
        if(invoice == None):
            invoice = Invoice()

        invoice.name = invoice_data['client_name'] if invoice_data['client_name'] else ''
        invoice.address = invoice_data['client_address'] if invoice_data['client_address'] else ''
        invoice.number = invoice_data['invoice_number'] if invoice_data['invoice_number'] else ''
        invoice.comment = invoice_data['comment'] if invoice_data['comment'] else ''
        invoice.issued_by = invoice_data['issued_by'] if invoice_data['issued_by'] else ''
        invoice.date = invoice_data['date'] if invoice_data['date'] else ''
        invoice.subtotal = invoice_data['subtotal'] if invoice_data['subtotal'] else ''
        invoice.additional_charge = invoice_data['additional'] if invoice_data['additional'] else ''
        invoice.total = invoice_data['total'] if invoice_data['total'] else ''

        return invoice


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='detail')
    item = models.ForeignKey('Stock.Item', on_delete=models.CASCADE , related_name='stock')
    rate = models.FloatField()
    quantity = models.FloatField()
    amount = models.FloatField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(editable=False)
    updated_at = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(InvoiceDetail, self).save(*args, **kwargs)

    @staticmethod
    def save_invoice_detail(invoice_data , invoice):
        if invoice.detail.exists():
            all_details = invoice.detail.all().order_by('id')

        details = {}
        for i in range(1, 7):
            index = i - 1
            if invoice.detail.exists():   #if details of invoice exists
                if len(all_details) > index:   #  Number of invoice details in greater than index
                    detail = all_details[index]  #
                else:
                    detail = InvoiceDetail() #for new entry of invoice detail from edit
            else:
                detail = InvoiceDetail()  #for new invoice creation
            detail.invoice = invoice
            if invoice_data['item-'+str(i)] == '' or invoice_data['quantity-'+str(i)] == '' or invoice_data['rate-'+str(i)] == '' or invoice_data['total-'+str(i)] == '':
                break

            detail.item = Item.objects.get(pk=invoice_data['item-'+str(i)])
            detail.rate = invoice_data['rate-'+str(i)]
            detail.quantity = invoice_data['quantity-'+str(i)]
            detail.amount = invoice_data['total-'+str(i)]

            details[str(i)] = detail

        return details


class Sales:

    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]

    @staticmethod
    def get_sales(self,from_date, to_date):
        cursor = connection.cursor()
        query = """select a.item_id, a.item_name , a.sales_quantity , a.sales_amount , b.stock_quantity , b.stock_amount , b.stock_quantity - a.sales_quantity as remaining_quantity , a.sales_amount - b.stock_amount as profit from
        (
            select item.name as item_name, item.id as item_id , sum(sales.quantity) as sales_quantity, sum(sales.amount) as sales_amount
            from public."Stock_item" item
            inner join public."Sales_invoicedetail" sales
            on item.id = sales.item_id
            WHERE sales.created_at::date = %s
            group by item.id
        ) a
            inner join

        (
            select item.name as item_name, item.id as item_id, sum(incoming.quantity) as stock_quantity, sum(incoming.amount) as stock_amount from public."Stock_item" item
            left join public."Stock_incomingitem" incoming
            on item.id = incoming.code_id
            WHERE incoming.created_at::date = %s
            group by item.id
        )  b
        on a.item_id = b.item_id """;

        cursor.execute(query,from_date,to_date);
        row = self.dictfetchall(cursor)
        return row


class EmptyValueException(Exception):
    pass