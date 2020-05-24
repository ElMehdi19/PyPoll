const sendVote = poll_id => {
    fetch(`${window.origin}/api/1.0/vote/${poll_id}`)
        .then(response => {
            if (response.status >= 400) {
                return response.json().then(respErr => {
                    let error = respErr;
                    throw error;
                })
            }
            return response.json().then(responseBody => {
                const pollData = responseBody.poll;
                const pollTitle = pollData.poll_title;
                const pollOptions = pollData.poll_options;
                const pollBallot = document.querySelector('div#voting-ballot form');
                const ballotTitle = document.querySelector('div#voting-ballot b#poll-vote-title');
                pollOptions.forEach(option => {
                    const optiongroup = document.createElement('div');
                    const optionTag = document.createElement('input');
                    const optionLabel = document.createElement('label');

                    optiongroup.classList.add('form-check');
                    optionTag.setAttribute('type', 'radio');
                    optionTag.setAttribute('name', 'option');
                    optionTag.setAttribute('value', option);
                    optionTag.setAttribute('id', `option${pollOptions.indexOf(option)}`);
                    optionTag.classList.add('form-check-input');

                    optionLabel.setAttribute('for', `option${pollOptions.indexOf(option)}`);
                    optionLabel.classList.add('form-check-label');
                    optionLabel.textContent = option;

                    optiongroup.appendChild(optionTag);
                    optiongroup.appendChild(optionLabel);

                    pollBallot.appendChild(optiongroup);
                });
                ballotTitle.textContent = pollTitle;

                const submitGroup = document.createElement('div');
                const submitVoteBtn = document.createElement('button');

                submitGroup.classList.add('form-group');
                submitVoteBtn.classList.add('btn', 'btn-primary', 'float-right');
                submitVoteBtn.textContent = 'Vote';

                submitGroup.appendChild(submitVoteBtn);
                pollBallot.appendChild(submitGroup);

                pollBallot.parentNode.style.display = 'block';
                pollBallot.addEventListener('submit', event => {
                    event.preventDefault();
                    const csrf = document.querySelector('input#vote-csrf').value;
                    const chosenOption = document.querySelector('input[name=option]:checked');
                    if (!chosenOption) return console.log('Please choose an option');
                    return fetch(`${window.origin}/api/1.0/vote/${poll_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({ vote: chosenOption.value }),
                        headers: new Headers({ 'content-type': 'application/json', 'X-CSRFToken':csrf })
                    })
                        .then(response => {
                            if (response.status >= 400) {
                                return response.json().then(respError => {
                                    let err = respError;
                                    throw err;
                                });
                            }
                            return response.json().then(respBody => {
                                const message = document.createElement('div');
                                message.innerHTML = `Thanks for voting! <br>Visit this page again on 
                                                        <b>${respBody.end_date}</b> to see the results. `;
                                pollBallot.parentNode.classList.remove('card');
                                pollBallot.parentNode.classList.add('alert', 'alert-success');
                                pollBallot.parentNode.innerHTML = message.innerHTML;        
                            });
                        })
                        .catch(respError => {
                            console.log(respError);
                        });
                });
            });
        })
        .catch(responseError => {
            console.log(responseError.message);
        });
}