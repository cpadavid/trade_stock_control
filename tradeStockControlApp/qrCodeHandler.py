# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import qrcode
from PIL import ImageFont
from PIL import ImageDraw

def generateQrCodeHandler(stockInstance):
    try:
        print stockInstance.item_no
        
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4,
        )
        
        # Special encoding for mobile apps
        stockDict = {}
        stockDict["stockId".encode('ascii', 'ignore')] = int(stockInstance.stock_id)
        stockDict["itemNo".encode('ascii', 'ignore')] = stockInstance.item_no.encode('ascii', 'ignore')
        stockDict["description".encode('ascii', 'ignore')] = stockInstance.description.encode('ascii', 'ignore')
        stockDict["color".encode('ascii', 'ignore')] = stockInstance.color.encode('ascii', 'ignore')
        stockDict["size".encode('ascii', 'ignore')] = stockInstance.size.encode('ascii', 'ignore')
        stockDict["price".encode('ascii', 'ignore')] = int(stockInstance.price)
        
        data = stockDict
        
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image()
        
        draw = ImageDraw.Draw(img)
        print 'read font'
        font = ImageFont.truetype("tradeStockControlApp\\static\\assets\\fonts\\wt009.ttf", 25)
        draw.text((40,10), "{}".format(stockInstance.description), font=font)
        
        img.save("tradeStockControlApp\\static\\qrCode\\{}_{}_{}.jpg".format(stockInstance.stock_id, stockInstance.item_no, stockInstance.description))
        
    except Exception as e:
        raise e