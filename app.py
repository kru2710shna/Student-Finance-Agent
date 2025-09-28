import streamlit as st
import pandas as pd
from modules import ocr_engine, categorizer, storage, finance_utils, visualizer
from datetime import date

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="🎓 Student Finance Agent", layout="wide")
st.title("🎓 Student Finance Agent – Your Mini CFO")
st.markdown("Automating your student finances: receipts → insights → dashboard 📊")

# -----------------------------
# Sidebar: Upload & Input
# -----------------------------
with st.sidebar:
    st.header("📤 Upload & Add Data")

    # Receipt upload
    uploaded_file = st.file_uploader("Upload a receipt (png/jpg)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        text = ocr_engine.extract_text(uploaded_file)
        st.success("Receipt uploaded and processed ✅")

        # Categorize using Claude/Groq
        category, insights = categorizer.categorize_and_analyze(text)
        amount = finance_utils.extract_amount(text)

        # Save locally
        storage.save_expense({
            "raw_text": text,
            "category": category,
            "amount": amount,
            "insight": insights,
            "date": str(date.today())
        })

        st.write("🧾 OCR Extracted:", text)
        st.write(f"📂 Category: {category}")
        st.write(f"💡 Insight: {insights}")

    st.markdown("---")

    # Add manual reminder
    st.subheader("📅 Add Reminder")
    reminder_name = st.text_input("Reminder name (e.g., Rent, Tuition)")
    reminder_date = st.date_input("Due Date", date.today())
    reminder_amount = st.number_input("Amount", min_value=0.0)
    if st.button("Save Reminder"):
        storage.save_reminder({
            "name": reminder_name,
            "due": str(reminder_date),
            "amount": reminder_amount
        })
        st.success("Reminder saved ✅")

    st.markdown("---")

    # Roommates (bill split)
    st.subheader("👥 Roommates")
    roommates_input = st.text_input("Enter names (comma separated)", "Alex,Maya")
    roommates = [r.strip() for r in roommates_input.split(",") if r.strip()]

# -----------------------------
# Main Dashboard
# -----------------------------
st.subheader("📊 Dashboard")
expenses = storage.load_expenses()

if expenses:
    df = pd.DataFrame(expenses)

    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Income (set demo)", "$3000")
    col2.metric("💸 Total Expenses", f"${df['amount'].sum():.2f}")
    col3.metric("⏳ Cash Runway", f"{finance_utils.cash_runway(df, balance=3000)} months")

    # Charts
    col4, col5 = st.columns(2)
    with col4:
        st.plotly_chart(visualizer.cash_flow_chart(df), use_container_width=True)
    with col5:
        st.plotly_chart(visualizer.category_chart(df), use_container_width=True)

    # Insights
    st.subheader("💡 Insights")
    for _, row in df.iterrows():
        st.markdown(f"- **{row['category']}** (${row['amount']:.2f}): {row.get('insight', 'No insight')}")

    # Reminders
    st.subheader("📅 Payment Reminders")
    reminders = storage.load_reminders()
    if reminders:
        st.table(reminders)
    else:
        st.info("No reminders added yet.")

    # Split Bills
    st.subheader("👥 Split Bills Summary")
    st.table(finance_utils.split_bills(df, roommates=roommates))

else:
    st.info("No expenses yet. Upload receipts to get started!")
