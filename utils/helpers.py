# utils/helpers.py

import hashlib
from datetime import datetime

def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def get_timestamp():
    return datetime.utcnow().isoformat()

def clean_text(text):
    return " ".join(text.split())

def deduplicate_data(data_list, key="url"):
    seen = set()
    unique = []

    for item in data_list:
        identifier = item.get(key)
        if identifier not in seen:
            seen.add(identifier)
            unique.append(item)

    return unique
