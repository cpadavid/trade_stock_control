# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'newStock/', views.newStock, name='newStock'),
    url(r'checkStock/', views.checkStock, name='checkStock'),
    url(r'sellStock/', views.sellStock, name='sellStock'),
    url(r'packStock/', views.packStock, name='packStock'),
    url(r'refillStock/', views.refillStock, name='refillStock'),
    url(r'editStock/', views.editStock, name='editStock'),
    url(r'calcStock/', views.calcStock, name='calcStock'),
    # url(r'genInvoiceStock/', views.genInvoiceStock, name='genInvoiceStock'),
    url(r'checkInStoreOrderHist/', views.checkInStoreOrderHist, name='checkInStoreOrderHist'),
    # url(r'sendInvoice/', views.sendInvoice, name='sendInvoice'),
    url(r'sellInstoreOrder/', views.sellInstoreOrder, name='sellInstoreOrder'),
    # url(r'getStock/', views.getStock, name='getStock'),
    url(r'genOrderHistExcel/', views.genOrderHistExcel, name='genOrderHistExcel'),
]
