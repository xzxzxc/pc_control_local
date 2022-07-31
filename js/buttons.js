"use strict";
!function () {
	const dispatchContainer = { dispatchedOnce: true };
	const clearContainer = (container) => { container.ended = true; }
	const dispathTime = 100, defInterval = 1000, delay = 50;
	const setBtn = (container, btn) => {
		container.action = btn.getAttribute('data-action'); container.cmd = btn.getAttribute('data-cmd');
		container.keys = btn.getAttribute('data-keys'); container.interval = btn.getAttribute('data-interval');
		container.ended = false; container.start = new Date().getTime();
		container.dispatchedOnce = false;
	};
	const getAction = (container) => {
		let action, body;
		if (container.action) {
			action = container.action;
		}
		if (container.cmd) {
			action = '/cmd';
			body = container.cmd;
		}
		if (container.keys) {
			action = `/press`;
			body = container.keys;
		}
		return { action, body };
	}
	const touchStart = function () {
		setBtn(dispatchContainer, this);
	}
	const touchEnd = function () {
		clearContainer(dispatchContainer);
	}
	document.addEventListener('DOMContentLoaded', () => {
		Array.from(document.getElementsByTagName('button'))
			.forEach((button) => {
				button.addEventListener('touchstart', touchStart);
				button.addEventListener('touchend', touchEnd);
				button.addEventListener('touchcancel', touchEnd);
			});
	});
	const suportsRepeats = (act) => act.startsWith('/press?keys');

	const dispatchFunc = async (container, startTime, getAction, suportsRepeats, post) => {
		if (container.ended && container.dispatchedOnce)
			return;
		const { action, body } = getAction(container);
		if (!action)
			return;
		let interval = container.interval;
		interval = interval ? interval : defInterval;
		const diff = startTime - container.start;
		let repeats = 0;
		if (diff > interval) {
			container.start = startTime;
			repeats = Math.floor(diff / interval);
		}
		else if (!container.dispatchedOnce) {
			if (diff > delay)
				repeats = 1;
			else
				repeats = 0;
		}
		if (repeats === 0)
			return;
		container.dispatchedOnce = true;
		if (repeats === 1) {
			await post(action, body);
			return;
		}
		if (suportsRepeats(action)) {
			action = action.getWithQueryParam('repeats', repeats);
			await post(action, body);
		}
		else {
			for (let j = 0; j < repeats; j++) {
				await post(action, body);
			}
		}
	}
	clearContainer(dispatchContainer);
	Dispatcher.registerModule(dispatchContainer, dispatchFunc, dispathTime, getAction, suportsRepeats, post);
}();
