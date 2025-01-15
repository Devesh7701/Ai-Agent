import os
import google.generativeai as genai

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

# Function to interact with the user and provide guidance
def market_research_agent():
    print("Welcome to the AI Market Research Agent!\n")
    print("Answer a few questions to help us analyze your startup idea.")

    # Collecting user inputs
    product_name = input("1. What is the name of your product? ")
    target_audience = input("2. Who is your target audience? ")
    unique_features = input("3. What are the unique features of your product? ")
    competitors = input("4. Who are your main competitors? ")
    business_model = input("5. What is your business model (e.g., subscription, one-time purchase)? ")

    # Generate a query based on user input
    user_input = (
        f"I have a startup idea called '{product_name}'. The target audience is {target_audience}. "
        f"The unique features of the product are: {unique_features}. The main competitors are: {competitors}. "
        f"The business model is: {business_model}. Please analyze the market, identify challenges, and provide a step-by-step "
        f"workflow for launching this product, along with potential difficulties and strategies to overcome them."
    )

    # Send the query to the Gemini API
    response = chat_session.send_message(user_input)

    # Display the response
    print("\n--- AI Analysis and Guidance ---\n")
    print(response.text)

# Run the agent
if __name__ == "__main__":
    market_research_agent()
