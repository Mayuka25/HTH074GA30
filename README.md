

> A Generative AI-powered corporate onboarding system that uses company SOPs to generate grounded learning content, assess employee knowledge, identify knowledge gaps, and recommend the next learning topic.

## Overview

OnboardAI is an adaptive corporate onboarding and knowledge coaching system designed to help new employees learn company policies, procedures, safety guidelines, security practices, and workflows.

The system uses **synthetic company SOP documents as its knowledge base**. When an employee asks about a topic, the system retrieves the relevant SOP and sends the retrieved information to **Google Gemini** to generate a simple, grounded explanation.

Employees can then take AI-generated quizzes. Their performance is analyzed to identify weak areas and recommend what they should learn next.

## Problem

New employees often need to learn information from multiple company documents before becoming productive.

Traditional onboarding can provide the same learning sequence to every employee, even though different employees may have different knowledge gaps.

OnboardAI addresses this by providing:

* Company-specific knowledge
* AI-generated explanations
* AI-generated assessments
* Performance tracking
* Weak-area detection
* Adaptive learning recommendations

## Solution

The system follows this learning cycle:

```text
Synthetic Company SOPs
        ↓
SOP Retrieval
        ↓
Relevant SOP
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
```

## Generative AI

Google Gemini is used for two primary functions.

### Grounded Explanation

When an employee asks about a topic:

```text
Employee Query
      ↓
SOP Retrieval
      ↓
Relevant SOP Content
      ↓
Google Gemini
      ↓
Simple Explanation
```

Gemini is instructed to use only the provided SOP information and not invent company policies.

### Quiz Generation

Gemini generates a multiple-choice assessment from the selected SOP.

Each quiz contains:

* 5 questions
* 4 options per question
* One correct answer
* Explanation for the correct answer

The quiz-generation prompt requires every question to be grounded in the provided SOP.

## Knowledge Base

The prototype contains 12 synthetic company SOP documents:

1. Company Overview
2. HR Policies
3. Attendance Policy
4. Leave Policy
5. Workplace Communication
6. Workplace Safety
7. Equipment Safety
8. Data Security
9. Password Security
10. Remote Work Policy
11. Project Workflow
12. Emergency Procedures

These synthetic documents simulate internal company knowledge without using real confidential company information.

## SOP Retrieval

The current prototype uses **Python keyword-based SOP retrieval**.

The retrieval process:

1. Loads the available SOP documents.
2. Compares the employee's query with SOP names and content.
3. Calculates a relevance score.
4. Ranks matching SOPs.
5. Selects the most relevant SOP.
6. Provides the selected content to Gemini.

## Adaptive Learning

The system evaluates employee performance after each assessment.

| Score        | Status        | Action                        |
| ------------ | ------------- | ----------------------------- |
| Below 60%    | Weak          | Continue practicing the topic |
| 60–79%       | Reinforcement | Reinforce the topic           |
| 80% or above | Mastered      | Move toward the next topic    |

The recommendation is explainable because the system provides the reason behind the recommendation.

Example:

```text
Score: 40%

Status: Weak

Recommendation:
Equipment Safety

Reason:
Your score is 40%, so this topic needs more practice.
```

After improvement:

```text
Score: 80%

Status: Mastered

Recommendation:
Next learning topic
```

## Progress Tracking

The system tracks employee learning progress, including:

* Topic-wise scores
* Performance status
* Weak areas
* Overall readiness
* Recommended next topic

## Dashboard

The web dashboard contains:

### Dashboard

* Overall readiness
* Topics completed
* Topics needing attention
* Current learning focus
* AI recommendation

### Learn

Allows employees to enter a topic and receive an AI-generated explanation based on the relevant SOP.

### Assessment

Allows employees to generate and complete an AI-generated quiz.

### Progress

Displays employee scores and learning status for assessed topics.

## Technology Stack

| Layer           | Technology                     | Purpose                         |
| --------------- | ------------------------------ | ------------------------------- |
| AI              | Google Gemini                  | Explanation and quiz generation |
| LLM SDK         | Google GenAI Python SDK        | Gemini API integration          |
| Backend         | Python + Flask                 | Backend application and APIs    |
| Retrieval       | Python keyword-based retrieval | Relevant SOP selection          |
| Knowledge Base  | Synthetic `.txt` SOPs          | Company knowledge               |
| API             | Flask REST-style endpoints     | Frontend-backend communication  |
| Frontend        | HTML, CSS, JavaScript          | Web dashboard                   |
| Version Control | Git + GitHub                   | Source-code management          |
| Runtime         | Python                         | Application execution           |

## Project Structure

```text
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
```

## Setup

### Clone the repository

```bash
git clone https://github.com/Mayuka25/HTH074GA30.git
```

### Enter the project

```bash
cd HTH074GA30
```

### Install dependencies

```bash
pip install flask google-genai
```

### Configure Gemini API

Set the Gemini API key as an environment variable.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

**Do not commit the API key to GitHub.**

### Run the application

```powershell
python backend\app.py
```

Open:

```text
http://127.0.0.1:5000/dashboard
```

## Security

The prototype uses synthetic SOP data rather than real confidential company information.

The Gemini API key is stored as an environment variable and is not included in the frontend source code.

The backend controls which SOP content is sent to Gemini.

For production deployment, additional authentication, authorization, secure secret management, data protection, and enterprise security controls would be required.

## Key Innovation

The main idea behind OnboardAI is the **adaptive learning loop**.

Instead of providing every employee with the same fixed learning sequence, the system uses assessment performance to identify knowledge gaps and determine what the employee should learn next.

```text
Learn
  ↓
Assess
  ↓
Measure Performance
  ↓
Identify Knowledge Gap
  ↓
Adapt
  ↓
Learn Again
```

## Future Scope

Possible future improvements include:

* Personalized daily learning plans
* Persistent employee data storage
* Manager-facing readiness reports
* Multi-role onboarding tracks
* Semantic/vector-based document retrieval
* Authentication and role-based access
* Enterprise document integration
* Advanced learning analytics

## Project Status

**Core MVP — Functional**

```text
SOP Knowledge Base       ✓
SOP Retrieval             ✓
Gemini Integration        ✓
Grounded Explanation      ✓
Quiz Generation           ✓
Quiz Scoring              ✓
Weak-Area Detection       ✓
Adaptive Recommendation   ✓
Progress Tracking         ✓
Web Dashboard             ✓
```

This version is **only based on what we've actually built in this project**. No Team ELEXA, no unrelated previous project details, and no imaginary features.
