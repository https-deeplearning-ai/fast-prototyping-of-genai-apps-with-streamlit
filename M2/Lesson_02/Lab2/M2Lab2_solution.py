import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import matplotlib.pyplot as plt
from snowflake.cortex import complete

# Connect to Snowflake and load data
session = get_active_session()
df = session.table('reviews_with_sentiment').to_pandas()

# App title and sidebar filters
st.title("Product Intelligence Dashboard")
products = df['PRODUCT'].unique()
selected_products = st.sidebar.multiselect("Select Products:", options=products, default=products)

# Check if any products are selected
if not selected_products:
    st.warning("⚠️ Please select at least one product from the sidebar to view the dashboard.")
else:
    filtered_df = df[df['PRODUCT'].isin(selected_products)]
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head())
    
    # Visualization: Average Sentiment by Region
    st.subheader("Average Sentiment by Region")
    region_sentiment = filtered_df.groupby("REGION")['SENTIMENT_SCORE'].mean().sort_values()
    
    if not region_sentiment.empty:
        fig, ax = plt.subplots()
        region_sentiment.plot(kind="barh", ax=ax, title="Average Sentiment by Region")
        ax.set_xlabel("Sentiment Score")
        st.pyplot(fig)
    else:
        st.info("No data available for the selected products.")
    
    # Highlight Delivery Issues
    st.subheader("Delivery Issues by Region and Product")
    grouped_issues = filtered_df.groupby(['REGION', 'PRODUCT'])[['STATUS', 'SENTIMENT_SCORE']].first().reset_index()
    st.dataframe(grouped_issues)

# Chatbot assistant
st.subheader("Ask Questions About Your Data")
user_question = st.text_input("Enter your question here:")
df_string = df.to_string(index=False)

if user_question:
    response = complete(model="claude-3-5-sonnet", prompt=f"Answer this question using the dataset: {user_question} <context>{df_string}</context>", session=session)
    st.write(response)
