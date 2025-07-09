# src/application/services/pdf_generator.py

from pydantic import BaseModel
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from io import BytesIO
from typing import List, Optional

# Importa los DTOs desde sus ubicaciones correctas en src/application/dtos
from src.application.dtos.order import OrderResponseDto
from src.application.dtos.customer import CustomerResponseDto
from src.application.dtos.order_detail import OrderDetailResponseDto
from src.application.dtos.product import ProductResponseDto

# Para los DisplayCartItem que vienen del frontend, los definimos aquí o en un schema/dto específico para la comunicación frontend
# Si los DisplayCartItem son solo para el PDF y no se persisten en este formato, definirlos aquí es aceptable.
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

from datetime import datetime

def generate_order_pdf(
    order: OrderResponseDto,  # Ahora esperamos OrderResponseDto
    display_items: List[DisplayCartItemSchema], # Los items detallados desde el frontend
) -> BytesIO:
    """
    Genera un PDF de orden/factura utilizando ReportLab.

    Args:
        order: El objeto de la orden (OrderResponseDto) desde tu backend.
        display_items: Lista de DisplayCartItemSchema desde el frontend,
                       usados para detalles de los productos (nombre, SKU, etc.).
                       NOTA: Para facturas OFICIALES, los precios DEBERÍAN
                       validarse contra los de `order.details` para evitar fraudes.

    Returns:
        Un objeto BytesIO que contiene el PDF generado.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=30,
                            leftMargin=30,
                            topMargin=30,
                            bottomMargin=30)
    
    styles = getSampleStyleSheet()

    # Estilos personalizados
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, leading=28, alignment=1, spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='HeaderStyle', fontSize=12, leading=14, spaceAfter=6, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=10, leading=12, spaceAfter=3))
    styles.add(ParagraphStyle(name='ItemHeaderStyle', fontSize=10, leading=12, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ItemDataStyle', fontSize=9, leading=11))
    styles.add(ParagraphStyle(name='TotalStyle', fontSize=14, leading=16, alignment=2, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='FooterStyle', fontSize=8, leading=10, alignment=1, spaceBefore=20))

    elements = []

    # --- Encabezado General ---
    elements.append(Paragraph("Presupuesto / Factura de Venta", styles['TitleStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # Información de la Empresa (Placeholder)
    elements.append(Paragraph("<b>Tu Empresa S.A.C.</b>", styles['HeaderStyle']))
    elements.append(Paragraph("RUC: 20XXXXXXXXX", styles['NormalStyle']))
    elements.append(Paragraph("Dirección: Av. Siempre Viva 742, Los Olivos, Lima", styles['NormalStyle']))
    elements.append(Paragraph("Teléfono: +51 987 654 321 | Email: info@tuempresa.com", styles['NormalStyle']))
    elements.append(Spacer(1, 0.2 * inch))

    # --- Información de la Orden y Cliente ---
    elements.append(Paragraph(f"<b>Orden ID:</b> {order.id}", styles['HeaderStyle']))
    elements.append(Paragraph(f"<b>Fecha:</b> {order.created_at.strftime('%d/%m/%Y %H:%M')}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>Estado:</b> {order.status.name if order.status else 'Desconocido'}", styles['NormalStyle'])) # Usa order.status.name
    if order.store:
        elements.append(Paragraph(f"<b>Tienda:</b> {order.store.name}", styles['NormalStyle']))
    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph("<b>Información del Cliente:</b>", styles['HeaderStyle']))
    customer = order.customer # Accede al cliente desde el DTO de la orden
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

    # --- Tabla de Ítems del Carrito/Orden ---
    data = [
        [
            Paragraph("SKU", styles['ItemHeaderStyle']),
            Paragraph("Producto", styles['ItemHeaderStyle']),
            Paragraph("Dimensiones", styles['ItemHeaderStyle']),
            Paragraph("Opciones Extra", styles['ItemHeaderStyle']),
            Paragraph("Cant.", styles['ItemHeaderStyle']),
            Paragraph("P. Unit.", styles['ItemHeaderStyle']),
            Paragraph("Subtotal", styles['ItemHeaderStyle'])
        ]
    ]

    for item in display_items: # Iteramos sobre los display_items del frontend
        dimensions_str = ""
        if item.height and item.width:
            dimensions_str += f"{item.height}cm x {item.width}cm"
        if item.linear_meter:
            if dimensions_str: dimensions_str += " / "
            dimensions_str += f"{item.linear_meter} m L"
        if not dimensions_str:
            dimensions_str = "-"

        extra_options_str = ""
        if item.extra_options:
            extra_options_str = "\n".join([
                f"{opt.name} (x{opt.quantity}) " + (f"- {opt.linear_meter}m L" if opt.linear_meter else "")
                for opt in item.extra_options
            ])
        else:
            extra_options_str = "-"
        
        # Usamos los precios y subtotales de DisplayCartItemSchema para el PDF "raw" como se pidió.
        # Para una factura final, idealmente se usarían los precios_at_order del OrderDetailResponseDto
        # del backend para cada item y se recalcularía el subtotal aquí.
        
        data.append([
            Paragraph(item.sku or '-', styles['ItemDataStyle']),
            Paragraph(item.name, styles['ItemDataStyle']),
            Paragraph(dimensions_str, styles['ItemDataStyle']),
            Paragraph(extra_options_str, styles['ItemDataStyle']),
            Paragraph(str(item.quantity), styles['ItemDataStyle']),
            Paragraph(f"S/. {item.price:.2f}", styles['ItemDataStyle']),
            Paragraph(f"S/. {item.subtotal:.2f}", styles['ItemDataStyle']) # subtotal del item del frontend
        ])

    table = Table(data, colWidths=[1.0*inch, 1.8*inch, 1.2*inch, 1.8*inch, 0.6*inch, 0.9*inch, 0.9*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

    # --- Totales (estos siempre vienen de la orden del backend) ---
    elements.append(Paragraph(f"<b>Total Base:</b> S/. {order.total_amount:.2f}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>Margen de Ganancia:</b> S/. {order.profit_margin:.2f}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>Descuento Aplicado:</b> S/. {order.discount_applied:.2f}", styles['NormalStyle']))
    elements.append(Paragraph(f"<b>TOTAL FINAL:</b> S/. {order.final_amount:.2f}", styles['TotalStyle']))
    elements.append(Spacer(1, 0.5 * inch))

    # --- Notas (si las hay en la orden) ---
    if order.notes:
        elements.append(Paragraph(f"<b>Notas:</b>", styles['HeaderStyle']))
        elements.append(Paragraph(order.notes, styles['NormalStyle']))
        elements.append(Spacer(1, 0.2 * inch))

    # Pie de página
    elements.append(Paragraph("Gracias por su compra!", styles['FooterStyle']))
    elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['FooterStyle']))

    doc.build(elements)
    buffer.seek(0)
    return buffer