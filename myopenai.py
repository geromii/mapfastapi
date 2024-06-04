from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Your role is to provide summaries of events, as you know them. The user will provide a year and a modern day country. Your role is to reference specific noteworthy events that were occurring during that period in that region. Write three sentences, then conclude with a score on a scale of 0-100 representing how eventful that period was. "
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Scotland, 1668"
        }
      ]
    }
  ],
  temperature=0.5,
  max_tokens=998,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
import json

print(response)


