# --- INTEGRACIÓN GEMINI / OPENAI ---
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import vision  # si lo usas en otra parte
import base64
import requests
from django.conf import settings
import openai

# Cargar variables de entorno desde .env en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ===== API KEY GEMINI =====
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Falta GOOGLE_API_KEY o GENAI_API_KEY en .env o en el entorno")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-pro")

# ===== API KEY OPENAI (DALL·E) =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Si quieres que sea opcional, puedes no lanzar error aquí
    raise RuntimeError("Falta OPENAI_API_KEY en .env o en el entorno")

openai.api_key = OPENAI_API_KEY


def get_agriculture_answer(question: str, crop_info: dict | None = None) -> dict:
    """
    Consulta a Gemini para preguntas agrícolas y genera imágenes con DALL-E si lo pide.
    Retorna dict con keys: ok(bool), answer(str), source(str), image_url(str|None)
    """
    prompt = question.strip() if question else ""
    if crop_info:
        prompt += (
            f"\nContexto: cultivo={crop_info.get('name')}, "
            f"lat={crop_info.get('lat')}, lon={crop_info.get('lon')}"
        )

    image_keywords = [
        "imagen", "foto", "dibuja", "genera una imagen", "visualiza",
        "picture", "draw", "generate an image", "show me a picture",
    ]
    wants_image = any(kw in prompt.lower() for kw in image_keywords)

    def generate_dalle_image(query: str) -> str | None:
        try:
            response = openai.Image.create(
                prompt=query,
                n=1,
                size="512x512",
            )
            return response["data"][0]["url"] if response and "data" in response else None
        except Exception as e:
            import sys
            print("DALL-E error:", e, file=sys.stderr)
            return None

    try:
        if wants_image:
            tema = (
                prompt.split("imagen de")[-1].strip()
                if "imagen de" in prompt.lower()
                else prompt
            )
            image_url = generate_dalle_image(tema)
            answer = "Aquí tienes una imagen generada por IA."
            return {
                "ok": True,
                "answer": answer,
                "source": "dalle",
                "image_url": image_url,
            }
        else:
            response = model.generate_content(prompt)
            return {
                "ok": True,
                "answer": response.text,
                "source": "gemini",
                "image_url": None,
            }
    except Exception as e:
        return {
            "ok": False,
            "answer": f"Error de red al contactar IA: {str(e)}",
            "source": "gemini",
            "image_url": None,
        }


def recommend_sowing_window(lat: float, lon: float, crop_name: str) -> dict:
    """
    Recomienda ventana de siembra usando Gemini.
    """
    prompt = (
        f"Recomienda la mejor ventana de siembra para {crop_name} "
        f"en lat={lat}, lon={lon}. Indica meses ideales y consideraciones climáticas."
    )
    try:
        response = model.generate_content(prompt)
        return {
            "ok": True,
            "window_text": response.text,
            "source": "gemini",
        }
    except Exception as e:
        return {
            "ok": False,
            "window_text": f"Error de red al contactar IA: {str(e)}",
            "source": "gemini",
        }
