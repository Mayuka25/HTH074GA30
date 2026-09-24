const API = "http://127.0.0.1:5000";

let currentQuiz = null;
let selectedAnswers = {};


// -----------------------------
// NAVIGATION
// -----------------------------

function showSection(sectionId) {

    document.querySelectorAll(".section").forEach(section => {
        section.classList.remove("active-section");
    });

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.remove("active");
    });

    const section = document.getElementById(sectionId);

    if (section) {
        section.classList.add("active-section");
    }

    const buttons = document.querySelectorAll(".nav-item");

    buttons.forEach(button => {
        if (button.getAttribute("onclick")?.includes(sectionId)) {
            button.classList.add("active");
        }
    });

    const titles = {
        dashboard: "Welcome back, Alex 👋",
        learn: "Knowledge Coach",
        quiz: "Adaptive Assessment",
        progress: "Your learning progress"
    };

    document.getElementById("page-title").textContent =
        titles[sectionId] || "OnboardAI";
}


// -----------------------------
// LOAD PROGRESS
// -----------------------------

async function loadProgress() {

    try {

        const response = await fetch(
            `${API}/api/progress?employee=Alex`
        );

        if (!response.ok) {
            throw new Error("Unable to load progress");
        }

        const data = await response.json();

        updateDashboard(data);
        renderProgress(data);

    } catch (error) {

        console.error(error);

        document.getElementById("current-description").textContent =
            "Connect to the Flask backend to load your onboarding progress.";
    }
}


function updateDashboard(data) {

    const readiness = data.readiness || 0;

    document.getElementById("readiness").textContent =
        readiness;

    document.getElementById("readiness-bar").style.width =
        `${readiness}%`;

    const weakAreas = data.weak_areas || [];

    document.getElementById("weak-count").textContent =
        weakAreas.length;

    const progress = data.progress || {};

    const topics = Object.keys(progress);

    document.getElementById("completed").textContent =
        topics.length;

    if (topics.length > 0) {

        const latestTopic = topics[topics.length - 1];

        const latestData = progress[latestTopic];

        document.getElementById("current-topic").textContent =
            formatTopic(latestTopic);

        document.getElementById("current-description").textContent =
            `Latest assessment score: ${latestData.score}%. Status: ${latestData.status}.`;

        if (weakAreas.length > 0) {

            document.getElementById("recommended-topic").textContent =
                formatTopic(weakAreas[0]);

            document.getElementById("recommendation-reason").textContent =
                `This topic is below the mastery threshold, so the adaptive engine has prioritized it for reinforcement.`;

        } else {

            document.getElementById("recommended-topic").textContent =
                "Next learning topic";

            document.getElementById("recommendation-reason").textContent =
                "Your assessed topics are currently at or above the mastery threshold. Continue to the next topic.";

        }

    } else {

        document.getElementById("current-topic").textContent =
            "Start your first assessment";

        document.getElementById("recommended-topic").textContent =
            "Waiting for assessment";

    }
}


// -----------------------------
// LEARNING
// -----------------------------

async function learnTopic() {

    const topic = document.getElementById("learn-topic").value.trim();
    const result = document.getElementById("learn-result");

    if (!topic) {
        result.innerHTML = `
            <span class="section-label">ERROR</span>
            <h3>Please enter a topic.</h3>
        `;
        return;
    }

    result.innerHTML = `
        <span class="section-label">AI COACH</span>
        <h3>Thinking...</h3>
        <p>Finding the relevant company SOP and generating your explanation.</p>
    `;

    try {

        const response = await fetch(
            `${API}/api/learn?topic=${encodeURIComponent(topic)}`
        );

        const text = await response.text();

        console.log("API response:", text);

        if (!response.ok) {
            throw new Error(text);
        }

        let data;

        try {
            data = JSON.parse(text);
        } catch (error) {
            throw new Error(
                "Server returned HTML instead of JSON. Check Flask routes."
            );
        }

        result.innerHTML = `
            <span class="section-label">AI EXPLANATION</span>

            <h3>${data.topic}</h3>

            <div class="ai-answer">
                ${formatText(data.explanation)}
            </div>

            <small>
                Grounded in company SOP • Retrieval score: ${data.source_score}
            </small>
        `;

    } catch (error) {

        console.error("Learn error:", error);

        result.innerHTML = `
            <span class="section-label">ERROR</span>

            <h3>Unable to load this topic</h3>

            <p>${error.message}</p>
        `;
    }
}


function formatExplanation(text) {

    if (!text) {
        return "<p>No explanation returned.</p>";
    }

    const lines = text.split("\n");

    let html = "";

    let listStarted = false;

    lines.forEach(line => {

        const clean = line.trim();

        if (!clean) {
            return;
        }

        if (clean.startsWith("-") || clean.startsWith("*")) {

            if (!listStarted) {
                html += "<ul>";
                listStarted = true;
            }

            html += `<li>${escapeHtml(clean.substring(1).trim())}</li>`;

        } else {

            if (listStarted) {
                html += "</ul>";
                listStarted = false;
            }

            html += `<p>${escapeHtml(clean)}</p>`;
        }
    });

    if (listStarted) {
        html += "</ul>";
    }

    return html;
}


// -----------------------------
// QUIZ
// -----------------------------

