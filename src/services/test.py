# src/application/services/pdf_generator.py

from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from io import BytesIO
from typing import List, Optional
from datetime import datetime

# Importa los DTOs desde sus ubicaciones correctas en src/application/dtos
from src.application.dtos.order import OrderResponseDto
from src.application.dtos.customer import CustomerResponseDto
from src.application.dtos.order_detail import OrderDetailResponseDto
from src.application.dtos.product import ProductResponseDto

# Para los DisplayCartItem que vienen del frontend, los definimos aquí o en un schema/dto específico para la comunicación frontend
# Si los DisplayCartItem son solo para el PDF y no se persisten en este formato, definir aquí es aceptable.
# Si se usan para otras comunicaciones, irían en src/application/dtos/cart_display.py por ejemplo.
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


def generate_order_pdf(
    order: OrderResponseDto,
    display_items: List[dict]
) -> BytesIO:
    """
    Genera un PDF de orden/factura utilizando ReportLab con un formato similar al presupuesto.pdf.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    styles.add(ParagraphStyle(name='HeaderCompanyStyle', fontSize=12, leading=14, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderClientStyle', fontSize=10, leading=12, alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=10, leading=12, spaceAfter=3))
    styles.add(ParagraphStyle(name='SmallNormalStyle', fontSize=9, leading=11, spaceAfter=2))
    styles.add(ParagraphStyle(name='ItemHeaderStyle', fontSize=10, leading=12, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ItemDataStyle', fontSize=9, leading=11))
    styles.add(ParagraphStyle(name='TotalStyle', fontSize=10, leading=12, alignment=2, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='FooterStyle', fontSize=8, leading=10, alignment=1, spaceBefore=10))
    styles.add(ParagraphStyle(name='ContactInfoStyle', fontSize=9, leading=11, alignment=0))


    elements = []

    # Información de la empresa (similar a la cabecera del presupuesto.pdf)
    elements.append(Paragraph(f"Lima, {datetime.now().strftime('%d de %B de %Y')}", styles['NormalStyle']))
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph("<b>LASER COLOR VELOZ</b>", styles['HeaderCompanyStyle']))
    elements.append(Paragraph("EDITORIAL GLOBAL MULTIPRINT EIRL", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))

    # Información del cliente
    customer = order.customer
    if customer:
        customer_name = customer.business_name if customer.entity_type == 'J' else f"{customer.name} {customer.last_name}"
        elements.append(Paragraph(f"Señores: <b>{customer_name}</b>", styles['HeaderClientStyle']))
        if customer.entity_type == 'J' and customer.ruc:
            elements.append(Paragraph(f"Ruc: {customer.ruc}", styles['NormalStyle']))
        elif customer.entity_type == 'N' and customer.dni:
            elements.append(Paragraph(f"DNI: {customer.dni}", styles['NormalStyle']))
        elements.append(Paragraph("De nuestra mayor consideración:", styles['NormalStyle']))
    else:
        elements.append(Paragraph("Señores: Cliente no especificado", styles['HeaderClientStyle']))
        elements.append(Paragraph("De nuestra mayor consideración:", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph("<b>FACTURA PROFORMA:</b>", styles['HeaderClientStyle']))
    elements.append(Spacer(1, 10 * mm))


    # Tabla de items (ajustada a 4 columnas y contenido de descripción combinado)
    data = [
        [
            Paragraph("CANT", styles['ItemHeaderStyle']),
            Paragraph("DESCRIPCIÓN", styles['ItemHeaderStyle']),
            Paragraph("PRECIO UNID.", styles['ItemHeaderStyle']),
            Paragraph("PRECIO", styles['ItemHeaderStyle'])
        ]
    ]

    total_general = 0.0

    for item in display_items:
        # Construir string de descripción completo
        description_parts = [Paragraph(item['name'], styles['ItemDataStyle'])]

        dimensions_str = ""
        if item.get('height') and item.get('width'):
            dimensions_str += f"{item['height']}cm x {item['width']}cm"
        if item.get('linear_meter'):
            if dimensions_str: 
                dimensions_str += " / "
            dimensions_str += f"{item['linear_meter']} m L"
        if dimensions_str:
            description_parts.append(Paragraph(dimensions_str, styles['SmallNormalStyle']))
        
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
            description_parts.append(Paragraph("Opciones Extra:", styles['SmallNormalStyle']))
            for opt_p in extra_options_list:
                description_parts.append(Paragraph(opt_p, styles['SmallNormalStyle']))
        
        # Asumiendo una "Presentación del producto" si aplica
        # description_parts.append(Paragraph("Presentación del producto: Individual, caja y bolsa plástica transparente", styles['SmallNormalStyle']))
        # description_parts.append(Paragraph("Impresión blanco un lado", styles['SmallNormalStyle']))

        producto_subtotal = item['price'] * item['quantity']
        item_total = producto_subtotal + item.get('total_extra_options', 0)
        total_general += item_total

        data.append([
            Paragraph(str(item['quantity']), styles['ItemDataStyle']),
            description_parts, # Esto será una lista de elementos ReportLab
            Paragraph(f"S/. {item['price']:.2f}", styles['ItemDataStyle']),
            Paragraph(f"S/. {item_total:.2f}", styles['ItemDataStyle'])
        ])

    # Fila del total al final de la tabla
    data.append([
        Paragraph("", styles['ItemHeaderStyle']),
        Paragraph("TOTAL", styles['ItemHeaderStyle']),
        Paragraph("", styles['ItemHeaderStyle']),
        Paragraph(f"S/. {total_general:.2f}", styles['ItemHeaderStyle'])
    ])

    table = Table(data, colWidths=[0.8*inch, 3.2*inch, 1.2*inch, 1.2*inch]) # Ancho de columnas ajustado para 4 columnas
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")), # Color de fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'), # Alineación de encabezados
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white), # Fondo blanco para las filas de datos
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('SPAN', (1, -1), (2, -1)), # Fusionar celdas para la fila TOTAL
        ('ALIGN', (3, -1), (3, -1), 'RIGHT'), # Alineación del total final
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'), # Negrita para la fila TOTAL
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E0E0E0")), # Fondo para la fila TOTAL
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

    # Frase de propuesta económica
    elements.append(Paragraph("Es grato dirigirnos a Uds. A fin de hacerles llegar nuestra propuesta económica por lo siguiente:", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))

    # Detalles de la factura (Fecha y Factura Proforma)
    elements.append(Paragraph("<b>FECHA:</b> Lima, 18 de Noviembre del 2024", styles['NormalStyle']))
    elements.append(Paragraph("<b>FACTURA PROFORMA:</b>", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))

    # Modalidad de cobro
    elements.append(Paragraph("<b>MODALIDAD DE COBRO</b>", styles['HeaderCompanyStyle']))
    elements.append(Paragraph("EFECTIVO:", styles['NormalStyle']))
    elements.append(Paragraph("VISA", styles['NormalStyle']))
    elements.append(Paragraph("TRANSFERENCIA:", styles['NormalStyle']))
    elements.append(Paragraph("BCP", styles['NormalStyle']))
    elements.append(Paragraph("N° DE CTA.: BCP 191-2536429-0-93", styles['NormalStyle']))
    elements.append(Paragraph("INTERBANCARIA: 00219100253642909359", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))

    # Condiciones
    elements.append(Paragraph("Adelanto del 50%, con previa aprobación de la muestra.", styles['NormalStyle']))
    elements.append(Paragraph("El delivery no esta considerada en la cotización", styles['NormalStyle']))
    elements.append(Spacer(1, 5 * mm))

    # Información de contacto y dirección de la empresa
    elements.append(Paragraph("995558329", styles['ContactInfoStyle']))
    elements.append(Paragraph("laser.guizado.plaza@gmail.com", styles['ContactInfoStyle']))
    elements.append(Paragraph("www.lasercolorveloz.com", styles['ContactInfoStyle']))
    elements.append(Paragraph("958863047 :745 9011", styles['ContactInfoStyle']))
    elements.append(Paragraph("con la calidad Canon", styles['ContactInfoStyle']))
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph("C.C. Guizado Record Plaza", styles['ContactInfoStyle']))
    elements.append(Paragraph("1er Piso Stand 102 A-194", styles['ContactInfoStyle']))
    elements.append(Paragraph("Jr. Huaraz 1717 (altura de la Cra. 9 de la Av. Brasil)", styles['ContactInfoStyle']))
    elements.append(Paragraph("Breña", styles['ContactInfoStyle']))
    elements.append(Spacer(1, 2 * mm))


    doc.build(elements)
    buffer.seek(0)
    return buffer