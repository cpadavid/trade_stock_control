# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A6
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import json
# import webcolors
from actionHandler import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from models import *

def generateInvoiceHandler(request, orderNo):
    try:
        print "Enter to reporthandler"
        print request
        
        # data = json.loads(request.body)
        data = request.data
        
        print data
    
        name = data["name"]
        telNo = data["telNo"]
        email = data["email"]
        remark = data["remark"]
        
        print "Remark: {}".format(remark)
    
        pdfName = "{}_{}.pdf".format(telNo, orderNo)
        
        # Define table styles
        pdfmetrics.registerFont(TTFont("WT009", "tradeStockControlApp/static/assets/fonts/wt009.ttf"))
        
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='WT009')) 
        
        centerStyles=getSampleStyleSheet()
        centerStyles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='WT009'))
        
        # PDF
        doc = SimpleDocTemplate('tradeStockControlApp/static/invoice/{}'.format(pdfName),pagesize=A6,
                                rightMargin=20,leftMargin=20,
                                topMargin=20,bottomMargin=20)
        
        # Start print PDF
        Story=[]
        # logo = "/Users/davidleung/desktop/tradeStockControl/tradeStockControlApp/static/images/company_logo.jpg"
        logo = "tradeStockControlApp/static/images/company_logo.jpg"
        orderNumber = orderNo
        
        # Image
        im = Image(logo, 1.75*inch, 1.75*inch)
        Story.append(im)
        
        # Spacer
        Story.append(Spacer(1, 5))
        
        # Order Number, Name, Phone, Email
        ptext = u'<font size=8>Order No: {}</font>'.format(orderNumber)
        Story.append(Paragraph(ptext, styles["Justify"]))
        
        ptext = u'<font size=8>Name: {}</font>'.format(name)
        Story.append(Paragraph(ptext, styles["Justify"]))  
        
        ptext = u'<font size=8>Phone No: {}</font>'.format(telNo)
        Story.append(Paragraph(ptext, styles["Justify"]))  
        
        ptext = u'<font size=8>Email: {}</font>'.format(email)
        Story.append(Paragraph(ptext, styles["Justify"]))
         
        # Items Table
        itemList = data['selledItemList']
        
        formattedTableData = []
        
        itemNoHeader = 'Item No'
        orderStatusHeader = 'Status'
        qtyHeader = 'Qty'
        priceHeader = 'Price'
        
        formattedTableData = [[itemNoHeader, orderStatusHeader, qtyHeader, priceHeader]]
        
        totalPrice = 0
        preOrderPrice = 0
        for item in itemList:
            
            orderStatus = ''
            if item['orderStatus'] == IN_STORE:
                orderStatus = IN_STORE_DISPLAY
            else:
                orderStatus = PRE_ORDER_DISPLAY
                
            row1 = []
            row2 = []
            row2Var = ''
            stockId = item['stockId']
            stockInstance = getStock(stockId)
            row1.append(stockInstance.item_no)
            row1.append(orderStatus)
            row1.append(item['quantity'])
            price = int(item['quantity']) * int(stockInstance.price)
            row1.append(price)
            # row2Var = "{}, {}, {}".format(stockInstance.description, webcolors.hex_to_name(stockInstance.color), stockInstance.size)
            row2Var = "{}, {}, {}".format(stockInstance.description, stockInstance.color, stockInstance.size)
            row2.append(row2Var)
            formattedTableData.append(row1)
            formattedTableData.append(row2)
            if item['orderStatus'] == 'INSTORE':
                totalPrice += price
            else:
                preOrderPrice += price
        # totalPriceRow = ['Total:', '', '', '{}({})'.format(totalPrice, preOrderPrice)]
        totalPriceRow = ['Total:', '', '', totalPrice]
        formattedTableData.append(totalPriceRow)
        
        # Table Style
        totalItems = len(itemList)
        t=Table(formattedTableData,colWidths=[2.55*inch, 0.45*inch, 0.45*inch],repeatRows=1)
        table_style=[
        ('ALIGN',(0,0),(-1,-1),'RIGHT'),
        ('ALIGN',(0,0),(0,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('BOX',(0,0),(-1,-1),0.25,colors.black),
        ('LINEABOVE',(0,-1),(-1,-1),0.25,colors.black),
        ('FONT',(0,0),(-1,-1),'WT009')]
        
        t.setStyle(TableStyle(table_style))
        Story.append(t)
        
        # Remarks
        ptext = u'<font size=8>Remark: {}</font>'.format(remark)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        
        # Footer
        ptext = '<font size=8>Instagram: aangshop</font>'
        Story.append(Paragraph(ptext, centerStyles["Center"]))
        # ptext = '<font size=8>Website: https://www.aangshop.com/</font>'
        # Story.append(Paragraph(ptext, centerStyles["Center"]))
        # Story.append(Spacer(1, 12))
        date = datetime.datetime.now()
        d = '{}-{}-{}'.format(date.year, date.month, date.day)
        ptext = '<font size=8>Date: {}</font>'.format(d)
        Story.append(Paragraph(ptext, centerStyles["Center"]))
        
        
        # Build
        doc.build(Story)
        
        return pdfName
        
    except Exception as e:
        raise e