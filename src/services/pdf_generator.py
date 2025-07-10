from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from io import BytesIO
from typing import List, Optional
from datetime import datetime
import locale

from src.application.dtos.order import OrderResponseDto
from src.application.dtos.customer import CustomerResponseDto
from src.application.dtos.order_detail import OrderDetailResponseDto
from src.application.dtos.product import ProductResponseDto

class MyCartDetailExtraOptionSchema(BaseModel):
    extra_option_id: int
    quantity: int
    linear_meter: Optional[float] = None
    width: Optional[float] = None
    giga_select: Optional[str] = None

class DisplayProductExtraOptionSchema(MyCartDetailExtraOptionSchema):
    name: str
    price: float

class DisplayCartItemSchema(BaseModel):
    product_id: int
    height: float
    width: float
    quantity: int
    linear_meter: float
    subtotal: float # Subtotal calculado en frontend (útil para presupuesto)
    total_extra_options: float
    extra_options: List[DisplayProductExtraOptionSchema]
    sku: str
    name: str # Nombre del producto (del frontend)
    price: float # Precio unitario (del frontend)
    image: Optional[str] = None # URL de imagen

    class Config:
        from_attributes = True # Para permitir mapeo si se usa de forma diferente

LOGO_PATH = "./src/shared/generate_pdf/laser.png"
FOOTER_UBICATION = "./src/shared/generate_pdf/footer_ubication.png"
def _header_footer_template(canvas_obj, doc):
    """
    Función que dibuja el encabezado y pie de página en cada página del PDF,
    incluyendo un logo en el encabezado.
    """
    canvas_obj.saveState()
    styles = getSampleStyleSheet()
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            pass  # fallback to default
    
    # Estilos específicos para header/footer
    styles.add(ParagraphStyle(name='HeaderCompanyFixedStyle', fontSize=10, leading=12, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderClientFixedStyle', fontSize=9, leading=11, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='DateStyle', fontSize=12, leading=11, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalFixedStyle', fontSize=8, leading=10, spaceAfter=1))
    styles.add(ParagraphStyle(name='FooterContactInfoStyle', fontSize=12, leading=12, alignment= 1, fontName='Helvetica', spaceAfter=6, spaceBefore=2 , ))
    styles.add(ParagraphStyle(name='PageNumberStyle', fontSize=8, leading=10, alignment=2)) # Para el número de página

    #############################
    ######## H E A D E R ########
    #############################
    # Posiciones fijas para el encabezado
    header_y_start = A4[1] - doc.topMargin + 15 * mm # 15mm desde el margen superior
   
    # Información de la empresa    # Fecha del documento
    doc_date_p = Paragraph(f"Lima, {datetime.now().strftime('%d de %B del %Y')}", styles['DateStyle'])
    doc_date_p.wrapOn(canvas_obj, doc.width, doc.topMargin)
    doc_date_p.drawOn(canvas_obj, doc.leftMargin, header_y_start ) 

    try:
        logo_width = 75 * mm
        logo_height = 22.5 * mm # Ajusta esto para mantener la proporción o especifica ambos
        logo_x = A4[0] - doc.rightMargin - logo_width + 5*mm
        logo_y = A4[1] - doc.topMargin + 8 * mm # Posiciona el logo en Y
        canvas_obj.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)

        company_address_p = Paragraph("EDITORIAL GLOBAL MULTIPRINT EIRL", styles['HeaderCompanyFixedStyle'])
        
        max_text_width = doc.width / 2 # O ajusta según el espacio disponible a la derecha
        company_address_p.wrapOn(canvas_obj, max_text_width, doc.topMargin)

        # Dibuja la información de la empresa debajo del logo, alineada a la derecha
        company_address_x = A4[0]  - company_address_p.width + 20 * mm
        company_address_y = logo_y + 1 * mm # 5mm de espacio debajo del logo

        company_address_p.drawOn(canvas_obj, company_address_x, company_address_y)
    except FileNotFoundError:
        # Manejo de error si el logo no se encuentra
        print(f"Advertencia: Logo no encontrado en {LOGO_PATH}. Continuando sin logo.")
        # Si el logo no se encuentra, dibuja la información de la empresa en la posición original
        company_name_p = Paragraph("<b>LASER COLOR VELOZ</b>", styles['HeaderCompanyFixedStyle'])
        company_address_p = Paragraph("EDITORIAL GLOBAL MULTIPRINT EIRL", styles['NormalFixedStyle'])
        company_name_p.wrapOn(canvas_obj, doc.width/2, doc.topMargin)
        company_address_p.wrapOn(canvas_obj, doc.width/2, doc.topMargin)
        company_name_p.drawOn(canvas_obj, doc.leftMargin, header_y_start)
        company_address_p.drawOn(canvas_obj, doc.leftMargin, header_y_start - 4 * mm)
    except Exception as e:
        print(f"Error al cargar o dibujar el logo: {e}")
        # En caso de otros errores, también dibuja el texto sin logo
        company_name_p = Paragraph("<b>LASER COLOR VELOZ</b>", styles['HeaderCompanyFixedStyle'])
        company_address_p = Paragraph("EDITORIAL GLOBAL MULTIPRINT EIRL", styles['NormalFixedStyle'])
        company_name_p.wrapOn(canvas_obj, doc.width/2, doc.topMargin)
        company_address_p.wrapOn(canvas_obj, doc.width/2, doc.topMargin)
        company_name_p.drawOn(canvas_obj, doc.leftMargin, header_y_start)
        company_address_p.drawOn(canvas_obj, doc.leftMargin, header_y_start - 4 * mm)
    
    #############################
    ######## F O O T E R ########
    #############################
    footer_y_start = doc.bottomMargin - 15 * mm
    
    # Información de contacto (alineada a la izquierda)
    contact_info = [
        "995558329",
        "laser.guizado.plaza@gmail.com",
        "www.lasercolorveloz.com",
        "958863047 :745 9011",
        "con la calidad Canon"
    ]
    
    for i, line in enumerate(contact_info):
        p = Paragraph(line, styles['FooterContactInfoStyle'])
        p.wrapOn(canvas_obj, doc.width / 2, doc.bottomMargin)
        p.drawOn(canvas_obj, doc.leftMargin, footer_y_start + (len(contact_info) - i - 1) * 3 * mm)


    footer_ubication_width = 85 * mm  # Ancho del box de ubicación
    footer_ubication_height = 65 * mm  # Alto del box de ubicación
    footer_ubication_x = A4[0] - doc.rightMargin - footer_ubication_width + 14 * mm 
    footer_ubication_y = doc.bottomMargin - 25 * mm     
    canvas_obj.drawImage(FOOTER_UBICATION, footer_ubication_x, footer_ubication_y, width=footer_ubication_width, height=footer_ubication_height, preserveAspectRatio=True)


    # Dirección (alineada a la derecha del contacto)
    address_info = [
        "C.C. Guizado Record Plaza",
        "1er Piso Stand 102 A-194",
        "Jr. Huaraz 1717 (altura de la Cra. 9 de la Av. Brasil)",
        "Breña"
    ]

    box_width = 75 * mm  # Ajusta el ancho según lo que quieras probar

    # Calcula el alto real sumando el alto de cada línea
    line_heights = []
    for line in address_info:
        p = Paragraph(line, styles['FooterContactInfoStyle'])
        w, h = p.wrap(box_width - 4 * mm, doc.bottomMargin)
        line_heights.append(h)
    box_height = sum(line_heights) + 4 * mm  # 4mm de margen superior/inferior

    box_x = doc.leftMargin + doc.width / 2 + 10 * mm
    box_y = footer_y_start + 2 * mm + sum(line_heights[::-1][1:])  # Ajusta según tu diseño

    # Dibuja el rectángulo (box)
    canvas_obj.setStrokeColor(colors.red)
    canvas_obj.setLineWidth(1)
    canvas_obj.rect(box_x, box_y - box_height, box_width, box_height, stroke=1, fill=0)

    # Dibuja las líneas de dirección dentro del box, una debajo de otra
    current_y = box_y - 2 * mm  # Empieza desde arriba, deja margen superior
    for i, line in enumerate(address_info):
        p = Paragraph(line, styles['FooterContactInfoStyle'])
        w, h = p.wrap(box_width - 4 * mm, doc.bottomMargin)
        p.drawOn(canvas_obj, box_x + 2 * mm, current_y - h ) 
        current_y -= h

    # Número de página (centrado en el pie de página)
    # page_number = Paragraph(f"Página {doc.page}", styles['PageNumberStyle'])
    # page_number.wrapOn(canvas_obj, doc.width, doc.bottomMargin)
    # page_number_x = (doc.width - page_number.width) / 2 + doc.leftMargin
    # page_number_y = footer_y_start - 2 * mm  # Ajusta la posición Y según sea necesario
    # page_number.drawOn(canvas_obj, page_number_x, page_number_y)



    canvas_obj.restoreState()

