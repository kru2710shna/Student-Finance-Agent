import pytesseract
from PIL import Image
import io

def extract_text(uploaded_file):
    """Extract text from uploaded receipt using pytesseract."""
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image)
    return text.strip()
