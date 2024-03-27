from flask import Flask
import re
from flask_cors import CORS

app2 = Flask(__name__)
CORS(app2)

import textwrap
import google.generativeai as genai

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)


GOOGLE_API_KEY='AIzaSyAjgaUV_uyF7MRB_ei-p_DJGhrxsqFgmz0'
genai.configure(api_key=GOOGLE_API_KEY)

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

text=input()

def remove(cleaned_text):
    response2 = model.generate_content(f'''
        {cleaned_text}
        Take this text and convert it into this format, remove json text and it curly bracket if it is present in the text
        Emotion: ''''''{
                Tone: {"About the Tone"} ,
                Explanation: {"Explanination of Text"} ,
                Statistical Insights:{"Statistical Insights"} ,
            }''''''
    ''')
    cleaned_text = re.sub(r'[^a-zA-Z\s:{,}]', '', response2.text)
    return cleaned_text


@app2.route('/analyze-speech', methods=['POST'])
def analyze():
    #print("Started Working")
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

    #p=to_markdown(response.text)

    cleaned_text = re.sub(r'[^a-zA-Z\s:{,}]', '', response.text)
    print(cleaned_text)

    #processed_text = remove_json(cleaned_text)
    #print(processed_text)

    cl=remove(cleaned_text)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(cl)

    return (cl)

if __name__ == '__main__':
    app2.run(port=8888,debug=True)
