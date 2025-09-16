# app/routes.py
from flask import Blueprint, render_template, request, jsonify
from app.utils.query_rag import query_rag

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"response": "Please enter a message."})

    # Call RAG query function
    response_text, sources = query_rag(user_message)

    # Return both answer and sources
    return jsonify({
        "response": response_text,
        "sources": sources
    })
