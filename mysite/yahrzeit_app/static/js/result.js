'use strict';

const csrfToken = Cookies.get('csrftoken');


if (document.getElementById('create-acct')) {
    document.getElementById('create-acct').addEventListener('click', () => {
        fetch('api/activate-res', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        }).then((res) => {
            return res.json();
        }).then((resData) => {
            console.log(resData.status);
            window.location.href = '/yahrzeit/create-account-form';
        });
    });


    document.getElementById('login').addEventListener('click', () => {
        fetch('api/activate-res', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        }).then((res) => {
            return res.json();
        }).then((resData) => {
            console.log(resData.status);
            window.location.href = '/yahrzeit/login-form';
        });
    });

} else {
    document.getElementById('save-res').addEventListener('click', () => {
        fetch('api/save-res', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        }).then((res) => {
            return res.json();
        }).then((resData) => {
            console.log(resData.status);
            window.location.href = '/yahrzeit/dashboard';
        });
    });
}
