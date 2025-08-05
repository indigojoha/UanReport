if (sessionStorage.getItem('secretUserID') === null || sessionStorage.getItem('secretUserID') === '') {
	window.location.href = "../login/index.html";
}
