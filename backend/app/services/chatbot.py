def get_chatbot_response(message: str) -> str:
    message = message.lower().strip()
    if "hello" in message or "hi" in message:
        return "Hello! How can I assist you today?"
    elif "bye" in message or "goodbye" in message:
        return "Goodbye! Have a great day!"
    elif "how are you" in message:
        return "I’m doing great, thanks for asking! How about you?"
    else:
        return "Hmm, I’m not sure how to respond to that. Try saying 'hello' or 'bye'!"