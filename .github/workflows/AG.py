# ----------------------------------------------- imports
import requests
import re
# import json
from geopy.geocoders import Nominatim
# ----------------------------------------------- response

token = "AaSswxJp"

url = f"https://api.divar.ir/v8/posts-v2/web/{token}"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "br, gzip, deflate",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "origin": "https://divar.ir",
    "referer": f"https://divar.ir/v/{token}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers).json()

# ----------------------------------------------- functions
# -------------------- h_title
def house_title(response):
    try:
        h_title = response['sections'][1]['widgets'][0]['data']['title']
    except Exception:
        h_title = None

    return h_title

# -------------------- h_area
def house_area(response):
    try:
        h_area = ''
        for item in response['sections'][4]['widgets'][0]['data']['items']:
            if item['title'] == 'متراژ':
                h_area = item['value']
    except Exception:
        h_area = None

    return h_area

# -------------------- h_built_year
def house_built_year(response):
    try:
        h_built_year = ''
        for item in response['sections'][4]['widgets'][0]['data']['items']:
            if item['title'] == 'ساخت':
                h_built_year = item['value']
    except Exception:
        h_built_year = None

    return h_built_year

# -------------------- h_room
def house_room(response):
    try:
        h_room = ''
        for item in response['sections'][4]['widgets'][0]['data']['items']:
            if item['title'] == 'اتاق':
                h_room = item['value']
    except Exception:
        h_room = None

    return h_room

# -------------------- h_sale_price
def house_sale_price(response):
    try:
        h_price = ''
        for item in response['sections'][4]['widgets']:
            if re.findall(r"'title': 'قیمت کل', 'value': '(.*)',", str(item['data'])) != []:
                h_price = re.findall(r"'title': 'قیمت کل', 'value': '(.*)',", str(item['data']))[0]
    except Exception:
        h_price = None

    return h_price

# -------------------- h_price_per_square_meter
def house_price_per_square_meter(response):
    try:
        h_price_per_square_meter = ''
        for item in response['sections'][4]['widgets']:
            if re.findall(r"'title': 'قیمت هر متر', 'value': '(.*)',", str(item['data'])) != []:
                h_price_per_square_meter = re.findall(r"'title': 'قیمت هر متر', 'value': '(.*)',", str(item['data']))[0]
    except Exception:
        h_price_per_square_meter = None

    return h_price_per_square_meter

# -------------------- h_rent_price
def house_rent_price(response):
    try:
        h_rent_price = ''
        for item in response['sections'][4]['widgets']:
            if re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data'])) != []:
                h_rent_price = re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data']))[0]
    except Exception:
        h_rent_price = None

    return h_rent_price

# -------------------- h_deposit_price
def house_deposit_price(response):
    try:
        h_deposit_price = ''
        for item in response['sections'][4]['widgets']:
            if re.findall(r"'title': 'ودیعه', 'value': '(.*)',", str(item['data'])) != []:
                h_deposit_price = re.findall(r"'title': 'ودیعه', 'value': '(.*)',", str(item['data']))[0]
    except Exception:
        h_deposit_price = None

    return h_deposit_price

# -------------------- h_floor
def house_floor(response):
    try:
        h_floor = ''
        for item in response['sections'][4]['widgets']:
            if re.findall(r"'title': 'طبقه', 'value': '(.*)',", str(item['data'])) != []:
                h_floor = re.findall(r"'title': 'طبقه', 'value': '(.*)',", str(item['data']))[0]
    except Exception:
        h_floor = None

    return h_floor

# -------------------- h_location
def house_location(response):
    geolocator = Nominatim(user_agent="my-geocoder")
    try:
        latitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point']['latitude']
    except Exception:
        latitude = None

    try:
        longitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point']['longitude']
    except Exception:
        longitude = None

    if latitude is None or longitude is None:
        return None
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return None

    h_location = geolocator.reverse((latitude, longitude), language='fa')
    return h_location.address if h_location else None

