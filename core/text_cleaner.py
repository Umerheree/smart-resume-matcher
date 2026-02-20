import re

def extract_contact_info(text):
    """
    Finds email and phone numbers in the raw resume text.
    """
    # Regex for standard email formats
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    
    # Regex for various phone formats (e.g., +92 300 1234567, 0300-1234567, etc.)
    phone = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    return {
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found"
    }

def clean_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters (keep only a-z and spaces)
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = " ".join(text.split())
    return text