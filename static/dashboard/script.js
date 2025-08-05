username = sessionStorage.getItem('username');
if (username.toLowerCase().charAt(username.length - 1) === 's' || username.toLowerCase().charAt(username.length - 1) === 'z')
	username += "'";
else
	username += "'s";

document.getElementById('title-text').textContent = username + " Dashboard";