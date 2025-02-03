import requests
import os
from dotenv import load_dotenv
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from openai import OpenAI
# import openai
from groq import Groq
# from groqcloud import LLM, LLMProvider
# from actions import get_response_time
# from actions import get_seo_page_report
from actions import get_page_summary
# from prompts import system_prompt
from prompts import react_system_prompt
from json_helpers import extract_json

# llm_instance = LLM.create(LLMProvider.OPENAI,model_name = "llama-3.3-70b-versatile")

# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQCLOUD_API_KEY"),
)
# openai_client = os.getenv("GROQCLOUD_API_KEY")
# api_endpoint = "https://api.groq.com/openai/v1"  # Example endpoint, adjust based on actual GroqCloud API documentation

def generate_text_with_conversation(messages, model = "llama-3.3-70b-versatile"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        )
    return response.choices[0].message.content


available_actions = {
    # "get_seo_page_report": get_seo_page_report
    "get_page_summary": get_page_summary
}
# available_actions = {
#     "get_response_time": get_response_time
# }

user_prompt = "what is the response time of facebook.com?"

messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": user_prompt},
]

turn_count = 1
max_turns = 5


while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages, model="llama-3.3-70b-versatile")

    print(response)

    json_function = extract_json_from_text(response)

    if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            print(f" -- running {function_name} {function_parms}")
            action_function = available_actions[function_name]
            #call the function
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
    else:
         break
