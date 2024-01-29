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

    // codeEditor.setSize("100%", "100%");



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

    // Ensure this is after the CodeMirror instance has been created
    const cmResizeHandle = document.createElement('div');
    cmResizeHandle.className = 'codemirror-resize';
    codeEditor.getWrapperElement().appendChild(cmResizeHandle);
    let isResizing = false;

    cmResizeHandle.addEventListener('mousedown', function (e) {
        isResizing = true;
        let startY = e.clientY;
        let startHeight = codeEditor.getWrapperElement().offsetHeight;

        function doDrag(e) {
            if (isResizing) {
                const newHeight = startHeight + e.clientY - startY;
                codeEditor.setSize(null, newHeight + 'px');
            }
        }

        function stopDrag(e) {
            isResizing = false;
            document.documentElement.removeEventListener('mousemove', doDrag, false);
            document.documentElement.removeEventListener('mouseup', stopDrag, false);
        }

        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
    });

});
