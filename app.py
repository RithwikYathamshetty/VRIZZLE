import streamlit as st
import pandas as pd
from datetime import date
import io

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💸", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .metric-container { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
        div[data-testid="stMetric"] {
            background-color: #f8f9fb;
            border: 1px solid #e0e4ea;
            border-radius: 10px;
            padding: 16px 20px;
        }
        div[data-testid="stMetric"] label { font-size: 0.85rem; color: #6b7280; }
        .stDataFrame { border-radius: 10px; overflow: hidden; }
        section[data-testid="stSidebar"] { background-color: #f4f6fb; }
    </style>
""", unsafe_allow_html=True)

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Other"]
CATEGORY_COLORS = {
    "Food": "#FF6B6B",
    "Travel": "#4ECDC4",
    "Bills": "#45B7D1",
    "Shopping": "#96CEB4",
    "Other": "#FFEAA7",
}

if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["Date", "Amount", "Category", "Description"]
    )


def add_expense(exp_date, amount, category, description):
    new_row = pd.DataFrame([{
        "Date": exp_date,
        "Amount": round(amount, 2),
        "Category": category,
        "Description": description.strip() if description.strip() else "—",
    }])
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_row], ignore_index=True
    )


def get_filtered_df(category_filter):
    df = st.session_state.expenses.copy()
    if category_filter != "All":
        df = df[df["Category"] == category_filter]
    return df


# Sidebar
with st.sidebar:
    st.title("🔍 Filters & Actions")
    st.divider()

    category_filter = st.selectbox(
        "Filter by Category", ["All"] + CATEGORIES, index=0
    )

    st.divider()
    st.subheader("⚠️ Danger Zone")

    if st.button("🗑️ Delete All Expenses", use_container_width=True, type="primary"):
        st.session_state.expenses = pd.DataFrame(
            columns=["Date", "Amount", "Category", "Description"]
        )
        st.success("All expenses deleted.")

    df_all = st.session_state.expenses
    if not df_all.empty:
        csv_buffer = io.StringIO()
        df_all.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_buffer.getvalue(),
            file_name="expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()
    st.caption("Built with Streamlit · Pandas")


# Header 
st.title("💸 Personal Expense Tracker")
st.caption("Track your daily spending, visualize categories, and stay on budget.")
st.divider()

# Add Expense Form
with st.expander("➕ Add New Expense", expanded=True):
    col1, col2, col3, col4 = st.columns([1.2, 1, 1.2, 2])
    with col1:
        exp_date = st.date_input("Date", value=date.today())
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
    with col3:
        category = st.selectbox("Category", CATEGORIES)
    with col4:
        description = st.text_input("Description", placeholder="e.g. Lunch at office")

    submitted = st.button("Add Expense", type="primary", use_container_width=False)
    if submitted:
        if amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            add_expense(exp_date, amount, category, description)
            st.success(f"✅ Expense of ₹{amount:.2f} under **{category}** added!")

st.divider()

# Metrics
filtered_df = get_filtered_df(category_filter)
df_all = st.session_state.expenses

total_all = df_all["Amount"].sum() if not df_all.empty else 0.0
total_filtered = filtered_df["Amount"].sum() if not filtered_df.empty else 0.0
num_entries = len(filtered_df)
avg_expense = (total_filtered / num_entries) if num_entries > 0 else 0.0
top_category = (
    df_all.groupby("Category")["Amount"].sum().idxmax()
    if not df_all.empty else "—"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 Total Spent", f"₹{total_all:,.2f}")
m2.metric(
    "🔎 Filtered Total",
    f"₹{total_filtered:,.2f}",
    delta=f"{category_filter}" if category_filter != "All" else "All categories",
)
m3.metric("🧾 Entries Shown", num_entries)
m4.metric("📊 Avg per Entry", f"₹{avg_expense:,.2f}")

st.divider()

#  Table & Charts
left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("📋 Expense Log")
    if filtered_df.empty:
        st.info("No expenses found. Add one above!")
    else:
        display_df = filtered_df.copy()
        display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.strftime("%d %b %Y")
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
        display_df = display_df.sort_values("Date", ascending=False).reset_index(drop=True)
        display_df.index += 1
        st.dataframe(display_df, use_container_width=True, height=320)

with right:
    st.subheader("🗂️ Category Summary")
    if df_all.empty:
        st.info("No data to summarize yet.")
    else:
        summary = (
            df_all.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .rename(columns={"Amount": "Total Spent"})
            .sort_values("Total Spent", ascending=False)
        )
        summary["% Share"] = (summary["Total Spent"] / summary["Total Spent"].sum() * 100).round(1)
        summary["Total Spent"] = summary["Total Spent"].apply(lambda x: f"₹{x:,.2f}")
        summary["% Share"] = summary["% Share"].apply(lambda x: f"{x}%")
        summary = summary.reset_index(drop=True)
        summary.index += 1
        st.dataframe(summary, use_container_width=True, height=220)

st.divider()

# Pie Chart
st.subheader("📈 Spending Breakdown by Category")
if df_all.empty:
    st.info("Add expenses to see the chart.")
else:
    pie_data = (
        df_all.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Amount": "Total"})
    )
    pie_data = pie_data.set_index("Category")
    st.bar_chart(pie_data, use_container_width=True, height=320, color="#4ECDC4")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("**Category-wise Totals**")
        st.dataframe(
            pie_data.style.format("₹{:.2f}"),
            use_container_width=True,
        )
    with chart_col2:
        if len(df_all) > 1:
            st.markdown("**Spending Over Time**")
            time_data = (
                df_all.groupby("Date")["Amount"]
                .sum()
                .reset_index()
                .rename(columns={"Amount": "Daily Spend"})
                .set_index("Date")
            )
            st.line_chart(time_data, use_container_width=True, height=200)
