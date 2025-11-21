# ...existing code...
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # carga variables desde .env en la raíz del proyecto

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta la variable de entorno GOOGLE_API_KEY en .env o en el entorno")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-pro")

def chat_with_ai(prompt):
    response = model.generate_content(prompt)
    return response.text

def get_agriculture_answer(prompt, context=None):
    try:
        if context:
            prompt = f"{prompt} Contexto: {context}"
        answer = model.generate_content(prompt)
        return {"answer": answer.text}
    except Exception as e:
        return {"answer": f"Error interno IA: {str(e)}"}

if __name__ == "__main__":
    user_input = input("Escribe tu mensaje: ")
    print("IA:", chat_with_ai(user_input))
# ...existing code...