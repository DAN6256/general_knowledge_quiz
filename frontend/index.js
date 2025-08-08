const BASE_URL = "https://general-knowledge-quiz-rvb4.onrender.com";
let currentQuestion = null;

async function fetchData(endpoint) {
    const response = await fetch(`${BASE_URL}/${endpoint}`);
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    return response.json();
}

async function spinQuestion() {
    try {
        const questionData = await fetchData("question/random");
        console.log("Fetched question:", questionData);

        if (!questionData || !questionData.question) {
            throw new Error("Invalid question format");
        }

        currentQuestion = questionData;

        // Hide the main spin button
        const spinButton = document.querySelector(".spin-button");
        spinButton.style.display = "none";

        // Show the quiz container
        const quizContainer = document.getElementById("quiz-container");
        quizContainer.style.display = "block";

        // Display the question
        const questionText = document.getElementById("question-text");
        questionText.innerText = questionData.question;
        questionText.style.display = "block";

        // Hide previous answer
        const answerText = document.getElementById("answer-text");
        answerText.innerText = "";
        answerText.style.display = "none";
    } catch (error) {
        alert("Error fetching question.");
        console.error(error);
    }
}

function showAnswer() {
    if (currentQuestion && currentQuestion.answer) {
        const answerDiv = document.getElementById("answer-text");
        answerDiv.innerText = currentQuestion.answer;
        answerDiv.style.display = "block";
    }
}

function resetForNewQuestion() {
    // Hide the quiz container
    const quizContainer = document.getElementById("quiz-container");
    quizContainer.style.display = "none";
    
    // Show the main spin button again
    const spinButton = document.querySelector(".spin-button");
    spinButton.style.display = "block";
    
    // Clear current question
    currentQuestion = null;
}