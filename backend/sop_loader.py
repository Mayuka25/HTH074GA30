from pathlib import Path

SOP_DIR = Path(__file__).resolve().parent.parent / "data" / "sops"


def load_sops():
    documents = {}

    for path in SOP_DIR.glob("*.txt"):
        documents[path.stem] = path.read_text(encoding="utf-8")

    return documents


def search_sops(query):
    query = query.lower().strip()
    query_words = query.split()

    results = []

    for name, text in load_sops().items():
        text_lower = text.lower()

        score = 0

        # Exact topic/name match gets highest priority
        topic_name = name.replace("_", " ")

        if query == topic_name:
            score += 100

        # Individual query words
        for word in query_words:
            if word in topic_name:
                score += 10

            if word in text_lower:
                score += 1

        if score > 0:
            results.append((score, name, text))

    results.sort(key=lambda x: x[0], reverse=True)

    return results