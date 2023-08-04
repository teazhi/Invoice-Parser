import os
import pdfplumber
import json
from reportlab.pdfgen.canvas import Canvas
import traceback
from sys import exit

print("Please place all invoices in the same folder as this script and then provide the path to the folder.")
path = input("Path (default = current directory):")

try:
    if len(path) == 0:
        directoryPath = os.listdir('.')
    else:
        directoryPath = os.listdir(path)

    allInvoices = []
    EXPORT_FILE_NAME = "INVOICE_EXPORT.pdf"

    for i in range(len(directoryPath)):
        if directoryPath[i] != EXPORT_FILE_NAME and 'inv' in directoryPath[i].lower():
            if '.pdf' in directoryPath[i].lower():
                os.rename(directoryPath[i], f'invoice{i}.pdf')
                allInvoices.append(f'invoice{i}.pdf')
            else:
                print("No PDF file in this directory. Please add you invoice PDF into this directory and try again.")
                exit()

    invoiceParseResults = []
    invoiceItems = []

    for invoice in allInvoices:
        print("Parsing invoice: " + invoice)
        invoicenum = ""

        pdf = pdfplumber.open(invoice)

        PAGE_X_SIZE = 612.0
        PAGE_Y_SIZE = 750.0
        FONT_SIZE = 7
        HEADER = FONT_SIZE*5

        canvas = Canvas(EXPORT_FILE_NAME, pagesize=(PAGE_X_SIZE, PAGE_Y_SIZE))
        canvas.setFont("Helvetica", FONT_SIZE)

        currentPage = 0
        count = 0

        while currentPage < len(pdf.pages)-1:
            invoicenum = pdf.pages[currentPage].extract_tables()[0][0][0]
            # extract items list from invoice
            text = pdf.pages[currentPage].extract_table()
            for item in text:
                if item[3] is not None and 'UPC' not in item[0] and len(item) > 12:
                        temp = list(filter(lambda x: x is not None, item))
                        numinvaid = 0
                        tempdict = {}
                        if len(item[0]) == 0: 
                            tempdict['BARCODE'] = "NO BARCODE FOUND"
                            numinvaid += 1
                        else:    
                            tempdict['BARCODE'] = item[0]
                        tempdict['SHORT_DESC'] = item[7]
                        if len(item[3]) == 0: 
                            tempdict['LONG_DESC'] = "INVAID SHORT DESCRIPTION"
                            numinvaid += 1
                        else:
                            tempdict['LONG_DESC'] = "JFC/" + item[3] + " $" + item[11]
                        # tempdict['SLOT #'] = item[2]
                        # tempdict['ITEM #'] = item[3]
                        tempdict['QTY (CASE)'] = item[5]
                        tempdict['QTY (EACH)'] = item[6]
                        tempdict['EACH PRICE'] = item[11]
                        tempdict['UNIT PRICE'] = item[13]
                        tempdict['TOTAL/AMOUNT'] = item[15]
                        if numinvaid < 2:
                            invoiceItems.append(tempdict)

            x_pos = 25
            header_pos = PAGE_Y_SIZE-(FONT_SIZE*2)
            og_y_pos = PAGE_Y_SIZE-HEADER-FONT_SIZE
            y_pos = og_y_pos

            canvas.drawString(x_pos, header_pos, "INVOICE #")
            canvas.drawString(x_pos, header_pos-(FONT_SIZE+1), invoicenum[invoicenum.find("\n"):].strip())

            while count < len(invoiceItems):
                LENGTH_BETWEEN_LINES = FONT_SIZE+3
                cols = 3
                if y_pos <= FONT_SIZE*3:
                    x_pos += PAGE_X_SIZE//cols
                    y_pos = og_y_pos
                    cols -= 1

                if invoiceItems[count]['TOTAL/AMOUNT'] != "":
                    canvas.drawString(x_pos, y_pos, f"{invoiceItems[count]['BARCODE']}")
                    y_pos -= LENGTH_BETWEEN_LINES
                    canvas.drawString(x_pos, y_pos, f"{invoiceItems[count]['SHORT_DESC']}")
                    y_pos -= LENGTH_BETWEEN_LINES
                    canvas.drawString(x_pos, y_pos, f"{invoiceItems[count]['LONG_DESC']}")
                    y_pos -= LENGTH_BETWEEN_LINES
                    canvas.drawString(x_pos, y_pos, f"Total: {invoiceItems[count]['TOTAL/AMOUNT']}")
                    y_pos -= LENGTH_BETWEEN_LINES+(FONT_SIZE//2)
                
                count += 1

            currentPage += 1
            canvas.showPage()
            x_pos = 30
            header_pos = PAGE_Y_SIZE-(FONT_SIZE*3)
            og_y_pos = PAGE_Y_SIZE-HEADER-FONT_SIZE
            y_pos = og_y_pos
            canvas.setFont("Helvetica", FONT_SIZE)

        canvas.save()
    with open('items_data.json', 'w+') as outfile:
        outfile.write(json.dumps(invoiceItems, indent=4))
except Exception as e:
    traceback.print_exception(e)
    wait_for_it = input('Press enter to close the terminal window')
