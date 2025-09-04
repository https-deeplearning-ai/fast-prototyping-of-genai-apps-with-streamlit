# import packages
from dotenv import load_dotenv
import openai
import streamlit as st

@st.cache_data
def get_response(user_prompt, efforts, verbosities):
    response = client.responses.create(
        model="gpt-5",
        input=[{"role": "user", "content": user_prompt}],  # Prompt
        reasoning={"effort": efforts},
        text={"verbosity": verbosities},
    )
    return response

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
    index=1,
)

verbosities = st.radio(
    "Verbosity:",
    options=["low", "medium", "high"],
    captions=["Low verbosity", "Medium verbosity", "High verbosity"],
    index=1,
)

with st.spinner("AI is working..."):
    response = get_response(user_prompt, efforts, verbosities)

# print the response from OpenAI
st.write(response.output[1].content[0].text)
