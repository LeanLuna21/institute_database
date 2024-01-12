import jinja2
import pdfkit
from datetime import datetime
# usamos este modulo para abrir el pdf una vez generado
import webbrowser


def open_pdf_with_default_reader(pdf_path):
    try:
        webbrowser.open(pdf_path)
    except Exception as e:
        print(f"Error: {e}")

def convert_to_pdf(legajo,apellido,nombre,mes,importe,deudas,fotocs):
    alumno_nombre = apellido +" "+ nombre 
    
    item1 = "Cuota mes corriente"
    item2 = "Monto adeudado"
    item3 = "Fotocopias"

    subtotal1 = importe
    subtotal2 = deudas
    subtotal3 = fotocs

    total = subtotal1 + subtotal2 + subtotal3

    fecha_hoy = datetime.now().strftime("%d %b, %Y")

    context = {'alumno_nombre': alumno_nombre, 'fecha_hoy': fecha_hoy, 'total': f'${total:.2f}', 'mes': mes, 'legajo': legajo,
            'item1': item1, 'subtotal1': f'${subtotal1:.2f}',
            'item2': item2, 'subtotal2': f'${subtotal2:.2f}',
            'item3': item3, 'subtotal3': f'${subtotal3:.2f}'
            }

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'resources/facturas/invoice.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    path_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe' 
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output_pdf = 'resources/facturas/factura.pdf'
    pdfkit.from_string(output_text, output_pdf, configuration=config, css='resources/facturas/invoice.css')

    # Call the open_pdf_with_default_reader function
    try:
        pdf_path = "C:/Users/Lea/Desktop/Proyecto_ALAS/resources/facturas/factura.pdf" #NO OLVIDAR CAMBIAR ESTO
        open_pdf_with_default_reader(pdf_path)
    except Exception as e:
        print('The following error has occurred: ',e,' unable to proceed')

    # C:/Users/Lea/Desktop/Proyecto_ALAS/dist/interface/resources/facturas/factura.pdf

  