def generate_order_pdf(
    order: OrderResponseDto,
    display_items: List[dict]
) -> BytesIO:
    """
    Genera un PDF de orden/factura utilizando ReportLab.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=80, bottomMargin=80)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, leading=28, alignment=1, spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderCompanyStyle', fontSize=12, leading=14, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderClientStyle', fontSize=10, leading=12, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderStyle', fontSize=12, leading=14, spaceAfter=6, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=10, leading=12, spaceAfter=3))
    styles.add(ParagraphStyle(name='ItemHeaderStyle', fontSize=10, leading=12, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ItemDataStyle', fontSize=9, leading=11))
    styles.add(ParagraphStyle(name='TotalStyle', fontSize=14, leading=16, alignment=2, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='FooterStyle', fontSize=8, leading=10, alignment=1, spaceBefore=20))

    elements = []

    # Encabezado
    # elements.append(Paragraph(f"Lima, {datetime.now().strftime('%d de %B de %Y')}", styles['NormalStyle']))
    elements.append(Paragraph("Presupuesto / Factura de Venta", styles['TitleStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # Información de la empresa
    elements.append(Paragraph("<b>Laser Cotización S.A.C.</b>", styles['HeaderStyle']))
    elements.append(Paragraph("RUC: 20XXXXXXXXX", styles['NormalStyle']))
    elements.append(Paragraph("Dirección: Av. Industrial 123, Los Olivos, Lima", styles['NormalStyle']))
    elements.append(Paragraph("Teléfono: +51 987 654 321 | Email: info@lasercotizacion.com", styles['NormalStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # Información de la orden
    elements.append(Paragraph(f"<b>Orden ID:</b> {order.id}", styles['HeaderStyle']))
    elements.append(Paragraph(f"<b>Fecha:</b> {order.created_at.strftime('%d/%m/%Y %H:%M')}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>Estado:</b> {order.status.name if order.status else 'Desconocido'}", styles['NormalStyle']))
    if order.store:
        elements.append(Paragraph(f"<b>Tienda:</b> {order.store.name}", styles['NormalStyle']))
    elements.append(Spacer(1, 0.1 * inch))

    # Información del cliente
    elements.append(Paragraph("<b>Información del Cliente:</b>", styles['HeaderStyle']))
    customer = order.customer
    if customer:
        customer_name = customer.business_name if customer.entity_type == 'J' else f"{customer.name} {customer.last_name}"
        elements.append(Paragraph(f"<b>Nombre/Razón Social:</b> {customer_name}", styles['NormalStyle']))
        if customer.entity_type == 'J' and customer.ruc:
            elements.append(Paragraph(f"<b>RUC:</b> {customer.ruc}", styles['NormalStyle']))
        elif customer.entity_type == 'N' and customer.dni:
            elements.append(Paragraph(f"<b>DNI:</b> {customer.dni}", styles['NormalStyle']))
        elements.append(Paragraph(f"<b>Email:</b> {customer.email}", styles['NormalStyle']))
        elements.append(Paragraph(f"<b>Teléfono:</b> {customer.phone_number}", styles['NormalStyle']))
    else:
        elements.append(Paragraph("Cliente no especificado.", styles['NormalStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # Tabla de items
    data = [
        [
            Paragraph("SKU", styles['ItemHeaderStyle']),
            Paragraph("Producto", styles['ItemHeaderStyle']),
            Paragraph("Dimensiones", styles['ItemHeaderStyle']),
            Paragraph("Opciones Extra", styles['ItemHeaderStyle']),
            Paragraph("Cant.", styles['ItemHeaderStyle']),
            Paragraph("P. Unit.", styles['ItemHeaderStyle']),
            Paragraph("Total Extra", styles['ItemHeaderStyle']),
            Paragraph("Subtotal", styles['ItemHeaderStyle'])
        ]
    ]

    total_general = 0.0

    for item in display_items:
        # Construir string de dimensiones
        dimensions_str = ""
        if item.get('height') and item.get('width'):
            dimensions_str += f"{item['height']}cm x {item['width']}cm"
        if item.get('linear_meter'):
            if dimensions_str: 
                dimensions_str += "\n"
            dimensions_str += f"{item['linear_meter']} m L"
        if not dimensions_str:
            dimensions_str = "-"

        # Construir string de opciones extra
        extra_options_str = ""
        if item.get('extra_options') and len(item['extra_options']) > 0:
            extra_options_list = []
            for opt in item['extra_options']:
                opt_str = f"• {opt['name']}"
                if opt.get('quantity'):
                    opt_str += f" (x{opt['quantity']})"
                if opt.get('linear_meter'):
                    opt_str += f" - {opt['linear_meter']}m L"
                opt_str += f" - S/. {opt['price']:.2f}"
                extra_options_list.append(opt_str)
            extra_options_str = "\n".join(extra_options_list)
        else:
            extra_options_str = "Sin opciones extra"

        # Calcular el subtotal del producto base
        producto_subtotal = item['price'] * item['quantity']
        item_total = producto_subtotal + item.get('total_extra_options', 0)
        total_general += item_total

        data.append([
            Paragraph(item.get('sku', '-'), styles['ItemDataStyle']),
            Paragraph(item['name'], styles['ItemDataStyle']),
            Paragraph(dimensions_str, styles['ItemDataStyle']),
            Paragraph(extra_options_str, styles['ItemDataStyle']),
            Paragraph(str(item['quantity']), styles['ItemDataStyle']),
            Paragraph(f"S/. {item['price']:.2f}", styles['ItemDataStyle']),
            Paragraph(f"S/. {item.get('total_extra_options', 0):.2f}", styles['ItemDataStyle']),
            Paragraph(f"S/. {item_total:.2f}", styles['ItemDataStyle'])
        ])

    table = Table(data, colWidths=[0.8*inch, 1.5*inch, 1.0*inch, 1.8*inch, 0.5*inch, 0.7*inch, 0.7*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

    # Totales
    elements.append(Paragraph(f"<b>Total Base:</b> S/. {order.total_amount:.2f}", styles['NormalStyle']))
    if order.profit_margin > 0:
        elements.append(Paragraph(f"<b>Margen de Ganancia:</b> S/. {order.profit_margin:.2f}", styles['NormalStyle']))
    if order.discount_applied > 0:
        elements.append(Paragraph(f"<b>Descuento Aplicado:</b> -S/. {order.discount_applied:.2f}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>TOTAL FINAL:</b> S/. {order.final_amount:.2f}", styles['TotalStyle']))
    elements.append(Spacer(1, 0.5 * inch))

    # Notas
    if order.notes:
        elements.append(Paragraph(f"<b>Notas:</b>", styles['HeaderStyle']))
        elements.append(Paragraph(order.notes, styles['NormalStyle']))
        elements.append(Spacer(1, 0.2 * inch))

    # Pie de página
    elements.append(Paragraph("¡Gracias por su compra!", styles['FooterStyle']))
    elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['FooterStyle']))

    doc.build(elements, onFirstPage=_header_footer_template, onLaterPages=_header_footer_template)
    buffer.seek(0)
    return buffer