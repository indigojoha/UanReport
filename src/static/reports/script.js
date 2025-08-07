const container = document.getElementById('container');

// 0 = none; 1 = archive, warn; 2 = archive, warn, suspend; 3 = archive, warn, suspend, ban 
const RIGHTS = sessionStorage.getItem('rights') ? parseInt(sessionStorage.getItem('rights')) : 0;

// there is no in-game chat, so no need for the commented ones 
const reasons = [
	'Inappropriate nickname',
	'Cheating',
	'Cheating > Invalid moves',
	'Cheating > Invalid ability',
	'Cheating > Invalid item',
	// 'Spamming',
	// 'Harassment',
]

const LOCALE = {
	SEE_TEAMS_BUTTON: 'See teams',
	HIDE_TEAMS_BUTTON: 'Hide teams',
	PASS_BUTTON: 'Pass',
	WARN_BUTTON: 'Warn',
	SUSPEND_BUTTON: 'Suspend',
	BAN_BUTTON: 'Ban',
}

parameters = new URLSearchParams(window.location.search);
const VIEWING_RESOLVED = parameters.get('resolved') === 'true' || false;

if (VIEWING_RESOLVED)
	document.getElementById('title-text').textContent = 'Resolved Reports';
else
	document.getElementById('title-text').textContent = 'Unresolved Reports';

function createObject(data) {
	const rusername = data.reporter;

	const dusername = data.reported;

	const obj = document.createElement('div');
	obj.className = 'object';
	obj.textContent = data.date + ' > ' + data.reason;
	if (VIEWING_RESOLVED) {
		switch (data.resolution) {
			case "pass":
				obj.textContent = '[Passed] ' + obj.textContent;
				break;
			case "warn":
				obj.textContent = '[Warned] ' + obj.textContent;
				break;
			case "suspend":
				obj.textContent = '[Suspended (' + data.days + 'd)] ' + obj.textContent;
				break;
			case "ban":
				obj.textContent = '[Banned] ' + obj.textContent;
				break;
			default:
				obj.textContent = '[Unknown resolution] ' + obj.textContent;
				break;
		}
	}

	const dropdown = document.createElement('div');
	dropdown.className = 'dropdown';

	const dropdownText = document.createElement('div');
	dropdownText.className = 'dropdown-text';
	dropdownText.textContent = 'Reporter: ' + rusername + '\nReported: ' + dusername + '\nReason: ' + data.reason;
	if (VIEWING_RESOLVED)
		dropdownText.textContent += '\nResolution: ' + (data.resolution || 'Unknown resolution');

	const seeTeamBtn = document.createElement('button');
	seeTeamBtn.style.marginTop = '36px';
	seeTeamBtn.className = 'see-team-btn';
	seeTeamBtn.textContent = LOCALE.SEE_TEAMS_BUTTON;

	const subDropdown = document.createElement('div');
	subDropdown.className = 'sub-dropdown';
	subDropdown.style.display = 'none';
	subDropdown.textContent = data.teams;

	seeTeamBtn.addEventListener('click', (e) => {
		const currentlyVisible = subDropdown.style.display === 'block';

		if (!currentlyVisible)
			seeTeamBtn.textContent = LOCALE.HIDE_TEAMS_BUTTON;
		else
			seeTeamBtn.textContent = LOCALE.SEE_TEAMS_BUTTON;

		e.stopPropagation();
		subDropdown.style.display = currentlyVisible ? 'none' : 'block';
	});

	const buttonContainer = document.createElement('div');
	buttonContainer.className = 'dropdown-buttons';

	if (!VIEWING_RESOLVED && RIGHTS > 0)
		for (let i = 1; i <= RIGHTS + 1; i++) {
			const btn = document.createElement('button');
			btn.className = 'dropdown-btn';

			if (i === 1) {
				btn.textContent = LOCALE.PASS_BUTTON;
				btn.style.backgroundColor = '#41a841ff'; // green 
			} else if (i === 2) {
				btn.textContent = LOCALE.WARN_BUTTON;
				btn.style.backgroundColor = '#BB9900'; // yellow 
			} else if (i === 3) {
				btn.textContent = LOCALE.SUSPEND_BUTTON;
				btn.style.backgroundColor = '#CC6600'; // orange 
			} else if (i === 4) {
				btn.textContent = LOCALE.BAN_BUTTON;
				btn.style.backgroundColor = '#CC0000'; // red 
			}

			btn.addEventListener('click', (e) => {
				let durationInDays = null;
				if (i === 3)
					durationInDays = 7;

				fetch('/api/take_action?userid=' + sessionStorage.getItem('secretUserID'), {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						reportid: data.reportid,
						action: i - 1,
						extra: {
							days: durationInDays
						}
					})
				})
				.then(response => {
					if (!response.ok) {
						return response.json().then(data => {
							throw new Error('Failed to take action: ' + data.error);
						});
					} else {
						container.removeChild(obj);
						if (container.children.length === 0) {
							document.getElementById('no-reports').style.display = 'block';
						}
					}

					// return response.json();
				});
			});

			buttonContainer.appendChild(btn);
		}

	dropdown.appendChild(dropdownText);
	dropdown.appendChild(seeTeamBtn);
	dropdown.appendChild(buttonContainer);
	dropdown.appendChild(subDropdown);
	dropdown.style.display = 'none';

	obj.appendChild(dropdown);

	obj.addEventListener('click', (e) => {
		if (e.target === obj) {
			const currentlyVisible = dropdown.style.display === 'flex';
			dropdown.style.display = currentlyVisible ? 'none' : 'flex';
			if (currentlyVisible)
			{
				subDropdown.style.display = 'none';
				seeTeamBtn.textContent = LOCALE.SEE_TEAMS_BUTTON;
			}
		}
	});

	container.appendChild(obj);
}

