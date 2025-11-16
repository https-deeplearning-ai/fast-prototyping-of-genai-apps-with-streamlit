`Module 3`
# Lab 1: Deploying Your Prototype

## Overview
- In the course, under the section *"Deploying your Prototype"* section, watch the *"Lab 1: Deploying Your Prototype"* video for instructions on running the lab.
- Use these files for app deployment: [`streamlit_app.py`](streamlit_app.py) and [`requirements.txt`](requirements.txt)
- You have 2 methods of app deployment:
  1. Deploying to Streamlit in Snowflake
  2. Deploy to Streamlit Community Cloud

## Deploying to Streamlit in Snowflake
- In the course watch the *"Deploying Your Prototype Internally on Snowflake"* video.
- Follow step-by-step instructions in [Module 2 Lab 2](https://github.com/https-deeplearning-ai/fast-prototyping-of-genai-apps-with-streamlit/tree/main/M2/Lesson_02/Lab2).
- To deploy, go to Snowsight's [Streamlit in Snowflake](https://app.snowflake.com/_deeplink/#/streamlit-apps).

## Deploy to Streamlit Community Cloud
- In the course, watch the *"Deploying to Streamlit Community Cloud"* video and also "Connecting Streamlit Community Cloud to Snowflake" video.
- To deploy, go to [Streamlit Community Cloud](https://streamlit.io/cloud).
- Once logged in, click on *"Create app"* in the top-right hand corner.
- Click on *"Deploy a public app from GitHub"*.
- Select the repo, branch, main file path, adjust the app URL (if needed).
- Once the app is deployed, make sure to add the proper secrets information to connect to Snowflake as mentioned in the first bullet point. This is provided in this repo at [`.streamlit/secrets.toml`](.streamlit/secrets.toml). On a deployed app, click on the "Manage app" button on the bottom-right hand corner.
  - Instead of using the actual password for the `password` parameter, it could be replaced by using a [programmatic access tokens (PAT)](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens) for authentication.
    - To ensure that the app can access Snowflake the [network policy](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens#network-policy-requirements) should be in place.
    - To do this, in Snowsight, click on your image profile in the lower left corner, then click on *"Settings"*.
    - A new page appears, click on the *"Authentication"* tab, then in the *"Programmatic access tokens"* section, click on "Generate new token".
    - Once the token has been generated, find the three dots, click on it, then click on *"Bypass requirements for network policy"*.
    - Specify the duration and click on the blue "Grant access" button.
