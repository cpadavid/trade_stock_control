# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate
# from django.conf import settings
# from django.core.mail import EmailMessage

# API testing
from rest_framework import status
from rest_framework.decorators import api_view

# Model
from models import *
from django.db import connection

# Report Lab
from django.core.files.storage import FileSystemStorage

# Handler
from actionHandler import *
from reportHandler import *

# Create your views here.
@login_required
def index(request):
    stockTable = getStockTable()
    inStoreOrderHistTable = getInStoreOrderHistTable()
    template = 'homeIndex.html'
    return render(request, template, {'stockTableResult': stockTable, 'inStoreOrderHistResult': inStoreOrderHistTable})


# New Stock
@api_view(['POST'])
def newStock(request):
    print"Enter to New Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            newStockHandler(request)
            stockTable = getStockTable()
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context, status=status.HTTP_201_CREATED)
    except Exception as e:
        data['message'] = "Server: New Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
    
    data['message'] = "Server: New Stock Fail."
    return JsonResponse(data, status=400)
    

"""
# Get stock vs filter stock problem at action handler
# Get Stock
@api_view(['POST'])
def getStock(request):
    print"Enter to Get Stock Views"
    data = {}    
    try:
        if request.method == 'POST':
            stockInstance = getStockHandler(request)
            data = serializers.serialize('json', stockInstance)
            return JsonResponse(data, status=200, safe=False)
    except Exception as e:
        print e
        data['message'] = "Server: Get Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Get Stock Fail."
    return JsonResponse(data, status=400)
"""    
    
    
# Check Stock
@api_view(['POST'])
def checkStock(request):
    print"Enter to Check Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            stockTable = checkStockHandler(request)
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context)
    except Exception as e:
        print e
        data['message'] = "Server: Check Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Check Stock Fail."
    return JsonResponse(data, status=400)


# Sell Stock
@api_view(['POST'])
def sellStock(request):
    print"Enter to Sell Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            stockTable = sellStockHandler(request)
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context, status=status.HTTP_200_OK)
    except Exception as e:
        print e
        data['message'] = "Server: Sell Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Sell Stock Fail."
    return JsonResponse(data, status=400)


# Pack Stock
@api_view(['POST'])
def packStock(request):
    print"Enter to Pack Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            stockTable = packStockHandler(request)
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context, status=status.HTTP_200_OK)
    except Exception as e:
        print e
        data['message'] = "Server: Pack Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Sell Stock Fail."
    return JsonResponse(data, status=400)


# Refill Stock
@api_view(['POST'])
def refillStock(request):
    print"Enter to Refill Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            stockTable = refillStockHandler(request)
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context, status=status.HTTP_200_OK)
    except Exception as e:
        print e
        data['message'] = "Server: Refill Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Refill Stock Fail."
    return JsonResponse(data, status=400)


# Edit Stock
@api_view(['POST'])
def editStock(request):
    print"Enter to Edit Stock Views"
    data = {}
    try:
        if request.method == 'POST':
            stockTable = editStockHandler(request)
            template = 'homeIndex.html'
            context = {
                'stockTableResult': stockTable,
            }
            return render(request, template, context, status=status.HTTP_200_OK)
    except Exception as e:
        print e
        data['message'] = "Server: Edit Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Edit Stock Fail."
    return JsonResponse(data, status=400)


# Report
@api_view(['POST'])
def calcStock(request):
    print"Enter to Calc Stock"
    data = {}
    try:
        if request.method == 'POST':
            sales, cost, profit, currentStockValue = calcStockHandler(request)
        
            data = {
                'salesResult': sales,
                'costResult': cost,
                'profitResult': profit,
                'stockValueResult': currentStockValue
            }
            return JsonResponse(data, status=200)
            
    except Exception as e:
        print e
        data['message'] = "Server: Calc Stock Fail, {}".format(e)
        return JsonResponse(data, status=400)

    data['message'] = "Server: Calc Stock Fail."
    return JsonResponse(data, status=400)
    
 
