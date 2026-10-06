import os
import json
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Initialize Gemini Client using environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    raw_notes = request.form.get('raw_notes', '')

    if not raw_notes.strip():
        return render_template('index.html', error="Please enter study notes.")

    prompt = f"""
You are an expert AI tutor. Analyze the following study notes and output a valid JSON object with:
1. "summary": An array of key summary points.
2. "quiz": An array of multiple choice questions, each with "question", "options" (list of 4 strings), and "answer" (correct string option).

Notes:
{raw_notes}
"""

    try:
        # Calls the current active Gemini 2.5 Flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Parse output or fallback handling
        output = response.text
        return render_template('result.html', result=output)

    except Exception as e:
        print(f"Error during generation: {e}")
        return render_template('index.html', error="AI generation failed. Please check your API key.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)