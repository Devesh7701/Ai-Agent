from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
