# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xlsxwriter
import time
import datetime
import StringIO


ORDER_HIST_HEADER = ["Phone No", "Item No", "Description", "Order Status"]

def createOrderHistExcelHandler(entryList):

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')

    xlsxName = "Order_Hist_{}.xlsx".format(st)
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    
    # workbook = xlsxwriter.Workbook("tradeStockControlApp\static\orderHistExcel\{}".format(xlsxName))

    # Add format to header
    bold = workbook.add_format({'bold': True})

    # Add a format to use wrap the cell text.
    wrap = workbook.add_format({'text_wrap': True})

    bold_wrap = workbook.add_format({'text_wrap': True,
                                     'bold': True})
    
    # Color Format
    headerFormat_bold = workbook.add_format({'bg_color': '#4472C4',
                                        'font_color': '#FFFFFF',
                                        'bold': True})

    ws = workbook.add_worksheet("Order History")
    
    ws.freeze_panes(1,0)
    rowCounter = 1
    
    for entry in entryList:
        if rowCounter == 1:
            colCounter = 0
            for header in ORDER_HIST_HEADER:
                if '\n' in header:
                    ws.write(0, colCounter, header, bold_wrap)
                else:
                    ws.write(0, colCounter, header, bold)
                colCounter += 1
            rowCounter += 1
        
        ws.write('A' + str(rowCounter), entry[0])
        ws.write('B' + str(rowCounter), entry[1])
        ws.write('C' + str(rowCounter), entry[2])
        ws.write('D' + str(rowCounter), entry[3])
        rowCounter += 1
    
    workbook.close()
    
    xlsx_data = output.getvalue()
    return xlsx_data
    
    # return xlsxName
    