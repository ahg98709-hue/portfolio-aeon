
import re
import json
import base64
import hashlib
import random
import string
import uuid
from typing import List, Dict, Optional

# --- Case Conversion ---

def to_uppercase(text: str) -> str: return text.upper()
def to_lowercase(text: str) -> str: return text.lower()
def to_title_case(text: str) -> str: return text.title()
def to_sentence_case(text: str) -> str: return text.capitalize()
def reverse_string(text: str) -> str: return text[::-1]

def snake_to_camel(text: str) -> str:
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(text: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

def to_kebab_case(text: str) -> str:
    return text.replace('_', '-').replace(' ', '-').lower()

# --- Validation (Regex) ---

def is_email(text: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", text))

def is_url(text: str) -> bool:
    return bool(re.match(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text))

def is_phone_number(text: str) -> bool:
    return bool(re.search(r"(\+\d{1,3})?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text))

def is_ipv4(text: str) -> bool:
    return bool(re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", text))

def is_hex_color(text: str) -> bool:
    return bool(re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", text))

def is_date_iso(text: str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", text))

def extract_emails(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

def extract_urls(text: str) -> List[str]:
    return re.findall(r"http[s]?://[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)", text)

# --- Encoding/Decoding ---

def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decode_base64(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except:
        return ""

def to_hex(text: str) -> str:
    return text.encode().hex()

def from_hex(text: str) -> str:
    try:
        return bytes.fromhex(text).decode()
    except:
        return ""

# --- Hashing ---

def hash_md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def hash_sha1(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def hash_sha512(text: str) -> str:
    return hashlib.sha512(text.encode()).hexdigest()

# --- Content Generation ---

def generate_random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_uuid() -> str:
    return str(uuid.uuid4())

def generate_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

def lorem_ipsum() -> str:
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

# --- Statistics ---

def count_words(text: str) -> int:
    return len(text.split())

def count_chars(text: str) -> int:
    return len(text)

def count_vowels(text: str) -> int:
    return sum(1 for char in text.lower() if char in 'aeiou')

def most_common_word(text: str) -> str:
    words = text.split()
    if not words: return ""
    return max(set(words), key=words.count)

# --- Formatting ---

def remove_whitespace(text: str) -> str:
    return "".join(text.split())

def truncate(text: str, length: int) -> str:
    return text[:length] + "..." if len(text) > length else text

def wrap_text(text: str, width: int) -> str:
    import textwrap
    return textwrap.fill(text, width)

def indent_text(text: str, prefix: str = "    ") -> str:
    return "\n".join(prefix + line for line in text.splitlines())
