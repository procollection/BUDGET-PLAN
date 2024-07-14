import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    'Category': ['Housing', 'Utilities', 'Transportation', 'Food', 'Savings', 'Debt Repayment', 'Insurance', 'Entertainment & Recreation', 'Miscellaneous'],
    'Amount': [2250, 375, 750, 750, 1500, 750, 375, 375, 375]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Percentage'] = (df['Amount'] / df['Amount'].sum()) * 100

# Streamlit app
st.set_page_config(page_title="Budget Dashboard", layout="wide")
st.title('Personal Budget Dashboard')

# User Inputs for Dynamic Updates
st.sidebar.header('Adjust your Budget')
total_income = st.sidebar.number_input('Monthly Income', min_value=1000, value=7500, step=100)

for i, category in enumerate(df['Category']):
    df.at[i, 'Amount'] = st.sidebar.number_input(category, min_value=0, value=int(df.at[i, 'Amount']), step=50)

df['Percentage'] = (df['Amount'] / total_income) * 100

# Dashboard Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income}")
col2.metric("Total Expenses", f"${df['Amount'].sum()}")
col3.metric("Savings Rate", f"{100 - df['Percentage'].sum():.2f}%")

# Enhanced Visualizations
fig, ax = plt.subplots(1, 2, figsize=(15, 5))

# Pie Chart
ax[0].pie(df['Amount'], labels=df['Category'], autopct='%1.1f%%', startangle=90)
ax[0].axis('equal')
ax[0].set_title('Expenses Distribution')

# Bar Chart
df_sorted = df.sort_values(by='Amount', ascending=False)
ax[1].bar(df_sorted['Category'], df_sorted['Amount'], color='skyblue')
ax[1].set_title('Expenses by Category')
ax[1].set_ylabel('Amount ($)')
ax[1].set_xticklabels(df_sorted['Category'], rotation=45, ha='right')

st.pyplot(fig)

# Data Table
st.write("### Detailed Budget Data")
st.dataframe(df)

# Download Button for Budget Data
@st.cache
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df)
st.download_button(
    label="Download Budget Data as CSV",
    data=csv,
    file_name='budget_data.csv',
    mime='text/csv',
)

# Additional Features: Expense Categories Breakdown
st.write("### Expense Categories Breakdown")
breakdown = df.groupby('Category')['Amount'].sum().reset_index()
breakdown['Percentage'] = (breakdown['Amount'] / breakdown['Amount'].sum()) * 100
st.dataframe(breakdown)

st.write("### Savings Advice")
if (100 - df['Percentage'].sum()) < 20:
    st.warning("Your savings rate is below 20%. Consider reducing expenses or increasing your income to improve your savings rate.")
else:
    st.success("Great! Your savings rate is healthy. Keep up the good work!")
