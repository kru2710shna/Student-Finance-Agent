import json
import os

DATA_FILE = "data/expenses.json"
REMINDER_FILE = "data/reminders.json"


def save_expense(expense: dict):
    """Append a new expense to the local JSON file."""
    if not os.path.exists("data"):
        os.makedirs("data")

    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    data.append(expense)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_expenses():
    """Load all saved expenses."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_reminder(reminder: dict):
    """Append a reminder (e.g., rent due) to reminders.json."""
    if not os.path.exists("data"):
        os.makedirs("data")

    data = []
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            data = json.load(f)

    data.append(reminder)

    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_reminders():
    """Load all reminders with safe empty handling."""
    if not os.path.exists(REMINDER_FILE):
        return []
    try:
        with open(REMINDER_FILE, "r") as f:
            content = f.read().strip()
            if not content:  # empty file
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

