// document.addEventListener('DOMContentLoaded', event => {
const addOptions = () => {
    const addOptionButton = document.querySelector('#add-opt-btn');
    let numberOfOptions = 2;
    addOptionButton.addEventListener('click', event => {
        event.preventDefault();
        numberOfOptions += 1;
        const options = event.target.parentNode.querySelector('div#options div#row');
        const optionNode = options.firstElementChild;
        const newOption = optionNode.cloneNode(true)
        const newOptionInput = newOption.querySelector('input');
        const deleteOptionBtn = document.createElement('button');
        const newOptionWrapper = document.createElement('div');
        const newOptionCol = document.createElement('div');
        const deleteOptionBtnCol = document.createElement('div');
        newOptionInput.setAttribute('name', `option${numberOfOptions}`);
        newOptionInput.setAttribute('id', `option${numberOfOptions}`);
        newOptionInput.setAttribute('placeholder', '');
        newOptionInput.setAttribute('value', '');
        newOptionInput.textContent = null;
        deleteOptionBtn.classList.add('btn', 'btn-danger');
        deleteOptionBtn.textContent = 'X';
        newOptionCol.classList.add('col-8', 'mb-2', 'ml-2');
        newOptionCol.appendChild(newOptionInput);
        deleteOptionBtnCol.classList.add('col-2');
        deleteOptionBtnCol.setAttribute('id', 'delete-option-btn');
        deleteOptionBtnCol.appendChild(deleteOptionBtn);
        deleteOptionBtnCol.addEventListener('click', event => {
            event.preventDefault();
            const targetBtn = document.querySelector('div#delete-option-btn');
            const targetInput = event.target.parentNode.previousElementSibling;
            if (targetBtn.nextElementSibling === null) numberOfOptions -= 1;
            targetBtn.parentNode.removeChild(targetBtn);
            targetInput.parentNode.removeChild(targetInput);
        });
        options.appendChild(newOptionCol);
        options.appendChild(deleteOptionBtnCol);
    });
// });
}