#!/usr/bin/env python3
"""Minimal Flask server: serves the blog and proxies proof-grading requests to Gemini."""

import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
MODEL = "gemini-2.5-flash"

app = Flask(__name__, static_folder="docs", static_url_path="")

SYSTEM_PROMPT = (
    "You are a concise, friendly math grader for a complex analysis blog. "
    "The student has submitted a proof or proof sketch. "
    "Give feedback in 1-3 sentences: say whether the argument is correct, and if not, "
    "give a brief hint. Use LaTeX notation with $...$ for inline math and $$...$$ for display math. "
    "Do not give away the full answer."
)


@app.route("/")
def index():
    return send_from_directory("docs", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("docs", path)


@app.route("/grade", methods=["POST"])
def grade():
    data = request.get_json()
    proof = data.get("proof", "").strip()
    context = data.get("context", "")

    if not proof:
        return jsonify({"feedback": "Please write something first."})

    prompt = f"{SYSTEM_PROMPT}\n\nThe question is: {context}\n\nThe student's response:\n{proof}"

    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return jsonify({"feedback": response.text})
    except Exception as e:
        return jsonify({"feedback": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=8000, debug=True)
