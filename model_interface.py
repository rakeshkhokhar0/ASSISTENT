"""
interact with model 
"""
import subprocess
import json

def call_model(prompt:str) -> str:
    """"
    call ollama locally and return raw text output str
    """
    try:
        result = subprocess.run(
            ["ollama","run","phi3:3.8b"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            # timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        print("Model error:", e)
        return ""
    
    