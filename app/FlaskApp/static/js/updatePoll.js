const updatePoll = poll_id => {
    const pollView = `${window.origin}/api/1.0/poll/${poll_id}?token=${cookiesObj.authenticated}`;
    fetch(pollView).then(response => {
        if (response.status >= 400){
            return response.json().then(respError => {
                let error = respError.message;
                throw error;
            });
        }
        return response.json().then(responseBody => {
            const pollData = responseBody.poll;
            const updateForm = document.forms[0];
            const textArea = updateForm.querySelector('textarea');
            const options = updateForm.querySelector('#options-container div#options');
            const newOptions = options.cloneNode(false);
            const optionsRow = document.createElement('div');
            const pollStarts = updateForm.querySelector('input#start_date');
            const pollEnds = updateForm.querySelector('input#end_date');
            const guests = updateForm.querySelector('#guests');
            // const email = updateForm.querySelector('#email');
            const submitbtn = updateForm.querySelector('input[type=submit]');
            textArea.textContent = pollData.title;
            pollStarts.setAttribute('value', pollData.formated_dates.starts);
            pollEnds.setAttribute('value', pollData.formated_dates.ends);
            guests.checked = pollData.settings['guestsAllowed'] ? true : false;
            // email.setAttribute('value', pollData.user_email);
            submitbtn.setAttribute('value', 'Update');
            optionsRow.className = 'row';
            optionsRow.setAttribute('id', 'row');
            let option_id = 1;
            pollData.options.forEach(option => {
                const optionWrapper = document.createElement('div');
                optionWrapper.classList.add('col-8', 'mb-2', 'ml-2');
                const optionInput = document.createElement('input');
                optionInput.setAttribute('id', `option${option_id}`);
                optionInput.setAttribute('name', `option${option_id}`);
                optionInput.setAttribute('type', 'text');
                optionInput.classList.add('form-control', 'form-control-md');
                optionInput.setAttribute('value', option);
                if (option_id > 2){
                    const deleteNewOptionCol = document.createElement('div');
                    const deleteNewOption = document.createElement('button');
                    deleteNewOption.classList.add('btn', 'btn-danger');
                    deleteNewOption.textContent = 'X';
                    deleteNewOption.addEventListener('click', event => {
                        event.preventDefault();
                    });
                    deleteNewOptionCol.classList.add('col-2');
                    deleteNewOptionCol.setAttribute('id', 'delete-option-btn');
                    deleteNewOptionCol.appendChild(deleteNewOption);
                    optionWrapper.appendChild(optionInput);
                    optionsRow.appendChild(optionWrapper);
                    optionsRow.appendChild(deleteNewOptionCol);
                }
                else{
                    optionWrapper.appendChild(optionInput);
                    optionsRow.appendChild(optionWrapper);
                }
                option_id += 1;
            });
            newOptions.appendChild(optionsRow);
            options.innerHTML = newOptions.innerHTML;
        }).catch(respError => {
            console.log(respError);
        });
    });
    addOptions();
    const updateForm = document.forms[0];
    updateForm.addEventListener('submit', event => {
        event.preventDefault();
        const pollTitle = event.target.querySelector('#title');
        const pollField = event.target.querySelector('fieldset');
        const optionsFields = pollField.querySelectorAll('div#options input');
        const startDate = pollField.querySelector('input#start_date');
        const endDate = pollField.querySelector('input#end_date');
        const allowGuests = pollField.querySelector('input#guests').checked;
        let options = []
        Array.from(optionsFields).forEach(item => {
            options.push(item.value);
        });
        const postedData = {
            title : pollTitle.value,
            options : options,
            start_date : startDate.value,
            end_date : endDate.value,
            guestsAllowed : allowGuests
        }
        return fetch(`${window.origin}/api/1.0/poll/${poll_id}`, {
            method: 'PUT',
            body: JSON.stringify({ token: cookiesObj.authenticated, ...postedData }),
            headers: new Headers({'content-type': 'application/json'})
        }).then(response => {
            if (response.status >= 400){
                return response.json().then(respError => {
                    let err = respError;
                    throw err;
                });
            }
            return response.json().then(respBody => {
                console.log(respBody);
                window.location.replace(`${window.origin}/${poll_id}/admin`);

            });
        }).catch(respError => {
            if (respError.status == 'date_error'){
                startDate.classList.add('is-invalid');
                endDate.classList.add('is-invalid');
                console.log(startDate);
            }
            if (respError.status == 'fields_error'){
                respError.fields.forEach(field => {
                    if (field !== 'options'){
                        console.log(field);
                        updateForm.querySelector(`#${field}`).classList.add('is-invalid');
                    }
                });
            }
            console.log(respError);
        });
    });
}