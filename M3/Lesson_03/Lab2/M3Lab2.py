import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from snowflake.core import Root
## Use this for Streamlit in Snowflake deployment
# from snowflake.snowpark.context import get_active_session

# Establish Snowflake session

## Use this for Streamlit in Snowflake deployment
# session = get_active_session()

## Use this for Streamlit Community Cloud deployment
session = st.connection("snowflake").session()

# Create tabs
tab1, tab2 = st.tabs(["Data & Plots", "RAG App"])

# Tab 1: Data and Plots
with tab1:
    st.title("Customer Sentiment and Delivery Analysis")

    # Data loading functions
    @st.cache_data
    def load_data():
        query_reviews = """
        SELECT
            *
        FROM
            REVIEWS_WITH_SENTIMENT
        """
        return session.sql(query_reviews).to_pandas()

    # Load data
    df = load_data()

    # Average sentiment by product
    st.header("Average Sentiment by Product")
    avg_sentiment_product = df.groupby("PRODUCT")["SENTIMENT_SCORE"].mean().sort_values()

    fig1, ax1 = plt.subplots(figsize=(8,5))
    avg_sentiment_product.plot(kind="barh", color="skyblue", ax=ax1)
    ax1.set_xlabel("Sentiment Score")
    ax1.set_ylabel("Product")
    st.pyplot(fig1)

    # Filter by product selection
    product = st.selectbox("Choose a product", ["All Products"] + list(df["PRODUCT"].unique()))

    if product != "All Products":
        filtered_data = df[df["PRODUCT"] == product]
    else:
        filtered_data = df

    # Display combined dataset
    st.subheader(f"📁 Reviews for {product}")
    st.dataframe(filtered_data)

    # Average sentiment by delivery status
    st.header(f"Average Sentiment by Delivery Status for {product}")
    avg_sentiment_status = filtered_data.groupby("STATUS")["SENTIMENT_SCORE"].mean().sort_values()

    fig2, ax2 = plt.subplots(figsize=(8,5))
    avg_sentiment_status.plot(kind="barh", color="slateblue", ax=ax2)
    ax2.set_xlabel("Sentiment Score")
    ax2.set_ylabel("Delivery Status")
    st.pyplot(fig2)

# Tab 2: RAG App
with tab2:
    st.title("RAG App")

    session = get_active_session()

    # Input box for user prompt
    prompt = st.text_input("Enter your query:", value="Any goggles review?")

    if prompt:
        if st.button("Run Query"):
            root = Root(session)

            # Query service
            svc = (root
                .databases["AVALANCHE_DB"]
                .schemas["AVALANCHE_SCHEMA"]
                .cortex_search_services["AVALANCHE_SEARCH_SERVICE"]
            )

            resp = svc.search(
                query=prompt,
                columns=["CHUNK", "file_name"],
                limit=3
            ).to_json()

            # JSON formatting
            json_conv = json.loads(resp) if isinstance(resp, str) else resp
            search_df = pd.json_normalize(json_conv['results'])

            for _, row in search_df.iterrows():
                st.write(f"**{row['CHUNK']}**")
                st.caption(row['file_name'])
                st.write('---')
