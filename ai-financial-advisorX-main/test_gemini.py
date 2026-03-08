import os
from modules.ai_advisor import validate_gemini_connection
import config

print("Testing API Connection...")
success, message = validate_gemini_connection()
print(f"Success: {success}")
print(message)
