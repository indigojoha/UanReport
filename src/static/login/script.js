function submitForm(userid) {
	fetch('/api/try_login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ userid: userid })
	})
	.then(response => response.json())
	.then(data => {
		username = data.name;
		rights = data.rights;
		if (rights === -1) {
			sessionStorage.removeItem('secretUserID');
			sessionStorage.removeItem('username');
			sessionStorage.removeItem('rights');
			sessionStorage.setItem('loginError', 'Invalid User ID');
			location.reload();
		} else {
			sessionStorage.setItem('secretUserID', userid);
			sessionStorage.setItem('username', username);
			sessionStorage.setItem('rights', rights);
			window.location.href = '../dashboard/index.html';
		}
	})
}

if (sessionStorage.getItem('loginError') !== null) {
	document.querySelector('.error-text').style.display = 'block';
	document.querySelector('.error-text').textContent = sessionStorage.getItem('loginError');
	sessionStorage.removeItem('loginError');
}

autologinArg = new URLSearchParams(window.location.search).get('autologin');
if (autologinArg) {
	submitForm(autologinArg);
}
