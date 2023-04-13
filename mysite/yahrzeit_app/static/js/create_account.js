'use strict';

document.querySelector('.calculator-form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const retypePassword = document.getElementById('retype-password').value;

    if (password === retypePassword) {
        if (password.match(/[A-Z]/)
            && password.match(/[a-z]/)
            && password.match(/[0-9]/)
            && password.match(/[!@#$%\^&\*\(\)-_=\+\[\]\{\}\\\|;:'"\,<\.>\/\?~`]/)
            && password.length >= 8) {
            const csrfToken = Cookies.get('csrftoken');
            console.log(csrfToken);
            fetch('api/create-account', {
                method: 'POST',
                body: JSON.stringify({
                    'email': email,
                    'password': password,
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            }).then((res) => {
                return res.json()
            }).then((resData) => {
                if (resData.status === 'success') {
                    console.log('success')
                    window.location.href = '/yahrzeit/dashboard';
                } else {
                    alert('That email is already associated with an account');
                }
            });
        } else {
            alert('password doesn\'t meet requirements');
        }
    } else {
        alert('passwords don\'t match');
    }
});