
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from supabase import create_client


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FinTrack | Expense Manager",
    page_icon="💳",
    layout="wide"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background: #F4F7FB;
}

[data-testid="stSidebar"] {
    background: #111827;
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    color: #6B7280;
    font-size: 15px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.metric-label {
    color: #6B7280;
    font-size: 14px;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #111827;
}

.section-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
}

div[data-testid="stForm"] {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
}

.stButton button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------- CLOUD DATABASE ----------------

COLUMNS = [
    "date",
    "type",
    "category",
    "description",
    "amount"
]


# ---------------- SUPABASE CONNECTION ----------------

@st.cache_resource
def get_supabase():

    url = str(
        st.secrets["SUPABASE_URL"]
    ).strip().rstrip("/")

    key = str(
        st.secrets["SUPABASE_KEY"]
    ).strip()

    # Remove REST API path if accidentally added
    if url.endswith("/rest/v1"):
        url = url[:-8]

    # Validate Supabase URL
    if not url.startswith("https://") or ".supabase.co" not in url:
        raise ValueError(
            "Invalid Supabase URL. "
            "Use the Project URL from Supabase settings."
        )

    if not key:
        raise ValueError(
            "Supabase publishable key is missing."
        )

    return create_client(
        url,
        key
    )


# ---------------- LOAD DATA ----------------

def load_data():

    try:

        supabase = get_supabase()

        response = (
            supabase
            .table("transactions")
            .select("date,type,category,description,amount")
            .order("date", desc=True)
            .execute()
        )

        df = pd.DataFrame(
            response.data
        )

        if df.empty:

            return pd.DataFrame(
                columns=COLUMNS
            )

        # Ensure required columns exist
        for col in COLUMNS:

            if col not in df.columns:

                df[col] = ""

        # Convert amount to numeric
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

        # Convert date
        df["date"] = (
            pd.to_datetime(
                df["date"],
                errors="coerce"
            )
            .dt.strftime("%Y-%m-%d")
        )

        return df[COLUMNS]

    except Exception as e:

        st.error(
            f"Could not load transactions from Supabase: {e}"
        )

        return pd.DataFrame(
            columns=COLUMNS
        )


# ---------------- INSERT TRANSACTION ----------------

def insert_transaction(row):

    payload = row.copy()

    payload["date"] = str(
        payload["date"]
    )

    payload["amount"] = float(
        payload["amount"]
    )

    (
        get_supabase()
        .table("transactions")
        .insert(payload)
        .execute()
    )


# ---------------- CLEAR TRANSACTIONS ----------------

def clear_transactions():

    (
        get_supabase()
        .table("transactions")
        .delete()
        .gte("id", 0)
        .execute()
    )


# ---------------- GET DATA ----------------

df = load_data()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("# 💳 FinTrack")

    st.caption("PERSONAL FINANCE")

    st.divider()

    page = st.radio(
        "MENU",
        [
            "Dashboard",
            "Add Transaction",
            "Analytics",
            "Transaction History"
        ]
    )

    st.divider()

    st.markdown("### 💡 Smart Finance")

    st.caption(
        "Manage your income, expenses "
        "and savings in one place."
    )

    st.divider()

    st.caption(
        "FFM CIE 2 | Student Project"
    )


# ---------------- CALCULATIONS ----------------

income = df.loc[
    df["type"] == "Income",
    "amount"
].sum()

expenses = df.loc[
    df["type"] == "Expense",
    "amount"
].sum()

balance = income - expenses

