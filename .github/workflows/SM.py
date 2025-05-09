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

# Clean title text
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

# Extract area from title if needed
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

# Read input files
with open('title.txt', 'r', encoding='utf-8') as f:
    raw_titles = [line.strip() for line in f if line.strip()]

with open('area.txt', 'r', encoding='utf-8') as f:
    raw_areas = [line.strip() for line in f]

with open('built_year.txt', 'r', encoding='utf-8') as f:
    raw_years = [line.strip() for line in f]

# Validate row count consistency
if not (len(raw_titles) == len(raw_areas) == len(raw_years)):
    raise ValueError("❌ Line count mismatch between files!")

# Build output data
data = []
for raw_title, raw_area, raw_year in zip(raw_titles, raw_areas, raw_years):
    cleaned_title = clean_title(raw_title)

    # Area
    area_str = convert_persian_digits(raw_area.strip())
    try:
        area = int(area_str.replace(',', '')) if area_str else None
    except ValueError:
        area = None
    if area is None:
        area = extract_area_from_title(cleaned_title)

    # Built year
    year_str = convert_persian_digits(raw_year.strip())
    try:
        built_year = int(year_str) if year_str else None
    except ValueError:
        built_year = None

    data.append({
        'title': cleaned_title,
        'area': area,
        'built_year': built_year
    })

# Save result
with open('cleaned_titles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)