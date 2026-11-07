
import os
import json
import urllib.request
import urllib.error
import urllib.parse

import streamlit as st


def demo(q):
    q = q.lower()

    if "feedback" in q or "rating" in q:
        return (
            "A useful feedback process collects response ratings "
            "to evaluate whether an answer solved the user's problem."
        )

    if "sentiment" in q:
        return (
            "Sentiment analysis estimates the emotional tone of text "
            "using natural language processing techniques."
        )

    return (
        "Thanks for your question! This is InsightAI demo mode. "
        "Configure a Gemini API key to enable live AI-generated answers. "
        "You can still test response ratings, feedback collection, "
        "sentiment labels and analytics."
    )


def answer(q):

    # Step 1: Read Gemini API key from Streamlit Secrets
    key = ""

    try:
        key = (
            st.secrets.get("GOOGLE_API_KEY", "")
            or st.secrets.get("GEMINI_API_KEY", "")
        ).strip()
    except Exception:
        pass

    # Step 2: Check environment variables if Secrets are unavailable
    if not key:
        key = (
            os.getenv("GOOGLE_API_KEY", "")
            or os.getenv("GEMINI_API_KEY", "")
        ).strip()

    # Step 3: Use demo mode if no API key is available
    if not key:
        return demo(q), "Demo mode - no Gemini API key"

    # Step 4: Select Gemini model
    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    try:
        model = st.secrets.get("GEMINI_MODEL", model)
    except Exception:
        pass

    # Step 5: Prepare Gemini API endpoint
    encoded_model = urllib.parse.quote(model, safe="")

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{encoded_model}:generateContent"
        f"?key={key}"
    )

    # Step 6: Prepare request payload
    payload = {
        "system_instruction": {
            "parts": [
                {
                    "text": (
                        "You are InsightAI, a helpful and careful AI assistant. "
                        "Give accurate, clear and useful answers. "
                        "Explain uncertainty when necessary. "
                        "Never ask users for passwords, OTPs or API keys."
                    )
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": str(q)}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    # Step 7: Create HTTP request
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    # Step 8: Send request and process response
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        candidates = data.get("candidates", [])

        if not candidates:
            return (
                "Gemini did not generate a response. "
                "The request may have been blocked by safety filters.",
                "Gemini response unavailable"
            )

        parts = candidates[0].get("content", {}).get("parts", [])

        response_text = "\n".join(
            part["text"]
            for part in parts
            if "text" in part
        ).strip()

        if not response_text:
            return (
                "Gemini returned an empty response. Please try again.",
                "Empty response"
            )

        return response_text, f"Live response - {model}"

    # Step 9: Handle API errors
    except urllib.error.HTTPError as e:

        error_details = e.read().decode("utf-8", errors="replace")

        return (
            f"Gemini API error (HTTP {e.code}): {error_details[:500]}",
            "API error"
        )

    except urllib.error.URLError as e:

        return (
            f"Network connection error: {e.reason}",
            "Connection error"
        )

    except Exception as e:

        return (
            f"Unexpected error: {type(e).__name__}: {e}",
            "Application error"
        )

