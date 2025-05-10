import pandas as pd
import numpy as np
import re
import json

# Convert Persian digits to English
def convert_persian_digits(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    return text.translate(str.maketrans(persian_digits, english_digits))

# Remove unmatched parentheses
def remove_unmatched_parentheses(text):
    text = re.sub(r'\(([^)]*$)', r'\1', text)
    text = re.sub(r'(^[^(]*)\)', r'\1', text)
    return text

# Clean title
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

# Extract area from title
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

# Extract room from title if None
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

# Extract floor and max_floor from title if None
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

# Extract floor and max_floor
def extract_floor(text):
    text = convert_persian_digits(text.strip())
    if not text:
        return None, None

    # Handle "همکف از X"
    if 'همکف' in text and 'از' in text:
        match = re.search(r'همکف\s*از\s*(\d+)', text)
        if match:
            try:
                return 0, int(match.group(1))
            except:
                return 0, None

    # Handle X از Y
    if 'از' in text:
        parts = text.split('از')
        try:
            floor = int(parts[0].strip())
            max_floor = int(parts[1].strip())
            return floor, max_floor
        except:
            return None, None

    # Handle همکف only
    if 'همکف' in text:
        return 0, None

    # Handle simple floor number
    try:
        floor = int(text)
        return floor, None
    except:
        return None, None

# Read files
with open('title.txt', 'r', encoding='utf-8') as f:
    raw_titles = [line.strip() for line in f if line.strip()]

with open('area.txt', 'r', encoding='utf-8') as f:
    raw_areas = [line.strip() for line in f]

with open('built_year.txt', 'r', encoding='utf-8') as f:
    raw_years = [line.strip() for line in f]

with open('room.txt', 'r', encoding='utf-8') as f:
    raw_rooms = [line.strip() for line in f]

with open('floor.txt', 'r', encoding='utf-8') as f:
    raw_floors = [line.strip() for line in f]

# Ensure all lists have same length
if not (len(raw_titles) == len(raw_areas) == len(raw_years) == len(raw_rooms) == len(raw_floors)):
    raise ValueError("❌ Line count mismatch between files!")

# Build dataset
data = []
for title_raw, area_raw, year_raw, room_raw, floor_raw in zip(raw_titles, raw_areas, raw_years, raw_rooms, raw_floors):
    title = clean_title(title_raw)

    # Area
    area_str = convert_persian_digits(area_raw.strip())
    try:
        area = int(area_str.replace(',', '')) if area_str else None
    except ValueError:
        area = None
    if area is None:
        area = extract_area_from_title(title)

    # Built year
    year_str = convert_persian_digits(year_raw.strip())
    try:
        built_year = int(year_str) if year_str else None
    except ValueError:
        built_year = None

    # Room
    room = None
    if room_raw.strip():
        room_str = convert_persian_digits(room_raw.strip())
        try:
            room = int(room_str) if room_str else None
        except ValueError:
            room = None
    if room is None:
        room = extract_room_from_title(title)

    # Floor
    floor, max_floor = None, None
    if floor_raw.strip():
        floor, max_floor = extract_floor(floor_raw)
    if floor is None:
        floor, max_floor = extract_floor_from_title(title)

    data.append({
        'title': title,
        'area': area,
        'built_year': built_year,
        'room': room,
        'floor': floor,
        'max_floor': max_floor
    })

# Save to JSON
with open('cleaned_titles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)