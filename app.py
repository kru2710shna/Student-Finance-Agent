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

        # Categorize using Groq API (or fallback)
        category, insights = categorizer.categorize_and_analyze(text)
        amount = finance_utils.extract_amount(text)

        # ✅ Smart Categorization Learning (user correction)
        corrected_category = st.selectbox(
            "Is this category correct?",
            ["Housing", "Food", "Transport", "Education", "Subscription", "Misc"],
            index=["Housing", "Food", "Transport", "Education", "Subscription", "Misc"].index(category)
            if category in ["Housing", "Food", "Transport", "Education", "Subscription", "Misc"] else 5
        )
        if corrected_category != category:
            st.info(f"Updated category from {category} → {corrected_category}")
            categorizer.save_correction(text, corrected_category)
            category = corrected_category  # overwrite before saving

        # Save locally
        storage.save_expense({
            "raw_text": text,
            "category": category,
            "amount": amount,
            "insight": insights,
            "date": str(date.today())
        })

        st.write("🧾 OCR Extracted:", text)
        st.write(f"📂 Final Category: {category}")
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

    # -----------------------------
    # Agentic Features
    # -----------------------------
    # Scenario Chat
    st.subheader("🤖 Scenario Chat – Ask What-If Questions")
    user_query = st.text_input("Example: 'What if I spend $200 more on food next month?'")
    if user_query:
        try:
            scenario_answer = categorizer.run_scenario_chat(user_query, expenses)
            st.success(f"💬 Agent: {scenario_answer}")
        except Exception as e:
            st.error(f"Scenario planning failed: {e}")

    # Smart Categorization Log
    st.subheader("📘 Learning Log (Corrections Applied)")
    corrections = categorizer.load_corrections()
    if corrections:
        corr_df = pd.DataFrame(list(corrections.items()), columns=["Vendor/Keyword", "Corrected Category"])
        st.table(corr_df)
    else:
        st.info("No corrections learned yet.")

else:
    st.info("No expenses yet. Upload receipts to get started!")
