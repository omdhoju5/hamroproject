from django.conf.urls import url

from . import views

app_name = 'sales'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^makeinvoice/$', views.make_invoice, name='make_invoice'),
    url(r'^edit/(?P<invoice_id>(\d+))/$',views.edit, name='edit_invoice'),
    url(r'^edit/(?P<invoice_id>)/$', views.edit, name='edit_invoice'),
    url(r'^invoice/list/$', views.list_invoice, name='list_invoice'),
    # url(r'^dispatch/(?P<item_id>(\d+))/$',views.dispatch , name='dispatch_item')

    # url(r'^save/$', views.save, name='save'),
]

# url(r'^list/$', views.list , name='list'),
# #ex: /polls/5/
# url(r'^(?P<question_id>[0-9]+)/$',views.detail , name='detail'),
# # ex: /polls/5/results/
# url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#  ex: /polls/5/vote/