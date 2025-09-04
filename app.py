# import packages
from dotenv import load_dotenv
import openai
import streamlit as st


# load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI()

st.title("Hello, GenAI!")
st.write("This is your first Streamlit app.")

user_prompt = st.text_input(
    "Enter your prompt:", "Explain generative AI in one sentence."
)

efforts = st.radio(
    "Effort:",
    options=["minimal", "low", "medium", "high"],
    captions=["Shorter response", "Short response", "Medium response", "Long response"],
    index=2,
)

verbosities = st.radio(
    "Verbosity:",
    options=["low", "medium", "high"],
    captions=["Low verbosity", "Medium verbosity", "High verbosity"],
    index=2,
)

response = client.responses.create(
    model="gpt-5",
    input=[{"role": "user", "content": user_prompt}],  # Prompt
    reasoning={"effort": efforts},
    text={"verbosity": verbosities},
)

# print the response from OpenAI
st.write(response.output[1].content[0].text)
