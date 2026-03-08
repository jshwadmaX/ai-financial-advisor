@echo off
echo =======================================================
echo          AI Financial Advisor Setup & Launcher
echo =======================================================
echo.
echo Checking and installing requirements...
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit Application...
echo The app will open in your default browser.
echo.
streamlit run app.py
pause
