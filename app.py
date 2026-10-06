import os
import json
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize Gemini Client using environment variable
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    raw_notes = request.form.get('raw_notes', '')

    if not raw_notes.strip():
        return render_template('index.html', error="Please enter study notes before generating.")

    if not client:
        return render_template('index.html', error="GEMINI_API_KEY is missing on Render Environment Variables.")

    prompt = f"""
Analyze the following study notes and output a valid JSON object with:
1. "summary": A list of clear bullet point strings summarizing key concepts.
2. "quiz": A list of 3 multiple-choice question objects, each containing:
   - "question": string
   - "options": list of 4 choice strings
   - "answer": string (exact match to correct option)

Notes:
{raw_notes}
"""

    try:
        # Enforce JSON output format
        config = types.GenerateContentConfig(response_mime_type="application/json")
        
        # Primary call using gemini-2.5-flash
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=config
            )
        except Exception as primary_error:
            # Fallback to gemini-1.5-flash if 503 or demand spike occurs
            print(f"Primary model failed ({primary_error}), trying fallback model...")
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config=config
            )

        data = json.loads(response.text)
        return render_template('result.html', summary=data.get('summary', []), quiz=data.get('quiz', []))

    except Exception as e:
        print(f"Error during generation: {e}")
        return render_template('index.html', error=f"AI generation failed: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)