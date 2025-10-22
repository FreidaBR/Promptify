from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/refine', methods=['POST'])
def refine_prompt():
    data = request.get_json()
    user_prompt = data.get('prompt', '')

    system_prompt = f"""You are a prompt optimization expert. Improve this prompt to get better AI responses:
\"{user_prompt}\"

Make it more specific, structured, and effective while keeping the original intent.
Respond with ONLY the improved prompt."""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "llama2", "prompt": system_prompt, "stream": True},
            stream=True
        )

        refined = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                refined += chunk.get("response", "")

        return jsonify({"refined": refined.strip()})
    except Exception as e:
        return jsonify({"error": f"Could not connect to Ollama: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)