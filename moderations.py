from openai import OpenAI
client = OpenAI()

response = client.moderations.create(input="Go commit suicide")

output = response.results[0]

for line in str(output).split(','):
    print(line)
