# CyberGuard AI

A Gemini-powered cybersecurity awareness chatbot built with Flask.

## Files
- `app.py` - Flask backend + Gemini API
- `templates/index.html` - chatbot UI
- `static/style.css` - styling
- `requirements.txt` - Python packages
- `render.yaml` - Render deployment configuration

## Run locally

1. Install Python.
2. Open a terminal in this project folder.
3. Run:
   `pip install -r requirements.txt`
4. Create a `.env` file:
   `GEMINI_API_KEY=YOUR_API_KEY`
5. Run:
   `python app.py`
6. Open `http://127.0.0.1:5000`

## Render

Create a new Web Service from this project/repository.

Build Command:
`pip install -r requirements.txt`

Start Command:
`gunicorn app:app`

Add Environment Variable:
Key: `GEMINI_API_KEY`
Value: your Gemini API key

The backend uses model:
`gemini-3.1-flash`

Note: model availability depends on the Gemini API account/region. If the API reports that this model is unavailable, use the currently available Gemini Flash model shown in your Gemini API documentation/console.
