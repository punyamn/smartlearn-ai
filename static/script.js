function checkAnswer(selectedButton) {
    const quizItem = selectedButton.closest('.quiz-item');
    const correctAnswer = quizItem.getAttribute('data-correct').trim();
    const selectedText = selectedButton.textContent.trim();
    const feedbackText = quizItem.querySelector('.feedback-text');
    const allButtons = quizItem.querySelectorAll('.option-btn');

    allButtons.forEach(btn => btn.disabled = true);

    if (selectedText === correctAnswer) {
        selectedButton.classList.add('correct');
        feedbackText.textContent = "✅ Correct Answer!";
        feedbackText.className = "feedback-text text-correct";
    } else {
        selectedButton.classList.add('wrong');
        feedbackText.textContent = `❌ Incorrect. Correct answer: "${correctAnswer}"`;
        feedbackText.className = "feedback-text text-wrong";
        
        allButtons.forEach(btn => {
            if (btn.textContent.trim() === correctAnswer) {
                btn.classList.add('correct');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('notesForm');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', () => {
            submitBtn.textContent = "⏳ Generating AI Quiz...";
            submitBtn.style.opacity = "0.7";
            submitBtn.disabled = true;
        });
    }
});