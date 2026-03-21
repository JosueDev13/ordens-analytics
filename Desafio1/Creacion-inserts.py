import csv
from datetime import datetime

customers = {}
products = {}
locations = {}
orders = {}
sales = []

def clean_text(text):
    return text.replace("'", "''") if text else ''

with open('/Users/joshuasaib/Desktop/Desafio1/Desafio1_DMD941-2.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    reader.fieldnames = [col.strip() for col in reader.fieldnames]

    for row in reader:

        prod_id = row['Product ID']
        if prod_id and prod_id not in products:
            products[prod_id] = (
                prod_id,
                clean_text(row['Category']),
                clean_text(row['Sub-Category']),
                clean_text(row['Product Name'])
            )

        try:
            if row['Sales'] == '':
                continue

            sales_value = float(row['Sales'])
            order_date = datetime.strptime(row['Order Date'], '%m/%d/%Y')
            ship_date = datetime.strptime(row['Ship Date'], '%m/%d/%Y')

            cust_id = row['Customer ID']
            if cust_id and cust_id not in customers:
                customers[cust_id] = (
                    cust_id,
                    clean_text(row['Customer Name']),
                    clean_text(row['Segment'])
                )
            loc_key = (
                row['Country'],
                row['City'],
                row['State'],
                row['Postal Code'],
                row['Region']
            )

            if loc_key not in locations:
                locations[loc_key] = len(locations) + 1

            location_id = locations[loc_key]

            order_id = row['Order ID']
            if order_id and order_id not in orders:
                orders[order_id] = (
                    order_id,
                    order_date.strftime('%Y-%m-%d'),
                    ship_date.strftime('%Y-%m-%d'),
                    clean_text(row['Ship Mode']),
                    cust_id
                )
            sales.append((
                order_id,
                prod_id,
                location_id,
                sales_value
            ))

        except Exception as e:
            print("Error en fila:", row)
            print("Detalle:", e)
            continue
#Aqui generamos los scripts
with open('/Users/joshuasaib/Desktop/Desafio1/output.sql', 'w', encoding='utf-8') as f:

    # CUSTOMERS
    for c in customers.values():
        f.write(f"""
INSERT INTO customers (customer_id, customer_name, segment)
VALUES ('{c[0]}', '{c[1]}', '{c[2]}');
""")

    # PRODUCTS
    for p in products.values():
        f.write(f"""
INSERT INTO products (product_id, category, sub_category, product_name)
VALUES ('{p[0]}', '{p[1]}', '{p[2]}', '{p[3]}');
""")

    # LOCATIONS
    for loc, loc_id in locations.items():
        f.write(f"""
INSERT INTO locations (location_id, country, city, state, postal_code, region)
VALUES ({loc_id}, '{loc[0]}', '{loc[1]}', '{loc[2]}', '{loc[3]}', '{loc[4]}');
""")

    # ORDERS
    for o in orders.values():
        f.write(f"""
INSERT INTO orders (order_id, order_date, ship_date, ship_mode, customer_id)
VALUES ('{o[0]}', '{o[1]}', '{o[2]}', '{o[3]}', '{o[4]}');
""")

    # SALES
    for s in sales:
        f.write(f"""
INSERT INTO sales (order_id, product_id, location_id, sales)
VALUES ('{s[0]}', '{s[1]}', {s[2]}, {s[3]});
""")

print("Script SQL generado correctamente xd")