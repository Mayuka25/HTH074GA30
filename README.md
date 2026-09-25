OnboardAI — Adaptive Corporate Onboarding & Knowledge Coach

A Generative AI-powered onboarding coach that uses company SOPs to generate grounded learning content, assess employee knowledge, identify knowledge gaps, and adapt the employee's learning path.

🚀 Overview

OnboardAI is an AI-powered corporate onboarding and knowledge coaching system designed to help new employees become productive faster.

Instead of giving every employee the same fixed onboarding sequence, OnboardAI uses Generative AI + company SOP retrieval + adaptive assessment to personalize the learning journey based on the employee's demonstrated knowledge.

The system uses synthetic company SOP documents as its knowledge base. When an employee asks about a topic, the system first retrieves the most relevant SOP and then uses Google Gemini to generate a simple explanation based only on the retrieved information.

Employees can then take AI-generated assessments. Their scores are analyzed to identify weak areas and determine what they should learn next.

🎯 Problem

New employees often need to learn company policies, safety procedures, workflows, communication practices, and security guidelines before becoming productive.

However, this information can be:

Scattered across different documents
Difficult for new employees to understand
Time-consuming to learn
Delivered through the same learning path for every employee
Difficult for managers to track

OnboardAI addresses this by creating a personalized, adaptive onboarding experience.

💡 Solution

OnboardAI combines:

Synthetic company SOP knowledge
Document retrieval
Generative AI
AI-generated assessments
Performance scoring
Weak-area detection
Adaptive topic recommendation
Employee progress tracking
Personalized dashboard
Core Learning Loop
Company SOPs
     ↓
SOP Retrieval
     ↓
Relevant Knowledge
     ↓
Google Gemini
     ↓
AI Explanation / Quiz
     ↓
Employee Assessment
     ↓
Score Calculation
     ↓
Weak-Area Detection
     ↓
Adaptive Recommendation
     ↓
Progress Dashboard
🤖 Generative AI Component

Google Gemini is used for two major tasks:

1. Grounded Learning Explanation

When an employee asks about a topic:

Employee Query
      ↓
SOP Retrieval
      ↓
Relevant SOP
      ↓
Gemini
      ↓
Simple Employee-Friendly Explanation

Gemini is instructed to use only the provided SOP content and avoid inventing company policies.

2. AI Quiz Generation

Gemini generates multiple-choice questions using the selected SOP.

Each quiz contains:

5 questions
4 options per question
One correct answer
Explanation for the correct answer

The prompt explicitly requires questions to be grounded in the provided SOP.

🧠 Adaptive Learning Engine

The adaptive engine analyzes employee quiz performance.

Score	Status	Learning Action
< 60%	Weak	Continue practicing the same topic
60–79%	Reinforcement	Reinforce the topic
≥ 80%	Mastered	Move toward the next learning topic

The recommendation includes an explanation so that the adaptation is transparent rather than a black-box decision.

Example
Equipment Safety → 40%

Status:
WEAK

Recommendation:
Equipment Safety

Reason:
Your score is 40%, so this topic needs more practice.

After improvement:

Equipment Safety → 80%

Status:
MASTERED

Recommendation:
Next learning topic
📚 Knowledge Base

The prototype contains 12 synthetic company SOP documents:

Company Overview
HR Policies
Attendance Policy
Leave Policy
Workplace Communication
Workplace Safety
Equipment Safety
Data Security
Password Security
Remote Work Policy
Project Workflow
Emergency Procedures

The SOPs are synthetic and are used to simulate internal company knowledge without exposing real confidential company information.

🔍 Retrieval System

The current prototype uses Python keyword-based SOP retrieval.

When a user enters a topic, the retrieval system:

Reads the available SOP documents.
Matches the employee query against SOP names and content.
Calculates a relevance score.
Ranks matching documents.
Selects the most relevant SOP.
Sends the selected SOP content to Gemini.

Example:

Query:
equipment safety

        ↓

equipment_safety.txt
        ↓

Highest relevance
        ↓

Gemini
🖥️ Dashboard

The web dashboard provides four major areas:

Dashboard

Displays:

Overall onboarding readiness
Topics completed
Topics needing attention
Current learning focus
AI recommendation
Learn

Employees can enter a company topic and receive an AI-generated explanation grounded in the available SOP.

Assessment

Employees can generate and complete an AI-generated quiz based on a selected SOP.

Progress

Displays employee learning progress, including:

Topic scores
Performance status
Weak areas
Overall readiness
🏗️ System Architecture
                    ┌─────────────────────┐
                    │   Synthetic SOPs    │
                    │     12 Documents    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Python Retrieval   │
                    │ Keyword-based Search│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Google Gemini    │
                    │  Grounded GenAI     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        AI Explanation                 Quiz Generation
                                             │
                                             ▼
                                    Employee Answers
                                             │
                                             ▼
                                    Score Calculation
                                             │
                                             ▼
                                    Adaptive Engine
                                             │
                                             ▼
                                  Learning Recommendation
                                             │
                                             ▼
                                    Progress Tracking
                                             │
                                             ▼
                                    Employee Dashboard
