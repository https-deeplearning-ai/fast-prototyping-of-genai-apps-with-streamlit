import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import matplotlib.pyplot as plt
from snowflake.cortex import complete

# Initialize the Streamlit app
st.title("Avalanche Streamlit App")

# Get data from Snowflake
session = st.connection("snowflake").session()
query = """
SELECT
    *
FROM
    REVIEWS_WITH_SENTIMENT
"""
df_reviews = session.sql(query).to_pandas()
df_string = df_reviews.to_string(index=False)

# Convert date columns to datetime
df_reviews['REVIEW_DATE'] = pd.to_datetime(df_reviews['REVIEW_DATE'])
df_reviews['SHIPPING_DATE'] = pd.to_datetime(df_reviews['SHIPPING_DATE'])

# Visualization: Average Sentiment by Product
st.subheader("Average Sentiment by Product")
product_sentiment = df_reviews.groupby("PRODUCT")["SENTIMENT_SCORE"].mean().sort_values()

fig, ax = plt.subplots()
product_sentiment.plot(kind="barh", ax=ax, title="Average Sentiment by Product")
ax.set_xlabel("Sentiment Score")
plt.tight_layout()
st.pyplot(fig)

# Product filter on the main page
st.subheader("Filter by Product")

product = st.selectbox("Choose a product", ["All Products"] + list(df_reviews["PRODUCT"].unique()))

if product != "All Products":
    filtered_data = df_reviews[df_reviews["PRODUCT"] == product]
else:
    filtered_data = df_reviews


# Display the filtered data as a table
st.subheader(f"📁 Reviews for {product}")
st.dataframe(filtered_data)

# Visualization: Sentiment Distribution for Selected Products
st.subheader(f"Sentiment Distribution for {product}")
fig, ax = plt.subplots()
filtered_data['SENTIMENT_SCORE'].hist(ax=ax, bins=20)
ax.set_title("Distribution of Sentiment Scores")
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Chatbot for Q&A
st.subheader("Ask Questions About Your Data")
user_question = st.text_input("Enter your question here:")

if user_question:

    response = complete(model="claude-3-5-sonnet", prompt=f"Answer this question using the dataset: {user_question} <context>{df_string}</context>", session=session)
    st.write(response)
