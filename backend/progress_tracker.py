progress = {}


def save_progress(employee, topic, score, status):
    """
    Save the employee's score for a topic.
    """

    if employee not in progress:
        progress[employee] = {}

    progress[employee][topic] = {
        "score": score,
        "status": status
    }


def get_progress(employee):
    """
    Return all learning progress for an employee.
    """

    if employee not in progress:
        return {}

    return progress[employee]


def calculate_readiness(employee):
    """
    Calculate overall onboarding readiness.
    """

    employee_progress = get_progress(employee)

    if not employee_progress:
        return 0

    scores = [
        data["score"]
        for data in employee_progress.values()
    ]

    return round(sum(scores) / len(scores))


def get_weak_areas(employee):
    """
    Find topics where the employee needs improvement.
    """

    employee_progress = get_progress(employee)

    weak_topics = []

    for topic, data in employee_progress.items():
        if data["score"] < 60:
            weak_topics.append(topic)

    return weak_topics