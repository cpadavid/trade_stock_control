# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from rest_framework import status
from rest_framework.response import Response

# Model
from models import *
from django.db import connection
from django.conf import settings
from django.core.mail import EmailMessage

import datetime
import time
# import webcolors

from qrCodeHandler import *
from excelHandler import *

IN = "IN"
OUT = "OUT"


# Stock Table
def getStockTable():

    try:
        entryList = Stock.objects.all()
        return entryList
    except Exception as e:
        raise e


def getStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        stockId = str(data['stockId'])
        return getStock(stockId)
    except Exception as e:
        raise e

        
def getStock(stockId):
    try:
        print stockId
        entry = Stock.objects.get(pk=stockId)
        print entry
        return entry
    except Exception as e:
        raise e


def newStockHandler(request):

    try:
        data = request.data
        
        dataCost = int(data['cost'])
        dataPrice = int(data['price'])
        dataQty = int(data['qty'])
        dataColor = data['color']
        
        # webcolors.hex_to_name(dataColor)
        
        if dataCost < 0 or dataPrice < 0:
            raise ValueError("Stock Cost or Price cannot smaller then 0.")
        elif dataQty < 0:
            raise ValueError("Quantity cannot smaller then 0.")
        
        stockInstance = Stock.objects.create(
            item_no = data['itemNo'], 
            description = data['desc'], 
            stock_type = data['type'],
            color = data['color'],
            size = data['size'],
            cost = data['cost'],
            price = data['price'],
            quantity = data['qty']
        )
        
        updateTransHist(stockInstance.pk, data['qty'], IN)
        
        generateQrCodeHandler(stockInstance)
        
    except Exception as e:
        raise e
    

def checkStockHandler(request):
    
    try:
        # data = json.loads(request.body)
        data = request.data
        
        itemNo = data['checkItemNo']
        desc = data['checkDesc']
        
        entryList = Stock.objects.filter(item_no__icontains=itemNo, description__icontains=desc)
        
        return entryList
    except Exception as e:
        raise e


def sellStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        stockId = data["stockId"]
        stockInstance = getStock(stockId)
        stockInstance.quantity -= 1
        if stockInstance.quantity < 0:
            raise ValueError("Stock Quantity cannot small then 0.".format(e))
        else:
            updateTransHist(stockInstance.pk, 1, OUT)
            stockInstance.save()
        return getStockTable()

    except Exception as e:
        raise e


def sellMoreThenOneQtyHandler(stockId, stockQty):
    try:
        stockInstance = getStock(stockId)
        stockInstance.quantity -= int(stockQty)
        
        """
        if stockInstance.quantity < 0:
            raise ValueError("Stock Quantity cannot smaller then 0.")
        else:
            updateTransHist(stockInstance.pk, stockQty, OUT)
            stockInstance.save()
        """
        updateTransHist(stockInstance.pk, stockQty, OUT)
        stockInstance.save()
        return getStockTable()
    except Exception as e:
        raise e   
        

def packStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        stockId = data["stockId"]
        stockQty = data["quantity"]
        return sellMoreThenOneQtyHandler(stockId, stockQty)
    except Exception as e:
        raise e


def refillStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        stockId = data["stockId"]
        stockQty = data["quantity"]
        stockInstance = getStock(stockId)
        stockInstance.quantity += int(stockQty)
        updateTransHist(stockInstance.pk, stockQty, IN)
        stockInstance.save()
        return getStockTable()
    except Exception as e:
        raise e


def updateTransHist(stockId, qty, inOrOut):
    try:
        stockTransHistInstance = StockTransHist.objects.create(
            stock_id_id = stockId,
            quantity = qty,
            in_out = inOrOut
        )
    except Exception as e:
        raise e


def editStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        print data
        stockId = data["stockId"]
        itemNo = data["itemNo"]
        desc = data["desc"]
        dataType = data["type"]
        color = data["color"]
        size = data["size"]
        cost = int(data["cost"])
        price = int(data["price"])
        print stockId
        
        # webcolors.hex_to_name(data["color"])
        
        stockInstance = getStock(stockId)

        stockInstance.item_no = itemNo
        stockInstance.description = desc
        stockInstance.stock_type = dataType
        stockInstance.color = color
        stockInstance.size = size
        
        if request.user.is_superuser:
            stockInstance.cost = cost
        
        stockInstance.price = price
        if stockInstance.cost < 0 or stockInstance.price < 0:
            raise ValueError("Stock Cost or Price cannot smaller then 0.")
        # elif stockInstance.quantity < 0:
        #     raise ValueError("Quantity cannot smaller then 0.")
        else:
            stockInstance.save()
            
        generateQrCodeHandler(stockInstance)
        
        return getStockTable()
    except Exception as e:
        raise e


def calcStockHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        strFromDate = str(data["fromDate"])
        strToDate = str(data["toDate"])
        fromDate = datetime.datetime.strptime(strFromDate, "%Y-%m-%d").date()
        toDate = datetime.datetime.strptime(strToDate, "%Y-%m-%d").date()
        toDate = datetime.datetime.combine(toDate, datetime.datetime.max.time()).date()
        
        entryList = []
        if fromDate == "" or toDate == "" or fromDate is None or toDate is None:
            raise ValueError("From Date or To Date cannot be Empty.")
        elif fromDate > toDate:
            raise ValueError("From Date cannot after To Date.")
        else:
            entryList = Stock.objects.filter(stocktranshist__last_modified_time__range=(fromDate, toDate)).values('cost', 'price', 'stocktranshist__quantity', 'stocktranshist__in_out')
            print entryList.query
            
        sales, cost, profit, totalStockCost = 0, 0, 0, 0
        if len(entryList) != 0:
            print "Entry List is not empty, start calculation."
            for entry in entryList:
                print entry
                stockCost = entry['cost']
                stockPrice = entry['price']
                qty = entry['stocktranshist__quantity']
                action = entry['stocktranshist__in_out']
                
                if action == OUT:
                    sales += stockPrice*qty
                    cost += stockCost*qty
                    profit += (stockPrice - stockCost)*qty
        else:
            print "Entry List is empty."
            
        allEntryList = getStockTable()
        for allEntry in allEntryList:
            print allEntry
            totalStockCost += int(allEntry.quantity) * int(allEntry.cost)
        
        print "From To Date {}, {}".format(fromDate, toDate)        
        return sales, cost, profit, totalStockCost
    except Exception as e:
        raise e


def getInStoreOrderHistTable():
    try:
        
        entryList = InStoreOrderStock.objects.select_related('inStoreOrderHist', 'stock').all()

        returnEntryList = {}
        for order in entryList:
            histId = order.inStoreOrderHist.instore_order_id
            if histId not in returnEntryList:
                returnEntryList[histId] = []
                returnEntryList[histId].append(order)
            else:
                returnEntryList[histId].append(order)
        return returnEntryList
    except Exception as e:
        raise e


def checkInStoreOrderHistHandler(request):
    try:
        # data = json.loads(request.body)
        data = request.data
        telNo = str(data["telNo"])
        orderNo = str(data["orderNo"])
        # entryList = InStoreOrderStock.objects.select_related('inStoreOrderHist', 'stock').filter(inStoreOrderHist__tel_no__contains=telNo, inStoreOrderHist_id__contains=orderNo)
        entryList = InStoreOrderStock.objects.select_related('inStoreOrderHist', 'stock').filter(inStoreOrderHist__tel_no__contains=telNo, inStoreOrderHist__instore_order_id__contains=orderNo)
        returnEntryList = {}
        for order in entryList:
            histId = order.inStoreOrderHist.instore_order_id
            if histId not in returnEntryList:
                returnEntryList[histId] = []
                returnEntryList[histId].append(order)
            else:
                returnEntryList[histId].append(order)
        return returnEntryList
    except Exception as e:
        raise e


