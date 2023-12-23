import streamlit as st, pandas as pd, numpy as np, datetime
import plotly.express as px
import seaborn as sns

### importdata ###

df = pd.read_csv('customer_order.csv')
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])


### streamlit dashboard ###

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.title("Total Orders/Invoice from E-Commerce 2017-2018 :bar_chart:")
st.markdown("Analysis dashboard that explains growth of **total order by some state(s)** and compare it to growth of **total order by all states** :chart_with_upwards_trend:")

col1, col2 = st.columns((2))

start_date = pd.to_datetime(df["order_purchase_timestamp"]).min()
end_date = pd.to_datetime(df["order_purchase_timestamp"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", end_date))

df = df[(df["order_purchase_timestamp"] >= date1) & (df["order_purchase_timestamp"] <= date2)].copy()

st.sidebar.header("Filter: ")
state = st.sidebar.multiselect("Pick the State(s)", df["customer_state"].unique(), ["SP", "RJ", "MG", "RS", "PR"])
if not state:
    df2 = df.copy()
else:
    df2 = df[df["customer_state"].isin(state)]

#data for chart

invoice_df = df.set_index("order_purchase_timestamp")["order_id"].resample("M").nunique()

state_df = df2.set_index("order_purchase_timestamp")["order_id"].resample("M").nunique()

#chart

with col1:
    st.subheader("Total Order/Invoice by All States")
    fig = px.line(invoice_df, x = invoice_df.index, y = "order_id",
                  labels={
                      "order_purchase_timestamp": "Month",
                      "order_id": "Total Order/Invoice"
                  },
                  template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Total Order/Invoice by State(s)")
    fig = px.line(state_df, x =state_df.index, y = "order_id",
                  labels={
                      "order_purchase_timestamp": "Month",
                      "order_id": "Total Order/Invoice"
                  })
    st.plotly_chart(fig,use_container_width=True, height = 200)