🛠️ Technology Stack
Layer	Technology	Purpose
AI	Google Gemini	Grounded explanations and quiz generation
LLM SDK	Google GenAI Python SDK	Communication with Gemini API
Backend	Python + Flask	Application server and APIs
Retrieval	Python keyword-based retrieval	SOP selection
Knowledge Base	Synthetic .txt SOPs	Company knowledge
API	REST-style Flask endpoints	Frontend-backend communication
Frontend	HTML, CSS, JavaScript	Employee dashboard
Version Control	Git + GitHub	Source-code management
Runtime	Python	Application execution
📁 Project Structure
HTH074GA30/
│
├── backend/
│   ├── app.py
│   ├── sop_loader.py
│   ├── gemini_service.py
│   ├── quiz_service.py
│   ├── adaptive_engine.py
│   └── progress_tracker.py
│
├── data/
│   └── sops/
│       ├── attendance_policy.txt
│       ├── company_overview.txt
│       ├── data_security.txt
│       ├── emergency_procedures.txt
│       ├── equipment_safety.txt
│       ├── hr_policies.txt
│       ├── leave_policy.txt
│       ├── password_security.txt
│       ├── project_workflow.txt
│       ├── remote_work_policy.txt
│       ├── workplace_communication.txt
│       └── workplace_safety.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
⚙️ Setup
1. Clone the repository
git clone https://github.com/Mayuka25/HTH074GA30.git
2. Enter the project directory
cd HTH074GA30
3. Install dependencies
pip install flask google-genai
4. Configure Gemini API Key

Set your Gemini API key as an environment variable.

Windows PowerShell:

$env:GEMINI_API_KEY="YOUR_API_KEY"

Do not commit the API key to GitHub.

5. Run the application
python backend\app.py
6. Open the dashboard
http://127.0.0.1:5000/dashboard
🔐 Data & API Security

The prototype uses synthetic SOP documents rather than real confidential company information.

The Gemini API key is stored as an environment variable and is not included in the frontend or source code.

The backend controls which retrieved SOP content is provided to Gemini.

For production deployment, enterprise-grade data controls, authentication, authorization, secure secret management, and appropriate data-processing policies would be required.

🧪 Example User Journey
Step 1 — Learn

Employee searches:

equipment safety

The system retrieves the relevant SOP and Gemini generates a grounded explanation.

Step 2 — Assessment

The employee generates a 5-question assessment based on the same SOP.

Step 3 — Performance

Suppose the employee scores:

40%

The system identifies:

Status: Weak
Step 4 — Adaptation

The system recommends continuing with:

Equipment Safety

because the employee demonstrated a knowledge gap.

Step 5 — Improvement

The employee retakes the assessment and scores:

80%

The topic becomes:

Mastered

The learning path can then move toward another topic.

🌟 Key Innovation

The key innovation of OnboardAI is the adaptive learning loop.

A conventional chatbot can answer an employee's question.

OnboardAI goes further:

Understand
   ↓
Learn
   ↓
Assess
   ↓
Identify knowledge gap
   ↓
Adapt
   ↓
Learn again

The same company knowledge base can therefore produce different learning paths for different employees based on their demonstrated performance.

🎯 Key Features
✅ Synthetic company knowledge base
✅ SOP document retrieval
✅ Grounded Gemini explanations
✅ AI-generated assessments
✅ Automatic scoring
✅ Weak-area detection
✅ Explainable adaptive recommendations
✅ Employee progress tracking
✅ Overall readiness calculation
✅ Interactive learning dashboard
✅ GitHub-based development workflow
🔮 Future Scope

The system can be extended with:

Personalized daily learning plans
Persistent employee databases
Manager-facing readiness reports
Multi-role onboarding tracks
Semantic/vector-based retrieval
Authentication and role-based access
Enterprise document connectors
More advanced learning analytics
🏆 Hackathon MVP

This project was developed as a 24-hour hackathon MVP for the Generative AI track.

The prototype focuses on demonstrating the complete adaptive onboarding loop rather than production-scale enterprise deployment.

👥 Team

Team: ELEXA
Project: OnboardAI — Adaptive Corporate Onboarding & Knowledge Coach

📌 Project Status

Core MVP: Functional ✅

SOP Knowledge Base       ✅
Document Retrieval       ✅
Gemini Integration       ✅
Grounded Explanation     ✅
Quiz Generation          ✅
Quiz Scoring             ✅
Weak-Area Detection      ✅
Adaptive Recommendation  ✅
Progress Tracking        ✅
Web Dashboard            ✅
