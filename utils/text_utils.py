import re

def extract_contact_info(text):
    """Finds email and phone numbers in raw text."""
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    return {
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found"
    }

def clean_text(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = " ".join(text.split())
    return text