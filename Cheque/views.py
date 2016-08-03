from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader

from Cheque.models import Cheque

def success(request):
    template = loader.get_template('cheque/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request));


def save(request):
    cheque_data = {
                    'cheque_name':request.POST['cheque_name'],
                    'cheque_amount':request.POST['cheque_amount'],
                    'cheque_date' : request.POST['cheque_date'],
                    'cheque_number' : request.POST['cheque_number'],
                    'cheque_remark' :request.POST['cheque_remark'],
                   }
    Cheque.save_cheque(cheque_data)

    return HttpResponseRedirect(reverse('cheque:list'));

def index(request):

    number = request.GET['cheque_number'] if request.GET else ''
    name = request.GET['cheque_name'] if request.GET else ''
    date_search = request.GET['cheque_date'] if request.GET else ''
    cheque_list = Cheque.objects.filter(number__icontains=number.strip(), name__icontains=name.strip())
    if date_search != '':
        cheque_list = cheque_list.filter(date__exact=date_search)


    template = loader.get_template('cheque/list.html')
    context = {
        'cheque_list': cheque_list,
    }
    return HttpResponse(template.render(context, request));




