# import packages
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI()

# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "..", "..", "..", "data", "customer_reviews.csv")
    return csv_path

@st.cache_data
def get_sentiment(text):
    if not text or pd.isna(text):
        return "Neutral"
    try:
        response = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": "Classify the sentiment of the following review as exactly one word: Positive, Negative, or Neutral."},
                {"role": "user", "content": f"What's the sentiment of this review? {text}"}
            ],
            reasoning={"effort": "minimal"},
            text={"verbosity": "low"},
        )
        return response.output[1].content[0].text.strip()
    except Exception as e:
        st.error(f"API error: {e}")
        return "Neutral"


st.title("🔍 GenAI Sentiment Analysis Dashboard")
st.write("This is your GenAI-powered data processing app.")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Load Dataset"):
        try:
            csv_path = get_dataset_path()
            df = pd.read_csv(csv_path)
            st.session_state["df"] = df.head(10)
            st.success("Dataset loaded successfully!")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path.")

with col2:
    if st.button("🔍 Analyze Sentiment"):
        if "df" in st.session_state:
            try:
                with st.spinner("Analyzing sentiment..."):
                    st.session_state["df"].loc[:, "Sentiment"] = st.session_state["df"]["SUMMARY"].apply(get_sentiment)
                    st.success("Sentiment analysis completed!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
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
    st.dataframe(filtered_df)

    # Visualization using Plotly if sentiment analysis has been performed
    if "Sentiment" in st.session_state["df"].columns:
        st.subheader(f"📊 Sentiment Breakdown for {product}")
        
        # Create Plotly bar chart for sentiment distribution using filtered data
        sentiment_counts = filtered_df["Sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']

        # Define custom order and colors
        sentiment_order = ['Negative', 'Neutral', 'Positive']
        sentiment_colors = {'Negative': 'red', 'Neutral': 'lightgray', 'Positive': 'green'}
        
        # Only include sentiment categories that actually exist in the data
        existing_sentiments = sentiment_counts['Sentiment'].unique()
        filtered_order = [s for s in sentiment_order if s in existing_sentiments]
        filtered_colors = {s: sentiment_colors[s] for s in existing_sentiments if s in sentiment_colors}
        
        # Reorder the data according to our custom order (only for existing sentiments)
        sentiment_counts['Sentiment'] = pd.Categorical(sentiment_counts['Sentiment'], categories=filtered_order, ordered=True)
        sentiment_counts = sentiment_counts.sort_values('Sentiment')
        
        fig = px.bar(
            sentiment_counts,
            x="Sentiment",
            y="Count",
            title=f"Distribution of Sentiment Classifications - {product}",
            labels={"Sentiment": "Sentiment Category", "Count": "Number of Reviews"},
            color="Sentiment",
            color_discrete_map=filtered_colors
        )
        fig.update_layout(
            xaxis_title="Sentiment Category",
            yaxis_title="Number of Reviews",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)


    st.plotly_chart(
        px.scatter(
            filtered_df, x="DATE", y="SENTIMENT_SCORE", title="Sentiment Score Distribution", hover_data=["PRODUCT"]
        )
    )