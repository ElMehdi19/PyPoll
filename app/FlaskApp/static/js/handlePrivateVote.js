const handlePrivateVote = (poll_id, csrf) => {
    const ballot_wrapper = document.querySelector('#voting-ballot');
    ballot_wrapper.style.display = 'block';
    const public_form = document.forms['public-form'];
    public_form.addEventListener('submit', event => {
        event.preventDefault();
        const public_token = public_form.querySelector('#public-token').value;
        const baseapi = `http://127.0.0.1:5000/api/1.0/vote/${poll_id}?token=${public_token}`;
        return fetch(baseapi).then(response => {
            if (response.status >= 400){
                return response.json().then(responseError => {
                    let error = responseError;
                    throw error;
                });
            }
            return response.json().then(responseBody => {
                event.target.classList.remove('form-inline');
                event.target.classList.add('p-3');
                event.target.innerHTML = '';
                const pollData = responseBody.poll;
                const pollTitle = pollData.poll_title;
                const pollOptions = pollData.poll_options;
                const pollBallot = event.target;
                const ballotTitle = document.querySelector('div#voting-ballot b#poll-vote-title');
                const parent = event.target.parentNode;
                const legend = parent.querySelector('legend');
                const csrf_token = document.createElement('input');
                legend.textContent = legend.textContent.replace('Login to vote', 'Vote');
                csrf_token.setAttribute('type', 'hidden');
                csrf_token.setAttribute('value', csrf);
                csrf_token.setAttribute('id', 'csrf'),
                pollBallot.appendChild(csrf_token);
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
                ballotTitle.style.display = 'block';
                ballotTitle.textContent = pollTitle;
                const submitGroup = document.createElement('div');
                const submitVoteBtn = document.createElement('button');

                submitGroup.classList.add('form-group');
                submitVoteBtn.classList.add('btn', 'btn-primary', 'float-right');
                submitVoteBtn.textContent = 'Vote';

                submitGroup.appendChild(submitVoteBtn);
                pollBallot.appendChild(submitGroup);

                pollBallot.addEventListener('submit', event => {
                    event.preventDefault();
                    const chosenOption = document.querySelector('input[name=option]:checked');
                    if (!chosenOption) return console.log('Please choose an option');
                    return fetch(baseapi, {
                        method: 'PUT',
                        body: JSON.stringify({ token:public_token, vote: chosenOption.value }),
                        headers: new Headers({ 'content-type': 'application/json', 'X-CSRFToken': csrf })
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
        }).catch(responseError => {
            const input = event.target.querySelector('input');
            input.classList.add('is-invalid');
        });
    });
}