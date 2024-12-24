const form = document.getElementById('userForm');
const hobbySelect = document.getElementById('hobbySelect');
const sportsOptions = document.getElementById('sportsOptions');
const customHobby = document.getElementById('customHobby');
const addPhoneButton = document.getElementById('addPhone');
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');
const closeModalButton = document.getElementById('closeModal');
const phoneInput = document.getElementById('phone');
const phoneLabel = document.getElementById('phoneLabel');

hobbySelect.addEventListener('change', () => {
    sportsOptions.classList.add('hidden');
    customHobby.classList.add('hidden');
    
    if (hobbySelect.value === 'спорт') {
        sportsOptions.classList.remove('hidden');
    } else if (hobbySelect.value === 'другое') {
        customHobby.classList.remove('hidden');
    }
});

const formatPhoneNumber = (input) => {
    let value = input.value.replace(/\D/g, '');
    if (value.startsWith('8')) value = value.slice(1);

    const formattedValue = value.replace(/^(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})$/, (_, p1, p2, p3, p4) => {
        return `8${p1 ? `(${p1}` : ''}${p2 ? `)${p2}` : ''}${p3 ? `-${p3}` : ''}${p4 ? `-${p4}` : ''}`;
    });

    input.value = formattedValue;
};

phoneInput.addEventListener('input', (event) => formatPhoneNumber(phoneInput));

addPhoneButton.addEventListener('click', () => {
    const phoneInput = document.createElement('input');
    phoneInput.type = 'tel';
    phoneInput.name = 'another phone';
    phoneInput.required = true;
    phoneInput.addEventListener('input', (event) => formatPhoneNumber(phoneInput)); // Привязка обработки ввода
    phoneLabel.appendChild(phoneInput);
});

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    let output = '';
    for (const [key, value] of formData.entries()) {
        if (value != "") {
            output += `<p><strong>${key}:</strong> ${value}</p>`;
        }
    }
    modalContent.innerHTML = output;
    modal.classList.remove('hidden');
});

closeModalButton.addEventListener('click', () => {
    modal.classList.add('hidden');
});
