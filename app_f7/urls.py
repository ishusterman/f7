from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [

    #url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    #url(r'^save/', views.save, name='save'),
    url(r'^logoff/', views.logoff, name='logoff'),
    url(r'^$', views.index, name='index'),
    #url(r'^test/', views.test_formset, name='test_formset'),
    url(r'^report1/', views.report, name='report'),
    url(r'^report2/', views.report, name='report'),
    url(r'^report3/', views.report, name='report'),
    #url(r'^report1_show/', views.report1, name='report1'),

    ]
