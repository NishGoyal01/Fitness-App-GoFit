document.getElementById('login-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const user_id = document.getElementById('user_id').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            window.location.href = 'dashboard.html';
        }
    });
});

document.getElementById('signup-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const gender = document.getElementById('gender').value;
    const age = document.getElementById('age').value;
    const subscription = document.getElementById('subscription').value;

    fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, gender, age, subscription })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
});