savings_rate = (
    balance / income * 100
    if income > 0 else 0
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Welcome back! Here is your financial overview.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    budget = st.number_input(
        "Monthly Budget (₹)",
        min_value=0.0,
        value=10000.0,
        step=500.0,
        key="budget"
    )

    # Financial Cards

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    💚 Total Income
                </div>
                <div class="metric-value">
                    ₹{income:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    ❤️ Total Expenses
                </div>
                <div class="metric-value">
                    ₹{expenses:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    💰 Available Balance
                </div>
                <div class="metric-value">
                    ₹{balance:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    📈 Savings Rate
                </div>
                <div class="metric-value">
                    {savings_rate:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Budget Overview

    st.write("")

    st.subheader("💳 Budget Overview")

    remaining = budget - expenses

    if expenses > budget:

        st.warning(
            f"You exceeded your budget by "
            f"₹{expenses - budget:,.0f}"
        )

    else:

        st.success(
            f"₹{remaining:,.0f} budget remaining"
        )

    st.progress(
        min(expenses / budget, 1.0)
        if budget > 0 else 0
    )

    # Recent Transactions

    st.write("")

    st.subheader("🧾 Recent Transactions")

    if not df.empty:

        recent = df.sort_values(
            "date",
            ascending=False
        ).head(5)

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No transactions yet. "
            "Add your first transaction."
        )


# ---------------- ADD TRANSACTION ----------------

elif page == "Add Transaction":

    st.markdown(
        '<div class="main-title">Add Transaction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Record your income or spending.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    with st.form("transaction_form"):

        tx_date = st.date_input(
            "Transaction Date",
            value=date.today()
        )

        tx_type = st.selectbox(
            "Transaction Type",
            ["Expense", "Income"]
        )

        categories = [
            "Food",
            "Transport",
            "Education",
            "Shopping",
            "Bills",
            "Health",
            "Entertainment",
            "Salary",
            "Other"
        ]

        category = st.selectbox(
            "Category",
            categories
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch or monthly salary"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=50.0
        )

        submitted = st.form_submit_button(
            "💾 Save Transaction",
            type="primary",
            use_container_width=True
        )

        if submitted:

            if amount <= 0:

                st.error(
                    "Enter an amount greater than zero."
                )

            else:

                new_row = {
                    "date": tx_date.isoformat(),
                    "type": tx_type,
                    "category": category,
                    "description": description,
                    "amount": float(amount)
                }

                try:

                    insert_transaction(
                        new_row
                    )

                except Exception as e:

                    st.error(
                        f"Could not save transaction "
                        f"to Supabase: {e}"
                    )

                    st.stop()

                st.success(
                    "Transaction saved successfully!"
                )

                st.rerun()


# ---------------- ANALYTICS ----------------

elif page == "Analytics":

    st.markdown(
        '<div class="main-title">'
        'Financial Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand your spending patterns.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if df.empty:

        st.info(
            "Add transactions to view analytics."
        )

    else:

        expense_df = df[
            df["type"] == "Expense"
        ].copy()

        if not expense_df.empty:

            # Category Totals

            category_totals = (
                expense_df.groupby(
                    "category",
                    as_index=False
                )["amount"].sum()
            )

            st.subheader("Expense Breakdown")

            left, right = st.columns(2)

            # Pie Chart

            with left:

                fig1 = px.pie(
                    category_totals,
                    names="category",
                    values="amount",
                    hole=0.55,
                    title="Spending by Category"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

            # Monthly Bar Chart

            with right:

                expense_df["month"] = (
                    pd.to_datetime(
                        expense_df["date"],
                        errors="coerce"
                    )
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly = (
                    expense_df.groupby(
                        "month",
                        as_index=False
                    )["amount"].sum()
                )

                fig2 = px.bar(
                    monthly,
                    x="month",
                    y="amount",
                    title="Monthly Spending",
                    labels={
                        "month": "Month",
                        "amount": "Expenses (₹)"
                    }
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

        else:

            st.info(
                "Add expense transactions "
                "to display charts."
            )


# ---------------- TRANSACTION HISTORY ----------------

elif page == "Transaction History":

    st.markdown(
        '<div class="main-title">'
        'Transaction History'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View, search and download your transactions.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if df.empty:

        st.info(
            "No transactions available."
        )

    else:

        search = st.text_input(
            "🔎 Search",
            placeholder="Search category or description"
        )

        filtered_df = df.copy()

        if search:

            filtered_df = filtered_df[
                filtered_df["category"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered_df["description"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        # Display Transactions

        st.dataframe(
            filtered_df.sort_values(
                "date",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        # Download CSV

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "transactions.csv",
            "text/csv"
        )

        st.divider()

        # Clear All Transactions

        if st.button(
            "🗑️ Clear All Transactions"
        ):

            try:

                clear_transactions()

            except Exception as e:

                st.error(
                    f"Could not clear Supabase "
                    f"transactions: {e}"
                )

                st.stop()

            st.success(
                "Transactions cleared."
            )

            st.rerun()


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "FinTrack | Personal Expense Tracker | FFM CIE 2"
)
