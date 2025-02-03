import os
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()
# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Initialize a chat session
chat_session = model.start_chat(history=[])

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    product_name = request.form['product_name']
    target_audience = request.form['target_audience']
    unique_features = request.form['unique_features']
    competitors = request.form['competitors']
    business_model = request.form['business_model']

    # Generate a query based on user input
    user_input = (
        f"I have a startup idea called '{product_name}'. The target audience is {target_audience}. "
        f"The unique features of the product are: {unique_features}. The main competitors are: {competitors}. "
        f"The business model is: {business_model}. Please analyze the market, identify challenges, and provide a step-by-step "
        f"workflow for launching this product, along with potential difficulties and strategies to overcome them."
    )

    # Send the query to the Gemini API
    response = chat_session.send_message(user_input)

    # Render the response back to the user
    return render_template('index.html', analysis=response.text)

if __name__ == "__main__":
    app.run(debug=True)
