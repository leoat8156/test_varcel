from flask import Flask, request
from flask_cors import CORS
import os
from flask_vercel import FlaskVercel

app2 = Flask(__name__)
CORS(app2)

import textwrap
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

@app2.route('/analyze-speech', methods=['POST'])
def analyze():
    text = request.get_data(as_text=True)
    response = model.generate_content(f'''Analyze the text given below and identify emotional tones with a short explanination, and provide meaningful statistical insights.
    {text}
                                    
    strictly use this format:-
        ''''''{
            ''''''"Emotion": {
                "Tone": "Text Tone",
                "Explanation": "Explain the Text",
                "Statistical Insights": "statistical insights to provide from the given text."
            }'''''''
        }''''''


    If there is any text which has no emotion use tone as Neutral and explain the text

    if there are no statistical insights the just print "There are no statistical insights to provide from the given text."

    Give it in json format
    ''')

    cleaned_text = re.sub(r'[^a-zA-Z\s:{,}]', '', response.text)
    cl = remove(cleaned_text)
    return (cl)

if __name__ == '__main__':
    app2.run(vercel=True)
