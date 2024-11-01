import streamlit as st
import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()


def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def query_data(query):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def display_query_results():
    st.header("Ejecutar Consultas SQL")


    query_selection = st.selectbox("Seleccione una consulta:", [
        "Ventas Totales por Producto",
        "Pedido Más Antiguo por Cliente",
        "Monto Máximo de Pedidos por Cliente",
        "Stock Promedio de Productos",
        "Estado de Pedidos",
        "Total de Pagos por Cliente",
        "Total de Pedidos por Cliente",
        "Promedio de Monto de Pedidos por Cliente",
        "Cantidad de Productos Vendidos por Producto",
        "Pagos Realizados en un Rango de Fechas",
        "Estado de Envíos por Dirección",
        "Clientes sin Pedidos",
        "Productos con Bajo Stock",
        "Total de Ventas por Mes",
        "Clientes que Realizaron el Mayor Número de Pedidos"
    ])

    if query_selection == "Ventas Totales por Producto":
        query = """
            SELECT 
                p.name AS producto,
                SUM(oi.quantity * oi.price) AS total_ventas
            FROM 
                Products p
            JOIN 
                OrderItems oi ON p.product_id = oi.product_id
            GROUP BY 
                p.name
            ORDER BY 
                total_ventas DESC;
        """
    elif query_selection == "Pedido Más Antiguo por Cliente":
        query = """
            SELECT 
                c.name AS cliente,
                MIN(o.order_date) AS fecha_pedido_mas_antiguo
            FROM 
                Customers c
            LEFT JOIN 
                Orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.name
            ORDER BY 
                fecha_pedido_mas_antiguo;
        """
    elif query_selection == "Monto Máximo de Pedidos por Cliente":
        query = """
            SELECT 
                c.name AS cliente,
                MAX(o.amount) AS maximo_pedido
            FROM 
                Customers c
            JOIN 
                Orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.name
            ORDER BY 
                maximo_pedido DESC;
        """
    elif query_selection == "Stock Promedio de Productos":
        query = """
            SELECT 
                AVG(stock) AS promedio_stock
            FROM 
                Products;
        """
    elif query_selection == "Estado de Pedidos":
        query = """
            SELECT 
                o.status AS estado,
                COUNT(o.id) AS total_pedidos
            FROM 
                Orders o
            GROUP BY 
                o.status
            ORDER BY 
                total_pedidos DESC;
        """
    elif query_selection == "Total de Pagos por Cliente":
        query = """
            SELECT 
                c.name AS cliente,
                SUM(p.amount) AS total_pagos
            FROM 
                Customers c
            JOIN 
                Orders o ON c.customer_id = o.customer_id
            JOIN 
                Payments p ON o.id = p.order_id
            GROUP BY 
                c.name
            ORDER BY 
                total_pagos DESC;
        """
    elif query_selection == "Total de Pedidos por Cliente":
        query = """
            SELECT 
                c.name AS cliente,
                COUNT(o.id) AS total_pedidos
            FROM 
                Customers c
            JOIN 
                Orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.name
            ORDER BY 
                total_pedidos DESC;
        """
    elif query_selection == "Promedio de Monto de Pedidos por Cliente":
        query = """
            SELECT 
                c.name AS cliente,
                AVG(o.amount) AS promedio_monto_pedido
            FROM 
                Customers c
            JOIN 
                Orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.name
            ORDER BY 
                promedio_monto_pedido DESC;
        """
    elif query_selection == "Cantidad de Productos Vendidos por Producto":
        query = """
            SELECT 
                p.name AS producto,
                SUM(oi.quantity) AS total_vendidos
            FROM 
                Products p
            JOIN 
                OrderItems oi ON p.product_id = oi.product_id
            GROUP BY 
                p.name
            ORDER BY 
                total_vendidos DESC;
        """
    elif query_selection == "Pagos Realizados en un Rango de Fechas":
        query = """
            SELECT 
                SUM(p.amount) AS total_pagado,
                COUNT(p.id) AS cantidad_pagos
            FROM 
                Payments p
            WHERE 
                p.payment_date BETWEEN '2023-01-01' AND '2023-12-31';  -- Ajusta las fechas según sea necesario
        """
    elif query_selection == "Estado de Envíos por Dirección":
        query = """
            SELECT 
                s.shipping_address AS direccion_envio,
                COUNT(s.order_id) AS total_envios
            FROM 
                Shipping s
            GROUP BY 
                s.shipping_address
            ORDER BY 
                total_envios DESC;
        """
    elif query_selection == "Clientes sin Pedidos":
        query = """
            SELECT 
                c.name AS cliente
            FROM 
                Customers c
            LEFT JOIN 
                Orders o ON c.customer_id = o.customer_id
            WHERE 
                o.id IS NULL;
        """
    elif query_selection == "Productos con Bajo Stock":
        query = """
            SELECT 
                p.name AS producto,
                p.stock AS stock_actual
            FROM 
                Products p
            WHERE 
                p.stock < 10  -- Ajusta el umbral según tus necesidades
            ORDER BY 
                p.stock ASC;
        """
    elif query_selection == "Total de Ventas por Mes":
        query = """
            SELECT 
                DATE_FORMAT(o.order_date, '%Y-%m') AS mes,
                SUM(oi.quantity * oi.price) AS total_ventas
            FROM 
                Orders o
            JOIN 
                OrderItems oi ON o.id = oi.order_id
            GROUP BY 
                mes
            ORDER BY 
                mes;
        """
    elif query_selection == "Clientes que Realizaron el Mayor Número de Pedidos":
        query = """
            SELECT 
                c.name AS cliente,
                COUNT(o.id) AS total_pedidos
            FROM 
                Customers c
            JOIN 
                Orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.name
            ORDER BY 
                total_pedidos DESC
            LIMIT 10;  -- Ajusta el límite según tus necesidades
        """

   
    if st.button("Ejecutar consulta"):
        results = query_data(query)
        if results:
           
            df_results = pd.DataFrame(results)
            if query_selection in ["Ventas Totales por Producto", "Monto Máximo de Pedidos por Cliente", "Total de Pagos por Cliente", "Total de Pedidos por Cliente", "Promedio de Monto de Pedidos por Cliente", "Cantidad de Productos Vendidos por Producto"]:
                df_results.columns = ["Producto/Cliente", "Resultado"]
            elif query_selection == "Pedido Más Antiguo por Cliente":
                df_results.columns = ["Cliente", "Fecha del Pedido Más Antiguo"]
            elif query_selection == "Stock Promedio de Productos":
                df_results.columns = ["Promedio de Stock"]
            elif query_selection == "Estado de Pedidos":
                df_results.columns = ["Estado", "Total de Pedidos"]
            elif query_selection == "Total de Ventas por Mes":
                df_results.columns = ["Mes", "Total Ventas"]
            elif query_selection == "Clientes que Realizaron el Mayor Número de Pedidos":
                df_results.columns = ["Cliente", "Total de Pedidos"]
            elif query_selection == "Pagos Realizados en un Rango de Fechas":
                df_results.columns = ["Total Pagado", "Cantidad de Pagos"]
            elif query_selection == "Estado de Envíos por Dirección":
                df_results.columns = ["Dirección de Envío", "Total de Envíos"]
            elif query_selection == "Clientes sin Pedidos":
                df_results.columns = ["Cliente"]
            elif query_selection == "Productos con Bajo Stock":
                df_results.columns = ["Producto", "Stock Actual"]

            st.write("Resultados:")
            st.dataframe(df_results)
        else:
            st.write("No se encontraron resultados.")


