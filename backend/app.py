from flask import Flask, jsonify, request
from sop_loader import search_sops
from gemini_service import generate_grounded_explanation
from quiz_service import generate_quiz
from adaptive_engine import calculate_score, recommend_next_topic
from progress_tracker import (
    save_progress,
    get_progress,
    calculate_readiness,
    get_weak_areas
)

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


@app.route("/api/learn")
def learn():
    query = request.args.get("topic", "").strip()

    if not query:
        return jsonify({
            "error": "Topic is required"
        }), 400

    results = search_sops(query)

    if not results:
        return jsonify({
            "error": "No relevant SOP found for this topic."
        }), 404

    score, topic, content = results[0]

    explanation = generate_grounded_explanation(
        topic,
        content
    )

    return jsonify({
        "topic": topic,
        "explanation": explanation,
        "source_score": score
    })


@app.route("/api/quiz")
def quiz():
    query = request.args.get("topic", "").strip()

    if not query:
        return jsonify({
            "error": "Topic is required"
        }), 400

    results = search_sops(query)

    if not results:
        return jsonify({
            "error": "No relevant SOP found for this topic."
        }), 404

    score, topic, content = results[0]

    quiz_data = generate_quiz(
        topic,
        content
    )

    return jsonify({
        "topic": topic,
        "quiz": quiz_data
    })


@app.route("/api/submit-quiz", methods=["POST"])
def submit_quiz():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    topic = data.get("topic")
    questions = data.get("questions")
    answers = data.get("answers")

    if not topic or not questions or not answers:
        return jsonify({
            "error": "topic, questions and answers are required"
        }), 400

    if len(questions) != len(answers):
        return jsonify({
            "error": "Number of answers must match number of questions"
        }), 400

    # Calculate quiz score
    score = calculate_score(
        questions,
        answers
    )

    # Decide what the employee should learn next
    recommendation = recommend_next_topic(
        topic,
        score
    )

    # Identify employee
    employee = data.get("employee", "Alex")

    # Save employee progress
    save_progress(
        employee,
        topic,
        score,
        recommendation["status"]
    )

    # Return complete progress information
    return jsonify({
        "employee": employee,
        "topic": topic,
        "score": score,
        "recommendation": recommendation,
        "readiness": calculate_readiness(employee),
        "weak_areas": get_weak_areas(employee),
        "progress": get_progress(employee)
    })

@app.route("/api/progress")
def progress():

    employee = request.args.get("employee", "Alex").strip()

    return jsonify({
        "employee": employee,
        "readiness": calculate_readiness(employee),
        "weak_areas": get_weak_areas(employee),
        "progress": get_progress(employee)
    })


if __name__ == "__main__":
    app.run(debug=False)