
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

    console.log('Cookie Value for', name, ':', cookieValue); // DEBUG
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed'); // DEBUG
    console.log('exercise js loaded'); // DEBUG
    const submitButton = document.getElementById('submit');
    const resultArea = document.getElementById('result-area');
    const exerciseIsTest = submitButton.getAttribute('exercise-is-test') === 'true';
    const exerciseId = submitButton.getAttribute('exercise-id');
    const csrftoken = getCookie('csrftoken');

    if (!submitButton) {
        console.error('Submit button not found!'); // DEBUG
        return;
    }
    console.log('Exercise is a test:', exerciseIsTest);
    console.log('Exercise ID:', exerciseId);
    console.log('CSRF Token:', csrftoken);

    submitButton.addEventListener('click', function (event) {
        event.preventDefault();

        const url = exerciseIsTest ? `/exercises/api/submit_test/${exerciseId}/` : `/exercises/api/submit_code/${exerciseId}/`;
        console.log('Submitting to URL:', url); // DEBUG
        let data = {};

        if (exerciseIsTest) {
            let answers = {};
            document.querySelectorAll('[name^="name_answer_"]').forEach(input => {
                answers[input.name] = input.checked;
            });
            data['answer'] = answers;
            console.log('Test answers:', answers); // DEBUG
        } else {
            const codeArea = document.querySelector('.task-area');
            data['answer'] = codeArea.value;
            console.log('Code answer:', codeArea.value); // DEBUG
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                console.log('Response received'); // DEBUG
                return response.json();
            })
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
