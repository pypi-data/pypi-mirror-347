var SSR = (() => {
return (function(exports, react_dom_server_edge) {

"use strict";
//#region rolldown:runtime
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJS = (cb, mod) => function() {
	return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
	if (from && typeof from === "object" || typeof from === "function") for (var keys = __getOwnPropNames(from), i = 0, n = keys.length, key; i < n; i++) {
		key = keys[i];
		if (!__hasOwnProp.call(to, key) && key !== except) __defProp(to, key, {
			get: ((k) => from[k]).bind(null, key),
			enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
		});
	}
	return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", {
	value: mod,
	enumerable: true
}) : target, mod));

//#endregion
react_dom_server_edge = __toESM(react_dom_server_edge);

//#region mountaineer_exceptions/views/node_modules/react/cjs/react.production.js
var require_react_production = __commonJS({ "mountaineer_exceptions/views/node_modules/react/cjs/react.production.js"(exports) {
	var REACT_ELEMENT_TYPE$1 = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE$1 = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler"), REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), MAYBE_ITERATOR_SYMBOL = Symbol.iterator;
	function getIteratorFn(maybeIterable) {
		if (null === maybeIterable || "object" !== typeof maybeIterable) return null;
		maybeIterable = MAYBE_ITERATOR_SYMBOL && maybeIterable[MAYBE_ITERATOR_SYMBOL] || maybeIterable["@@iterator"];
		return "function" === typeof maybeIterable ? maybeIterable : null;
	}
	var ReactNoopUpdateQueue = {
		isMounted: function() {
			return !1;
		},
		enqueueForceUpdate: function() {},
		enqueueReplaceState: function() {},
		enqueueSetState: function() {}
	}, assign = Object.assign, emptyObject = {};
	function Component(props, context, updater) {
		this.props = props;
		this.context = context;
		this.refs = emptyObject;
		this.updater = updater || ReactNoopUpdateQueue;
	}
	Component.prototype.isReactComponent = {};
	Component.prototype.setState = function(partialState, callback) {
		if ("object" !== typeof partialState && "function" !== typeof partialState && null != partialState) throw Error("takes an object of state variables to update or a function which returns an object of state variables.");
		this.updater.enqueueSetState(this, partialState, callback, "setState");
	};
	Component.prototype.forceUpdate = function(callback) {
		this.updater.enqueueForceUpdate(this, callback, "forceUpdate");
	};
	function ComponentDummy() {}
	ComponentDummy.prototype = Component.prototype;
	function PureComponent(props, context, updater) {
		this.props = props;
		this.context = context;
		this.refs = emptyObject;
		this.updater = updater || ReactNoopUpdateQueue;
	}
	var pureComponentPrototype = PureComponent.prototype = new ComponentDummy();
	pureComponentPrototype.constructor = PureComponent;
	assign(pureComponentPrototype, Component.prototype);
	pureComponentPrototype.isPureReactComponent = !0;
	var isArrayImpl = Array.isArray, ReactSharedInternals = {
		H: null,
		A: null,
		T: null,
		S: null,
		V: null
	}, hasOwnProperty = Object.prototype.hasOwnProperty;
	function ReactElement(type, key, self, source, owner, props) {
		self = props.ref;
		return {
			$$typeof: REACT_ELEMENT_TYPE$1,
			type,
			key,
			ref: void 0 !== self ? self : null,
			props
		};
	}
	function cloneAndReplaceKey(oldElement, newKey) {
		return ReactElement(oldElement.type, newKey, void 0, void 0, void 0, oldElement.props);
	}
	function isValidElement(object) {
		return "object" === typeof object && null !== object && object.$$typeof === REACT_ELEMENT_TYPE$1;
	}
	function escape(key) {
		var escaperLookup = {
			"=": "=0",
			":": "=2"
		};
		return "$" + key.replace(/[=:]/g, function(match) {
			return escaperLookup[match];
		});
	}
	var userProvidedKeyEscapeRegex = /\/+/g;
	function getElementKey(element, index) {
		return "object" === typeof element && null !== element && null != element.key ? escape("" + element.key) : index.toString(36);
	}
	function noop$1() {}
	function resolveThenable(thenable) {
		switch (thenable.status) {
			case "fulfilled": return thenable.value;
			case "rejected": throw thenable.reason;
			default: switch ("string" === typeof thenable.status ? thenable.then(noop$1, noop$1) : (thenable.status = "pending", thenable.then(function(fulfilledValue) {
				"pending" === thenable.status && (thenable.status = "fulfilled", thenable.value = fulfilledValue);
			}, function(error) {
				"pending" === thenable.status && (thenable.status = "rejected", thenable.reason = error);
			})), thenable.status) {
				case "fulfilled": return thenable.value;
				case "rejected": throw thenable.reason;
			}
		}
		throw thenable;
	}
	function mapIntoArray(children, array, escapedPrefix, nameSoFar, callback) {
		var type = typeof children;
		if ("undefined" === type || "boolean" === type) children = null;
		var invokeCallback = !1;
		if (null === children) invokeCallback = !0;
		else switch (type) {
			case "bigint":
			case "string":
			case "number":
				invokeCallback = !0;
				break;
			case "object": switch (children.$$typeof) {
				case REACT_ELEMENT_TYPE$1:
				case REACT_PORTAL_TYPE:
					invokeCallback = !0;
					break;
				case REACT_LAZY_TYPE: return invokeCallback = children._init, mapIntoArray(invokeCallback(children._payload), array, escapedPrefix, nameSoFar, callback);
			}
		}
		if (invokeCallback) return callback = callback(children), invokeCallback = "" === nameSoFar ? "." + getElementKey(children, 0) : nameSoFar, isArrayImpl(callback) ? (escapedPrefix = "", null != invokeCallback && (escapedPrefix = invokeCallback.replace(userProvidedKeyEscapeRegex, "$&/") + "/"), mapIntoArray(callback, array, escapedPrefix, "", function(c) {
			return c;
		})) : null != callback && (isValidElement(callback) && (callback = cloneAndReplaceKey(callback, escapedPrefix + (null == callback.key || children && children.key === callback.key ? "" : ("" + callback.key).replace(userProvidedKeyEscapeRegex, "$&/") + "/") + invokeCallback)), array.push(callback)), 1;
		invokeCallback = 0;
		var nextNamePrefix = "" === nameSoFar ? "." : nameSoFar + ":";
		if (isArrayImpl(children)) for (var i = 0; i < children.length; i++) nameSoFar = children[i], type = nextNamePrefix + getElementKey(nameSoFar, i), invokeCallback += mapIntoArray(nameSoFar, array, escapedPrefix, type, callback);
		else if (i = getIteratorFn(children), "function" === typeof i) for (children = i.call(children), i = 0; !(nameSoFar = children.next()).done;) nameSoFar = nameSoFar.value, type = nextNamePrefix + getElementKey(nameSoFar, i++), invokeCallback += mapIntoArray(nameSoFar, array, escapedPrefix, type, callback);
		else if ("object" === type) {
			if ("function" === typeof children.then) return mapIntoArray(resolveThenable(children), array, escapedPrefix, nameSoFar, callback);
			array = String(children);
			throw Error("Objects are not valid as a React child (found: " + ("[object Object]" === array ? "object with keys {" + Object.keys(children).join(", ") + "}" : array) + "). If you meant to render a collection of children, use an array instead.");
		}
		return invokeCallback;
	}
	function mapChildren(children, func, context) {
		if (null == children) return children;
		var result = [], count = 0;
		mapIntoArray(children, result, "", "", function(child) {
			return func.call(context, child, count++);
		});
		return result;
	}
	function lazyInitializer(payload) {
		if (-1 === payload._status) {
			var ctor = payload._result;
			ctor = ctor();
			ctor.then(function(moduleObject) {
				if (0 === payload._status || -1 === payload._status) payload._status = 1, payload._result = moduleObject;
			}, function(error) {
				if (0 === payload._status || -1 === payload._status) payload._status = 2, payload._result = error;
			});
			-1 === payload._status && (payload._status = 0, payload._result = ctor);
		}
		if (1 === payload._status) return payload._result.default;
		throw payload._result;
	}
	var reportGlobalError = "function" === typeof reportError ? reportError : function(error) {
		if ("object" === typeof window && "function" === typeof window.ErrorEvent) {
			var event = new window.ErrorEvent("error", {
				bubbles: !0,
				cancelable: !0,
				message: "object" === typeof error && null !== error && "string" === typeof error.message ? String(error.message) : String(error),
				error
			});
			if (!window.dispatchEvent(event)) return;
		} else if ("object" === typeof process && "function" === typeof process.emit) {
			process.emit("uncaughtException", error);
			return;
		}
		console.error(error);
	};
	function noop() {}
	exports.Children = {
		map: mapChildren,
		forEach: function(children, forEachFunc, forEachContext) {
			mapChildren(children, function() {
				forEachFunc.apply(this, arguments);
			}, forEachContext);
		},
		count: function(children) {
			var n = 0;
			mapChildren(children, function() {
				n++;
			});
			return n;
		},
		toArray: function(children) {
			return mapChildren(children, function(child) {
				return child;
			}) || [];
		},
		only: function(children) {
			if (!isValidElement(children)) throw Error("React.Children.only expected to receive a single React element child.");
			return children;
		}
	};
	exports.Component = Component;
	exports.Fragment = REACT_FRAGMENT_TYPE$1;
	exports.Profiler = REACT_PROFILER_TYPE;
	exports.PureComponent = PureComponent;
	exports.StrictMode = REACT_STRICT_MODE_TYPE;
	exports.Suspense = REACT_SUSPENSE_TYPE;
	exports.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = ReactSharedInternals;
	exports.__COMPILER_RUNTIME = {
		__proto__: null,
		c: function(size) {
			return ReactSharedInternals.H.useMemoCache(size);
		}
	};
	exports.cache = function(fn) {
		return function() {
			return fn.apply(null, arguments);
		};
	};
	exports.cloneElement = function(element, config, children) {
		if (null === element || void 0 === element) throw Error("The argument must be a React element, but you passed " + element + ".");
		var props = assign({}, element.props), key = element.key, owner = void 0;
		if (null != config) for (propName in void 0 !== config.ref && (owner = void 0), void 0 !== config.key && (key = "" + config.key), config) !hasOwnProperty.call(config, propName) || "key" === propName || "__self" === propName || "__source" === propName || "ref" === propName && void 0 === config.ref || (props[propName] = config[propName]);
		var propName = arguments.length - 2;
		if (1 === propName) props.children = children;
		else if (1 < propName) {
			for (var childArray = Array(propName), i = 0; i < propName; i++) childArray[i] = arguments[i + 2];
			props.children = childArray;
		}
		return ReactElement(element.type, key, void 0, void 0, owner, props);
	};
	exports.createContext = function(defaultValue) {
		defaultValue = {
			$$typeof: REACT_CONTEXT_TYPE,
			_currentValue: defaultValue,
			_currentValue2: defaultValue,
			_threadCount: 0,
			Provider: null,
			Consumer: null
		};
		defaultValue.Provider = defaultValue;
		defaultValue.Consumer = {
			$$typeof: REACT_CONSUMER_TYPE,
			_context: defaultValue
		};
		return defaultValue;
	};
	exports.createElement = function(type, config, children) {
		var propName, props = {}, key = null;
		if (null != config) for (propName in void 0 !== config.key && (key = "" + config.key), config) hasOwnProperty.call(config, propName) && "key" !== propName && "__self" !== propName && "__source" !== propName && (props[propName] = config[propName]);
		var childrenLength = arguments.length - 2;
		if (1 === childrenLength) props.children = children;
		else if (1 < childrenLength) {
			for (var childArray = Array(childrenLength), i = 0; i < childrenLength; i++) childArray[i] = arguments[i + 2];
			props.children = childArray;
		}
		if (type && type.defaultProps) for (propName in childrenLength = type.defaultProps, childrenLength) void 0 === props[propName] && (props[propName] = childrenLength[propName]);
		return ReactElement(type, key, void 0, void 0, null, props);
	};
	exports.createRef = function() {
		return { current: null };
	};
	exports.forwardRef = function(render) {
		return {
			$$typeof: REACT_FORWARD_REF_TYPE,
			render
		};
	};
	exports.isValidElement = isValidElement;
	exports.lazy = function(ctor) {
		return {
			$$typeof: REACT_LAZY_TYPE,
			_payload: {
				_status: -1,
				_result: ctor
			},
			_init: lazyInitializer
		};
	};
	exports.memo = function(type, compare) {
		return {
			$$typeof: REACT_MEMO_TYPE,
			type,
			compare: void 0 === compare ? null : compare
		};
	};
	exports.startTransition = function(scope) {
		var prevTransition = ReactSharedInternals.T, currentTransition = {};
		ReactSharedInternals.T = currentTransition;
		try {
			var returnValue = scope(), onStartTransitionFinish = ReactSharedInternals.S;
			null !== onStartTransitionFinish && onStartTransitionFinish(currentTransition, returnValue);
			"object" === typeof returnValue && null !== returnValue && "function" === typeof returnValue.then && returnValue.then(noop, reportGlobalError);
		} catch (error) {
			reportGlobalError(error);
		} finally {
			ReactSharedInternals.T = prevTransition;
		}
	};
	exports.unstable_useCacheRefresh = function() {
		return ReactSharedInternals.H.useCacheRefresh();
	};
	exports.use = function(usable) {
		return ReactSharedInternals.H.use(usable);
	};
	exports.useActionState = function(action, initialState, permalink) {
		return ReactSharedInternals.H.useActionState(action, initialState, permalink);
	};
	exports.useCallback = function(callback, deps) {
		return ReactSharedInternals.H.useCallback(callback, deps);
	};
	exports.useContext = function(Context) {
		return ReactSharedInternals.H.useContext(Context);
	};
	exports.useDebugValue = function() {};
	exports.useDeferredValue = function(value, initialValue) {
		return ReactSharedInternals.H.useDeferredValue(value, initialValue);
	};
	exports.useEffect = function(create, createDeps, update) {
		var dispatcher = ReactSharedInternals.H;
		if ("function" === typeof update) throw Error("useEffect CRUD overload is not enabled in this build of React.");
		return dispatcher.useEffect(create, createDeps);
	};
	exports.useId = function() {
		return ReactSharedInternals.H.useId();
	};
	exports.useImperativeHandle = function(ref, create, deps) {
		return ReactSharedInternals.H.useImperativeHandle(ref, create, deps);
	};
	exports.useInsertionEffect = function(create, deps) {
		return ReactSharedInternals.H.useInsertionEffect(create, deps);
	};
	exports.useLayoutEffect = function(create, deps) {
		return ReactSharedInternals.H.useLayoutEffect(create, deps);
	};
	exports.useMemo = function(create, deps) {
		return ReactSharedInternals.H.useMemo(create, deps);
	};
	exports.useOptimistic = function(passthrough, reducer) {
		return ReactSharedInternals.H.useOptimistic(passthrough, reducer);
	};
	exports.useReducer = function(reducer, initialArg, init) {
		return ReactSharedInternals.H.useReducer(reducer, initialArg, init);
	};
	exports.useRef = function(initialValue) {
		return ReactSharedInternals.H.useRef(initialValue);
	};
	exports.useState = function(initialState) {
		return ReactSharedInternals.H.useState(initialState);
	};
	exports.useSyncExternalStore = function(subscribe, getSnapshot, getServerSnapshot) {
		return ReactSharedInternals.H.useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
	};
	exports.useTransition = function() {
		return ReactSharedInternals.H.useTransition();
	};
	exports.version = "19.1.0";
} });

//#endregion
//#region mountaineer_exceptions/views/node_modules/react/index.js
var require_react = __commonJS({ "mountaineer_exceptions/views/node_modules/react/index.js"(exports, module) {
	module.exports = require_react_production();
} });
var import_react = __toESM(require_react());

//#endregion
//#region ../mountaineer/mountaineer/static/live_reload.ts
var ReconnectWebSocket = class {
	ws = null;
	url;
	protocols;
	reconnectInterval = 1e3;
	maxReconnectInterval = 15e3;
	reconnectDecay = 1.5;
	reconnectAttempts = 0;
	forcedClose = false;
	messageQueue = [];
	onopen = null;
	onclose = null;
	onmessage = null;
	onerror = null;
	constructor(url, protocols) {
		this.url = url;
		this.protocols = protocols;
		this.connect(false);
	}
	connect(reconnectAttempt) {
		if (reconnectAttempt) {
			const delay = Math.min(this.reconnectInterval * Math.pow(this.reconnectDecay, this.reconnectAttempts), this.maxReconnectInterval);
			setTimeout(() => this.establishConnection(), delay);
		} else this.establishConnection();
	}
	establishConnection() {
		console.debug("Attempting WebSocket connection...");
		this.ws = new WebSocket(this.url, this.protocols);
		this.ws.onopen = (event) => {
			this.onReconnectSuccess(event);
		};
		this.ws.onmessage = (event) => {
			if (this.onmessage) this.onmessage(event);
		};
		this.ws.onerror = (event) => {
			if (this.onerror) this.onerror(event);
		};
		this.ws.onclose = (event) => {
			this.onReconnectClose(event);
		};
	}
	onReconnectSuccess(event) {
		console.log("WebSocket connected.");
		this.reconnectAttempts = 0;
		if (this.onopen) this.onopen(event);
		this.messageQueue.forEach((message) => this.send(message));
		this.messageQueue = [];
	}
	onReconnectClose(event) {
		this.ws = null;
		if (!this.forcedClose) {
			this.reconnectAttempts++;
			this.connect(true);
		}
		if (this.onclose) this.onclose(event);
	}
	send(data) {
		if (this.ws && this.ws.readyState === WebSocket.OPEN) this.ws.send(data);
		else this.messageQueue.push(data);
	}
	close() {
		if (this.ws) {
			this.forcedClose = true;
			this.ws.close();
		}
	}
	get readyState() {
		return this.ws ? this.ws.readyState : WebSocket.CLOSED;
	}
};
const mountLiveReload = ({ host, port, SSR_RENDERING, NODE_ENV, LIVE_RELOAD_PORT }) => {
	if (SSR_RENDERING === true || NODE_ENV !== "development") return;
	if (!host) host = "localhost";
	if (!port) {
		if (!LIVE_RELOAD_PORT) {
			console.error("process.env.LIVE_RELOAD_PORT is not passed from server to development client.");
			return;
		}
		port = Number(LIVE_RELOAD_PORT);
	}
	(0, import_react.useEffect)(() => {
		console.log("Connecting to live reload server...");
		const ws = new ReconnectWebSocket(`ws://${host}:${port}/build-events`);
		ws.onmessage = () => {
			window.location.reload();
		};
		ws.onerror = (event) => {
			console.error("WebSocket error:", event);
		};
	}, []);
};
var live_reload_default = mountLiveReload;

//#endregion
//#region mountaineer_exceptions/views/node_modules/react/cjs/react-jsx-runtime.production.js
var require_react_jsx_runtime_production = __commonJS({ "mountaineer_exceptions/views/node_modules/react/cjs/react-jsx-runtime.production.js"(exports) {
	var REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment");
	function jsxProd(type, config, maybeKey) {
		var key = null;
		void 0 !== maybeKey && (key = "" + maybeKey);
		void 0 !== config.key && (key = "" + config.key);
		if ("key" in config) {
			maybeKey = {};
			for (var propName in config) "key" !== propName && (maybeKey[propName] = config[propName]);
		} else maybeKey = config;
		config = maybeKey.ref;
		return {
			$$typeof: REACT_ELEMENT_TYPE,
			type,
			key,
			ref: void 0 !== config ? config : null,
			props: maybeKey
		};
	}
	exports.Fragment = REACT_FRAGMENT_TYPE;
	exports.jsx = jsxProd;
	exports.jsxs = jsxProd;
} });

//#endregion
//#region mountaineer_exceptions/views/node_modules/react/jsx-runtime.js
var require_jsx_runtime = __commonJS({ "mountaineer_exceptions/views/node_modules/react/jsx-runtime.js"(exports, module) {
	module.exports = require_react_jsx_runtime_production();
} });
var import_jsx_runtime = __toESM(require_jsx_runtime());

//#endregion
//#region mountaineer_exceptions/views/core/layout.tsx
const Layout = ({ children }) => {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "p-4 bg-zinc-50",
		children
	});
};
var layout_default = Layout;

