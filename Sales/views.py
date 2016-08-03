from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader

from Sales.models import Invoice, EmptyValueException, InvoiceDetail, Sales
from Stock.models import Item


def index(request):
    template = loader.get_template('sales/create_invoice.html')
    context = {

    }
    return HttpResponse(template.render(context, request));


def make_invoice(request):
    if (not request.POST):
        stock_items = Item.objects.all()

        template = loader.get_template('sales/create_invoice.html')

        context = {
            'stock_items': stock_items,
        }
        return HttpResponse(template.render(context, request));

    try:
        invoice = Invoice.save_invoice(request.POST, None)
        invoice.save()
        invoice_details = InvoiceDetail.save_invoice_detail(request.POST, invoice)


    except EmptyValueException as e:
        error = e.args[0]
        return render(request, 'sales/create_invoice.html', {
            'error_message': error["error_message"],
        })

    else:
        for invoice_detail in invoice_details.itervalues():
            invoice_detail.save()

    return HttpResponseRedirect(reverse('sales:make_invoice'));


def edit(request, invoice_id):
    try:
        if (not request.POST):
            stock_items = Item.objects.all()
            invoice = Invoice.objects.get(pk=invoice_id)
            if invoice.detail.exists():
                invoice_details = invoice.detail.all().order_by('id')
            else:
                invoice_details = ''

            template = loader.get_template('sales/edit_invoice.html')

            context = {
                'invoice_id': invoice_id,
                'stock_items': stock_items,
                'invoice': invoice,
                'invoice_details': invoice_details,
            }
            return HttpResponse(template.render(context, request))

        invoice_to_pass = Invoice.objects.get(pk=invoice_id)
        invoice = Invoice.save_invoice(request.POST, invoice_to_pass)
        invoice.save()
        invoice_details = InvoiceDetail.save_invoice_detail(request.POST, invoice)


    except EmptyValueException as e:
        error = e.args[0]
        return render(request, 'sales/edit_invoice.html', {
            'error_message': error["error_message"],
        })
    except Exception as ex:
        return HttpResponseRedirect(reverse('sales:make_invoice'));
        # return render(request, 'sales/create_invoice.html', {
        #     'error_message': ex,
        # })

    else:
        for invoice_detail in invoice_details.itervalues():
            invoice_detail.save()

    return HttpResponseRedirect(reverse('sales:make_invoice'));


def list_invoice(request):
    try:
        invoices = Invoice.objects.all().order_by('date').filter(is_active=True, is_deleted=False)

        template = loader.get_template('sales/list_invoice.html')

        context = {
            'invoices': invoices,
        }
    except Exception as e:
        return render(request, 'sales/list_invoice.html', {
            'error_message': e,
            'invoices': invoices,
        })

    return HttpResponse(template.render(context, request))


def delete_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        if invoice.is_deleted is False:
            invoice.is_deleted = True
        else:
            invoice.is_deleted = False

        invoice.save()

        invoices = Invoice.objects.all().order_by('date').filter(is_active=True, is_deleted=False)

        template = loader.get_template('sales/list_invoice.html')

        context = {
            'invoices': invoices,
        }

    except Exception as e:
        invoices = Invoice.objects.all().order_by('date').filter(is_active=True, is_deleted=False)
        return render(request, 'sales/list_invoice.html', {
            'error_message': e,
            'invoices': invoices,
        })
    return HttpResponse(template.render(context, request))


def show_sales(request):
    try:
        if (not request.POST):
            sales = Sales.get_sales(from_date=None, to_date=None)
        else:
            from_date = request.POST['from_date'] if request.POST['from_date'] != '' else ''
            to_date = request.POST['to_date'] if request.POST['to_date'] != '' else ''
            sales = Sales.get_sales(from_date=from_date, to_date=to_date)
    except Exception as e:

    return sales
