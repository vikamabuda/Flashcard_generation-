function startSession() {
    const studentId = document.getElementById("student_id").value;
    
    if (studentId) {
        loadFlashcard(studentId);
    } else {
        alert("Please select a valid student ID.");
    }
}

function loadFlashcard(studentId) {
    fetch(`/flashcard?student_id=${studentId}`)
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById("flashcard").style.display = "none";
                alert(data.message);
            } else {
                document.getElementById("mistake_type").innerText = data.mistake_type;
                document.getElementById("original_sentence").innerText = data.original_sentence;
                document.getElementById("corrected_sentence").innerText = data.corrected_sentence;
                document.getElementById("review_count").innerText = data.review_count;
                document.getElementById("review_btn").setAttribute("data-id", data.id);
                document.getElementById("flashcard").style.display = "block";
            }
        })
        .catch(error => console.error('Error:', error));
}

function reviewFlashcard() {
    const flashcardId = document.getElementById("review_btn").getAttribute("data-id");
    fetch(`/review/${flashcardId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        const studentId = document.getElementById("student_id").value;
        loadFlashcard(studentId);  // Load next flashcard for the same student
    })
    .catch(error => console.error('Error:', error));
}
