import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic

# Environment variables (.env) load karein
load_dotenv()

app = Flask(__name__)

# Anthropic Client setup
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    messages_history = data.get("history", [])

    if not messages_history:
        return jsonify({"answer": "Sawal khali hai, kuch likhein."}), 400

    # AI Instruction (System Prompt)
    system_prompt = (
        "Aap ek highly intelligent, advanced AI assistant hain. "
        "Aap user ke sawalon ka bohot detail, accurate aur professional tarike se jawab dete hain. "
        "Jawab mein Markdown (bold, lists, tables, code blocks) ka behtar istemal karein."
    )

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1500,
            system=system_prompt,
            messages=messages_history
        )
        answer_text = response.content[0].text
        return jsonify({"answer": answer_text})

    except anthropic.APIError as e:
        return jsonify({"answer": f"Anthropic API Error: {e.message}"}), 500
    except Exception as e:
        return jsonify({"answer": f"System Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
