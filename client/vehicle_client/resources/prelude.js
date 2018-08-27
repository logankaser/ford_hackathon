"use strict";

/* prelude.js Javascript's missing prelude */

function $(a) {
	if (/^f/.test(typeof a)) {
		document.addEventListener("DOMContentLoaded", a);
	} else {
		return document[{
		'#': "getElementById",
		'.': "getElementsByClassName",
		'@': "getElementsByName",
		'=': "getElementsByTagName",
		$: "createElement"}[a[0]]
		|| 'querySelectorAll'](a.slice(1));
	}
};

/* Returns an object where obj[cookiename] == cookievalue */
$.cookies = function(r,c,i) {
	r = document.cookie.split(/ ;| ,|=/);
	c = {};
	for (i=0;++i < r.length;) {
		c[r[i - 1]] = r[i];
	}
	return c;
};

/* Takes (cookie_name), Returns a cookie or null */
$.cookie = n => {
	n = document.cookie.match(RegExp('(?:^|;\\s*)' + n + '=([^;]*)'));
	return n ? n[1] : null;
};

/*
** Retrieve a network resource. Takes (url, type, callback),
** the callback is passed the response.
*/
$.get = function(u,t,c,r) {
	r = new XMLHttpRequest();
	r.open("GET", u);
	r.responseType = t;
	if (c)
		r.onreadystatechange = () => {
			if(r.readyState > 3)
				c(t == "json" && r.responseType !== t ? JSON.parse(r.response) : r.response)
		};
	r.send();
};

/*
** Post to a URL, Takes (url, type, data, callback)
** Callback is optional, it is passed the request object,
** and called when the request is done.
*/
$.post = function(u,t,d,c,r) {
	r = new XMLHttpRequest();
	r.open("POST", u);
	r.setRequestHeader("Content-Type", t);
	if (c)
		r.onreadystatechange = () => {
			if(r.readyState > 3)
				c(t == "json" && r.responseType !== t ? JSON.parse(r.response) : r.response)
		};
	r.send(d);
};
