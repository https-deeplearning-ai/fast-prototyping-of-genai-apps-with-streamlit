`Module 2`
# Lab 2: Using GenAI for Sentiment Analysis

In this lab, you'll build a product intelligence dashboard and deploy it on Streamlit in Snowflake (SiS).

## Creating the App
1. Open [Snowsight](https://app.snowflake.com/)
2. In the sidebar, click on the *"Projects"* button then click on *"Streamlit"*
3. After a few moments the default app should spin up where you'll find 3 panels (going from left to right): File/Database panel, Code panel and the app preview panel.

## Install Prerequisite Library
- Click on *Packages* in the middle Code panel
- This should bring up an Anaconda Packages management modal.
- In the "Find Packages" text box, enter the following Python packages:
  - `matplotlib`
  - `pandas`
  - `snowflake-ml-python`
- Click on the *"Save"* button.

## Building the App
- In the Streamlit in Snowflake app, copy contents of [`M2Lab2_solution.py`](M2Lab2_solution.py) and paste it into the middle Code panel
- On the top right corner you should see the blue *"Run"* button, click on it and the app should render in a few moments.
- Congrats! The app should appear in the app preview panel on the right.
