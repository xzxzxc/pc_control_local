"use strict";
!function () {
	const dispatchContainer = { dispatched_once: true };
	const clearContainer = (container) => { container.ended = true; }
	const setBtn = (container, btn) => {
		container.action = btn.getAttribute('data-action'); container.cmd = btn.getAttribute('data-cmd');
		container.keys = btn.getAttribute('data-keys'); container.interval = btn.getAttribute('data-interval');
		container.ended = false; container.start = new Date().getTime();
		container.dispatched_once = false;
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
	document.addEventListener('DOMContentLoaded', function () {
		Array.from(document.getElementsByTagName('button'))
			.forEach((button) => {
				button.addEventListener('touchstart', touchStart);
				button.addEventListener('touchend', touchEnd);
				button.addEventListener('touchcancel', touchEnd);
			});
	});
	const suportsRepeats = (act) => act.startsWith('/press?keys');
	const dispathTime = 100, defInterval = 1000;
	const dispatchFunc = ({ container, start_dispatch }) => {
		if (container.ended && container.dispatched_once)
			return;

		const action = getAction(container);
		if (!action)
			return;

		let interval = container.interval;
		interval = interval ? interval : defInterval;
		const diff = start_dispatch - container.start;

		let repeats = 0;
		if (diff > interval) {
			container.start = start_dispatch;
			repeats = Math.floor(diff / interval);
		}
		else if (!container.dispatched_once) {
			repeats = 1;
		}

		if (repeats === 0)
			return;

		container.dispatched_once = true;
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
	const dispather = (container) => {
		const start_dispatch = new Date().getTime();

		try {
			dispatchFunc({ container, start_dispatch });
		}
		catch (error) {
			console.log(error);
		}

		const curDispathTime = dispathTime - (new Date().getTime() - start_dispatch);
		if (curDispathTime <= 3) {
			dispather(container);
			return;
		}
		setTimeout(dispather, curDispathTime, container);
	}
	clearContainer(dispatchContainer);
	dispather(dispatchContainer);
}();
