"use strict";
!function () {
	const dispatchContainer = { dispatchedOnce: true };
	const clearContainer = (container) => { container.ended = true; }
	const setBtn = (container, btn) => {
		container.action = btn.getAttribute('data-action'); container.cmd = btn.getAttribute('data-cmd');
		container.keys = btn.getAttribute('data-keys'); container.interval = btn.getAttribute('data-interval');
		container.ended = false; container.start = new Date().getTime();
		container.dispatchedOnce = false;
	};
	const replaceAll = (str, search, replace) => str.split(search).join(replace);
	const getAction = (container) => {
		if (container.action)
			return container.action;
		if (container.cmd)
			return '/cmd/' + container.cmd;
		if (container.keys)
			return `/press?keys=${replaceAll(container.keys, '+', '%2B')}`;
		return null;
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
	const dispathTime = 100, defInterval = 1000;
	const dispatchFunc = (container, startTime, getAction, suportsRepeats) => {
		if (container.ended && container.dispatchedOnce)
			return;
		const action = getAction(container);
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
			repeats = 1;
		}
		if (repeats === 0)
			return;
		container.dispatchedOnce = true;
		if (repeats === 1) {
			post(action);
			return;
		}
		if (suportsRepeats(action)) {
			post(action + '&repeats=' + repeats);
		}
		else {
			for (let j = 0; j < repeats; j++) {
				post(action);
			}
		}
	}
	clearContainer(dispatchContainer);
	Dispatcher.registerModule(dispatchContainer, dispatchFunc, dispathTime, getAction, suportsRepeats, post);
}();
