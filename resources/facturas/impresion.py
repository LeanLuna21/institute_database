# from win32 import win32print
# import PyPDF2

# def list_printers():
#     printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)]
#     return printers

# if __name__ == "__main__":
#     available_printers = list_printers()
#     print("Available printers:")
#     for printer in available_printers:
#         print(printer)


# def print_pdf(pdf_path, printer_name):
#     # Open the PDF file
#     with open(pdf_path, 'rb') as file:
#         # Create a PDF reader object
#         pdf_reader = PyPDF2.PdfReader(file)

#         # Extract text from each page
#         text = ""
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()

#     # Set up the printer
#     printer = win32print.OpenPrinter(printer_name)
#     job = win32print.StartDocPrinter(printer, 1, ("Print Job", None, "RAW"))
#     win32print.StartPagePrinter(printer)

#     # Send the text to the printer
#     win32print.WritePrinter(printer, text.encode('utf-8'))

#     # End the print job
#     win32print.EndPagePrinter(printer)
#     win32print.EndDocPrinter(printer)
#     win32print.ClosePrinter(printer)

# if __name__ == "__main__":
#     # Specify the path to the PDF file and the printer name
#     pdf_path = "resources/facturas/factura.pdf"
#     printer_name = "EPSON L3150 Series"

#     # Call the print_pdf function
#     print_pdf(pdf_path, printer_name)



# from win32 import win32api, win32print

# if __name__ == "__main__":
#     # Specify the path to the PDF file and the printer name
#     pdf_path = "C:/Users/Lea/Desktop/Proyecto_ALAS/resources/facturas/factura.pdf"
    
#     win32api.ShellExecute(0,'print',pdf_path,win32print.GetDefaultPrinter(),'-',0)


import webbrowser

def open_pdf_with_default_reader(pdf_path):
    try:
        webbrowser.open(pdf_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the path to the PDF file
    pdf_path = r"C:/Users/Lea/Desktop/Proyecto_ALAS/resources/facturas/factura.pdf"

    # Call the open_pdf_with_default_reader function
    open_pdf_with_default_reader(pdf_path)
