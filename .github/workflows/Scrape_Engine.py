# --------------------------- imports
import requests
from datetime import timedelta
import time
from time import sleep
from random import uniform
import math
from geopy.geocoders import Nominatim
from multiprocessing import Process
import pandas as pd
import numpy as np
import re
import json
import sqlite3
import csv
import os
# ---------------------------
def divar():
    class Divar_new_detector:

        def __init__(self, min_sleep, max_sleep, sleep_threshold, num_iteration=1, tokens_set=set()):

            self.min_sleep = min_sleep

            self.max_sleep = max_sleep

            self.sleep_threshold = sleep_threshold

            self.tokens_set = tokens_set

            self.token_url = "https://api.divar.ir/v8/posts-v2/web/"

            self.url = "https://api.divar.ir/v8/postlist/w/search"

            self.headers = {
                "accept": "application/json , text/plain , */*",
                "accept-encoding": "gzip , deflate , br , zstd",
                "accept-language": "en-US , en;q=0.9 , fa;q=0.8 , de;q=0.7",
                "content_type": "application/json",
                "origin": "https://divar.ir",
                "referer": "https://divar.ir/",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "x-render-type": "CSR",
                "x-screen-size": "526x812",
                "x-standard-divar-error": "true"
            }
            self.primary_payload = {
                "city_ids": ["1"],
                "source_view": "CATEGORY",
                "disable_recommendation": False,
                "map_state": {
                    "camera_info": {
                        "bbox": {}
                    }
                },
                "search_data": {
                    "form_data": {
                        "data": {
                            "category": {
                                "str": {
                                    "value": "real-estate"
                                }
                            }
                        }
                    },
                    "server_payload": {
                        "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                        "additional_form_data": {
                            "data": {
                                "sort": {
                                    "str": {
                                        "value": "sort_date"
                                    }
                                }
                            }
                        }
                    }
                }
            }
            if self.__class__.__name__ == "Divar_new_detector":
                self.primary_requests(num_iteration)


        def tokens_set_update(self, response):
            try:
                for widget in response["list_widgets"]:
                    if widget["widget_type"] == "POST_ROW":
                        # demo
                        self.tokens_set.add(widget["data"]["token"])
                        # the code will be replaced by scraping , cleanup , insertion into database

            except Exception as e:
                print(f"examination of tokens failed due to {e} !")

        def payload_update(self, response):
            pass

        def primary_requests(self, num_iteration=1):

            for cnt in range(num_iteration):
                if cnt % self.sleep_threshold == 0:
                    sleep(uniform(self.min_sleep, self.max_sleep))

                try:
                    response = requests.post(url=self.url, headers=self.headers, json=self.primary_payload)
                    response = response.json()
                    self.payload_update(response)
                    self.tokens_set_update(response)

                except Exception as e:
                    print(f"request failed due to {e}")

    class Divar_old_detector(Divar_new_detector):

        def __init__(self, min_sleep, max_sleep, sleep_threshold, request_limit):
            super().__init__(min_sleep, max_sleep, sleep_threshold)

            self.secondary_payload = {
                "city_ids": ["1"],
                "source_view": "CATEGORY",
                "disable_recommendation": False,
                "map_state": {
                    "camera_info": {
                        "bbox": {}
                    }
                },
                "search_data": {
                    "form_data": {
                        "data": {
                            "category": {
                                "str": {
                                    "value": "real-estate"
                                }
                            }
                        }
                    },
                    "server_payload": {
                        "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                        "additional_form_data": {
                            "data": {
                                "sort": {
                                    "str": {
                                        "value": "sort_date"
                                    }
                                }
                            }
                        }
                    }
                },
                "tokens": None,
                "has_next_page": True,
                "pelle": {
                    "elastic": {
                        "tokens": None,
                        "documents": None
                    }
                },
                "last_post_date_epoch": None,
                "search_id": None,
                "search_uid": None,
                "posts_metadata": None
            }

            self.primary_requests()
            self.secondary_requests(request_limit)
            self.log()

        def payload_update(self, response):
            try:
                data = response["action_log"]["server_side_info"]["info"]
                self.secondary_payload["tokens"] = data["tokens"]
                self.secondary_payload["has_next_page"] = data["has_next_page"]
                self.secondary_payload["pelle"]["elastic"]["tokens"] = data["pelle"]["elastic"]["tokens"]
                self.secondary_payload["pelle"]["elastic"]["documents"] = data["pelle"]["elastic"]["documents"]
                self.secondary_payload["last_post_date_epoch"] = data["last_post_date_epoch"]
                self.secondary_payload["search_id"] = data["search_id"]
                self.secondary_payload["search_uid"] = data["search_uid"]
                self.secondary_payload["posts_metadata"] = data["posts_metadata"]

            except Exception as e:
                print(f"payload update failed due to {e} !")

        def secondary_requests(self, request_limit):
            cnt = 0
            while self.secondary_payload["has_next_page"] and cnt < request_limit:

                cnt += 1
                if cnt % self.sleep_threshold == 0:
                    sleep(uniform(self.min_sleep, self.max_sleep))

                try:
                    response = requests.post(url=self.url, headers=self.headers, json=self.secondary_payload)
                    response = response.json()
                    self.payload_update(response)
                    self.tokens_set_update(response)

                except:
                    print(f"request failed due to {response.status_code}")

        def log(self):
            print(f"number of collected ids from Divar: {len(self.tokens_set)}")

    # -----------------------------------------------
    divar_old_detector = Divar_old_detector(0.3, 0.5, 200, 1000)
    divar_new_detector = Divar_new_detector(0.3, 0.5, 200, 5, divar_old_detector.tokens_set)
    # ----------------------------------------------- response
    web_site = ['Divar']
    for website in [divar_old_detector]:
        lst_data = []
        lst_token = website.tokens_set
        for token in lst_token:
            try:
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
                                h_price_per_square_meter = \
                                re.findall(r"'title': 'قیمت هر متر', 'value': '(.*)',", str(item['data']))[0]
                    except Exception:
                        h_price_per_square_meter = None

                    return h_price_per_square_meter
                # -------------------- h_rent_price
                def house_rent_price(response):
                    try:
                        h_rent_price = ''
                        for item in response['sections'][4]['widgets']:
                            if re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data'])) != []:
                                h_rent_price = re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data']))[
                                    0]
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
                        latitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point'][
                            'latitude']
                    except Exception:
                        latitude = None

                    try:
                        longitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point'][
                            'longitude']
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
                    try:
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
                    except Exception:
                        h_elevator = None

                    return h_elevator
                # -------------------- h_parking
                def house_parking(response):
                    try:
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
                    except Exception:
                        h_parking = None

                    return h_parking
                # -------------------- h_storage_room
                def house_storage_room(response):
                    try:
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
                    except Exception:
                        h_storage_room = None

                    return h_storage_room
                # --------------------
                # ----------------------------------------------- json data

                def house_for_sale(response):
                    return {
                        "sale": True,
                        "rent": False,
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
                # ------------------------
                lst_data.append(data)
                sleep(0.7)

            except Exception:
                pass
        # ------------------------
        with open(f'real_estate_info_{web_site[[divar_old_detector].index(website)]}.json', 'w',
                  encoding='utf-8') as file:
            json.dump(lst_data, file, ensure_ascii=False, indent=4)



def melkradar():
    # ----------------------- Melkradar
    class Melkradar_new_detector:
        def __init__(self, min_sleep, max_sleep, sleep_threshold, num_iteration=1, tokens_set=set()):

            self.min_sleep = min_sleep

            self.max_sleep = max_sleep

            self.sleep_threshold = sleep_threshold

            self.tokens_set = tokens_set

            self.url = "https://melkradar.com/p/odata/PeoplePanel/estateMarker/getAdvers"

            self.divar_token_url = "https://api.divar.ir/v8/posts-v2/web/"

            self.primary_requests(num_iteration)

            if self.__class__.__name__ == "Melkradar_new_detector":
                pass


        def make_header(self):
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "Origin": "https://melkradar.com",
                "Referer": f"https://melkradar.com/p/result-list;EstateTypeGroup={self.estate_type};AdvertTypeGroup={self.advert_type};City_Id=7eefd59c-9962-4d1a-8fda-935480c82a25",
                "Accept-Language": "fa,en-US;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br"
            }

        def make_payload(self):
            self.payload = {
                "SearchInfo": {
                    "EstateTypeGroup": f"MelkRadar.Core.Model.Enum.EstateType'{self.estate_type}'",
                    "EstateTypeList": [],
                    "AdvertTypeGroup": f"MelkRadar.Core.Model.Enum.AdvertType'{self.advert_type}'",
                    "AdvertTypeList": [],
                    "CityAreaGroups": [],
                    "City_Id": "7eefd59c-9962-4d1a-8fda-935480c82a25",
                    "AreaSizeFrom": None,
                    "AreaSizeTo": None,
                    "SellTotalPriceMin": None,
                    "SellTotalPriceMax": None,
                    "RentMortgagePriceMin": None,
                    "RentMortgagePriceMax": None,
                    "RentMonthlyPriceMin": None,
                    "RentMonthlyPriceMax": None,
                    "Bedrooms": [],
                    "IsFullMortgage": False,
                    "BuildingAgeMax": None,
                    "BuildingAgeMin": None
                },
                "PageNo": 1,
                "PageSize": 20
            }

        def payload_update(self):
            pass

        def tokens_set_update(self, response):
            try:
                for ad in response["value"]:
                    if ad["MelkId"].isdigit() or len(ad["MelkId"]) != 8:
                        pass
                    else:
                        self.tokens_set.add(ad["MelkId"])

            except Exception as e:
                print(f"examination of tokens failed due to {e} !")

        def primary_requests(self, num_iteration=1):
            for (self.estate_type, self.advert_type) in [("Apartment", "Sale"), ("Apartment", "Rent"),
                                                         ("Office", "Sale"),
                                                         ("Office", "Rent")]:
                self.make_header()
                self.make_payload()
                for cnt in range(num_iteration):

                    if cnt % self.sleep_threshold == 0:
                        sleep(uniform(self.min_sleep, self.max_sleep))

                    response = requests.post(url=self.url, headers=self.headers, json=self.payload)
                    try:
                        response = response.json()
                        self.payload_update()
                        self.tokens_set_update(response)

                    except Exception as e:
                        print(f"request failed due to {e}")

    class Melkradar_old_detector(Melkradar_new_detector):

        def __init__(self, min_sleep, max_sleep, sleep_threshold, request_limit):

            super().__init__(min_sleep, max_sleep, sleep_threshold)

            self.secondary_requests(request_limit)

            self.log()

        def payload_update(self):
            try:
                self.payload["PageNo"] += 1

            except Exception as e:
                print(f"payload update failed due to {e}")

        def secondary_requests(self, request_limit):
            for (self.estate_type, self.advert_type) in [("Apartment", "Sale"), ("Apartment", "Rent"),
                                                         ("Office", "Sale"),
                                                         ("Office", "Rent")]:
                cnt = 0
                while cnt < request_limit:
                    cnt += 1
                    if cnt % self.sleep_threshold == 0:
                        sleep(uniform(self.min_sleep, self.max_sleep))
                    try:
                        response = requests.post(url=self.url, headers=self.headers, json=self.payload)
                        if not response:
                            break
                        response = response.json()
                        self.payload_update()
                        self.tokens_set_update(response)

                    except Exception as e:
                        print(f"request failed due to {e} !")

        def log(self):
            print(f"number of collected ids from Melkradar : {len(self.tokens_set)}")

    # -----------------------------------------------
    melkradar_old_detector = Melkradar_old_detector(0.3, 0.5, 100, 20)
    melkradar_new_detector = Melkradar_new_detector(0.3, 0.5, 100, 5, melkradar_old_detector.tokens_set)
    # ----------------------------------------------- response
    web_site = ['Melkradar']
    for website in [melkradar_old_detector]:
        lst_data = []
        lst_token = website.tokens_set
        for token in lst_token:
            try:
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
                                h_price_per_square_meter = \
                                re.findall(r"'title': 'قیمت هر متر', 'value': '(.*)',", str(item['data']))[0]
                    except Exception:
                        h_price_per_square_meter = None

                    return h_price_per_square_meter
                # -------------------- h_rent_price
                def house_rent_price(response):
                    try:
                        h_rent_price = ''
                        for item in response['sections'][4]['widgets']:
                            if re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data'])) != []:
                                h_rent_price = re.findall(r"'title': 'اجارهٔ ماهانه', 'value': '(.*)',", str(item['data']))[
                                    0]
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
                        latitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point'][
                            'latitude']
                    except Exception:
                        latitude = None

                    try:
                        longitude = response['sections'][6]['widgets'][0]['data']['location']['exact_data']['point'][
                            'longitude']
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
                    try:
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
                    except Exception:
                        h_elevator = None

                    return h_elevator
                # -------------------- h_parking
                def house_parking(response):
                    try:
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
                    except Exception:
                        h_parking = None

                    return h_parking
                # -------------------- h_storage_room
                def house_storage_room(response):
                    try:
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
                    except Exception:
                        h_storage_room = None

                    return h_storage_room
                # --------------------
                # ----------------------------------------------- json data
                def house_for_sale(response):
                    return {
                        "sale": True,
                        "rent": False,
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

                # ------------------------
                lst_data.append(data)
                sleep(0.7)

            except Exception:
                pass
        # ------------------------
        with open(f'real_estate_info_{web_site[[melkradar_old_detector].index(website)]}.json', 'w',
                  encoding='utf-8') as file:
            json.dump(lst_data, file, ensure_ascii=False, indent=4)


def cleaning():

    # ----------------------- Convert Persian digits to English
    def convert_persian_digits(text):
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        return text.translate(str.maketrans(persian_digits, english_digits))

    # ----------------------- Remove unmatched parentheses
    def remove_unmatched_parentheses(text):
        text = re.sub(r'\(([^)]*$)', r'\1', text)
        text = re.sub(r'(^[^)]*)\)', r'\1', text)
        return text

    # ----------------------- Clean title
    def clean_title(title):
        if pd.isna(title):
            return np.nan
        title = str(title).strip()
        title = convert_persian_digits(title)
        title = re.sub(r'[\u200c\u00a0]', ' ', title)
        title = re.sub(r'(\d+)', r' \1 ', title)
        title = re.sub(r'\s*/\s*', ' / ', title)
        title = re.sub(r'[^\w\s/،()\-]', '', title)
        title = remove_unmatched_parentheses(title)
        title = re.sub(r'\s+', ' ', title)
        return title.strip()

    # ----------------------- Extract area from title
    def extract_area_from_title(title):
        if pd.isna(title):
            return None
        title = convert_persian_digits(title)
        match = re.search(r'(\d{1,5}(?:,\d{3})?)\s*متر(?:ی)?\b', title)
        if match:
            try:
                return int(match.group(1).replace(',', ''))
            except ValueError:
                return None
        return None

    # ----------------------- Extract room from title if None
    def extract_room_from_title(title):
        if pd.isna(title):
            return None
        title = convert_persian_digits(title)
        match = re.search(r'(\d+)\s*(خواب|خوابه)', title)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    # ----------------------- Extract floor and max_floor from title if None
    def extract_floor_from_title(title):
        if pd.isna(title):
            return None, None
        title = convert_persian_digits(title)
        match = re.search(r'طبقه\s*(\d+)', title)
        if match:
            try:
                return int(match.group(1)), None
            except ValueError:
                return None, None
        return None, None

    # ----------------------- Extract floor and max_floor
    def extract_floor(text):
        text = convert_persian_digits(text.strip())
        if not text:
            return None, None

        if 'همکف' in text and 'از' in text:
            match = re.search(r'همکف\s*از\s*(\d+)', text)
            if match:
                try:
                    return 0, int(match.group(1))
                except:
                    return 0, None

        if 'از' in text:
            parts = text.split('از')
            try:
                floor = int(parts[0].strip()) if 'همکف' not in parts[0] else 0
                max_floor = int(parts[1].strip())
                return floor, max_floor
            except:
                return None, None

        if 'همکف' in text:
            return 0, None

        try:
            floor = int(text)
            return floor, None
        except:
            return None, None

    def parse_price_field(value):
        if value is None or str(value).strip() == '':
            return None
        value_str = str(value).strip()
        value_str = convert_persian_digits(value_str)
        if 'رایگان' in value_str:
            return 0
        value_str = re.sub(r'تومان', '', value_str).strip()
        value_str = value_str.replace(',', '').replace('٬', '')
        try:
            return int(value_str)
        except ValueError:
            return None

    # ----------------------- Clean location
    def clean_location(loc):
        if not loc or str(loc).lower() == 'none':
            return None
        loc = convert_persian_digits(loc)
        loc = re.sub(r'\d{5}-\d{5},?', '', loc)  # Remove postal codes and any trailing commas
        loc = re.sub(r'\s+', ' ', loc).strip(' ,')
        return loc

    # Replace NaN with None recursively
    def replace_nan_values(data):
        if isinstance(data, dict):
            return {k: replace_nan_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [replace_nan_values(item) for item in data]
        elif isinstance(data, float) and math.isnan(data):
            return None
        else:
            return data

    # ----------------------- Read data from JSON
    for file_name in ['Divar', 'Melkradar']:
        try:

            with open(f'real_estate_info_{file_name}.json', 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            data = []
            for idx, item in enumerate(raw_data):
                title = clean_title(item.get('title', ''))

                # ----------------------- Area
                area_raw = item.get('area', '')
                area_str = convert_persian_digits(str(area_raw).strip())
                try:
                    area = int(area_str.replace(',', '')) if area_str else None
                except ValueError:
                    area = None
                if area is None:
                    area = extract_area_from_title(title)

                # ----------------------- Built year
                year_raw = item.get('built_year', '')
                year_str = convert_persian_digits(str(year_raw).strip())
                try:
                    built_year = int(year_str) if year_str else None
                except ValueError:
                    built_year = None

                # ----------------------- Room
                room_raw = item.get('room', '')
                room = None
                if str(room_raw).strip():
                    room_str = convert_persian_digits(str(room_raw).strip())
                    try:
                        room = int(room_str)
                    except ValueError:
                        room = None
                if room is None:
                    room = extract_room_from_title(title)

                # ----------------------- Floor
                floor_raw = item.get('floor', '')
                floor, max_floor = None, None
                if str(floor_raw).strip():
                    floor, max_floor = extract_floor(str(floor_raw))
                if floor is None:
                    floor, max_floor = extract_floor_from_title(title)

                # ----------------------- Prices
                sale = item.get('sale', False)
                rent = item.get('rent', False)
                sale_price = parse_price_field(item.get('sale_price')) if sale else None
                price_per_m2 = parse_price_field(item.get('price_per_m2')) if sale else None
                rent_price = parse_price_field(item.get('rent_price')) if rent else None
                deposit_price = parse_price_field(item.get('deposit_price')) if rent else None

                # ----------------------- Location
                location = clean_location(item.get('location'))

                # ----------------------- Entry
                entry = {
                    'title': title,
                    'area': area,
                    'built_year': built_year,
                    'room': room,
                    'floor': floor,
                    'max_floor': max_floor,
                    'sale': sale,
                    'rent': rent,
                    'elevator': item.get('elevator', False),
                    'parking': item.get('parking', False),
                    'storage_room': item.get('storage_room', False),
                    'image_link': item.get('image_link', None),
                    'location': location
                }

                if sale:
                    entry['sale_price'] = sale_price
                    entry['price_per_m2'] = price_per_m2

                if rent:
                    entry['rent_price'] = rent_price
                    entry['deposit_price'] = deposit_price

                data.append(entry)

            # ----------------------- Replace NaNs with None before saving
            cleaned_data = replace_nan_values(data)

            # Save
            with open(f'cleaned_info_{file_name}.json', 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        except Exception:
            pass

def database():

    # ----------------------- sql_lite database file
    db_path = 'codescraper.db'

    # ----------------------- json files
    data_sources = {
        'cleaned_info_Divar.json': 'divar',
        'cleaned_info_Melkradar.json': 'melkradar'
    }

    # ----------------------- Connect to sql_lite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ----------------------- creating table
    def create_table_if_not_exists(table_name):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                area INTEGER,
                built_year INTEGER,
                room INTEGER,
                floor INTEGER,
                max_floor INTEGER,
                sale BOOLEAN,
                rent BOOLEAN,
                elevator BOOLEAN,
                parking BOOLEAN,
                storage_room BOOLEAN,
                image_link TEXT,
                location TEXT,
                rent_price INTEGER,
                deposit_price INTEGER,
                sale_price INTEGER,
                price_per_m2 INTEGER
            )
        """)
        conn.commit()

    # ----------------------- adding data
    def insert_data(table_name, data):
        inserted_rows = 0
        query = f"""
            INSERT INTO {table_name} (
                title, area, built_year, room, floor, max_floor, sale, rent,
                elevator, parking, storage_room, image_link, location,
                rent_price, deposit_price, sale_price, price_per_m2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for item in data:
            image_link = ','.join(item['image_link']) if item.get('image_link') and isinstance(item['image_link'],
                                                                                               list) else None

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
            except Exception as e:
                print(f"Error inserting '{item.get('title', 'Unknown')}': {e}")

        conn.commit()

    # ----------------------- export csv
    def export_to_csv(table_name):
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        with open(f'{table_name}.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)


    for json_file, table_name in data_sources.items():
        if not os.path.exists(json_file):
            print(f"File '{json_file}' not found.")
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        create_table_if_not_exists(table_name)
        insert_data(table_name, data)
        export_to_csv(table_name)

    # ----------------------- Close database
    cursor.close()
    conn.close()
    print("SQLite connection closed.")

def similarity():
    similarity_count = 0
    similarity = []

    with open('cleaned_info_Divar.json', 'r', encoding='utf-8') as file:
        divar_data = json.load(file)

    with open('cleaned_info_Melkradar.json', 'r', encoding='utf-8') as file:
        melkradar_data = json.load(file)

    for item_d in divar_data:
        for item_m in melkradar_data:
            sale = 0
            rent = 0
            area = 0
            built_year = 0
            room = 0
            floor = 0
            minus = 0

            if item_m['sale'] == item_d['sale']:
                sale += 1
            if item_m['rent'] == item_d['rent']:
                rent += 1

            if item_m['area'] == item_d['area']:
                if item_m['area'] != None:
                    area += 1

            if item_m['built_year'] == item_d['built_year']:
                if item_m['built_year'] != None:
                    built_year += 1

            if item_m['room'] == item_d['room']:
                if item_m['room'] != None:
                    room += 1
                else:
                    minus += 1

            if item_m['floor'] == item_d['floor']:
                if item_m['floor'] != None:
                    floor += 1
                else:
                    minus += 1
            if (sale + rent + area + built_year + room + floor) >= 6-minus:
                similarity_count += 1
                similarity.append(item_m['title'])

    print(f'Number of the similar houses: {similarity_count}')
    if similarity_count > 0 :
        for item in similarity:
            print(item)


if __name__ == "__main__":
    while True:
        start_time = time.time()

        p1 = Process(target=divar)
        p2 = Process(target=melkradar)

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        cleaning()

        database()

        similarity()

        print('\n')
        print("all processes are done.")

        end_time = time.time()
        print(str(timedelta(seconds=int(end_time - start_time))))

        # every 3 min this code will run automatically
        time.sleep(180)


