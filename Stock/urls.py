from django.conf.urls import url

from . import views

app_name = 'stock'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^received/$', views.received, name='received'),
    url(r'^receive/$', views.add_in_stock, name='add_in_stock'),
    url(r'^receive/(?P<item_id>(\d+))/$',views.add_in_stock , name='add_in_stock'),
    url(r'^dispatched/$', views.dispatched, name='dispatched'),
    url(r'^dispatch/$', views.dispatch, name='dispatch_item'),
    url(r'^dispatch/(?P<item_id>(\d+))/$',views.dispatch , name='dispatch_item'),
    url(r'^returned/$', views.returned, name='returned'),
    url(r'^return_item/$', views.return_item, name='return_item'),
    url(r'^return_item/(?P<item_id>(\d+))/$',views.return_item , name='return_item'),

    # url(r'^save/$', views.save, name='save'),
]

# url(r'^list/$', views.list , name='list'),
# #ex: /polls/5/
# url(r'^(?P<question_id>[0-9]+)/$',views.detail , name='detail'),
# # ex: /polls/5/results/
# url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#  ex: /polls/5/vote/