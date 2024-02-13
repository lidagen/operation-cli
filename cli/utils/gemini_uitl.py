import google.generativeai as genai


# Used to securely store your API key


def genai_no_stream(apikey, text):
    genai.configure(api_key=f"{apikey}", transport='rest')
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()

    response = chat.send_message(text)
    return response
