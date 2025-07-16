from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Image
from io import BytesIO
from typing import List, Optional
from datetime import datetime
import locale
from zoneinfo import ZoneInfo

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
LOGO_BCP = "./src/shared/generate_pdf/bcp.png"
LOGO_VISA = "./src/shared/generate_pdf/visa.png"
LOGO_YAPE = "./src/shared/generate_pdf/yape.png"

def _header_footer_template(canvas_obj, doc, store_info):
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
    styles.add(ParagraphStyle(name='HeaderCompanyFixedStyle', fontSize=9, leading=12, alignment=0, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='HeaderClientFixedStyle', fontSize=9, leading=11, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='DateStyle', fontSize=11, leading=11, alignment=0, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='NormalFixedStyle', fontSize=8, leading=10, spaceAfter=1))
    styles.add(ParagraphStyle(name='FooterContactInfoStyle', fontSize=13, leading=16, alignment= 1, fontName='Helvetica', spaceAfter=6, spaceBefore=2 , ))
    styles.add(ParagraphStyle(name='PageNumberStyle', fontSize=8, leading=10, alignment=2)) # Para el número de página

    #############################
    ######## H E A D E R ########
    #############################
    # Posiciones fijas para el encabezado
    header_y_start = A4[1] - 20 * mm   # 15mm desde el borde superior
   
    # Información de la empresa    # Fecha del documento
    doc_date_p = Paragraph(f"Lima, {datetime.now().strftime('%d de %B del %Y')}", styles['DateStyle'])
    doc_date_p.wrapOn(canvas_obj, doc.width, doc.height)
    doc_date_p.drawOn(canvas_obj, doc.leftMargin + 2 * mm, header_y_start + 10 * mm)  # Ajusta la posición Y según sea necesario

    logo_width = 75 * mm
    logo_height = 22.5 * mm # Ajusta esto para mantener la proporción o especifica ambos
    logo_x = A4[0] - doc.rightMargin - logo_width 
    logo_y = header_y_start 
    canvas_obj.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)

    #############################
    ######## F O O T E R ########
    #############################
    footer_y_start = 50 * mm  # 50mm desde el borde inferior

    styles.add(ParagraphStyle(name='TablePay', fontSize=12, leading=12, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TableContent', fontSize=10, leading=12, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NoteFooter', fontSize=10, leading=12, alignment=0, fontName='Helvetica'))

    # Dibujar una tabla de 2 filas y 1 columna , la primera fila background rojo que dira "Modalidad de pago" y la otra fila estara inicialmente como espacio vacio visible
    adelanto = Paragraph("- Se procede la impresión previa autorización del cliente.", styles['NoteFooter'])
    no_delivery = Paragraph("- El delivery no esta considerado en la cotización.", styles['NoteFooter'])
    title_footer_table = Paragraph("<b><font color=white>Modalidad de pago</font></b>", styles['TablePay'])
    efectivo = Paragraph("Efectivo:", styles['TableContent'])
    transferencia_bancaria = Paragraph("Transferencia Bancaria:", styles['TableContent'])    
    nro_cuenta = Paragraph("Nro. de Cuenta BCP:", styles['TableContent'])
    nro_cuenta_value = Paragraph(f"{store_info.bcp_cta}", styles['TableContent'])
    nro_cci = Paragraph("Nro. de CCI Interbancaria:", styles['TableContent'])
    nro_cci_value = Paragraph(f"{store_info.bcp_cci}", styles['TableContent'])

    bcp_logo = Image(LOGO_BCP, width=12 * mm, height=3 * mm)
    visa_logo = Image(LOGO_VISA, width=12 * mm, height= 4 * mm)
    yape_logo = Image(LOGO_YAPE, width= 10 * mm, height= 10 * mm)

    payment_terms_table_data = [
        [adelanto,''],
        [no_delivery,''],
        [title_footer_table, ''],
        [efectivo,visa_logo, yape_logo],
        [transferencia_bancaria, bcp_logo],
        [nro_cuenta,nro_cuenta_value,''] ,
        [nro_cci, nro_cci_value,''] 
    ]
    footer_payment_info_table = Table(
        payment_terms_table_data,
        colWidths=[(doc.width / 2 + 15 * mm) * 0.45, 
                   (doc.width / 2 + 15 * mm) * 0.15,
                    (doc.width / 2 + 15 * mm) * 0.40
                  ]  # Ajusta proporción texto/logo
    )
    
    footer_payment_info_table.setStyle(TableStyle([ 
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)), # Fusiona las dos celdas de la primera fila
        ('SPAN', (0, 2), (2, 2)),  # La primera fila abarca ambas columnas
        ('BACKGROUND', (0, 2), (2, 2), colors.HexColor("#ec2e2c")),  # Rojo para la primera fila   
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Fuente negrita
        ('FONTSIZE', (0, 0), (-1, -1), 10) , # Tamaño de fuente
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 2), (-1, -1), 0.5, colors.black),  # Borde de la tabla
        ('SPAN', (1, 5), (2, 5)),
        ('SPAN', (1, 6), (2, 6)),
    ]))
    footer_payment_info_table.wrapOn(canvas_obj, doc.width, doc.bottomMargin)
    footer_payment_info_table.drawOn(canvas_obj, doc.leftMargin, 23 * mm)  # Ajusta la posición Y según sea necesario      

    phone = ''
    for i in range(len(store_info.phone_number)):
        if i == 3:
            phone += ' '
        if i == 6:
            phone += ' '
        if i == 9:
            phone += ' '
        phone += store_info.phone_number[i]
    
    # Footer con información de contacto y ubicación
    styles.add(ParagraphStyle(name='FooterContact', fontSize=10,  alignment=0, fontName='Helvetica'))

    email_logo = Image("./src/shared/generate_pdf/email.png", width=5 * mm, height=5 * mm)
    web_logo = Image("./src/shared/generate_pdf/web.png", width=5 * mm, height=5 * mm)
    phone_logo = Image("./src/shared/generate_pdf/phone.png", width=5 * mm, height=5 * mm)

    email = Paragraph(f"{store_info.email}", styles['FooterContact'])
    web_laser = Paragraph("www.lasercolorveloz.com", styles['FooterContact'])
    web_toque = Paragraph("www.toqueunicoperu.com", styles['FooterContact'])
    contact_phone = Paragraph(f"{phone}", styles['FooterContact'])

    contact_table_data = [
        [email_logo,email,phone_logo,contact_phone],  # Primera fila con email y teléfono
        [web_logo,web_laser , web_logo,web_toque],  # Segunda fila con web y teléfono,
    ]
    footer_contact_info_table = Table(
        contact_table_data,
        colWidths=[(doc.width / 2 - 4 * mm)* 0.07 ,
                   (doc.width / 2 - 4 * mm) * 0.61,
                   (doc.width / 2 - 4 * mm)* 0.07,
                   (doc.width / 2 - 4 * mm)* 0.6   ]  # Ajusta el ancho de la columna
    )
    footer_contact_info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    footer_contact_info_table.wrapOn(canvas_obj, doc.width / 2, doc.bottomMargin)
    footer_contact_info_table.drawOn(canvas_obj, doc.leftMargin, 5 * mm)  # Ajusta la posición Y según sea necesario

    footer_ubication_width = 85 * mm  # Ancho del box de ubicación
    footer_ubication_height = 65 * mm  # Alto del box de ubicación
    footer_ubication_x = A4[0] - doc.rightMargin - footer_ubication_width + 9 * mm 
    footer_ubication_y =  3 * mm     
    canvas_obj.drawImage(FOOTER_UBICATION, footer_ubication_x, footer_ubication_y, width=footer_ubication_width, height=footer_ubication_height, preserveAspectRatio=True)


    # Dirección (alineada a la derecha del contacto)
    address_info = [
        "C.C. Guizado Record Plaza",
        "1er Piso",
        "Stand 194",
        "Jr. Huaraz 1717 (altura de la Cra. 9 de la Av. Brasil)",
        "Breña"
    ]


    box_width = 65 * mm  # Ajusta el ancho según lo que quieras probar
    # Calcula el alto real sumando el alto de cada línea
    line_heights = []
    for line in address_info:
        p = Paragraph(line, styles['FooterContactInfoStyle'])
        w, h = p.wrap(box_width - 4 * mm, doc.bottomMargin)
        line_heights.append(h)

    box_x = doc.leftMargin + doc.width / 2 + 38 * mm
    box_y = 17 * mm + sum(line_heights[::-1][1:])  # Ajusta según tu diseño

    # Dibuja las líneas de dirección dentro del box, una debajo de otra
    current_y = box_y - 2 * mm  # Empieza desde arriba, deja margen superior
    for i, line in enumerate(address_info):
        p = Paragraph(line, styles['FooterContactInfoStyle'])
        w, h = p.wrap(box_width - 4 * mm, doc.bottomMargin)
        p.drawOn(canvas_obj, box_x , current_y - h ) 
        current_y -= h

    # Número de página (centrado en el pie de página)
    page_number = Paragraph(f"P. {doc.page}", styles['PageNumberStyle'])
    page_number.wrapOn(canvas_obj, doc.width, doc.bottomMargin)
    page_number_x = (doc.width - page_number.width) / 2 + doc.leftMargin
    page_number_y =  3 * mm  # Ajusta la posición Y según sea necesario
    page_number.drawOn(canvas_obj, page_number_x, page_number_y)

    # Fecha de generación del PDF
    generated_date = datetime.now(ZoneInfo("America/Lima")).strftime("%d/%m/%Y %H:%M:%S")
    generated_date_p = Paragraph(f"Generado el: {generated_date}", styles['PageNumberStyle'])
    generated_date_p.wrapOn(canvas_obj, doc.width, doc.bottomMargin)
    generated_date_x =  0 * mm
    generated_date_y = 3 * mm  # Ajusta la posición Y según sea necesario
    generated_date_p.drawOn(canvas_obj, generated_date_x, generated_date_y)     
    
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
                            rightMargin=20, leftMargin=20,
                            topMargin=23 * mm, bottomMargin=68 * mm)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    styles.add(ParagraphStyle(name='Intro', fontSize=12, leading=28, alignment=0,  fontName='Helvetica'))
    styles.add(ParagraphStyle(name='IntroIdent', fontSize=12, leading=28, alignment=0, firstLineIndent=100, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='HeaderStyle', fontSize=12, leading=14, spaceAfter=6, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=12, leading=12, spaceAfter=1))
    styles.add(ParagraphStyle(name='ItemHeaderStyle', fontSize=10, leading=12, alignment=1, fontName='Helvetica-Bold'),)
    styles.add(ParagraphStyle(name='ItemDataStyle', fontSize=9, leading=11 , alignment=2, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='TotalStyle', fontSize=14, leading=16, alignment=2, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CodeName', fontSize=10, leading=10, alignment=1, ))
    styles.add(ParagraphStyle(name='NumberItem', fontSize=10, leading=10, alignment=1, ))
    styles.add(ParagraphStyle(name="ProductName", fontSize=10, leading=10, alignment=0, fontName='Helvetica'))
    styles.add(ParagraphStyle(name="Quantity", fontSize=10, leading=10, alignment=1, fontName='Helvetica'))



    elements = []

    # Infor Store
    store_info = order.store

    # Información del cliente
    customer = order.customer
    if customer:
        customer_name = customer.business_name if customer.entity_type == 'J' else f"{customer.name} {customer.last_name}"
        if customer.entity_type == 'J' and customer.ruc:
            elements.append(Paragraph(f"<b>Razón Social:</b> {customer_name}", styles['NormalStyle']))
            elements.append(Paragraph(f"<b>RUC:</b> {customer.ruc}", styles['NormalStyle']))
            if customer.name and customer.last_name:
                elements.append(Paragraph(f"<b>Representante:</b> {customer.name} {customer.last_name}", styles['NormalStyle']))
        elif customer.entity_type == 'N' and (customer.dni or customer.doc_foreign):
            elements.append(Paragraph(f"<b>Sr(a): </b> {customer_name}", styles['NormalStyle']))
            if customer.doc_foreign:
                elements.append(Paragraph(f"<b>Doc. Extranjeria:</b> {customer.doc_foreign}", styles['NormalStyle']))
            if customer.dni:
                elements.append(Paragraph(f"<b>DNI:</b> {customer.dni}", styles['NormalStyle']))                 
        elements.append(Paragraph(f"<b>Celular:</b> {customer.phone_number}", styles['NormalStyle']))
        elements.append(Paragraph(f"<b>Email:</b> {customer.email}", styles['NormalStyle']))
    else:
        elements.append(Paragraph("Cliente no especificado.", styles['NormalStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # # Información de la orden
    # elements.append(Paragraph(f"<b>Orden ID:</b> {order.id}", styles['HeaderStyle']))
    # elements.append(Paragraph(f"<b>Fecha:</b> {order.created_at.strftime('%d/%m/%Y %H:%M')}", styles['NormalStyle']))
    # elements.append(Paragraph(f"<b>Estado:</b> {order.status.name if order.status else 'Desconocido'}", styles['NormalStyle']))
    # if order.store:
    #     elements.append(Paragraph(f"<b>Tienda:</b> {order.store.name}", styles['NormalStyle']))
    # elements.append(Spacer(1, 0.1 * inch))
    # Introduccion del PDF
    elements.append(Paragraph("De nuestra mayor consideracion:", styles['Intro']))
    elements.append(Paragraph("Es grato dirigirnos a Uds. a fin de hacerle llegar nuestra propuesta economica por lo siguiente:", styles['IntroIdent']))

    # Tabla de items
    data = [
        [
            Paragraph("<font color=white>Item</font>", styles['ItemHeaderStyle']),
            Paragraph("<font color=white>Codigo</font>", styles['ItemHeaderStyle']),
            Paragraph("<font color=white>Producto</font>", styles['ItemHeaderStyle']),
            Paragraph("<font color=white>Cant.</font>", styles['ItemHeaderStyle']),
            Paragraph("<font color=white>P.Unit</font>", styles['ItemHeaderStyle']),
            Paragraph("<font color=white>Importe</font>", styles['ItemHeaderStyle'])
        ]
    ]

    subtotal_row_indices = []
    extras_row_indices = []

    for idx, product in enumerate(display_items, start=1):
        # atributos del producto
        product_id = product.get('product_id')
        product_name = product.get('name') or ''
        sku = product.get('sku') or ''
        width = product.get('width') or 0
        linear_meter = product.get('linear_meter') or 0
        quantity = product.get('quantity') or 1
        price = product.get('price') or 0
        extra_options = product.get('extra_options', [])
        subtotal = product.get('subtotal') 
        total_extra_options = product.get('total_extra_options') 

        if product_id == 1:
             product_name = f"<b>{product_name}</b> | Largo: {linear_meter}m | Ancho: {width}m | Area: {linear_meter * width} m²"
        elif product_id is not None and 2 <= product_id <= 9:
            product_name  = f"<b>{product_name}</b> | Metro Lineal: {linear_meter} m"

        data.append([
            Paragraph(str(idx), styles['NumberItem']),
            Paragraph(f"<b>{sku}</b>", styles['CodeName']),
            Paragraph(product_name,styles['ProductName']),
            Paragraph(str(quantity), styles['Quantity']),
            Paragraph(f"{price:.2f}", styles['ItemDataStyle']),
            Paragraph(f"{price * quantity:.2f}", styles['ItemDataStyle']),
        ])

        if extra_options:
            data.append([
                Paragraph("", styles['ItemDataStyle']),
                Paragraph("", styles['ItemDataStyle']),
                Paragraph("Extras:", ),
                Paragraph("", styles['ItemDataStyle']),
                Paragraph("", styles['ItemDataStyle']),
                Paragraph("", styles['ItemDataStyle'])
            ])

            extras_row_indices.append(len(data) - 1)

            for extra in extra_options:
                extra_option_id = extra.get('extra_option_id')
                extra_name = extra.get('name')
                extra_linear_meter = extra.get('linear_meter')
                extra_width = extra.get('width')
                extra_quantity = extra.get('quantity', 1)
                # convertir a int el quantity si no tiene valor decimal pero si tiene queda como float
                if extra_quantity is not None and isinstance(extra_quantity, float) and extra_quantity.is_integer():
                    extra_quantity = int(extra_quantity)


                extra_price = extra.get('price')
                if 1 <= extra_option_id <= 4:
                    if 1 <= extra_option_id <= 2:
                        extra_name += f" | Seleccionado: {extra.get('giga_select')}"
                if extra_linear_meter and 5 <= extra_option_id <= 8:
                    extra_name += f" | Metro Lineal: {extra_linear_meter} m"
                if extra_linear_meter and 10 <= extra_option_id <= 13:
                    extra_name += f" | Largo: {extra_linear_meter}m | Ancho: {extra_width}m"
                
                data.append([
                    Paragraph("", ),
                    Paragraph("", ),
                    Paragraph(extra_name, ),
                    Paragraph(str(extra_quantity), styles['Quantity']),
                    Paragraph(f"{extra_price:.2f}", styles['ItemDataStyle']),
                    Paragraph(f"{extra_price * extra_quantity:.2f}", styles['ItemDataStyle'])
                ])

        data.append([
            Paragraph("",), 
            Paragraph("<b>Sub Total Producto:</b>", styles['ItemDataStyle']),
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
            Paragraph(f"{(subtotal or 0) + (total_extra_options or 0):.2f}", styles['ItemDataStyle'])
        ])
        subtotal_row_indices.append(len(data) - 1)

    # Totales
    gravado_row_idx = len(data)
    data.append([        
        Paragraph("<b>Gravado (S/.):</b>", styles['ItemDataStyle']),
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
        Paragraph(f'{order.total_amount:.2f}', styles['ItemDataStyle'])
    ])

    igv_row_idx = len(data)
    data.append([        
        Paragraph("<b>IGV 18% (S/.):</b>", styles['ItemDataStyle']),
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
        Paragraph(f'{(order.final_amount / 1.18) * 0.18:.2f}', styles['ItemDataStyle'])
    ])

    total_row_idx = len(data)
    data.append([        
        Paragraph("<b>Total Carrito (S/.):</b>", styles['ItemDataStyle']),
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
            Paragraph("",), 
        Paragraph(f'{order.final_amount:.2f}', styles['ItemDataStyle'])
    ])

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#ec2e2c")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]
    for idx in subtotal_row_indices:
        table_style.append(('SPAN', (1, idx), (4, idx)))
        # table_style.append(('SPAN', (0, idx), (1, idx)))


    for idx in extras_row_indices:
        table_style.append(('SPAN', (2, idx), (5, idx)))

    for idx in [gravado_row_idx, igv_row_idx, total_row_idx]:
        table_style.append(('SPAN', (0, idx), (4, idx )))



        
    table = Table(data, colWidths=[0.35 * inch,0.65*inch, 4.4* inch, 0.55*inch, 0.7*inch, 0.7*inch])
    table.setStyle(TableStyle(table_style))
    
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))




    # doc.build(elements, onFirstPage=_header_footer_template, onLaterPages=_header_footer_template)
    doc.build(
    elements,
    onFirstPage=lambda canvas_obj, doc: _header_footer_template(canvas_obj, doc, store_info),
    onLaterPages=lambda canvas_obj, doc: _header_footer_template(canvas_obj, doc, store_info)
)
    buffer.seek(0)
    return buffer