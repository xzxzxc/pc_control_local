"use strict";
const post = (action) => {
	if (!action)
		return;
	fetch(action, { method: 'POST' });
}
