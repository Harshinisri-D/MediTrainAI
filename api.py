import os
import time
from dotenv import load_dotenv
from groq import Groq
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize the Groq client
client = Groq(api_key=os.getenv("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"))

def get_users():
    # Use RandomUser.me API instead
    url = "https://randomuser.me/api/?results=10"  # Endpoint to get 10 random users
    response = requests.get(url, timeout=20)  # Timeout in seconds

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the response as JSON
    else:
        return {"error": f"Failed to fetch users: {response.status_code}"}


def get_response(text):
    """
    Sends a request to the AI model and returns the response.
    :param text: The user's input text
    :return: The response from the AI model
    """
    try:
        # Define the system message to make the chatbot act like a patient
        system_message = """
        You are a patient speaking with a doctor. You are experiencing health issues such as mild fever, headache, fatigue, or any other common symptoms. 
        Respond to the doctor's questions with honesty, but keep in mind that you are just a patient who may or may not know the full details of their condition.
        Avoid providing medical advice or over-explaining. Just answer based on the common symptoms and your understanding.
        """

        # Send a request to the AI model
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},  # Updated system message for patient role
                {"role": "user", "content": text}  # User's input (doctor's question)
            ],
            model="llama3-8b-8192"  # Adjust this model name if necessary
        )

        # Return the response content from the AI model
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I could not generate a response at the moment."


@app.route("/response", methods=["POST"])
def response():
    try:
        # Get the data from the request
        data = request.get_json()  # This should correctly handle the JSON body

        # Extract the text input from the data
        user_input = data.get("text")

        # Get the AI response
        response_text = get_response(user_input)

        # Return the response in JSON format
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/test_users", methods=["GET"])
def test_users():
    try:
        # Fetch users using the get_users function
        response = get_users()

        # Log the full response to see what we're getting back
        print("API Response:", response)

        # Extract the user data from the response, with a fallback
        users = response.get("results", [])
 # Safely get the 'data' key

        # Return the extracted users in JSON format
        return jsonify(users)

    except Exception as e:
        print(f"Error: {e}")
        # Return the error as a JSON response with status code 500
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
