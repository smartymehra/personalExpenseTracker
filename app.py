import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "transactions.csv"

COLUMNS = ["date", "type", "category", "description", "amount"]

def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.title("💰 Personal Expense Tracker")
st.caption("Track income, expenses, budgets and savings. Demo project for FFM CIE 2.")

df = load_data()

with st.sidebar:
    st.header("Add transaction")
    tx_date = st.date_input("Date", value=date.today())
    tx_type = st.selectbox("Transaction type", ["Expense", "Income"])
    categories = ["Food", "Transport", "Education", "Shopping", "Bills", "Health", "Entertainment", "Salary", "Other"]
    category = st.selectbox("Category", categories)
    description = st.text_input("Description", placeholder="e.g., Lunch / monthly salary")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0)
    if st.button("Add transaction", type="primary"):
        if amount <= 0:
            st.error("Enter an amount greater than zero.")
        else:
            new_row = pd.DataFrame([{
                "date": tx_date.isoformat(), "type": tx_type, "category": category,
                "description": description, "amount": float(amount)
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Transaction saved.")
            st.rerun()

st.subheader("Monthly budget")
budget = st.number_input("Set monthly budget (₹)", min_value=0.0, value=10000.0, step=500.0)
if df.empty:
    income = expenses = 0.0
else:
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    income = df.loc[df["type"] == "Income", "amount"].sum()
    expenses = df.loc[df["type"] == "Expense", "amount"].sum()
balance = income - expenses
savings_rate = (balance / income * 100) if income > 0 else 0
remaining_budget = budget - expenses

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total income", f"₹{income:,.2f}")
m2.metric("Total expenses", f"₹{expenses:,.2f}")
m3.metric("Balance / savings", f"₹{balance:,.2f}")
m4.metric("Savings rate", f"{savings_rate:.1f}%")

if expenses > budget:
    st.warning(f"Budget exceeded by ₹{expenses-budget:,.2f}.")
else:
    st.info(f"Budget remaining: ₹{remaining_budget:,.2f}")

st.subheader("Financial analysis")
if not df.empty:
    expense_df = df[df["type"] == "Expense"].copy()
    if not expense_df.empty:
        expense_df["amount"] = pd.to_numeric(expense_df["amount"], errors="coerce").fillna(0)
        category_totals = expense_df.groupby("category", as_index=False)["amount"].sum()
        left, right = st.columns(2)
        with left:
            st.plotly_chart(px.pie(category_totals, names="category", values="amount",
                                  title="Expenses by category"), use_container_width=True)
        with right:
            expense_df["month"] = pd.to_datetime(expense_df["date"], errors="coerce").dt.to_period("M").astype(str)
            monthly = expense_df.groupby("month", as_index=False)["amount"].sum()
            st.plotly_chart(px.bar(monthly, x="month", y="amount", title="Monthly expenses"),
                           use_container_width=True)
    else:
        st.info("Add an expense transaction to display expense charts.")
    st.subheader("Transactions")
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download transactions CSV", csv, "transactions.csv", "text/csv")
    if st.button("Clear all transactions"):
        save_data(pd.DataFrame(columns=COLUMNS))
        st.rerun()
else:
    st.info("No transactions yet. Add income and expenses from the sidebar or load the sample dataset.")

st.caption("Prototype note: this version stores data locally in data/transactions.csv. Cloud deployment or cloud database integration is a separate implementation step.")
