"use strict";

document.addEventListener('DOMContentLoaded', function () {
	const buttons = Array.from(document.getElementsByTagName('button'));

	buttons.forEach((button) => button.onclick = onCLick);
});

String.prototype.replaceAll = function (search, replace) {
	return this.split(search).join(replace);
}

function onCLick() {
	const action = this.getAttribute('data-action');
	if (action) {
		post(action);
		return;
	}

	const cmd = this.getAttribute('data-cmd');
	if (cmd) {
		post('/cmd/' + cmd);
		return;
	}

	const keys = this.getAttribute('data-keys');
	if (!keys) {
		return;
	}
	let repeat = this.getAttribute('data-repeat');
	let keys_sets;
	if (repeat !== null) {
		keys_sets = (keys + ',').repeat(repeat).split(',');
	}
	else {
		keys_sets = [keys];
	}
	keys_sets.forEach((keys) => {
		const action = `/press?keys=${keys.replaceAll('+', '%2B')}`;
		post(action);
	});
}

function post(action) {
	if (!action)
		return;

	const requests = new XMLHttpRequest();
	requests.open("POST", action);
	requests.send();
}