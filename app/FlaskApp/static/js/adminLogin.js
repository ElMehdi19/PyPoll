const logAdmin = poll_id => {
    const loginForm = document.forms['adminForm'];
    loginForm.addEventListener('submit', event => {
        event.preventDefault();
        const csrf = loginForm.querySelector('#admin-csrf').value;
        const token = loginForm.querySelector('#admin-token').value;
        fetch(`${window.origin}/api/1.0/poll/${poll_id}`, {
            method: 'POST',
            body: JSON.stringify({ token: token }),
            headers: new Headers({ 'content-type': 'application/json', 'X-CSRFToken':csrf })
        })
            .then(response => {
                if (response.status >= 400) {
                    return response.json().then(responseError => {
                        let err = responseError;
                        throw err;
                    })
                }
                return response.json().then(responsBody => {
                    if (responsBody.status === 'success') window.location.replace(`${window.location}/admin`);
                });
            })
            .catch(respErr => {
                const tokenInput = event.target.querySelector('input#admin-token');
                tokenInput.classList.add('is-invalid');
                console.log(respErr);
            });
    });
}