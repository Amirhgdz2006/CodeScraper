import pandas as pd
import numpy as np
import re
import json

# Convert Persian digits to English
def convert_persian_digits(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return text.translate(translation_table)

# Remove stray/unmatched parentheses
def remove_unmatched_parentheses(text):
    # Remove lone "(" not followed by closing ")"
    text = re.sub(r'\(([^)]*$)', r'\1', text)
    # Remove lone ")" not preceded by "("
    text = re.sub(r'(^[^(]*)\)', r'\1', text)
    return text

# Main cleaner function
def clean_title(title):
    if pd.isna(title):
        return np.nan

    title = str(title).strip()

    # Convert Persian digits to English
    title = convert_persian_digits(title)

    # Replace ZWNJ and non-breaking space with regular space
    title = re.sub(r'[\u200c\u00a0]', ' ', title)

    # Add space before and after numbers
    title = re.sub(r'(\d+)', r' \1 ', title)

    # Ensure space before and after "/"
    title = re.sub(r'\s*/\s*', ' / ', title)

    # Remove any unwanted characters except parentheses, slashes, dash, comma
    title = re.sub(r'[^\w\s/،()\-]', '', title)

    # Remove unmatched parentheses
    title = remove_unmatched_parentheses(title)

    # Remove multiple spaces
    title = re.sub(r'\s+', ' ', title)

    return title.strip()

# Read titles from file
with open('title.txt', 'r', encoding='utf-8') as f:
    titles = [line.strip() for line in f if line.strip()]

# Clean titles
cleaned_titles = [{'title': clean_title(title)} for title in titles]

# Save to JSON
with open('cleaned_titles.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_titles, f, ensure_ascii=False, indent=2)
