"use strict"
const Dispatcher = {
	modulesToStart: [],
	startedModules: [],
	documentLoaded: false,
	registerModule: function (container, dispatchFunc, interval, ...args) {
		const dispatcher = async (container, dispatchFunc, interval, args) => {
			const startDispatchTime = new Date().getTime();
			try {
				if (dispatchFunc.constructor.name === "AsyncFunction")
					await dispatchFunc(container, startDispatchTime, ...args);
				else
					dispatchFunc(container, startDispatchTime, ...args);
			}
			catch (error) {
				console.log(error);
			}
			const nextCallInterval = interval - (new Date().getTime() - startDispatchTime);
			if (nextCallInterval <= 3) {
				dispatcher(container, dispatchFunc, interval, args);
				return;
			}
			setTimeout(dispatcher, nextCallInterval, container, dispatchFunc, interval, args);
		}
		const module = { dispatcher, container, dispatchFunc, interval, args };
		if (!!this.documentLoaded) {
			dispatcher(container, dispatchFunc, interval, args);
			this.startedModules.push(module);
		}
		else {
			this.modulesToStart.push(module);
		}
	}
};
document.addEventListener('DOMContentLoaded', () => {
	Dispatcher.documentLoaded = true;
	Dispatcher.modulesToStart.forEach((module) =>
		module.dispatcher(module.container, module.dispatchFunc, module.interval, module.args));
	Dispatcher.startedModules.push(
		...Dispatcher.modulesToStart.splice(0, Dispatcher.modulesToStart.length));
});
