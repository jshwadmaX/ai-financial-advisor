# AI Financial Advisor

Welcome to the **AI Financial Advisor**, an intelligent, modular financial planning system that delivers personalized, data-driven financial advice using Google’s Gemini 2.0 Flash generative AI model.

## Features
- **Personal Financial Planning and Analysis**: Complete, data-driven overview of financial health (budget ratio, savings rate, debt-to-income balance).
- **AI-Powered Diagnostics**: Gemini AI interprets the data step-by-step and delivers actionable insights to increase savings, streamline expenses, and optimize investments.
- **Goal-Based Planning**: Setup specific long-term financial goals and let the AI build structured, time-bound investment strategies adapted to your income and risk tolerance.
- **Interactive Chatbot**: Ask the advisor any specific questions about your finances, investments, or goals and receive immediate answers tailored to your context.

## Prerequisites
- Python 3.8+
- Active Google Gemini API Key

## Setup & Running the Application

### 1. Simple Start (Windows only)
Just double-click on the `run.bat` file. It will automatically install the necessary Python dependencies and launch the Streamlit frontend. Your browser will open the app automatically.

### 2. Manual Start
If you prefer running from the command line:

```bash
# Install the required packages
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

## API Key Configuration
The application connects to Gemini using the API Key configured in the `.env` file. A working configuration is provided by default. If you need to change the key in the future, open `.env` in a text editor and replace the value after `GEMINI_API_KEY=`. You can also enter a different key directly inside the Streamlit user interface in the "Financial Profile Setup" sidebar.
