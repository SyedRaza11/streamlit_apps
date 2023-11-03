import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="October Data", layout="centered")

# Function to load and preprocess the data
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')
        
        
    for column in df.columns:
      df[column] = df[column].apply(lambda x: str(x))  # Convert to string
      df[column] = df[column].str.replace('[$,]', '', regex=True)
      df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(float)
      df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
      df['Year'] = df['Date'].dt.year
      df['Month'] = df['Date'].dt.month
      return df
# Load the data
file_path = r'oct_sales.csv'
df = load_data(file_path)


# Create a dropdown for selecting agent names
agent_options = ["All Agents"] + list(df['Agent'].unique())
selected_agent = st.selectbox("Select Agent:", agent_options)

# Filter the data based on the selected agent
if selected_agent == "All Agents":
    filtered_data = df
else:
    filtered_data = df[df['Agent'] == selected_agent]

# Calculate KPIs for the filtered data
total_orders = len(filtered_data)
total_revenue = filtered_data['Total Revenue'].sum()
#average_order_value = total_revenue / total_orders
total_sales = filtered_data['Total Selling'].sum()
total_gp = filtered_data['Total GP'].sum()

# Display KPIs at the top
st.markdown("<h1 style='text-align: center;'>Key Performance Indicators</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<h3>Total Orders</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 24px;'>{total_orders}</p>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<h3>Total Revenue</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 24px;'>${total_revenue:.2f}</p>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<h3>Average Order Value</h3>", unsafe_allow_html=True)
    #st.markdown(f"<p style='font-size: 24px;'>${average_order_value:.2f}</p>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<h3>Total Sales</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 24px;'>${total_sales:.2f}</p>", unsafe_allow_html=True)

# Display Total GP
st.markdown(f"<h3>Total GP</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 24px;'>${total_gp:.2f}</p>", unsafe_allow_html=True)

# Create a bar chart for Revenue Comparison of Agents
agent_sales_revenue = filtered_data.groupby('Agent')['Total Revenue'].sum().reset_index()
fig_revenue = px.bar(agent_sales_revenue, x='Agent', y='Total Revenue', title=f"Revenue Comparison of {selected_agent}")

# Create a bar chart for Sales Comparison of Agents
agent_sales_sales = filtered_data.groupby('Agent')['Total Selling'].sum().reset_index()
fig_sales = px.bar(agent_sales_sales, x='Agent', y='Total Selling', title=f"Sales Comparison of {selected_agent}")

# Create a bar chart for Company business Comparison (wider chart)
company_sales = filtered_data.groupby('Company')['Total Selling'].sum().reset_index()
fig_company = px.bar(company_sales, x='Company', y='Total Selling', title="Company Business Comparison")
fig_company.update_layout(width=1000)  # Adjust width to make it wider

# Create a bar chart for Month-Wise Count Comparison
monthly_counts = filtered_data.groupby(['Year', 'Month']).size().reset_index(name='Count')
monthly_counts['Year-Month'] = monthly_counts['Year'].astype(str) + '-' + monthly_counts['Month'].astype(str)
fig_monthly_counts = px.bar(monthly_counts, x='Year-Month', y='Count', title="Month-Wise Count Comparison")

# Create a bar chart for Payment Mode/Status Comparison
payment_mode_sales = filtered_data.groupby('Payment Mode/Status')['Total Selling'].sum().reset_index()
fig_payment_mode = px.bar(payment_mode_sales, x='Payment Mode/Status', y='Total Selling', title="Payment Mode/Status Comparison")

# Create a bar chart for Total GP Comparison of Agents
agent_gp = filtered_data.groupby('Agent')['Total GP'].sum().reset_index()
fig_gp = px.bar(agent_gp, x='Agent', y='Total GP', title=f"Total GP Comparison of {selected_agent}")

# Arrange charts side by side
st.header(f"{selected_agent} Sales and Revenue Comparison")
charts_col1, charts_col2 = st.columns(2)
charts_col1.plotly_chart(fig_revenue, use_container_width=True)
charts_col1.plotly_chart(fig_sales, use_container_width=True)
charts_col2.plotly_chart(fig_company, use_container_width=True)
charts_col2.plotly_chart(fig_monthly_counts, use_container_width=True)

st.header("Payment Mode/Status Comparison")
st.plotly_chart(fig_payment_mode, use_container_width=True)
st.plotly_chart(fig_gp, use_container_width=True)
