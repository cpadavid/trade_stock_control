# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

IN_STORE = 'INSTORE'
PRE_ORDER = 'PREORDER'
IN_STORE_DISPLAY = 'In-Store'
PRE_ORDER_DISPLAY = 'Pre-Order'

class Admin(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    user_name = models.CharField(max_length=50)
    user_pw = models.CharField(max_length=50)
    last_modified_time = models.DateTimeField(auto_now=True)
    

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    item_no = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    stock_type = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    last_modified_time = models.DateTimeField(auto_now=True)
    

class InStoreOrderHist(models.Model):
    instore_order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    tel_no = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    remark = models.CharField(max_length=200)
    last_modified_time = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50)
    

class InStoreOrderStock(models.Model):
    inStoreOrderHist = models.ForeignKey(InStoreOrderHist, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order_status = models.CharField(max_length=50)
    
    @property
    def total_price(self):
        return self.stock.price * self.quantity

    @property
    def display_status(self):
        if self.order_status == IN_STORE:
            return IN_STORE_DISPLAY
        elif self.order_status == PRE_ORDER:
            return PRE_ORDER_DISPLAY
        else:
            return self.order_status
        
    
class StockTransHist(models.Model):
    hist_id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    in_out = models.CharField(max_length=50)
    last_modified_time = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=50)
