import json
import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Parsa1385parsa@',
    'database': 'codescraper'
}

json_file = 'cleaned_info_Divar.json'
target_table = 'divar'

try:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"file {json_file} khonde shod {len(data)} radif peyda shod.")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("password va username dorost bode etesal bargharare")

    query = f"""
    INSERT INTO {target_table} (
        title, area, built_year, room, floor, max_floor, sale, rent,
        elevator, parking, storage_room, image_link, location,
        rent_price, deposit_price, sale_price, price_per_m2
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """