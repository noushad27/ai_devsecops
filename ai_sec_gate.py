from dotenv import load_dotenv
load_dotenv()

import os
import sys
import subprocess
import json
import time
from google import genai
from google.genai import types

if not os.getenv("GEMINI_API_KEY"):
    print("ERROR: GEMINI_API_KEY environment variable not set or .env file is malformed.")
    sys.exit(1)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_git_diff():
    try:
        diff = subprocess.check_output(["git", "diff", "HEAD"], text=True)
        return diff
    except subprocess.CalledProcessError:
        print("Failed to execute git diff.")
        sys.exit(1)

def analyze_code_security(diff_text):
    if not diff_text:
        print("No code changes detected. Security scan passed.")
        sys.exit(0)

    prompt = f"""
    You are an expert DevSecOps engineer. Review the following Git diff for security vulnerabilities.
    Focus on hardcoded secrets, SQL injection, and insecure configurations.
    Output ONLY a JSON object with this exact format:
    {{"status": "FAILED", "reason": "description of vulnerability"}} OR {{"status": "PASSED", "reason": "Looks secure"}}
    
    Git Diff:
    {diff_text}
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                wait_time = 3 ** attempt 
                print(f"API busy. Retrying in {wait_time} seconds (Attempt {attempt + 2}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"AI Analysis Failed: {e}")
                sys.exit(1)

if __name__ == "__main__":
    print("Running AI Security Gatekeeper...")
    diff = get_git_diff()
    result = analyze_code_security(diff)
    
    if result.get("status") == "FAILED":
        print(f"SECURITY SCAN FAILED: {result.get('reason')}")
        sys.exit(1) 
    else:
        print("SECURITY SCAN PASSED. Code is clean.")
        sys.exit(0)