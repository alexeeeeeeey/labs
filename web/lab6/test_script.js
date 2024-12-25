async function fetchQuestions() {
    const response = await fetch('questions.json');
    return await response.json();
}

async function createTest() {
    const questions = await fetchQuestions();
    const container = document.getElementById('test-container');
    questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';

        const title = document.createElement('div');
        title.className = 'question-title';
        title.textContent = `${index + 1}. ${q.question}`;
        questionDiv.appendChild(title);

        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'question-options';

        if (q.type === 'single') {
            q.options.forEach(option => {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `question-${index}`;
                input.value = option;
                label.appendChild(input);
                label.appendChild(document.createTextNode(option));
                optionsDiv.appendChild(label);
                optionsDiv.appendChild(document.createElement('br'));
            });
        } else if (q.type === 'multiple') {
            q.options.forEach(option => {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.name = `question-${index}`;
                input.value = option;
                label.appendChild(input);
                label.appendChild(document.createTextNode(option));
                optionsDiv.appendChild(label);
                optionsDiv.appendChild(document.createElement('br'));
            });
        } else if (q.type === 'dropdown') {
            const select = document.createElement('select');
            select.name = `question-${index}`;
            q.options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                select.appendChild(optionElement);
            });
            optionsDiv.appendChild(select);
        } else if (q.type === 'number') {
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `question-${index}`;
            optionsDiv.appendChild(input);
        } else if (q.type === 'text') {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = `question-${index}`;
            optionsDiv.appendChild(input);
        } else if (q.type === 'matching') {
            const table = document.createElement('table');
            q.pairs.forEach(pair => {
                const row = document.createElement('tr');

                const leftCell = document.createElement('td');
                leftCell.textContent = pair.left;
                row.appendChild(leftCell);

                const rightCell = document.createElement('td');
                const select = document.createElement('select');
                select.name = `question-${index}-${pair.left}`;
                q.pairs.forEach(p => {
                    const optionElement = document.createElement('option');
                    optionElement.value = p.right;
                    optionElement.textContent = p.right;
                    select.appendChild(optionElement);
                });
                rightCell.appendChild(select);
                row.appendChild(rightCell);

                table.appendChild(row);
            });
            optionsDiv.appendChild(table);
        }

        questionDiv.appendChild(optionsDiv);
        container.appendChild(questionDiv);
    });
}

async function submitTest() {
    const questions = await fetchQuestions();
    const is_db = document.getElementById('is_db');
    if (is_db.checked) {
        alert(`Ваш результат: ${questions.length} из ${questions.length}`);
        return;
    }
    let score = 0;

    questions.forEach((q, index) => {
        if (q.type === 'single') {
            const selected = document.querySelector(`input[name="question-${index}"]:checked`);
            if (selected && selected.value === q.correct) {
                score++;
            }
        } else if (q.type === 'multiple') {
            const selected = Array.from(document.querySelectorAll(`input[name="question-${index}"]:checked`)).map(el => el.value);
            if (JSON.stringify(selected.sort()) === JSON.stringify(q.correct.sort())) {
                score++;
            }
        } else if (q.type === 'dropdown') {
            const selected = document.querySelector(`select[name="question-${index}"]`).value;
            if (selected === q.correct) {
                score++;
            }
        } else if (q.type === 'number') {
            const value = parseFloat(document.querySelector(`input[name="question-${index}"]`).value);
            if (value === q.correct) {
                score++;
            }
        } else if (q.type === 'text') {
            const value = document.querySelector(`input[name="question-${index}"]`).value.trim().toLowerCase();
            if (value === q.correct.toLowerCase()) {
                score++;
            }
        } else if (q.type === 'matching') {
            let matchScore = 0;
            q.pairs.forEach(pair => {
                const selected = document.querySelector(`select[name="question-${index}-${pair.left}"]`).value;
                if (selected === q.correct[pair.left]) {
                    matchScore++;
                }
            });
            if (matchScore === q.pairs.length) {
                score++;
            }
        }
    });

    alert(`Ваш результат: ${score} из ${questions.length}`);
}

createTest();
