import re

def is_strong_password(password):
    # Minimum 6 characters
    return len(password) >= 6

def sanitize_input(text):
    # Basic protection against special characters
    return re.sub(r'[^\w\s]', '', text)
