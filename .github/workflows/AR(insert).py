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

    inserted_rows = 0
    for item in data:
        image_link = ','.join(item['image_link']) if item.get('image_link') and isinstance(item['image_link'], list) else None
        
        sale_price = item.get('sale_price') if item.get('sale', False) else None
        price_per_m2 = item.get('price_per_m2') if item.get('sale', False) else None
        rent_price = item.get('rent_price') if item.get('rent', False) else None
        deposit_price = item.get('deposit_price') if item.get('rent', False) else None

        values = (
            item.get('title'),
            item.get('area'),
            item.get('built_year'),
            item.get('room'),
            item.get('floor'),
            item.get('max_floor'),
            item.get('sale'),
            item.get('rent'),
            item.get('elevator'),
            item.get('parking'),
            item.get('storage_room'),
            image_link,
            item.get('location'),
            rent_price,
            deposit_price,
            sale_price,
            price_per_m2
        )
        try:
            cursor.execute(query, values)
            inserted_rows += 1
        except KeyError as e:
            print(f"{e} '{item.get('title', 'نامشخص')} eror")
        except Error as e:
            print(f"'{item.get('title', 'نامشخص')}': {e} eror")

    conn.commit()
    print(f"{inserted_rows} radif be dorosti {target_table} vared shod dakhelesh")

except Error as e:
    print(f"{e} eror ")
    print("database mordnazar vojod nadare")

except FileNotFoundError:
    print(f"{json_file} eror ")

except json.JSONDecodeError:
    print(f"{json_file} eror")

finally:
    try:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("etesal database baste shod")
    except:
        pass