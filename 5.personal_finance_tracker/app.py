import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize session state if not present
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

# Function to add a transaction
def add_transaction(type, amount, category, description):
    st.session_state['transactions'].append({
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Type': type,
        'Amount': amount,
        'Category': category,
        'Description': description
    })

# Sidebar: Add Transactions
st.sidebar.header("Add a Transaction")
type = st.sidebar.selectbox("Type", ["Income", "Expense"])
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
category = st.sidebar.selectbox("Category", ["Salary", "Freelance", "Food", "Transport", "Shopping", "Other"])
description = st.sidebar.text_input("Description")
if st.sidebar.button("Add Transaction"):
    add_transaction(type, amount, category, description)
    st.sidebar.success("Transaction added!")

# Convert transactions to DataFrame
df = pd.DataFrame(st.session_state['transactions'])

# Main UI: Display Transactions & Insights
st.title("💰 Personal Finance Tracker")
if not df.empty:
    # Show transactions
    st.subheader("Transaction History")
    st.dataframe(df)
    
    # Show income & expense summary
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = total_income - total_expense
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"$ {total_income:.2f}")
    col2.metric("Total Expense", f"$ {total_expense:.2f}")
    col3.metric("Balance", f"$ {balance:.2f}")
    
    # Visualization: Expense Breakdown
    st.subheader("Expense Breakdown")
    expense_df = df[df['Type'] == 'Expense']
    if not expense_df.empty:
        fig = px.pie(expense_df, values='Amount', names='Category', title="Expenses by Category")
        st.plotly_chart(fig)
    else:
        st.info("No expense data available for visualization.")
    
    # Download Data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Transactions", csv, "transactions.csv", "text/csv")
else:
    st.info("No transactions yet. Add your first transaction from the sidebar!")

st.write("🔹 Developed by Esha")
