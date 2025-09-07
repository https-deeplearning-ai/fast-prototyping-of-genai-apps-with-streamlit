# import packages
import streamlit as st
import pandas as pd
import re
import os
import string
import plotly.express as px


# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "..", "..", "data", "customer_reviews.csv")
    return csv_path


def clean_text(text):
    """
    Clean text by removing punctuation, converting to lowercase, and stripping whitespace.

    Args:
        text (str): Input text to clean

    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Strip whitespace
    text = text.strip()

    return text


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Ingest Dataset"):
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Dataset loaded successfully!")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path.")

with col2:
    if st.button("🧹 Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"][
                "SUMMARY"
            ].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")

if "df" in st.session_state:

    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox(
        "Choose a product",
        ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()),
    )

    st.subheader(f"🗂️ Dataset preview")
    if product != "All Products":
        filtered_df = st.session_state["df"][
            st.session_state["df"]["PRODUCT"] == product
        ]
    else:
        filtered_df = st.session_state["df"]

    st.dataframe(filtered_df.head())

    st.plotly_chart(
        px.scatter(
            filtered_df, x="DATE", y="SENTIMENT_SCORE", title="Sentiment Score Distribution", hover_data=["PRODUCT"]
        )
    )