# -------------------- h_image_link
def house_image_link(response):
    try:
        h_image_link = []
        for number_photo in range(0, 20):
            try:
                h_image_link.append(
                    response['sections'][3]['widgets'][0]['data']['items'][number_photo]['image']['url'])
            except IndexError:
                pass
    except Exception:
        h_image_link = None

    return h_image_link

# -------------------- h_elevator
def house_elevator(response):
    h_elevator = ''
    for item in response['sections'][4]['widgets']:
        if re.findall(r'آسانسور ندارد', str(item)) != []:
            h_elevator = False
            break
        elif re.findall(r'آسانسور', str(item)) != []:
            h_elevator = True
            break
        else:
            h_elevator = None

    return h_elevator

# -------------------- h_parking
def house_parking(response):
    h_parking = ''
    for item in response['sections'][4]['widgets']:
        if re.findall(r'پارکینگ ندارد', str(item)) != []:
            h_parking = False
            break
        elif re.findall(r'پارکینگ', str(item)) != []:
            h_parking = True
            break
        else:
            h_parking = None

    return h_parking


# -------------------- h_storage_room
def house_storage_room(response):
    h_storage_room = ''
    for item in response['sections'][4]['widgets']:
        if re.findall(r'انباری ندارد', str(item)) != []:
            h_storage_room = False
            break
        elif re.findall(r'انباری', str(item)) != []:
            h_storage_room = True
            break
        else:
            h_storage_room = None

    return h_storage_room
# --------------------
#----------------------------------------------- json data

def house_for_sale(response):
    return {
        "sale" : True,
        "rent" : False,
        "title": house_title(response),
        "area": house_area(response),
        "built_year": house_built_year(response),
        "room": house_room(response),
        "sale_price": house_sale_price(response),
        "price_per_m2": house_price_per_square_meter(response),
        "floor": house_floor(response),
        "location": house_location(response),
        "elevator": house_elevator(response),
        "parking": house_parking(response),
        "storage_room": house_storage_room(response),
        "image_link": house_image_link(response),
    }



def house_for_rent(response):
    return {
        "sale": False,
        "rent": True,
        "title": house_title(response),
        "area": house_area(response),
        "built_year": house_built_year(response),
        "room": house_room(response),
        "rent_price": house_rent_price(response),
        "deposit_price": house_deposit_price(response),
        "floor": house_floor(response),
        "location": house_location(response),
        "elevator": house_elevator(response),
        "parking": house_parking(response),
        "storage_room": house_storage_room(response),
        "image_link": house_image_link(response)
    }
# ----------------------------------------------- house for sale/rent
# ------------------------ detect
try:
    h_price = ''
    for item in response['sections'][4]['widgets']:
        if re.findall(r"'title': 'قیمت کل', 'value': '(.*)',", str(item['data'])) != []:
            h_price = re.findall(r"'title': 'قیمت کل', 'value': '(.*)',", str(item['data']))[0]
except Exception:
    h_price = None


if h_price == '':
    data = house_for_rent(response)
else:
    data = house_for_sale(response)

#------------------------

print(data)


# {'sale': True, 'rent': False, 'title': '۹۱ متر خاص، با نور و ویو باغ، واحدی استثنایی', 'area': '۹۱', 'built_year': '۱۳۹۹', 'room': '۲', 'sale_price': '۱۷٬۵۰۰٬۰۰۰٬۰۰۰ تومان', 'price_per_m2': '۱۹۲٬۳۰۷٬۰۰۰ تومان', 'floor': '۳', 'location': 'مسعود, هروی - حسین آباد, منطقه ۴ شهر تهران, شهر تهران, بخش مرکزی شهرستان تهران, شهرستان تهران, استان تهران, 16658-53507, ایران', 'elevator': True, 'parking': True, 'storage_room': True, 'image_link': ['https://s100.divarcdn.com/static/photo/neda/post/oyFtHU6LJAGxS1VGSLSQog/0fe498df-7c1f-482e-8ec0-511bb0e75e94.jpg', 'https://s100.divarcdn.com/static/photo/neda/post/Cmvt8PyWA9Vj1nIGRgYgcQ/6527d817-1592-4985-917b-cb51fa3977e3.jpg', 'https://s100.divarcdn.com/static/photo/neda/post/8y0CdCLX1XaB8gxxd8neXA/54b38570-e682-4c4d-94ef-7eac903e2cdd.jpg', 'https://s100.divarcdn.com/static/photo/neda/post/hPVhSx3C_UK9cp5-KOj_Hw/d2ee6731-b90e-40dc-a539-97825031dc65.jpg']}


