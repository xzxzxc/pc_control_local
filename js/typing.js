"use strict";
class Typer {
	constructor(inputEl, makeActionFunc, interval) {
		this.prevVal = '';
		inputEl.addEventListener("keydown", e => {
			if (e.keyCode === 13) {
				this.prevVal = e.srcElement.value = '';
				e.srcElement.blur();
			}
			else if (e.keyCode === 8 && !e.srcElement.value) {
				this.prevVal += '1'; // to send deleted count
			}
		});
		const getDeletedCount = (prevStr, newStr) => {
			if (!prevStr)
				return 0;
			if (!newStr)
				return prevStr.length;
			if (prevStr === newStr)
				return 0;
			for (let curIndex = 0; curIndex < prevStr.length; curIndex++) {
				if (prevStr[curIndex] !== newStr[curIndex]) {
					return prevStr.length - curIndex;
				}
			}
			return 0;
		}
		const dispatchFunc = async (container, startTime, inputEl, getDeletedCount, makeActionFunc) => {
			const newStr = inputEl.value;
			const prevStr = container.prevVal;
			const deletedCount = getDeletedCount(prevStr, newStr);
			container.prevVal = newStr;

			const typedStr = newStr.substring(prevStr.length - deletedCount);
			if (makeActionFunc.constructor.name === "AsyncFunction")
				await makeActionFunc(deletedCount, typedStr);
			else
				makeActionFunc(deletedCount, typedStr);
		}
		Dispatcher.registerModule(this, dispatchFunc, interval, inputEl, getDeletedCount, makeActionFunc)
	}
}
