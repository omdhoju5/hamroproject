from django.conf.urls import url

from . import views

app_name = 'cheque'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^success/$', views.success, name='success'),
    # url(r'^list/$', views.list , name='list'),
    # #ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$',views.detail , name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    #  ex: /polls/5/vote/
    url(r'^save/$', views.save, name='save'),
]