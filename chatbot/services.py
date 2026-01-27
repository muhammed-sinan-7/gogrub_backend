from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def ask_gemini(user_message: str, history=None) -> tuple[str, list]:
    model_id = "gemini-2.5-flash"
    
    system_prompt = (
        "You are a friendly customer support assistant for a food delivery service. "
        "We serve pizza, burgers, sushi, vegetarian dishes, rolls, seafood, and more. "
        "Always respond in a warm, simple, and user-friendly tone. "
        "Keep answers very short and easy to read. "
        "Limit responses to a maximum of 1–2 short lines. "
        "Avoid long explanations or technical details."
    )

    try:
        chat = client.chats.create(
            model=model_id,
            config={
                "system_instruction": system_prompt,
                "temperature": 0.7,
            },
            history=history or []
        )
        
        response = chat.send_message(user_message)
        
        current_history = history or []
        current_history.append({"role": "user", "parts": [{"text": user_message}]})
        current_history.append({"role": "model", "parts": [{"text": response.text}]})

        return response.text.strip(), current_history

    except Exception as e:
        print(f"Session Error: {e}")
        return "Sorry, our kitchen is busy right now. Please try again in a few moments!", history or []
