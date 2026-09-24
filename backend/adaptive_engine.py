from sop_loader import load_sops


def calculate_score(questions, answers):
    """
    Calculate quiz score based on submitted answers.
    """

    total = len(questions)
    correct = 0

    for i in range(total):
        if answers[i] == questions[i]["answer"]:
            correct += 1

    if total == 0:
        return 0

    score = (correct / total) * 100

    return round(score)


def classify_performance(score):
    """
    Classify employee performance using explainable rules.
    """

    if score >= 80:
        return "mastered"

    if score >= 60:
        return "reinforcement"

    return "weak"


def get_next_topic(current_topic):
    """
    Select another SOP topic after the current topic is mastered.
    """

    sops = load_sops()

    topics = list(sops.keys())

    for topic in topics:
        if topic != current_topic:
            return topic

    return current_topic


def recommend_next_topic(current_topic, score):
    """
    Recommend the next learning action based on quiz score.
    """

    performance = classify_performance(score)

    if performance == "weak":
        return {
            "recommendation": current_topic,
            "reason": f"Your score is {score}%, so this topic needs more practice.",
            "status": "weak"
        }

    if performance == "reinforcement":
        return {
            "recommendation": current_topic,
            "reason": f"Your score is {score}%. A quick reinforcement of this topic is recommended.",
            "status": "reinforcement"
        }

    next_topic = get_next_topic(current_topic)

    return {
        "recommendation": next_topic,
        "reason": f"You scored {score}% and demonstrated mastery of {current_topic}.",
        "status": "mastered"
    }