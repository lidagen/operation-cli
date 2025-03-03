from google import genai


# Used to securely store your API key


def genai_no_stream(apikey, text):
    client = genai.Client(api_key=f"{apikey}")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=text
    )
    return response
