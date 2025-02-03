import requests
import os
from dotenv import load_dotenv
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from groq import Groq
# from actions import get_page_summary
from actions import search_google_latest
from prompts import react_system_prompt
# from json_helpers import extract_json

# Load environment variables
load_dotenv()

import json

def extend_search_new(text_response, span):
    """
    Extends the JSON search to ensure a full JSON object is captured.
    This function assumes that JSON might not be fully captured in initial regex spans.
    """
    start, end = span
    open_braces = 0
    new_start = text_response.find('{', start)
    i = new_start
    
    while i < len(text_response):
        if text_response[i] == '{':
            open_braces += 1
        elif text_response[i] == '}':
            open_braces -= 1

        if open_braces == 0:  # Found the closing brace for the JSON
            return text_response[new_start:i+1]
        i += 1

    return text_response[new_start:end]  # Fallback in case of incomplete JSON

def extract_json(text_response):
    """
    Extract JSON objects from the given text_response.
    """
    pattern = r'\{.*?\}'
    matches = re.finditer(pattern, text_response, re.DOTALL)
    json_objects = []

    for match in matches:
        json_str = extend_search_new(text_response, match.span())
        try:
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            continue  # Skip invalid JSON strings

    return json_objects if json_objects else None


# Set the API key
client = Groq(
    api_key=os.getenv("GROQCLOUD_API_KEY"),
)
def generate_text_with_conversation(messages, model="llama-3.3-70b-versatile"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    return response.choices[0].message.content

available_actions = {
    # "get_seo_page_report": get_seo_page_report,
    # "get_response_time": get_response_time,
    # "get_page_summary": get_page_summary,
    "search_google_latest" : search_google_latest

}

def summarize_website(website_url):
    user_prompt = f"Summarize the content of the website {website_url}."

    messages = [
        {"role": "system", "content": react_system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = generate_text_with_conversation(messages, model="llama-3.3-70b-versatile")

    print("Website Summary:", response)
    return response

def analyze():
    name = input("In which field you want me to analyze: ")
    user_prompt = (
         f"Conduct a search for the latest advancements in {name} and give the full analysis report in bullet points."
    )

    messages = [
        {"role": "system", "content": react_system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    turn_count = 1
    max_turns = 5

    while turn_count <= max_turns:
        print(f"Loop: {turn_count}")
        print("----------------------")
        turn_count += 1

        response = generate_text_with_conversation(messages)
        print("Response:", response)

        json_function = extract_json_from_text(response)

        if json_function:
            function_name = json_function[0].get('function_name')
            function_parms = json_function[0].get('function_parms')
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")

            print(f" -- Running {function_name} with parameters {function_parms}")
            action_function = available_actions[function_name]

            # Call the function with unpacked parameters
            result = action_function(**function_parms)
            
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
        else:
            print("No valid JSON function found. Exiting loop.")
            break


# def analyze_website():
#     user_prompt = f"Conduct a search for the latest advancements in marketing and give the full analysis report in bullet points."

#     messages = [
#         {"role": "system", "content": react_system_prompt},
#         {"role": "user", "content": user_prompt},
#     ]

#     turn_count = 1
#     max_turns = 5

#     while turn_count <= max_turns:
#         print(f"Loop: {turn_count}")
#         print("----------------------")
#         turn_count += 1

#         response = generate_text_with_conversation(messages, model="llama-3.3-70b-versatile")

#         print("Response:", response)

#         json_function = extract_json_from_text(response)

#         if json_function:
#             function_name = json_function[0]['function_name']
#             function_parms = json_function[0]['function_parms']

#             if function_name not in available_actions:
#                 raise Exception(f"Unknown action: {function_name}: {function_parms}")

#             print(f" -- Running {function_name} with parameters {function_parms}")

#             action_function = available_actions[function_name]
#             # Call the function
#             result = action_function(**function_parms)

#             function_result_message = f"Action_Response: {result}"
#             messages.append({"role": "user", "content": function_result_message})

#             print(function_result_message)
#         else:
#             break

if __name__ == "__main__":
    # website_url = input("Enter a website URL to analyze: ")
    analyze()
