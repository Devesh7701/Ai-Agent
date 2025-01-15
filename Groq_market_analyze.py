import requests
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.getenv("GROQCLOUD_API_KEY"),
)
def ask_questions():
    print("Welcome to the Market Research AI Agent!")
    user_data = {}
    questions = [
        {"question": "What is your age?", "key": "age"},
        {"question": "What is your preferred product category?", "key": "product_category"},
        {"question": "How much do you spend monthly on this category?", "key": "monthly_budget"},
    ]
    for q in questions:
        user_data[q["key"]] = input(q["question"] + " ")
    return user_data

# def get_insights(user_data, model_name="llama-3.3-70b-versatile"):
#     if not isinstance(user_data, dict):
#         return "Invalid input format. Expected a dictionary."

#     url = f"{BASE_URL}/predict"
#     headers = {"Authorization": f"Bearer {GROQCLOUD_API_KEY}"}
#     payload = {
#         "model": model_name,  # Model name passed dynamically
#         "inputs": user_data
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=10)
#         response.raise_for_status()  # Raise exception for HTTP errors

#         return response.json().get("output", "No insights available.")
#     except requests.exceptions.RequestException as e:
#         print(f"API call failed: {e}")
#         return "Error fetching insights."


completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages = [
    {"role": "system", "content": "You are an advanced AI assistant working at a leading market research and analytics company. Your role is to guide users in making well-informed purchasing decisions. You analyze market trends, customer preferences, product reviews, and price-performance ratios to recommend the best products tailored to the user's needs."},
    {"role": "user", "content": str(ask_questions())},
    ]
)


def main():
    print("\nCollecting insights...\n")
    print("Here are the insights based on your responses:")
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main()







# from flask import Flask, request, jsonify, render_template
# import openai

# # Initialize the Flask app
# app = Flask(__name__)

# # Set OpenAI API Key
# openai.api_key = "your-openai-api-key"

# # Predefined questions for market research
# questions = [
#     "What is your age group? (e.g., 18-25, 26-35, etc.)",
#     "What is your primary occupation?",
#     "What type of products or services do you usually purchase online?",
#     "How often do you make online purchases? (e.g., weekly, monthly, rarely)",
#     "What factors influence your buying decisions the most? (e.g., price, quality, reviews)"
# ]

# # Route for the home page
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Route to handle the AI interaction
# @app.route('/ask_questions', methods=['POST'])
# def ask_questions():
#     user_responses = request.json.get("responses", [])
#     if len(user_responses) != len(questions):
#         return jsonify({"error": "Incomplete responses"}), 400
    
#     # Prepare the input for the AI agent
#     prompt = "Based on the following user responses, provide relevant insights:\n"
#     for i, question in enumerate(questions):
#         prompt += f"{i+1}. {question}\nResponse: {user_responses[i]}\n"
    
#     # Generate the response using OpenAI
#     try:
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=prompt,
#             max_tokens=200
#         )
#         return jsonify({"ai_response": response.choices[0].text.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
