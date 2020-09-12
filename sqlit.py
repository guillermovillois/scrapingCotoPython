import sqlite3
from product import product

conn = sqlite3.connect("coto_products2.db")
from datetime import date

dia = date.today()
c = conn.cursor()

# c.execute(
#     """CREATE TABLE products (
#             main_category text,
#             category text,
#             sub_category text,
#             sku text,
#             name text,
#             price integer,
#             date integer
#             )"""
# )

# c.execute("""DELETE FROM products WHERE date='2020-08-26';""")
# def insert_product(prod):
#     with conn:
#         c.execute("INSERT INTO products VALUES(?,?,?,?,?)", (
#             prod.category, prod.sku, prod.name, prod.price, prod.date))
#     print(product(prod.category, prod.sku, prod.name, prod.price))


# def get_product_by_sku(sku):
#     c.execute("SELECT * FROM products WHERE sku=='{}'".format(sku))
#     return c.fetchall()


# print(product('Harinas', '29304', 'harina', 55.3))
# insert_product(product('Harinas', '29304', 'harina', 55.3))
# print(get_product_by_sku('29304'))
# c.execute("SELECT count(*) FROM products")
# print(c.fetchall())
# print(date.today())
# c.execute("""DELETE FROM products WHERE date='2020-09-02';""".format(date.today()))

# c.execute('''DELETE FROM products WHERE date='{}';'''.format(date.today()))
# insert_product(
#     product(
#         "Almacén",
#         "Golosinas",
#         "Alfajores",
#         "00002722",
#         "Alfajor Terrabusi Chocolate 50 Gr X 6 Uni",
#         "185.39",
#     )
# )
# c.execute("""SELECT * FROM products WHERE DATE='2020-08-26' """ "")
c.execute("SELECT  *  FROM products limit 5")
c.execute("SELECT price, date FROM products where sku='00002722'")
# c.execute("""SELECT REPLACE('2020-09-03','03','02');""")
# c.execute("SELECT count(date) FROM products")
# c.execute("SELECT distinct date FROM products")
print(c.fetchall())
conn.commit()


conn.close()