def add_manual_data(table_name):
    if table_name == "Customers":
        name = st.text_input("Nombre")
        email = st.text_input("Email")
        phone = st.text_input("Teléfono")

        if st.button("Agregar Cliente"):
            data = pd.DataFrame({'name': [name], 'email': [email], 'phone': [phone]})
            insert_data("Customers", data)
            st.success("Cliente agregado exitosamente.")

    elif table_name == "Products":
        name = st.text_input("Nombre del Producto")
        description = st.text_area("Descripción")
        price = st.number_input("Precio", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock", min_value=0)

        if st.button("Agregar Producto"):
            data = pd.DataFrame({'name': [name], 'description': [description], 'price': [price], 'stock': [stock]})
            insert_data("Products", data)
            st.success("Producto agregado exitosamente.")

    elif table_name == "Orders":
        order_date = st.date_input("Fecha del Pedido")
        customer_id = st.number_input("ID del Cliente", min_value=1)
        amount = st.number_input("Monto", min_value=0.0, format="%.2f")
        status = st.selectbox("Estado", ["Pending", "Completed", "Shipped"])

        if st.button("Agregar Pedido"):
            data = pd.DataFrame({'order_date': [order_date], 'customer_id': [customer_id], 'amount': [amount], 'status': [status]})
            insert_data("Orders", data)
            st.success("Pedido agregado exitosamente.")

    elif table_name == "OrderItems":
        order_id = st.number_input("ID del Pedido", min_value=1)
        product_id = st.number_input("ID del Producto", min_value=1)
        quantity = st.number_input("Cantidad", min_value=1)
        price = st.number_input("Precio", min_value=0.0, format="%.2f")

        if st.button("Agregar Item de Pedido"):
            data = pd.DataFrame({'order_id': [order_id], 'product_id': [product_id], 'quantity': [quantity], 'price': [price]})
            insert_data("OrderItems", data)
            st.success("Item de pedido agregado exitosamente.")

    elif table_name == "Payments":
        order_id = st.number_input("ID del Pedido", min_value=1)
        amount = st.number_input("Monto", min_value=0.0, format="%.2f")
        payment_date = st.date_input("Fecha de Pago")

        if st.button("Agregar Pago"):
            data = pd.DataFrame({'order_id': [order_id], 'amount': [amount], 'payment_date': [payment_date]})
            insert_data("Payments", data)
            st.success("Pago agregado exitosamente.")

    elif table_name == "Shipping":
        order_id = st.number_input("ID del Pedido", min_value=1)
        shipping_address = st.text_input("Dirección de Envío")
        shipping_date = st.date_input("Fecha de Envío")
        delivery_date = st.date_input("Fecha de Entrega")
        tracking_number = st.text_input("Número de Seguimiento")

        if st.button("Agregar Envío"):
            data = pd.DataFrame({'order_id': [order_id], 'shipping_address': [shipping_address], 'shipping_date': [shipping_date], 'delivery_date': [delivery_date], 'tracking_number': [tracking_number]})
            insert_data("Shipping", data)
            st.success("Envío agregado exitosamente.")


st.title("Carga de Datos desde Archivo Excel")


table_selection = st.sidebar.selectbox("Seleccione la tabla para cargar datos:", [
    "Customers", "Products", "Orders", "OrderItems", "Payments", "Shipping"
])


add_manual_data(table_selection)


uploaded_file = st.file_uploader("Cargue un archivo Excel", type=["xlsx"])

if uploaded_file:
    
    try:
        data = pd.read_excel(uploaded_file)

        
        st.write("Datos cargados del archivo:")
        st.write(data)

       
        if st.button("Cargar datos en la base de datos"):
            insert_data(table_selection, data)
            st.success("Datos cargados exitosamente en la tabla seleccionada.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")


display_query_results()