fetch('/api/get_report_list?userid=' + sessionStorage.getItem('secretUserID') + '&resolved=' + VIEWING_RESOLVED)
.then(response => {
	if (!response.ok) {
		throw new Error('Failed to fetch report list');
	}
	return response.json();
})
.then(list => {
	if (list.length === 0) {
		document.getElementById('no-reports').style.display = 'block';
	} else {
		list.forEach(id => {
			fetch(`/api/get_report?userid=${sessionStorage.getItem('secretUserID')}&reportid=${id}&resolved=${VIEWING_RESOLVED}`)
			.then(response => {
				if (!response.ok) {
					return response.json().then(data => {
						throw new Error('Failed to fetch report: ' + data.error);
					});
				}
				return response.json();
			})
			.then(data => {
				createObject(data);
			})
			.catch(error => {
				console.error('Error fetching report:', error);
			});
		});
	}
})
.catch(error => {
	console.error('Error fetching report list:', error);
});

function wipeReports() {
	const okay = window.confirm("Are you sure you want to wipe all reports?");

	if (okay) {
		fetch(`/api/wipe_reports?userid=${sessionStorage.getItem('secretUserID')}&resolved=${VIEWING_RESOLVED}`, {
			method: 'DELETE'
		})
		.then(response => {
			if (!response.ok) {
				return response.json().then(data => {
					throw new Error('Failed to wipe reports: ' + data.error);
				});
			}
			return response.json();
		})
		.then(data => {
			console.log('Reports wiped successfully:', data);
			container.innerHTML = '';
			document.getElementById('no-reports').style.display = 'block';
		})
		.catch(error => {
			console.error('Error wiping reports:', error);
		});
	}
}

function addDummyReport() {
	const dummyData = {
		reporter: 'DummyReporter (696969)',
		reported: 'DummyReported (420420)',
		reason: "Inappropriate nickname",
		date: new Date().toISOString(),
		teams: 'DummyTeam1\n\n\nDummyTeam2'
	};

	fetch('/api/submit_report', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(dummyData)
	});
}
