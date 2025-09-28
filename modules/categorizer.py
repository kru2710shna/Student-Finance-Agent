import os
from dotenv import load_dotenv
import json 
# Try loading .env if present
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Only import Groq client if key exists
if API_KEY:
    try:
        from groq import Groq
        client = Groq(api_key=API_KEY)
    except ImportError:
        client = None
else:
    client = None


def categorize_and_analyze(text: str):
    """
    Categorize expenses and generate insights.
    - If Groq API key is set, use Claude (via Groq).
    - Otherwise fallback to keyword-based mock categorizer.
    """

    # ✅ Path 1: Use Groq Claude if available
    if client:
        prompt = f"""
        You are an expense categorization assistant.
        Given the OCR text below, identify:
        1. The most likely expense category (Housing, Food, Transport, Education, Subscription, Misc).
        2. A short financial insight (1 sentence) about this expense.

        OCR TEXT:
        {text}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",   # Claude via Groq
                messages=[
                    {"role": "system", "content": "You are a helpful finance assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=150,
            )

            reply = response.choices[0].message.content.strip()

            # Default fallback values
            category = "Misc"
            insight = "No insight generated."

            for line in reply.splitlines():
                if "category" in line.lower():
                    category = line.split(":")[-1].strip()
                elif "insight" in line.lower():
                    insight = line.split(":")[-1].strip()

            return category, insight

        except Exception as e:
            print(f"[WARN] Groq API failed: {e} — Falling back to keyword mode.")

    # ✅ Path 2: Fallback categorization (keywords)
    text_lower = text.lower()
    if "rent" in text_lower or "apartment" in text_lower:
        category = "Housing"
    elif "uber" in text_lower or "bus" in text_lower:
        category = "Transport"
    elif "grocery" in text_lower or "food" in text_lower:
        category = "Food"
    elif "tuition" in text_lower or "university" in text_lower:
        category = "Education"
    elif "spotify" in text_lower or "netflix" in text_lower:
        category = "Subscription"
    else:
        category = "Misc"

    insight = f"This looks like a {category} expense."
    return category, insight



CORRECTIONS_FILE = "data/category_corrections.json"

def save_correction(vendor_text: str, category: str):
    """Save user correction so the agent learns."""
    if not os.path.exists("data"):
        os.makedirs("data")
    corrections = {}
    if os.path.exists(CORRECTIONS_FILE):
        with open(CORRECTIONS_FILE, "r") as f:
            try:
                corrections = json.load(f)
            except:
                corrections = {}
    corrections[vendor_text.lower()] = category
    with open(CORRECTIONS_FILE, "w") as f:
        json.dump(corrections, f, indent=4)

def load_corrections():
    """Load saved corrections."""
    if not os.path.exists(CORRECTIONS_FILE):
        return {}
    try:
        with open(CORRECTIONS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}