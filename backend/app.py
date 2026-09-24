from flask import Flask, jsonify, request
from sop_loader import search_sops

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Adaptive Corporate Onboarding Coach is running!"
    })


@app.route("/api/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Query is required"
        }), 400

    results = search_sops(query)

    return jsonify({
        "query": query,
        "results": [
            {
                "topic": name,
                "content": text,
                "score": score
            }
            for score, name, text in results[:3]
        ]
    })


if __name__ == "__main__":
    app.run(debug=False)