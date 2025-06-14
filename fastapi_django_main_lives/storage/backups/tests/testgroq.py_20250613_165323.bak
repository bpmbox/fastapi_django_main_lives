import openai # openai v1.0.0+
client = openai.OpenAI(api_key="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",base_url="https://api.groq.com/openai/v1") # set proxy to base_url
# request sent to model set on litellm proxy, `litellm --model`
response = client.chat.completions.create(model="Llama3-70b-8192", messages = [
    {
        "role": "user",
        "content": "this is a test request, write a short poem"
    }
])

print(response)