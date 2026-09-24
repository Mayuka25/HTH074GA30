from pathlib import Path

SOP_DIR = Path(__file__).resolve().parent.parent / "data" / "sops"


def load_sops():
    documents = {}

    for path in SOP_DIR.glob("*.txt"):
        documents[path.stem] = path.read_text(encoding="utf-8")

    return documents
def search_sops(query):
    query_words = query.lower().split()
    results = []

    for name, text in load_sops().items():
        text_lower = text.lower()

        score = 0

        for word in query_words:
            if word in text_lower:
                score += 1

        if score > 0:
            results.append((score, name, text))

    results.sort(reverse=True)

    return results