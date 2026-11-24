
# InquiryFlow

An AI-powered customer inquiry organizer built with Python, Streamlit, and the Groq API.
Creator note: This is one of the mini projects to help me understand api, llm, and python. I understand the whole workflow.

## Overview

InquiryFlow helps businesses organize customer inquiries by automatically classifying messages, assigning priorities, and suggesting next actions.

Users can upload a CSV file, analyze messages using AI, review the results in a web interface, and download the organized data.

## Features

- Upload customer inquiries from CSV files
- AI-powered inquiry classification
- Priority assignment: High, Medium, Low
- Suggested next actions for support teams
- Interactive Streamlit interface
- Download analyzed results as CSV
- Input validation and basic error handling

## Technologies

- Python
- Streamlit
- pandas
- Groq API
- Open-weight LLM (GPT-OSS-20B)
- JSON

## How It Works

1. Upload a CSV containing customer IDs, names, and messages.
2. Python reads the data using pandas.
3. Customer messages are sent to the Groq API.
4. The AI generates a category, priority, and suggested action.
5. Results are displayed in Streamlit.
6. Users can download the analyzed CSV.

## Setup

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file containing:

    GROQ_API_KEY=your_api_key

Run the application:

    streamlit run web_app.py

## Input Format

Required CSV columns:

- id
- customer
- message

## Note

This is a portfolio demonstration using synthetic customer data. AI-generated classifications and suggested actions should be reviewed before use in real customer operations.
