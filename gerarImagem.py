import os
from flask import Flask, request, render_template, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json['prompt']
    try:
        result = client.images.generate(
            model="certificado",
            prompt=prompt,
            n=1
        )
        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        return jsonify({'prompt': prompt, 'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
