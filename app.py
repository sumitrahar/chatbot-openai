

from flask import Flask, request, jsonify, render_template
import openai
import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_base = "https://project-komp.openai.azure.com/"
openai.api_key = os.getenv("API_KEY")   # Replace with your actual key 
openai.api_version = "2023-09-01-preview"

@app.route('/')
def home():
    return render_template('index.html')  # Loads frontend

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing prompt"}), 400
        
        user_prompt = data["prompt"].strip()
        if not user_prompt:
            return jsonify({"error": "Prompt cannot be empty"}), 400

        # ✅ Get real-time date and time
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Enhanced system prompt with real-time info
        messages = [
            {"role": "system", "content": f"You are a helpful assistant. The current date and time is {current_datetime}."},
            {"role": "user", "content": user_prompt}
        ]

        # OpenAI API request
        response = openai.ChatCompletion.create(
            engine="gpt-4o",
            messages=messages
        )

        bot_reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": bot_reply})  # Return AI response
    
    except openai.error.OpenAIError as e:
        return jsonify({"error": "OpenAI API error: " + str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Server error: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
