"use strict";
(() => {
	function get(node, attr) {
		const value = node.getAttribute(attr);
		return value === null ? "" : value;
	};
	function makeListener(m, attrs) {
		for (var i = attrs.length - 1; i >= 0; --i)
			if (attrs[i] in m.dataset)
				m.dataset[attrs[i]] = m.dataset[attrs[i]].replace(/\.\./g, get(m, attrs[i]));
		return () => {
			for (var i = 0; i < attrs.length; ++i) {
				if (!(attrs[i] in m.dataset)) {
					if (m.hasAttribute(attrs[i])) m.removeAttribute(attrs[i]);
					else m.setAttribute(attrs[i], "");
					continue;
				}
				const tmp = m.dataset[attrs[i]];
				m.dataset[attrs[i]] = get(m, attrs[i]);
				m.setAttribute(attrs[i], tmp);
			}
		};
	}
	const nerves = [].slice.call(document.querySelectorAll("[data-nerve]"));
	for (var i = nerves.length - 1; i >= 0; --i) {
		const strand = nerves[i].dataset["nerve"];
		const muscles = [].slice.call(document.querySelectorAll("[data-" + strand + "]"));
		for (var j = muscles.length - 1; j >= 0; --j) {
			const attributes = muscles[j].dataset[strand].split(",");
			nerves[i].addEventListener("click", makeListener(muscles[j], attributes));
		}
	}
})();