async function loadQuiz() {

    const input = document.getElementById("quiz-topic");

    const topic = input.value.trim();

    if (!topic) {
        alert("Enter a topic first.");
        return;
    }

    const container = document.getElementById("quiz-container");

    container.innerHTML = `
        <div class="card">
            <p>Generating a grounded assessment...</p>
        </div>
    `;

    try {

        const response = await fetch(
            `${API}/api/quiz?topic=${encodeURIComponent(topic)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to generate quiz");
        }

        currentQuiz = data;

        selectedAnswers = {};

        renderQuiz(data);

    } catch (error) {

        container.innerHTML = `
            <div class="card">
                <h3>Quiz could not be loaded</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}


function renderQuiz(data) {

    const container = document.getElementById("quiz-container");

    const questions = data.quiz.questions;

    let html = `
        <div class="card quiz-card">

            <div class="card-header">

                <div>
                    <span class="section-label">
                        GROUNDED ASSESSMENT
                    </span>

                    <h3>${formatTopic(data.topic)}</h3>
                </div>

                <span class="topic-icon">
                    ✓
                </span>

            </div>
    `;

    questions.forEach((question, index) => {

        html += `
            <div class="quiz-question">

                <h3>
                    ${index + 1}. ${escapeHtml(question.question)}
                </h3>
        `;

        question.options.forEach(option => {

            html += `
                <button
                    class="option"
                    id="option-${index}-${encodeURIComponent(option)}"
                    onclick="selectAnswer(${index}, '${escapeJs(option)}')">

                    ${escapeHtml(option)}

                </button>
            `;
        });

        html += `</div>`;
    });

    html += `
            <button class="primary-btn"
                    onclick="submitQuiz()">
                Submit Assessment →
            </button>

        </div>
    `;

    container.innerHTML = html;
}


function selectAnswer(questionIndex, answer) {

    selectedAnswers[questionIndex] = answer;

    const questionButtons =
        document.querySelectorAll(
            `.quiz-question:nth-of-type(${questionIndex + 2}) .option`
        );

    questionButtons.forEach(button => {
        button.classList.remove("selected");
    });

    event.currentTarget.classList.add("selected");
}


async function submitQuiz() {

    if (!currentQuiz) {
        return;
    }

    const questions = currentQuiz.quiz.questions;

    const answers = [];

    for (let i = 0; i < questions.length; i++) {

        if (selectedAnswers[i] === undefined) {

            alert(
                `Please answer question ${i + 1} before submitting.`
            );

            return;
        }

        answers.push(selectedAnswers[i]);
    }

    const container = document.getElementById("quiz-container");

    try {

        const response = await fetch(
            `${API}/api/submit-quiz`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    employee: "Alex",
                    topic: currentQuiz.topic,
                    questions: questions,
                    answers: answers
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Submission failed");
        }

        showQuizResult(data);

        await loadProgress();

    } catch (error) {

        alert(error.message);
    }
}


function showQuizResult(data) {

    const container = document.getElementById("quiz-container");

    const recommendation =
        data.recommendation;

    container.innerHTML += `
        <div class="quiz-result">

            <span class="section-label"
                  style="color:#c9df69;">
                ASSESSMENT COMPLETE
            </span>

            <div style="margin-top:8px;">
                <strong>${data.score}%</strong>
            </div>

            <p>
                ${escapeHtml(recommendation.reason)}
            </p>

            <p>
                <b>Next:</b>
                ${formatTopic(recommendation.recommendation)}
            </p>

        </div>
    `;
}


// -----------------------------
// PROGRESS
// -----------------------------

function renderProgress(data) {

    const container =
        document.getElementById("progress-container");

    const progress = data.progress || {};

    const topics = Object.keys(progress);

    if (topics.length === 0) {

        container.innerHTML = `
            <div class="card">
                <h3>No assessments yet</h3>
                <p style="margin-top:8px;color:#6e7772;">
                    Complete your first assessment to begin
                    tracking your onboarding journey.
                </p>
            </div>
        `;

        return;
    }

    let html = "";

    topics.forEach(topic => {

        const item = progress[topic];

        html += `
            <div class="card progress-item">

                <div>

                    <div class="progress-topic">
                        ${formatTopic(topic)}
                    </div>

                    <div class="progress-bar">
                        <div
                            class="progress-fill"
                            style="width:${item.score}%">
                        </div>
                    </div>

                </div>

                <div style="text-align:right;">

                    <div class="progress-score">
                        ${item.score}%
                    </div>

                    <span class="progress-status">
                        ${item.status}
                    </span>

                </div>

            </div>
        `;
    });

    if (data.weak_areas?.length) {

        html += `
            <div class="card"
                 style="border-left:4px solid #e79555;">

                <span class="section-label">
                    ADAPTIVE SIGNAL
                </span>

                <h3 style="margin-top:7px;">
                    Reinforcement recommended
                </h3>

                <p style="margin-top:8px;color:#6e7772;font-size:11px;">
                    ${data.weak_areas
                        .map(formatTopic)
                        .join(", ")}
                    ${data.weak_areas.length === 1
                        ? " needs"
                        : " need"}
                    more practice.
                </p>

            </div>
        `;
    }

    container.innerHTML = html;
}


// -----------------------------
// HELPERS
// -----------------------------

function formatTopic(topic) {

    if (!topic) {
        return "";
    }

    return topic
        .replaceAll("_", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function escapeJs(value) {

    return String(value)
        .replaceAll("\\", "\\\\")
        .replaceAll("'", "\\'");
}


// -----------------------------
// INITIAL LOAD
// -----------------------------

document.addEventListener("DOMContentLoaded", () => {

    loadProgress();

});

function formatText(text) {

    return text
        .replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}