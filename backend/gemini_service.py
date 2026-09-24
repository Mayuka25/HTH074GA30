from google import genai
import os

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_grounded_explanation(topic, sop_content):
    prompt = f"""
You are an employee onboarding learning coach.

You MUST answer using ONLY the SOP content provided below.

Topic:
{topic}

SOP Content:
{sop_content}

Instructions:
1. Explain the topic in simple language for a new employee.
2. Use only facts present in the SOP.
3. Do not invent or assume company policies.
4. If something is not available in the SOP, say:
   "This information is not available in the provided company SOP."
5. Give a short explanation.
6. Include important rules as bullet points.

Now explain the topic.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text