import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

# Get Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Add it in Render Environment Variables."
    )

# Gemini Client
client = genai.Client(api_key=api_key)

# Gemini 3.5 Flash
MODEL = "gemini-3.5-flash"

SYSTEM_PROMPT = """
You are CyberGuard AI, a cybersecurity awareness chatbot.

Your job is to answer cybersecurity questions clearly,
simply, and safely.

Topics you can explain:

- Phishing and scam awareness
- Password security
- Account security
- Malware and virus awareness
- Email security
- Social media security
- UPI and online payment safety
- Privacy and safe browsing
- Cybersecurity concepts
- Cyber incident response
- Cybersecurity awareness for students

IMPORTANT:
Only provide legal, ethical, defensive and educational
cybersecurity guidance.

Do NOT provide instructions for:
- Unauthorized account access
- Credential theft
- Malware deployment
- Ransomware
- Stealing passwords
- Bypassing security
- Hacking real systems
- Evading detection

If a user asks for harmful or unauthorized instructions,
refuse that part and provide a safe defensive alternative.

Keep answers simple and useful.

If the user asks in Tamil or Thanglish,
answer in Tamil/Thanglish.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please enter a cybersecurity question."
        }), 400

    try:

        prompt = SYSTEM_PROMPT + """

User Question:
""" + user_message

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                )
            )
        )

        reply = response.text

        if not reply:
            reply = "Sorry, I could not generate a response."

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("Gemini API Error:", str(e))

        return jsonify({
            "reply": "Sorry, the AI service is temporarily unavailable. Please try again."
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
