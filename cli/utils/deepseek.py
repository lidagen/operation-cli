from openai import OpenAI


def genai_no_stream(apikey, text):
    client = OpenAI(api_key=apikey, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )

    return response.choices[0].message.content
