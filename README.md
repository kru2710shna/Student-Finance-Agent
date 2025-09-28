# 🎓 Student Finance Agent -- Your Mini CFO

An AI-powered **"mini-CFO dashboard"** designed for students to take
control of their finances.\
Built as part of **Paystand's AI Trail Assignment (3-day challenge)**,
this project demonstrates how automation and AI can streamline everyday
financial tasks at the student level -- mirroring how Paystand empowers
CFOs at the enterprise level.

------------------------------------------------------------------------

## 🚀 Features

-   **📤 Smart Receipt Processing**\
    Upload receipts/bills → OCR (pytesseract) extracts vendor, amount,
    and date → categorized automatically using **LLMs via Groq API**.

-   **📂 Categorization + Insights**\
    Transactions mapped into categories (Housing, Food, Transport,
    Education, Misc).\
    AI generates **human-like insights** (e.g., "Spending on food ↑ 20%
    from last month").

-   **📊 Dashboard Overview**

    -   Cash In vs Cash Out (monthly flow)\
    -   Top Spending Categories (pie chart)\
    -   Cash Runway estimation (how many months savings last)\
    -   Dynamic insights panel

-   **📅 Payment Reminders**\
    Add recurring bills (rent, tuition, subscriptions).\
    View upcoming due dates in the dashboard.

-   **👥 Split Bills with Roommates**\
    Input roommate names → expenses auto-divided equally or
    proportionally.\
    Dashboard shows "You owe / They owe."

-   **💾 Local Storage**\
    Lightweight JSON-based storage (no database setup required).

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   **Frontend/Dashboard**: Streamlit\
-   **OCR**: pytesseract + Pillow\
-   **AI Categorization/Insights**: Groq API (LLaMA models)\
-   **Visualization**: Plotly\
-   **Storage**: JSON (expenses + reminders)

------------------------------------------------------------------------

## 📂 Project Structure

    student-finance-agent/
    │── app.py                 # Main Streamlit app
    │── requirements.txt       # Dependencies
    │── README.md              # Project overview
    │── data/                  # Local JSON storage (expenses + reminders)
    │── assets/                # Sample receipts, icons
    │── modules/               # Core logic modules
    │   ├── ocr_engine.py      # OCR pipeline
    │   ├── categorizer.py     # Groq API categorization + insights
    │   ├── storage.py         # JSON storage handlers
    │   ├── finance_utils.py   # Cash runway, reminders, bill split logic
    │   └── visualizer.py      # Plotly dashboard charts

------------------------------------------------------------------------

## ▶️ How to Use

1.  **Clone the repo**

    ``` bash
    git clone https://github.com/<your-username>/student-finance-agent.git
    cd student-finance-agent
    ```

2.  **Install dependencies**

    ``` bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key**

    -   Create a `.env` file in the root:

        ``` env
        GROQ_API_KEY=your_api_key_here
        ```

4.  **Run the app**

    ``` bash
    streamlit run app.py
    ```

5.  **Explore**

    -   Upload receipts\
    -   Add payment reminders\
    -   Check dashboard metrics & insights\
    -   Split bills with roommates

------------------------------------------------------------------------

## DEMO
🎥 Demo → [Watch Demo Video]([https://drive.google.com/file/d/1A9h-YypFQQ0RZXPYxjwi_QpIGAUV0myn/view?usp=sharing](https://drive.google.com/file/d/19YMI-heNxQAKnC74Y6JB9YoWp75FW-cI/view))

## 🌍 Broad Use Cases

-   **Students**: Track tuition, rent, groceries, and shared bills
    easily.\
-   **Young Professionals**: Manage monthly expenses, subscriptions, and
    savings runway.\
-   **Research Groups**: Monitor grant spending and project expenses
    collaboratively.\
-   **Families/Roommates**: Automate bill splitting, reminders, and
    budgeting.

------------------------------------------------------------------------

## 📅 Daily Use Examples

-   Upload a **grocery receipt** → instantly see it categorized under
    Food, with insights about monthly spending.\
-   Add **rent reminder** → dashboard shows upcoming due date and
    amount.\
-   Enter **roommates' names** → bill-splitting view calculates
    everyone's share.\
-   Check **cash runway** → know how many months your savings last at
    current burn rate.

------------------------------------------------------------------------

## 🎯 Why This Project Stands Out

This project goes beyond a simple tracker:\
- Combines **AI, automation, and finance logic** in a single app.\
- Showcases **real-world use cases** (student-scale CFO dashboard).\
- Mirrors **Paystand's mission** of automating financial workflows ---
but for students.\
- Fully functional prototype, extensible to integrate with bank APIs,
email/calendar reminders, or fraud detection.

------------------------------------------------------------------------

👨‍💻 Built with ❤️ by Krushna Thakkar
