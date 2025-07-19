import pandas as pd
from io import StringIO

def generate_orders_csv(orders):
    data = []
    for order in orders:
        data.append({
            "ID": order.id,
            "Cliente": getattr(order.customer, "name", ""),
            "Tienda": getattr(order.store, "name", ""),
            "Estado": getattr(order.status, "name", ""),
            "Total": order.final_amount,
            "Fecha": order.created_at.strftime("%d/%m/%Y %H:%M") if order.created_at else ""
        })
    df = pd.DataFrame(data)
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output