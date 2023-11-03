import csv
import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Función para importar datos desde un archivo CSV a una tabla específica
def import_csv_to_table(csv_file_path, table_name, columns):
    with open(csv_file_path, 'r') as csv_file:
        # Omitir la cabecera
        dr = csv.DictReader(csv_file)
        to_db = [[i[col] for col in columns] for i in dr]

    placeholders = ', '.join('?' * len(columns))  # Crea los placeholders para la consulta SQL
    cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});", to_db)
    conn.commit()

# Ejemplo de cómo llamar a la función para cada tabla
import_csv_to_table('csv/categories.csv', 'categories', ['name', 'slug'])
import_csv_to_table('csv/users.csv', 'users', ['name', 'email', 'password'])
import_csv_to_table('csv/products.csv', 'products', ['title', 'description', 'photo', 'price', 'category_id', 'seller_id'])
# ... y así sucesivamente para las demás tablas

# No olvides cerrar la conexión a la base de datos
conn.close()