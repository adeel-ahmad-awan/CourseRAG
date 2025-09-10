from flask import Blueprint, render_template, request, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "")
    bot_response = f"You said: {user_message}"
    return jsonify({"response": bot_response})
