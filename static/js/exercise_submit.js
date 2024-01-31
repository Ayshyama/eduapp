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


    if (!exerciseIsTest) {
        // Initialize CodeMirror
        codeEditor = CodeMirror.fromTextArea(document.getElementById("task-area"), {
            mode: "python",
            theme: "material",
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true,
            autoCloseBrackets: true,
            extraKeys: {"Tab": "autocomplete"},
            id: 'code-mirror-element'
        });

        // Function to get the background color of CodeMirror
        function getCodeMirrorBackgroundColor() {
            const cmWrapper = codeEditor.getWrapperElement();
            const bgColor = window.getComputedStyle(cmWrapper).backgroundColor;
            return bgColor;
        }

        // Function to set the background color and text color of the result-area textarea based on the selected theme
        function setResultAreaStyles() {
            const resultArea = document.getElementById('result-area');
            const taskCode = document.getElementById('task-code');
            const themeSelector = document.getElementById('theme-selector');
            const selectedTheme = themeSelector.value;

            // Determine the text color based on the selected theme
            let textColor;
            if (selectedTheme === 'idea' || selectedTheme === 'eclipse') {
                textColor = 'black';
            } else {
                textColor = 'var(--text-color)';
            }

            // Set the background color and text color
            const bgColor = getCodeMirrorBackgroundColor();
            resultArea.style.backgroundColor = bgColor;
            resultArea.style.color = textColor;
            taskCode.style.backgroundColor = bgColor;
            taskCode.style.color = textColor;
        }


        // Call the function initially
        setResultAreaStyles();

        // Listen for changes in CodeMirror (e.g., theme changes) and update result-area background color
        codeEditor.on("change", function () {
            setResultAreaStyles();
        });

        // codeEditor.setSize("100%", "100%");
        const themeSelector = document.getElementById('theme-selector');

        // Listen for changes in CodeMirror theme and update result-area styles accordingly
        themeSelector.addEventListener('change', function (event) {
            const newTheme = event.target.value;
            codeEditor.setOption("theme", newTheme);

            loadThemeCSS(newTheme);

            setResultAreaStyles();
        });


        // CodeMirror resize handle
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

        // Функция для динамической загрузки CSS тем
        function loadThemeCSS(themeName) {
            const themeURL = `https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/${themeName}.min.css`;
            if (!document.querySelector(`link[href="${themeURL}"]`)) {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = themeURL;
                document.head.appendChild(link);
            }
        }
    }

    function generateHeartIcons(numHearts) {
        const heartContainer = document.getElementById('heart-container');
        heartContainer.innerHTML = '';

        const userLifeElement = document.getElementById('user-life');

        const heartSvgUrl = userLifeElement.getAttribute('data-heart-svg-url');

        let offset = -12;

        for (let i = 0; i < numHearts; i++) {
            const heartIcon = document.createElement('img');
            heartIcon.src = heartSvgUrl;
            heartIcon.classList.add('heart-icon');
            heartIcon.style.marginLeft = offset + 'px';

            heartIcon.alt = "Heart Icon";
            heartContainer.appendChild(heartIcon);

        }
    }

    const userLifeElement = document.getElementById('user-life');
    const initialLife = parseInt(userLifeElement.getAttribute('data-initial-life'));

    generateHeartIcons(initialLife);

    if (!submitButton) {
        console.error('Submit button not found!');
        return;
    }

    submitButton.addEventListener('click', function (event) {
        event.preventDefault();

        document.getElementById('submitLoading').style.display = 'block';
        document.getElementById('submitText').style.display = 'none';
        submitButton.disabled = true;

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

                // Update the displayed hearts based on user's life count
                generateHeartIcons(userLife);

                if (isCorrect) {
                    resultArea.style.backgroundColor = 'rgba(10,255,30,0.25)';
                } else {
                    resultArea.style.backgroundColor = 'rgba(255,30,10,0.25)';
                }
                resultArea.value = message;

                document.getElementById('submitLoading').style.display = 'none';
                document.getElementById('submitText').style.display = 'block';
                submitButton.disabled = false;
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                document.getElementById('submitLoading').style.display = 'none';
                document.getElementById('submitText').style.display = 'block';
                submitButton.disabled = false;
            });
    });


});
