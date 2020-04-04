"use strict";
const post = async (action, body) => {
	if (!action)
		return;
	if (body) {
		await fetch(action, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(body),
		});
		return;
	}
	await fetch(action, { method: 'POST' });
}
const get = async (action) => {
	const res = await fetch(action);
	if (res.ok)
		return await res.json();
	else
		return null;
}
String.prototype.getWithQueryParam = function (key, value) {
	const delemeterChar = this.indexOf('?') > 0 ? '&' : '?';
	return `${this}${delemeterChar}${key}=${value}`;
}
