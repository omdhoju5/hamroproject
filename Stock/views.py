import re

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from Stock.models import Item, IncomingItem, DispatchingItem, ReturningItem
from Stock.models import EmptyValueException


def index(request):
    name = request.GET['stock_name'] if request.GET else ''
    stock_list = Item.objects.filter(Q(name__icontains=name.strip()) | Q(identifier__icontains=name.strip()))
    template = loader.get_template('stock/list_stock.html')
    context = {
        'stock_list': stock_list,

    }
    return HttpResponse(template.render(context, request));


def add(request):
    if (not request.POST):
        template = loader.get_template('stock/add_item.html')

        context = {

        }
        return HttpResponse(template.render(context, request));

    try:
        stock_data = {
            'stock_name': request.POST['stock_name'],
            'stock_identifier': request.POST['stock_identifier'],
            'stock_company': request.POST['stock_company'],
        }
        stock = Item.save_stock(stock_data)

    except EmptyValueException as e:
        error = e.args[0]
        return render(request, 'stock/add_item.html', {
            'error_message': error["error_message"],
        })

    else:
        stock.save()

    return HttpResponseRedirect(reverse('stock:index'));


def add_in_stock(request, item_id=''):
    if (not request.POST):
        stock_items = Item.objects.all()
        if (not item_id == ''):
            stock = Item.objects.get(pk=item_id)
        else:
            stock = ''
        template = loader.get_template('stock/add_stock.html')
        context = {
            'stock': stock,
            'stock_items': stock_items,
        }
        return HttpResponse(template.render(context, request));
    else:
        try:
            incoming_item = IncomingItem.save_stock(request.POST)

        except EmptyValueException as e:
            error = e.args[0]
            return render(request, 'stock/add_stock.html', {
                'error_message': error["error_message"],
            })

        else:
            incoming_item.save()

    return HttpResponseRedirect(reverse('stock:received'));


def received(request):
    code_id = request.GET['stock_id'] if request.GET else ''
    stock_items = Item.objects.all()
    if(code_id != ''):
        items = IncomingItem.objects.filter(code_id=code_id)
    else:
        items = IncomingItem.objects.all()
    template = loader.get_template('stock/incoming_item.html')
    context = {
        'items': items,
        'stock_items': stock_items,
    }
    return HttpResponse(template.render(context, request));


def dispatch(request, item_id=''):
    stock_items = Item.objects.all()
    if (not request.POST):
        if (not item_id == ''):
            stock = Item.objects.get(pk=item_id)
        else:
            stock = ''
        template = loader.get_template('stock/add_dispatch.html')
        context = {
            'stock': stock,
            'stock_items': stock_items,
        }
        return HttpResponse(template.render(context, request));
    else:
        try:
            dispatch_item = DispatchingItem.dispatch(request.POST)

        except EmptyValueException as e:
            error = e.args[0]
            return render(request, 'stock/add_dispatch.html', {
                'error_message': error["error_message"],
                'stock_items': stock_items,
            })

        else:
            dispatch_item.save()

    return HttpResponseRedirect(reverse('stock:dispatched'));


def dispatched(request):
    stock_id = request.GET['stock_id'] if request.GET else ''
    stock_items = Item.objects.all()
    if(stock_id != ''):
        items = DispatchingItem.objects.filter(code_id=stock_id)
    else:
        items = DispatchingItem.objects.all()
    template = loader.get_template('stock/dispached.html')
    context = {
        'items': items,
        'stock_items': stock_items,
    }
    return HttpResponse(template.render(context, request));


def returned(request):
    code_id = request.GET['stock_id'] if request.GET else ''
    stock_items = Item.objects.all()
    if(code_id != ''):
        items = ReturningItem.objects.filter(code_id=code_id)
    else:
        items = ReturningItem.objects.all()
    template = loader.get_template('stock/returned.html')
    context = {
        'items': items,
        'stock_items': stock_items,
    }
    return HttpResponse(template.render(context, request));


def return_item(request, item_id=''):
    stock_items = Item.objects.all()
    if (not request.POST):
        if (not item_id == ''):
            stock = Item.objects.get(pk=item_id)
        else:
            stock = ''
        template = loader.get_template('stock/add_returned.html')
        context = {
            'stock': stock,
            'stock_items': stock_items,
        }
        return HttpResponse(template.render(context, request));
    else:
        try:
            dispatch_item = ReturningItem.returned(request.POST)

        except EmptyValueException as e:
            error = e.args[0]
            return render(request, 'stock/add_returned.html', {
                'error_message': error["error_message"],
                'stock_items':stock_items,
            })

        else:
            dispatch_item.save()

    return HttpResponseRedirect(reverse('stock:returned'));

# def test (request):
#     f = open('assignment_find_sum.txt', 'r')
#     sum = 0
#     list_of_numbers = []
#     for line in f:
#         print line
#         list_of_numbers.extend(re.findall('[0-9.]+'), line)
#     for i, val in enumerate(list_of_numbers):
#         sum = sum + val
#
#     f.close()
#     return

# def test(request):
#     name = request.GET['stock_id'] if request.GET else ''
#     stock_items = Item.objects.filter(name__icontains=name)
#     items = IncomingItem.objects.all()
#     template = loader.get_template('stock/incoming_item.html')
#     context = {
#         'items': items,
#         'stock_items': stock_items,
#     }
#     return HttpResponse(template.render(context, request));
