const getPollData = poll_id => {
    const APIVIEW = `${window.origin}/api/1.0/poll/${poll_id}?token=${cookiesObj.authenticated}`;
    return fetch(APIVIEW)
        .then(response => {
            if (response.status > 400) {
                return response.json().then(responseErr => {
                    let err = new Error(responseErr.message);
                    throw err
                });
            }
            return response.json().then(responseBody => {
                const pollData = responseBody.poll;
                const pollWrapper = document.querySelector('div#poll-data');
                const pollTitle = pollWrapper.querySelector('div#poll-header p#description');
                const pollOptions = pollWrapper.querySelector('div#poll-options ul#poll-list');
                const pollStartDate = pollWrapper.querySelector('div#poll-schedule p#poll-start-date');
                const pollEndDate = pollWrapper.querySelector('div#poll-schedule p#poll-end-date');
                const pollSettings = pollWrapper.querySelector('div#poll-settings');
                const pollPublicKey = pollSettings.querySelector('p#poll-public-key');
                const pollLiveDataWrapper = document.querySelector('div#live-data-wrapper')
                const pollLiveData = document.querySelector('div#live-data');
                pollTitle.textContent = pollData.title;
                pollWrapper.style.display = 'block';
                pollData.options.forEach(option => {
                    let optionTag = document.createElement('li');
                    optionTag.textContent = option;
                    pollOptions.appendChild(optionTag);
                });
                pollStartDate.textContent = pollData.start_date;
                pollEndDate.textContent = pollData.end_date;

                Object.keys(pollData.settings).forEach(key => {
                    let setting = pollSettings.querySelector(`p#poll-${key}`);
                    setting.textContent = pollData.settings[key];
                });
                pollPublicKey.textContent = pollData.public_key ? pollData.public_key : 'n/a';
                const numberOfVotes = pollLiveData.querySelector('#number-votes');
                const pollBallot = pollLiveData.querySelector('#poll-ballot');
                numberOfVotes.textContent = pollData.votes;
                pollBallot.textContent = pollData.ballot;
                pollBallot.setAttribute('href', pollData.ballot);
                if (pollData.settings['isLive']) {
                    if (pollData.public_key !== null) {
                        const pollPublicKey = pollLiveData.querySelector('#ballot-public-key');
                        const pollPublicKeyData = document.createElement('b');
                        pollPublicKeyData.textContent = pollData.public_key;
                        pollPublicKey.appendChild(pollPublicKeyData);
                        pollPublicKey.style.display = 'block';
                    }
                    const updateBtn = document.querySelector('#poll-update-btn');
                    updateBtn.parentNode.removeChild(updateBtn);
                    pollLiveDataWrapper.style.display = 'block';
                }
                if (pollData.settings['isCompleted']){
                    return window.location.replace(`${window.origin}/logout?next=${poll_id}`);
                }


            });
        })
        .catch(responseError => {
            console.log(responseError);
        });
    }