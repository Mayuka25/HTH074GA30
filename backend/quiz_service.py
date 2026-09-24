from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.5-flash-lite"


def fallback_quiz(topic, sop_content):
    """
    Grounded fallback quiz.
    Used when Gemini is temporarily unavailable.
    Questions are based directly on the provided SOP.
    """

    if "equipment" in topic.lower():
        return {
            "questions": [
                {
                    "question": "When must employees inspect equipment?",
                    "options": [
                        "After finishing work",
                        "Before starting work",
                        "Once a month",
                        "Only after a malfunction"
                    ],
                    "answer": "Before starting work",
                    "explanation": "The SOP states that employees must inspect equipment before starting work."
                },
                {
                    "question": "What must employees wear when operating machinery?",
                    "options": [
                        "Formal clothing",
                        "Safety shoes only",
                        "Required personal protective equipment (PPE)",
                        "No protective equipment"
                    ],
                    "answer": "Required personal protective equipment (PPE)",
                    "explanation": "The SOP requires employees to wear the required PPE when operating machinery."
                },
                {
                    "question": "What should an employee do if equipment malfunctions?",
                    "options": [
                        "Continue using it",
                        "Repair it without permission",
                        "Report it immediately to the supervisor",
                        "Ignore the problem"
                    ],
                    "answer": "Report it immediately to the supervisor",
                    "explanation": "The SOP states that equipment malfunctions must be reported immediately to the supervisor."
                },
                {
                    "question": "What must employees do before performing maintenance?",
                    "options": [
                        "Switch off the equipment",
                        "Increase the machine speed",
                        "Remove all PPE",
                        "Ask another employee to operate it"
                    ],
                    "answer": "Switch off the equipment",
                    "explanation": "The SOP requires employees to switch off equipment before performing maintenance."
                },
                {
                    "question": "Who is permitted to operate specialized machinery?",
                    "options": [
                        "Any employee",
                        "Only visitors",
                        "Only trained employees",
                        "Only managers"
                    ],
                    "answer": "Only trained employees",
                    "explanation": "The SOP states that only trained employees are permitted to operate specialized machinery."
                }
            ]
        }

    return {
        "questions": [
            {
                "question": "Which statement is directly supported by the provided SOP?",
                "options": [
                    "Follow the procedures described in the SOP.",
                    "Ignore the SOP.",
                    "Use outside company policies.",
                    "Assume missing information."
                ],
                "answer": "Follow the procedures described in the SOP.",
                "explanation": "This fallback question avoids inventing information that is not available in the provided SOP."
            }
        ]
    }


def generate_quiz(topic, sop_content):

    prompt = f"""
You are an employee onboarding quiz generator.

Create exactly 5 multiple-choice questions using ONLY the SOP content provided below.

Topic:
{topic}

SOP Content:
{sop_content}

STRICT RULES:
1. Every question must be directly supported by the SOP.
2. Do not use outside knowledge.
3. Each question must have exactly 4 options.
4. Only one option must be correct.
5. The correct answer must be one of the four options.
6. Include a short explanation for the correct answer.
7. Return ONLY valid JSON.
8. Do not add markdown or extra text.

Return this exact JSON structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Why this answer is correct according to the SOP."
        }}
    ]
}}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("Gemini unavailable. Using grounded fallback quiz.")
        print("Gemini error:", e)

        return fallback_quiz(topic, sop_content)