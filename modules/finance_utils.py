import re
import pandas as pd
from groq import Groq
import os 


def extract_amount(text: str) -> float:
    """Extract numeric amount from OCR text."""
    matches = re.findall(r"\d+\.\d{2}", text)
    if matches:
        return float(matches[0])
    return 0.0


def cash_runway(df: pd.DataFrame, balance: float = 1000) -> float:
    """Estimate how many months balance will last."""
    if "amount" not in df.columns:
        return 0
    monthly_expense = df["amount"].mean() * 4  # approx 4 weeks
    if monthly_expense == 0:
        return float("inf")
    return round(balance / monthly_expense, 1)


def split_bills(df: pd.DataFrame, roommates: list):
    """Split total expenses equally among roommates."""
    total = df["amount"].sum() if not df.empty else 0
    per_person = round(total / (len(roommates) + 1), 2) if roommates else total
    results = [{"Roommate": r, "Share": per_person} for r in roommates]
    results.append({"Roommate": "You", "Share": per_person})
    return pd.DataFrame(results)
