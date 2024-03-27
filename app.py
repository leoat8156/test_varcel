from flask import Flask, render_template, request
from flask_cors import CORS
import os
from flask_vercel import FlaskVercel
import textwrap
import google.generativeai as genai
import re

app = Flask(__name__)
CORS(app)

# Initialize FlaskVercel
vercel = FlaskVercel(app)

# Configure Google API key
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Define generation configuration and safety settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Initialize GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to convert text to markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to analyze speech
@app.route('/analyze-speech', methods=['POST'])
def analyze():
    text = request.get_data(as_text=True)
    response = model.generate_content(f'''Analyze the text given below and identify emotional tones with a short explanation, and provide meaningful statistical insights.
    {text}
                                    
    Strictly use this format:-
        ''''''{
            ''''''"Emotion": {
                "Tone": "Text Tone",
                "Explanation": "Explain the Text",
                "Statistical Insights": "Statistical insights to provide from the given text."
            }'''''''
        }''''''


    If there is any text which has no emotion, use tone as Neutral and explain the text.

    If there are no statistical insights, just print "There are no statistical insights to provide from the given text."

    Give it in JSON format
    ''')

    cleaned_text = re.sub(r'[^a-zA-Z\s:{,}]', '', response.text)
    cl = remove(cleaned_text)
    return (cl)

# Function to render index.html on the root URL
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(vercel=True)
