import os
import json
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Initialize Gemini Client (Reads GEMINI_API_KEY from environment variables)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    raw_notes = request.form.get('notes', '')

    if not raw_notes.strip():
        return render_template('index.html', error="Please paste some study notes first!")

    prompt = f"""
    You are an expert AI tutor. Analyze the following study notes and output a strict JSON object with two keys:
    1. "summary": An array of 3-5 concise bullet points summarizing core concepts.
    2. "quiz": An array of 3 multiple-choice questions based on the notes. Each question object must have:
       - "question": string
       - "options": array of 4 string options
       - "answer": string (must match one of the options exactly)

    Notes:
    \"\"\"{raw_notes}\"\"\"

    Output ONLY valid JSON. Do not wrap in markdown code blocks like ```json.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_text)

        summary = data.get('summary', [])
        quiz = data.get('quiz', [])

        return render_template('result.html', summary=summary, quiz=quiz)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="AI generation failed. Please check your API key.")

if __name__ == '__main__':
    app.run(debug=True)