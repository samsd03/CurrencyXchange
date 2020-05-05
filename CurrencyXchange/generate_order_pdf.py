import os
import sys
from reportlab.pdfgen import canvas
from CurrencyXchange import settings


def order_inv(order_id,date,name,from_currency,from_currency_quantity,to_currency):
    try:
        # Creating Canvas
        static_path = os.path.join(settings.STATICFILES_DIRS[0])
        invoice_number = str(order_id)
        pdf_name = str(order_id) + '.pdf'
        generation_path = os.path.join(static_path,'PDF/'+pdf_name)
        invoice_number = "INVOICE No. : {}".format(invoice_number)
        date = "DATE : {}".format(date)
        name = "CUSTOMER NAME : {}".format(name)
        from_currency = "FROM CURRENCY : {}".format(from_currency)
        quantity = "FROM CURRENCY Quantity: {}".format(from_currency_quantity)
        to_currency = "TO CURRENCY : {}".format(to_currency)

        c = canvas.Canvas(generation_path,pagesize=(200,180),bottomup=0)

        # Logo Section
        # Setting th origin to (10,40)
        c.translate(10,40)
        # Inverting the scale for getting mirror Image of logo
        c.scale(1,-1)
        # Inserting Logo into the Canvas at required position
        static_icon_path = os.path.join(static_path,'icon/currency_exchange.png')
        c.drawImage(static_icon_path,0,0,width=50,height=30)

        # Title Section
        # Again Inverting Scale For strings insertion
        c.scale(1,-1)
        # Again Setting the origin back to (0,0) of top-left
        c.translate(-10,-40)
        # Setting the font for Name title of company
        c.setFont("Helvetica-Bold",10)
        # Inserting the name of the company
        c.drawCentredString(125,20,"Currency Conversion")
        # For under lining the title
        c.line(70,22,180,22)
        # Changing the font size for Specifying Address
        c.setFont("Helvetica-Bold",5)
        c.drawCentredString(125,30,"Mumbai,Maharashtra")
        # c.drawCentredString(125,35,"New Delhi - 110034, India")
        # Changing the font size for Specifying GST Number of firm
        c.setFont("Helvetica-Bold",6)
        c.drawCentredString(125,42,"GSTIN : test123")

        # Line Seprating the page header from the body
        c.line(5,45,195,45)

        # Document Information
        # Changing the font for Document title
        c.setFont("Courier-Bold",8)
        c.drawCentredString(100,55,"ORDER-INVOICE")

        # This Block Consist of Costumer Details
        c.roundRect(15,63,170,70,10,stroke=1,fill=0)
        c.setFont("Times-Bold",5)
        c.drawRightString(90,70,invoice_number)
        c.drawRightString(90,80,date)
        c.drawRightString(90,90,name)
        c.drawRightString(90,100,from_currency)
        c.drawRightString(90,110,str(quantity))
        c.drawRightString(90,120,to_currency)

        # Declaration and Signature
        c.line(15,150,185,150)
        c.line(100,150,100,168)
        c.drawString(20,155,"We declare that above mentioned")
        c.drawString(20,160,"information is true.")
        c.drawString(20,165,"(This is system generated invoive)")
        c.drawRightString(160,160,"Signatory Not Required")

        # End the Page and Start with new
        c.showPage()
        # Saving the PDF
        c.save()

        return generation_path
    except Exception as e:
        print(e," ERROR IN order_inv --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
    

def transfer_statement_pdf(user_email,name,from_date,to_date,total_transaction,total_quantity):
    try:
        # Creating Canvas
        static_path = os.path.join(settings.STATICFILES_DIRS[0])
        pdf_name = str(user_email) + '_' +str(from_date) + '_' + to_date+ "_Monthly_statement" + '.pdf'
        generation_path = os.path.join(static_path,'MONTHLY_STATEMENT_PDF/'+pdf_name)
        
        name = "CUSTOMER NAME : {}".format(name)
        from_date = "FROM DATE : {}".format(from_date)
        to_date = "TO DATE : {}".format(to_date)
        total_transaction = "TOTAL TRANSACTION : {}".format(total_transaction)
        total_quantity = "TOTAL QUANTITY : {}".format(total_quantity)
        

        c = canvas.Canvas(generation_path,pagesize=(200,180),bottomup=0)

        # Logo Section
        # Setting th origin to (10,40)
        c.translate(10,40)
        # Inverting the scale for getting mirror Image of logo
        c.scale(1,-1)
        # Inserting Logo into the Canvas at required position
        static_icon_path = os.path.join(static_path,'icon/currency_exchange.png')
        c.drawImage(static_icon_path,0,0,width=50,height=30)

        # Title Section
        # Again Inverting Scale For strings insertion
        c.scale(1,-1)
        # Again Setting the origin back to (0,0) of top-left
        c.translate(-10,-40)
        # Setting the font for Name title of company
        c.setFont("Helvetica-Bold",10)
        # Inserting the name of the company
        c.drawCentredString(125,20,"Currency Conversion")
        # For under lining the title
        c.line(70,22,180,22)
        # Changing the font size for Specifying Address
        c.setFont("Helvetica-Bold",5)
        c.drawCentredString(125,30,"Mumbai,Maharashtra")
        # c.drawCentredString(125,35,"New Delhi - 110034, India")
        # Changing the font size for Specifying GST Number of firm
        c.setFont("Helvetica-Bold",6)
        c.drawCentredString(125,42,"GSTIN : test123")

        # Line Seprating the page header from the body
        c.line(5,45,195,45)

        # Document Information
        # Changing the font for Document title
        c.setFont("Courier-Bold",8)
        c.drawCentredString(100,55,"MONTHLY TRANSACTIONS")

        # This Block Consist of Costumer Details
        c.roundRect(15,63,170,50,10,stroke=1,fill=0)
        c.setFont("Times-Bold",5)
        c.drawRightString(90,70,name)
        c.drawRightString(90,80,from_date)
        c.drawRightString(90,90,to_date)
        c.drawRightString(90,100,total_transaction)
        c.drawRightString(90,110,total_quantity)

        # Declaration and Signature
        c.line(15,150,185,150)
        c.line(100,150,100,168)
        c.drawString(20,155,"We declare that above mentioned")
        c.drawString(20,160,"information is true.")
        c.drawString(20,165,"(This is system generated invoive)")
        c.drawRightString(160,160,"Signatory Not Required")

        # End the Page and Start with new
        c.showPage()
        # Saving the PDF
        c.save()

        return generation_path
    except Exception as e:
        print(e," ERROR IN transfer_statement_pdf --line number of error {}".format(sys.exc_info()[-1].tb_lineno))