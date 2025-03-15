from openai import OpenAI


def genai_no_stream(apikey, text):
    client = OpenAI(api_key=apikey, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": text},
        ],
        stream=False
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    stream = genai_no_stream("sk-759b1d5b1ee74adcbe570fa4c218ee17", "hello")
    print(stream)