# Generate Invoic
@api_view(['POST'])
def genInvoiceStock(request):
    print"Enter to Generate Invoic Stock"
    data = {}
    try:
        if request.method == 'POST':
            pdfName = generateInvoiceHandler(request)
            
            fs = FileSystemStorage("tradeStockControlApp/static/invoice")
            
            with fs.open(pdfName) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="'+pdfName+'"'
                response['PDF-NAME'] = pdfName
                response.write(pdf)
                return response
            
    except Exception as e:
        print e
        data['message'] = "Server: Generate Invoice Fail, {}".format(e)
        return JsonResponse(data, status=400)

    data['message'] = "Server: Generate Invoice Fail."
    return JsonResponse(data, status=400)


# Check In Store Order History
@api_view(['POST'])
def checkInStoreOrderHist(request):
    print"Enter to Check In Store Order History"
    data = {}
    try:
        if request.method == 'POST':
            # inStoreOrderHistTable = getInStoreOrderHistTable()
            inStoreOrderHistTable = checkInStoreOrderHistHandler(request)
            template = 'homeIndex.html'
            context = {
                'inStoreOrderHistResult': inStoreOrderHistTable
            }
            return render(request, template, context)
            
    except Exception as e:
        print e
        data['message'] = "Server: Check In Store Order Hist Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Check In Store Order Hist."
    return JsonResponse(data, status=400)


# Sell Instore Order
@api_view(['POST'])
def sellInstoreOrder(request):
    print"Enter to Sell In Store Order"
    data = {}
    try:
        if request.method == 'POST':
        
            reqData = request.data
            usr = reqData['username']
            pw = reqData['password']
            user = authenticate(username=usr, password=pw)
            if user is None:
                data['message'] = "Server: User is invalid."
                return JsonResponse(data, status=403)
        
            # Save data
            orderNo = sellInStoreOrderHandler(request)
            
            # Generate Invoice
            generateInvoiceHandler(request, orderNo)
            
            # Send Invoice automatically
            sendInvoiceHandler(request, orderNo)
            
            data['message'] = "Server: Sell In Store Order Success"
            return JsonResponse(data, status=200)
            
    except Exception as e:
        print e
        data['message'] = "Server: Sell In Store Order Fail, {}".format(e)
        return JsonResponse(data, status=400)
        
    data['message'] = "Server: Sell In Store Order Hist."
    return JsonResponse(data, status=400) 


# Will not call this view, as email will
# send when sellInStoreOrder is called
# Send Invoice
"""
@api_view(['POST'])
def sendInvoice(request):
    print"Enter to Send Invoice"
    data = {}
    try:
        # import os
        # print os.getcwd()
        
        data = json.loads(request.body)
        email = str(data["email"]).replace(" ","")
        telNo = str(data["telNo"]).replace(" ","")
        orderNo = str(data["orderNo"]).replace(" ","")
        
        # Send email
        subject = 'Thanks You for shopping at Aangshop'
        message = 'Welcome to Aangshop! We very much appreciate your business.\nLooks forward to see you again !'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER, email]
        email = EmailMessage(subject,message,from_email,to_list)    
        email.attach_file('tradeStockControlApp\\static\\invoice\\{}_{}.pdf'.format(telNo, orderNo))
        email.send()
        
        data['message'] = "Server: Send Invoice Success"
        return JsonResponse(data, status=200)
    except Exception as e:
        print e
        data['message'] = "Server: Send Invoice Fail, {}".format(e)
        return JsonResponse(data, status=400)

    data['message'] = "Server: Send Invoice Fail."
    return JsonResponse(data, status=400)
"""
 
# Generate Instore Order History Excel
@api_view(['GET'])
def genOrderHistExcel(request):
    print"Enter to Generate Instore Order History"
    data = {}
    try:
        if request.method == 'GET':
            
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            xlsx_data = getOrderHistHandler(request)
            response.write(xlsx_data)
            print "Return Response"
            return response
            
            """
            excelName = getOrderHistHandler(request)
            
            print excelName
            
            fs = FileSystemStorage("tradeStockControlApp/static/orderHistExcel/")

            with fs.open(excelName) as xlsx:
                response = HttpResponse(xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="'+excelName+'"'
                response['XLSX-NAME'] = excelName
                response.write(xlsx)
                return response
            """
            
    except Exception as e:
        print e
        data['message'] = "Server: Generate Instore Order History Excel Fail, {}".format(e)
        return JsonResponse(data, status=400)

    data['message'] = "Server: Generate Instore Order History Excel Fail."
    return JsonResponse(data, status=400) 
    