def sellInStoreOrderHandler(request):
    try:
        # data = json.loads(request.body)
        print "ActionHandler, sellInStoreOrderHandler"
        print request
        data = request.data
        print data
        reqName = data["name"]
        reqTelNo = data["telNo"]
        reqEmail = data["email"]
        reqRemark = data["remark"]
        selledItemList = data["selledItemList"]
        
        inStoreOrderHistInstance = InStoreOrderHist.objects.create(
            name = reqName,
            tel_no = reqTelNo, 
            email = reqEmail, 
            remark = reqRemark,
            last_modified_by = "Admin"
        )
        
        orderId = inStoreOrderHistInstance.instore_order_id
        
        for selledItem in selledItemList:
            stockId = selledItem["stockId"]
            qty = selledItem["quantity"]
            orderStatus = selledItem["orderStatus"]
            
            inStoreOrderStockInstance = InStoreOrderStock.objects.create(
                quantity = qty,
                inStoreOrderHist_id = orderId,
                stock_id = stockId,
                order_status = orderStatus
            )
            
            if orderStatus == IN_STORE:
                sellMoreThenOneQtyHandler(stockId, qty)
        
        return orderId
        
    except Exception as e:
        raise e    


def getOrderHistHandler(request):
    try:
        # Post method
        # data = request.data
        # strFromDate = str(data["fromDate"])
        # strToDate = str(data["toDate"])

        # Get method
        # print request.POST
        # strFromDate = request.GET["fromDate"]
        # strToDate = request.GET["getOrderHistTioDate"]
        
        strFromDate = "2017-01-01"
        strToDate = "2117-12-30"
        
        fromDate = datetime.datetime.strptime(strFromDate, "%Y-%m-%d").date()
        toDate = datetime.datetime.strptime(strToDate, "%Y-%m-%d").date()
        toDate = datetime.datetime.combine(toDate, datetime.datetime.max.time()).date()
        
        entryList = []
        if fromDate == "" or toDate == "" or fromDate is None or toDate is None:
            raise ValueError("From Date or To Date cannot be Empty.")
        elif fromDate > toDate:
            raise ValueError("From Date cannot after To Date.")
        else:
            entryList = InStoreOrderStock.objects.select_related('inStoreOrderHist', 'stock').filter(inStoreOrderHist__last_modified_time__range=(fromDate, toDate))
            print entryList.query
        
        returnEntryList = []
        for order in entryList:
            entry = (
                order.inStoreOrderHist.tel_no,
                order.stock.item_no,
                order.stock.description,
                order.display_status
            )
            print entry
            returnEntryList.append(entry)
            
        # xlsxName = createOrderHistExcelHandler(returnEntryList)    
        # return xlsxName
        
        xlsx_data = createOrderHistExcelHandler(returnEntryList)
        return xlsx_data
        
    except Exception as e:
        raise e
        
        
def sendInvoiceHandler(request, orderNo):
    try:
        
        data = request.data
        email = str(data["email"]).replace(" ","")
        telNo = str(data["telNo"]).replace(" ","")
        
        # Send email
        subject = 'Thanks You for shopping at Aangshop'
        message = 'Welcome to Aangshop! We very much appreciate your business.\nLooks forward to see you again !'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER, email]
        email = EmailMessage(subject,message,from_email,to_list)    
        email.attach_file('tradeStockControlApp\\static\\invoice\\{}_{}.pdf'.format(telNo, orderNo))
        email.send()
        
    except Exception as e:
        raise e
        

def voidOrderHandler(request):
    try:
        print "ActionHandler, voidOrderHandler"
        print request
        data = request.data
        print data
        reqOrderNo = data["orderNo"]
        
        inStoreOrderStockInstance = InStoreOrderStock.objects.select_related('inStoreOrderHist', 'stock').filter(inStoreOrderHist__last_modified_time__range=(fromDate, toDate))
        
        inStoreOrderHistInstance = InStoreOrderHist.objects.create(
            name = reqName,
            tel_no = reqTelNo, 
            email = reqEmail, 
            remark = reqRemark,
            last_modified_by = "Admin"
        )
        
        orderId = inStoreOrderHistInstance.instore_order_id
        
        for selledItem in selledItemList:
            stockId = selledItem["stockId"]
            qty = selledItem["quantity"]
            orderStatus = selledItem["orderStatus"]
            
            inStoreOrderStockInstance = InStoreOrderStock.objects.create(
                quantity = qty,
                inStoreOrderHist_id = orderId,
                stock_id = stockId,
                order_status = orderStatus
            )
            
            if orderStatus == IN_STORE:
                sellMoreThenOneQtyHandler(stockId, qty)
        
        return orderId
        
    except Exception as e:
        raise e    

