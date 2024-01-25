let codeEditor; // Global reference to the CodeMirror instance

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('submit');
    const resultArea = document.getElementById('result-area');
    const exerciseIsTest = submitButton.getAttribute('exercise-is-test') === 'true';
    const exerciseId = submitButton.getAttribute('exercise-id');
    const csrftoken = getCookie('csrftoken');

    // Initialize CodeMirror
    codeEditor = CodeMirror.fromTextArea(document.getElementById("task-area"), {
        mode: "python",
        theme: "monokai",
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        autoCloseBrackets: true,
        extraKeys: {"Tab": "autocomplete"}
    });
    codeEditor.setSize("300", "200");

    if (!submitButton) {
        console.error('Submit button not found!');
        return;
    }

    submitButton.addEventListener('click', function (event) {
        event.preventDefault();

        const url = exerciseIsTest ? `/exercises/api/submit_test/${exerciseId}/` : `/exercises/api/submit_code/${exerciseId}/`;
        let data = {};

        if (exerciseIsTest) {
            let answers = {};
            document.querySelectorAll('[name^="name_answer_"]').forEach(input => {
                answers[input.name] = input.checked;
            });
            data['answer'] = answers;
        } else {
            // Update the original textarea value with the CodeMirror content
            const codeArea = document.getElementById("task-area");
            codeArea.value = codeEditor.getValue();
            data['answer'] = codeArea.value;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            const isCorrect = data['is_correct'];
            const message = data['message'];
            const userLife = data['user_life'];
            document.getElementById('user-life').innerText = userLife;
            if (isCorrect) {
                resultArea.style.backgroundColor = 'green';
            } else {
                resultArea.style.backgroundColor = 'red';
            }
            resultArea.value = message;
        })
        .catch(error => {
            console.error('Error during fetch:', error);
        });
    });
});
