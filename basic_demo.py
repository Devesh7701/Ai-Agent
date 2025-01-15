# import requests
# from groq import Groq
# import os

# client = Groq(
#     api_key="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",
# )

# def ask_questions():
#     print("Welcome to the Market Research AI Agent!")
#     user_data = {}
#     questions = [
#         {"question": "What is your age?", "key": "age"},
#         {"question": "What is your preferred product category?", "key": "product_category"},
#         {"question": "How much do you spend monthly on this category?", "key": "monthly_budget"},
#     ]
#     for q in questions:
#         user_data[q["key"]] = input(q["question"] + " ")
#     return user_data

# s = str(ask_questions())
# # print(type(s))
# # print(ask_questions())
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "what should a person buy if he has the following need in India"+" "+s,
#         }
#     ],
#     model="llama3-8b-8192",
#     stream=False,
# )

# print(chat_completion.choices[0].message.content)
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.getenv("GROQCLOUD_API_KEY"),
)
# Example usage
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "till what date you are updated"}
    ]
)
# response = client.completions.create(prompt=[{"role": "user", "content": "write a haiku about ai"}],
#                                      model="gpt-4o")
print(completion.choices[0].message.content)
