import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your Render Environment Variables or .env file.")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash"

SYSTEM_PROMPT = """
You are CyberGuard AI, a cybersecurity awareness chatbot.
Answer users' cybersecurity questions clearly and safely.

Focus on:
- phishing and scam awareness
- password and account security
- malware and virus awareness
- social media and email safety
- UPI/online payment safety
- privacy and safe browsing
- cyber incident response and prevention
- cybersecurity concepts for students

You may explain defensive security concepts and safe, authorized practices.
Do not provide instructions that enable unauthorized access, credential theft,
malware deployment, evasion, or other harmful cyber activity.
If a request is unsafe, briefly refuse that part and redirect to defensive,
legal, educational guidance.

Use simple language. If the user writes Tamil/Thanglish, answer in Tamil/Thanglish.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a cybersecurity question."}), 400

    try:
        prompt = SYSTEM_PROMPT + "\n\nUser question:\n" + user_message
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        reply = getattr(response, "text", None) or "Sorry, I couldn't generate a response."
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Sorry, something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