# {'sale': False, 'rent': True, 'title': 'رهن آپارتمان ۱۱۵ متری ۲ خوابه در سمندر', 'area': '۱۱۵', 'built_year': '۱۴۰۳', 'room': '۲', 'rent_price': 'رایگان', 'deposit_price': '۱٬۲۰۰٬۰۰۰٬۰۰۰ تومان', 'floor': '۵ از ۵', 'location': 'بذر پاش, خزانه, منطقه ۱۶ شهر تهران, شهر تهران, بخش مرکزی شهرستان تهران, شهرستان تهران, استان تهران, 18319-65535, ایران', 'elevator': True, 'parking': True, 'storage_room': False, 'image_link': ['https://postimage01.divarcdn.com/static/photo/neda/post/sf0FEH7BoZh1jlhMjY0slA/9e06c11e-7c9c-4a29-906f-94f2a6e77ad6.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/QCv40rR-UO5L0UsNswvNSA/8121627e-75f2-442b-941b-0f217d4556db.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/0EoQaVw8xK-41e8imC94XA/d33a7e5f-dbf4-4b1b-89cd-32d258ec5cc0.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/dkNHdUPkRCTIT9MyfTdM4Q/4f6bf3f2-6c01-4230-b6f9-1763c3dd62f6.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/uLhcF755iwe5Bju-xnUWrg/2d3a3998-32a1-41b5-acaa-87bae579ba22.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/5SRBIGNe31r20RIbpFi6NQ/aae181a0-20ec-4da7-be40-57a22c24275f.jpg']}


# {'sale': False, 'rent': True, 'title': '۶۰متر فول امکانات/شاهین شمالی/ویودار رو به شهر', 'area': '۶۰', 'built_year': '۱۳۸۸', 'room': '۱', 'rent_price': '', 'deposit_price': '', 'floor': '۴ از ۵', 'location': 'بلوار کبیری طامه, شاهین - مخبری, جنت آباد, منطقه ۵ شهر تهران, شهر تهران, بخش مرکزی شهرستان تهران, شهرستان تهران, استان تهران, 14758-94433, ایران', 'elevator': True, 'parking': True, 'storage_room': True, 'image_link': ['https://postimage01.divarcdn.com/static/photo/neda/post/V52022a8hPolhZw-cTGecA/d03db0e7-6f58-46f7-abe9-746bd484640f.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/9OxkAuquVEPDyiOdj7hcGg/34a3ede8-7bfc-4db8-8150-f35d55128af3.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/IPMxk9tB_qSwxhJp5izo7g/c51c5a25-73b5-4cd1-8340-8a812d9aef21.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/vcdaGL0wZvCZW7nfBe6_fg/255cf96b-66ce-45ac-a4a3-daaafd3b0cd2.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/Hb_UPGdeC_STwjZ9g7DhAg/3ad4adaf-2766-4a2e-ae06-a1985ad1bf32.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/QwUgqNzon-lBuXqVlZ3krg/80564ab1-607a-48a3-9780-ab3be1eeada1.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/70TT27eBIYAIosF3HinMFA/c0c04d4a-a77a-448b-a20d-fec38480f561.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/WXO8tQ9GwngvOv6Y3uJyBw/8402e4c0-e0ef-4ba6-b494-d1c2f6ad220c.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/VwVADdunMMbfGmaz6JFsZg/27f3acd9-3225-4802-9018-be783969344f.jpg', 'https://postimage01.divarcdn.com/static/photo/neda/post/4Gm0zV369YnM8QCPT1Qelw/c976a5ec-8dcf-46bb-808c-b51ac5cc3183.jpg']}