//#endregion
//#region mountaineer_exceptions/views/_server/api.ts
const convertToUrlString = (value) => {
	if (value === null || value === void 0) return void 0;
	if (value instanceof Date) return value.toISOString();
	return String(value);
};
const processUrlParams = (params) => {
	const searchParams = new ServerURLSearchParams();
	for (const [key, value] of Object.entries(params)) {
		if (value === null || value === void 0) continue;
		if (Array.isArray(value)) value.forEach((item) => {
			const strValue = convertToUrlString(item);
			if (strValue !== void 0) searchParams.append(key, strValue);
		});
		else {
			const strValue = convertToUrlString(value);
			if (strValue !== void 0) searchParams.append(key, strValue);
		}
	}
	return searchParams;
};
const __getLink = (params) => {
	const url = new ServerURL(params.rawUrl);
	for (const [key, value] of Object.entries(params.pathParameters)) {
		const strValue = convertToUrlString(value);
		if (strValue === void 0) throw new Error(`Missing required path parameter ${key}`);
		url.pathname = decodeURIComponent(url.pathname).replace(`{${key}}`, strValue);
	}
	if (params.queryParameters) {
		const searchParams = processUrlParams(params.queryParameters);
		url.search = searchParams.toString();
	}
	return decodeURIComponent(url.toString());
};
var ServerURL = class {
	_protocol = "";
	_host = "";
	_pathname = "";
	_search = "";
	constructor(url, base) {
		if (url.match(/^[a-zA-Z]+:\/\//)) {
			const [protocol, rest] = url.split("://");
			const [host, ...pathParts] = rest.split("/");
			this._protocol = protocol;
			this._host = host;
			this._pathname = "/" + pathParts.join("/");
			return;
		}
		const [pathname, search] = url.split("?");
		if (base && !pathname.startsWith("/")) {
			const baseDir = base.endsWith("/") ? base : base + "/";
			this._pathname = this.normalizePath(baseDir + pathname);
		} else this._pathname = this.normalizePath(pathname);
		this._search = search ? `?${search}` : "";
	}
	normalizePath(path) {
		if (!path.startsWith("/")) path = "/" + path;
		const segments = path.split("/");
		const normalized = [];
		for (const segment of segments) {
			if (!segment || segment === ".") continue;
			if (segment === "..") normalized.pop();
			else normalized.push(segment);
		}
		return "/" + normalized.join("/");
	}
	get pathname() {
		return this._pathname;
	}
	set pathname(value) {
		this._pathname = this.normalizePath(value);
	}
	get search() {
		return this._search;
	}
	set search(value) {
		this._search = value ? value.startsWith("?") ? value : `?${value}` : "";
	}
	toString() {
		if (this._protocol && this._host) return `${this._protocol}://${this._host}${this._pathname}${this._search}`;
		return `${this._pathname}${this._search}`;
	}
};
var ServerURLSearchParams = class {
	params;
	constructor(init) {
		this.params = new Map();
		if (!init) return;
		if (typeof init === "string") {
			const query = init.startsWith("?") ? init.slice(1) : init;
			for (const pair of query.split("&")) {
				if (!pair) continue;
				const [key, value] = pair.split("=").map(decodeURIComponent);
				this.append(key, value ?? "");
			}
		} else for (const [key, value] of Object.entries(init)) if (Array.isArray(value)) for (const v of value) this.append(key, v);
		else this.append(key, value);
	}
	append(key, value) {
		const values = this.params.get(key) || [];
		values.push(String(value));
		this.params.set(key, values);
	}
	toString() {
		const pairs = [];
		for (const [key, values] of this.params) for (const value of values) pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
		return pairs.join("&");
	}
};

//#endregion
//#region mountaineer_exceptions/views/core/exception/_server/links.ts
const getLink = ({ exception, stack }) => {
	const url = `/_exception`;
	const queryParameters = {
		exception,
		stack
	};
	const pathParameters = {};
	return __getLink({
		rawUrl: url,
		queryParameters,
		pathParameters
	});
};

//#endregion
//#region mountaineer_exceptions/views/_server/links.ts
const linkGenerator = { exceptionController: getLink };
var links_default = linkGenerator;

//#endregion
//#region mountaineer_exceptions/views/core/exception/_server/useServer.ts
const useServer = () => {
	const [serverState, setServerState] = (0, import_react.useState)(SERVER_DATA["ExceptionController"]);
	const setControllerState = (payload) => {
		setServerState((state) => ({
			...state,
			...payload
		}));
	};
	return {
		...serverState,
		"linkGenerator": links_default
	};
};

//#endregion
//#region mountaineer_exceptions/views/core/exception/page.tsx
const Page = () => {
	const serverState = useServer();
	const [showFrame, setShowFrame] = (0, import_react.useState)(null);
	const timestamp = new Date().toISOString();
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
		/* @__PURE__ */ (0, import_jsx_runtime.jsx)("style", { children: serverState.formatting_style }),
		/* @__PURE__ */ (0, import_jsx_runtime.jsx)("style", { children: `
        .highlight pre {
          line-height: inherit !important;
          }
        ` }),
		/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "md:mx-20 space-y-6 rounded-lg p-8",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "space-y-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "text-sm text-zinc-500 font-mono",
					children: [
						"Timestamp: ",
						timestamp,
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
						"Environment: ",
						"production"
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
					className: "font-mono text-xl font-semibold text-zinc-800 whitespace-pre-wrap",
					children: serverState.exception
				})]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "space-y-4",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex items-center space-x-1 text-red-600 font-semibold whitespace-pre-wrap",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [serverState.parsed_exception.exc_type, ":"] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: serverState.parsed_exception.exc_value })]
				}), serverState.parsed_exception.frames.map((frame, index) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "border rounded-lg overflow-hidden bg-white",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "bg-gray-100 px-4 py-2 border-b flex justify-between items-center",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "font-mono text-sm text-gray-700",
							children: [
								frame.file_name,
								":",
								frame.line_number
							]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							type: "button",
							onClick: () => {
								if (showFrame !== frame.id) setShowFrame(frame.id);
								else setShowFrame(null);
							},
							className: "px-3 py-1 bg-blue-500 hover:bg-blue-600 transition-colors text-white rounded text-sm",
							children: frame.function_name
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "py-4 px-3 text-right font-mono text-sm bg-gray-50 text-gray-500 select-none border-r",
							children: Array.from({ length: frame.end_line_number - frame.start_line_number }, (_, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: `leading-6 ${frame.start_line_number + i === frame.line_number ? "bg-red-100 text-red-600 font-semibold px-2 -mx-2" : ""}`,
								children: frame.start_line_number + i
							}, i))
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "flex-1 p-4 overflow-x-auto font-mono text-sm bg-gray-800 !leading-6",
							dangerouslySetInnerHTML: { __html: frame.code_context }
						})]
					})]
				}), showFrame === frame.id && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 rounded-lg overflow-hidden border border-gray-200 shadow-sm mb-12",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "bg-gray-100 p-4 font-mono text-sm font-bold text-gray-700 border-b flex items-center",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "grow",
							children: "Local Variables"
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("button", {
							type: "button",
							onClick: () => setShowFrame(null),
							className: "py-1 px-2 -m-2 hover:bg-gray-500/10 rounded",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("svg", {
								xmlns: "http://www.w3.org/2000/svg",
								fill: "none",
								viewBox: "0 0 24 24",
								strokeWidth: 1.5,
								stroke: "currentColor",
								className: "size-6",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("title", { children: "Close" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", {
									strokeLinecap: "round",
									strokeLinejoin: "round",
									d: "M6 18 18 6M6 6l12 12"
								})]
							})
						})]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "divide-y divide-gray-200",
						children: Object.entries(frame.local_values).map(([key, html]) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "w-48 shrink-0 bg-gray-50 p-4 font-mono text-sm text-gray-600 border-r",
								children: key
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "flex-1 p-4 overflow-x-auto font-mono text-sm bg-gray-700",
								dangerouslySetInnerHTML: { __html: html }
							})]
						}, key))
					})]
				})] }, frame.id))]
			})]
		})
	] });
};
var page_default = Page;

//#endregion
//#region ../../../../../tmp/.tmptS9xS6/entrypoint.jsx
const Entrypoint = () => {
	live_reload_default({
		SSR_RENDERING: true,
		NODE_ENV: "production",
		LIVE_RELOAD_PORT: 0
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(layout_default, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(page_default, {}) });
};
const Index = () => (0, react_dom_server_edge.renderToString)(/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Entrypoint, {}));

//#endregion
exports.Index = Index
return exports;
})({}, react_dom_server_edge);
//# sourceMappingURL=entrypoint.js.map
})();