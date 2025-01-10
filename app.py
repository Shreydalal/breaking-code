from flask import Flask, request, jsonify, render_template
import requests
import os
import traceback
import re

app = Flask(__name__, template_folder='templates')

# Load the application token from environment variables for security
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "7d975e5a-9191-4559-b9bd-3a0b6df6dd8b"
FLOW_ID = "ab2b919f-9235-40fb-b867-f22ed23d44d1"

# Function to run the flow
def run_flow(message: str) -> dict:
    api_url = f"https://api.langflow.astra.datastax.com/lf/7d975e5a-9191-4559-b9bd-3a0b6df6dd8b/api/v1/run/ab2b919f-9235-40fb-b867-f22ed23d44d1?stream=false"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
    "Authorization": f"Bearer {APPLICATION_TOKEN}",  # Replace with your actual API key
    "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {str(e)}")  # Log the exception
        traceback.print_exc()
        return {"error": f"Request failed: {str(e)}"}

def clean_text(text: str) -> str:
    # Remove special characters like #, * (excluding ** for bold)
    text = re.sub(r"(?<!\*)[\\#*](?!\*)", "", text).strip()
    # Replace **text** with <strong>text</strong> for bold formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    return text

# In-memory chat history (to simulate session state in Flask)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        try:
            data = request.get_json()
            # print(f"Received JSON: {data}")  # Log incoming JSON

            if not data or not data.get("message", "").strip():
                return jsonify({"error": "Please enter a message"}), 400

            message = data["message"]
            # print(f"User Message: {message}")  # Log user's message

            # Call run_flow and log its response
            response = run_flow(message)
            # print(f"Langflow API Response: {response}")

            if "error" in response:
                # print(f"Langflow API Error: {response['error']}")
                return jsonify({"error": response["error"]}), 500

            # Extract and clean response
            response_text = (
                response.get("outputs", [{}])[0]
                .get("outputs", [{}])[0]
                .get("results", {})
                .get("message", {})
                .get("text", "No response text found")
            )

            cleaned_response_text = clean_text(response_text)

            if not cleaned_response_text:
                cleaned_response_text = "Sorry, I couldn't understand that."

            # print(f"Cleaned Response Text: {cleaned_response_text}")  # Log cleaned response

            return jsonify({"bot": cleaned_response_text})  # Return bot's response

        except Exception as e:
            # print(f"Unexpected Error: {str(e)}")  # Log unexpected errors
            traceback.print_exc()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    # Render a simple page for GET requests
    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=False,port=8080)
