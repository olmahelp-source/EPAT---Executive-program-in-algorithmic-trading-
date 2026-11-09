"use strict";
/* Algo Platform UI: vanilla JS, no build step. All server text is inserted via textContent
   (never innerHTML), so strategy names / reject reasons cannot inject markup. */

// ---------- tiny DOM helper ----------
function h(tag, props, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v === undefined || v === null || v === false) continue;
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === "value") el.value = v;
    else if (k === "style") el.style.cssText = v;      // CSSOM assignment is allowed by our CSP; a style="" attribute is not
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return el;
}
const svgNS = "http://www.w3.org/2000/svg";
function s(tag, attrs) {
  const el = document.createElementNS(svgNS, tag);
  for (const [k, v] of Object.entries(attrs || {})) el.setAttribute(k, v);
  return el;
}

// ---------- state & API ----------
const store = { token: null, me: null };
try { store.token = sessionStorage.getItem("token"); } catch (_) { /* private mode */ }
let toastTimer = null;

function toast(msg, isError) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast" + (isError ? " error" : "");
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, isError ? 7000 : 3000);
}

async function api(path, body) {
  const opts = { method: body === undefined ? "GET" : "POST", headers: {} };
  if (store.token) opts.headers.Authorization = "Bearer " + store.token;
  if (body !== undefined) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
  let res;
  try { res = await fetch(path, opts); } catch (_) { throw new Error("Cannot reach the server"); }
  let data = null;
  try { data = await res.json(); } catch (_) { /* non-JSON */ }
  if (res.status === 401 && store.token && path !== "/api/login") { logout(true); throw new Error("Session expired, please sign in again"); }
  if (!res.ok) throw new Error((data && data.message) || ("Request failed (" + res.status + ")"));
  return data;
}

// run an async action with a busy button and error toast
async function busy(btn, fn) {
  const label = btn.textContent;
  btn.disabled = true;
  btn.replaceChildren(h("span", { class: "spinner" }), "Working…");
  try { return await fn(); }
  catch (e) { toast(e.message, true); }
  finally { btn.disabled = false; btn.textContent = label; }
}

// ---------- formatting ----------
const nf = (d) => new Intl.NumberFormat(undefined, { maximumFractionDigits: d, minimumFractionDigits: d });
const fmt = {
  pct: (v, d = 2) => v == null ? "–" : nf(d).format(v * 100) + "%",
  num: (v, d = 2) => v == null ? "–" : nf(d).format(v),
  money: (v) => v == null ? "–" : (v < 0 ? "-$" : "$") + nf(2).format(Math.abs(v)),
  tone: (v) => v == null || v === 0 ? "" : (v > 0 ? "good" : "bad"),
};

// ---------- components ----------
function kpi(label, value, tone) {
  return h("div", { class: "kpi" }, h("div", { class: "l" }, label), h("div", { class: "v " + (tone || "") }, value));
}

function table(cols, rows, empty) {
  if (!rows || !rows.length) return h("p", { class: "hint" }, empty || "No data.");
  return h("div", { class: "scroll" }, h("table", null,
    h("thead", null, h("tr", null, cols.map((c) => h("th", null, c.label)))),
    h("tbody", null, rows.map((r) => h("tr", null, cols.map((c) => {
      const raw = r[c.key];
      const cell = c.render ? c.render(raw, r) : (raw == null ? "–" : raw);
      return h("td", { class: c.tone ? fmt.tone(raw) : "" }, cell);
    }))))));
}

/* series: [{name, cls, points: [[label, value], ...]}]; first series drives hover */
function lineChart(series, opts = {}) {
  const W = 800, H = opts.small ? 120 : 220, pad = 6;
  const all = series.flatMap((x) => x.points.map((p) => p[1])).filter((v) => v != null);
  if (!all.length) return h("p", { class: "hint" }, "No data yet.");
  let lo = Math.min(...all, opts.baseline ?? Infinity), hi = Math.max(...all, opts.baseline ?? -Infinity);
  if (lo === hi) { lo -= 1; hi += 1; }
  const y = (v) => H - pad - ((v - lo) / (hi - lo)) * (H - 2 * pad);
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: "none", role: "img", "aria-label": opts.label || "chart" });
  svg.setAttribute("class", opts.small ? "small" : "");
  for (let i = 0; i <= 3; i++) svg.append(s("line", { x1: 0, x2: W, y1: pad + i * (H - 2 * pad) / 3, y2: pad + i * (H - 2 * pad) / 3, class: "grid-line", "vector-effect": "non-scaling-stroke" }));
  for (const ser of series) {
    const n = ser.points.length;
    if (n < 2) continue;
    const xs = (i) => pad + (i / (n - 1)) * (W - 2 * pad);
    const d = ser.points.map((p, i) => (i ? "L" : "M") + xs(i).toFixed(1) + " " + y(p[1]).toFixed(1)).join(" ");
    if (opts.fill && ser === series[0]) {
      const base = y(opts.baseline ?? lo);
      svg.append(s("path", { d: d + ` L${xs(n - 1).toFixed(1)} ${base} L${xs(0).toFixed(1)} ${base} Z`, class: ser.fcls || "f0", opacity: ".13" }));
    }
    svg.append(s("path", { d, fill: "none", "stroke-width": "1.8", "vector-effect": "non-scaling-stroke", class: ser.cls || "s0" }));
  }
  const first = series[0].points;
  const tip = h("div", { class: "tip", hidden: true });
  const wrap = h("div", { class: "chart" },
    series.length > 1 || opts.legend ? h("div", { class: "legend" }, series.map((x) => h("span", null, h("span", { class: "dot " + (x.fcls || "f0") }), x.name))) : null,
    svg, tip,
    h("div", { class: "axis" }, h("span", null, first[0][0]), h("span", null, (opts.yFmt || fmt.num)(lo) + " – " + (opts.yFmt || fmt.num)(hi)), h("span", null, first[first.length - 1][0])));
  svg.addEventListener("pointermove", (e) => {
    const r = svg.getBoundingClientRect();
    const i = Math.max(0, Math.min(first.length - 1, Math.round(((e.clientX - r.left) / r.width) * (first.length - 1))));
    tip.hidden = false;
    tip.textContent = first[i][0] + "  " + series.map((x) => x.points[Math.min(i, x.points.length - 1)]).map((p) => (opts.yFmt || fmt.num)(p[1])).join(" · ");
  });
  svg.addEventListener("pointerleave", () => { tip.hidden = true; });
  return wrap;
}

function field(label, input) { return h("label", null, label, input); }

// ---------- views ----------
function renderLogin() {
  const user = h("input", { id: "u", autocomplete: "username", required: true });
  const pw = h("input", { id: "p", type: "password", autocomplete: "current-password", required: true });
  const msg = h("p", { class: "hint" }, "Passwords need 10+ characters with upper, lower and a digit. The first account created becomes the administrator.");
  const loginBtn = h("button", { class: "btn", type: "submit" }, "Sign in");
  const regBtn = h("button", { class: "btn ghost", type: "button" }, "Create account");
  const doLogin = async () => {
    const r = await api("/api/login", { username: user.value, password: pw.value });
    store.token = r.token;
    try { sessionStorage.setItem("token", r.token); } catch (_) { /* ignore */ }
    await boot();
  };
  regBtn.addEventListener("click", () => busy(regBtn, async () => {
    await api("/api/register", { username: user.value, password: pw.value });
    toast("Account created, signing in…");
    await doLogin();
  }));
  const form = h("form", { class: "card login", onsubmit: (e) => { e.preventDefault(); busy(loginBtn, doLogin); } },
    h("h1", null, "Algo Platform"), h("p", { class: "muted" }, "Backtest, optimise and paper-trade."),
    h("div", { class: "grid" }, field("Username", user), field("Password", pw)),
    h("div", { class: "row", style: "margin-top:14px" }, loginBtn, regBtn), msg);
  return form;
}

function logout(silent) {
  store.token = null; store.me = null;
  try { sessionStorage.removeItem("token"); } catch (_) { /* ignore */ }
  stopAuto();
  if (!silent) toast("Signed out");
  mount(renderLogin());
}

const TABS = [
  { id: "backtest", label: "Backtest", build: backtestView },
  { id: "builder", label: "Strategy builder", build: builderView },
  { id: "optimize", label: "Optimise", build: optimizeView },
  { id: "live", label: "Paper trading", build: liveView },
  { id: "admin", label: "Admin & audit", build: adminView, perm: ["users:manage", "risk:manage"] },
];

function mount(node) { document.getElementById("root").replaceChildren(node); }

function renderApp() {
  const perms = store.me.permissions;
  const tabs = TABS.filter((t) => !t.perm || t.perm.some((p) => perms.includes(p)));
  const content = h("div");
  const nav = h("nav", { class: "tabs", role: "tablist" });
  const select = (t) => {
    if (t.id !== "live") stopAuto();
    for (const b of nav.children) b.setAttribute("aria-selected", String(b.dataset.id === t.id));
    content.replaceChildren(t.build());
    try { sessionStorage.setItem("tab", t.id); } catch (_) { /* ignore */ }
  };
  for (const t of tabs) nav.append(h("button", { role: "tab", "data-id": t.id, "aria-selected": "false", onclick: () => select(t) }, t.label));
  let saved = "backtest";
  try { saved = sessionStorage.getItem("tab") || saved; } catch (_) { /* ignore */ }
  mount(h("div", null,
    h("header", { class: "top" }, h("div", { class: "wrap" }, h("span", { class: "brand" }, "Algo Platform"), h("span", { class: "spacer" }),
      h("span", { class: "who" }, store.me.username + " · " + store.me.role),
      h("button", { class: "btn ghost", onclick: () => logout(false) }, "Sign out"))),
    h("div", { class: "wrap" }, nav, content)));
  select(tabs.find((t) => t.id === saved) || tabs[0]);
}

// ----- strategy parameter form -----
let strategyCache = null;
async function strategies() { return strategyCache || (strategyCache = await api("/api/strategies")); }

function paramInputs(container, strat) {
  container.replaceChildren();
  const inputs = {};
  for (const [k, v] of Object.entries(strat.params)) {
    const isBool = typeof v === "boolean";
    const inp = isBool
      ? h("select", null, h("option", { value: "false" }, "false"), h("option", { value: "true" }, "true"))
      : h("input", { type: "number", step: "any", value: v, style: "width:110px" });
    if (isBool) inp.value = String(v);
    inputs[k] = { inp, isBool, def: v };
    container.append(field(k, inp));
  }
  return () => {
    const out = {};
    for (const [k, { inp, isBool }] of Object.entries(inputs)) out[k] = isBool ? inp.value === "true" : Number(inp.value);
    return out;
  };
}

function dataFields() {
  const symbols = h("input", { value: "AAA,BBB,CCC", style: "width:150px", "aria-label": "symbols" });
  const bars = h("input", { type: "number", value: 756, min: 150, max: 3000, style: "width:90px" });
  const seed = h("input", { type: "number", value: 7, style: "width:80px" });
  return { symbols, bars, seed, nodes: [field("Symbols (synthetic)", symbols), field("Bars", bars), field("Seed", seed)],
    get: () => ({ symbols: symbols.value.split(",").map((x) => x.trim()).filter(Boolean), bars: Number(bars.value), seed: Number(seed.value) }) };
}

// ----- backtest results -----
function backtestResults(r) {
  const m = r.metrics, t = r.trade_stats;
  const out = h("div");
  if (r.kill_switch) out.append(h("div", { class: "banner halt" }, h("strong", null, "Kill switch tripped during this backtest"), " — trading was halted and positions flattened."));
  out.append(h("div", { class: "kpis" },
    kpi("Total return", fmt.pct(m.total_return), fmt.tone(m.total_return)), kpi("CAGR", fmt.pct(m.cagr), fmt.tone(m.cagr)),
    kpi("Sharpe", fmt.num(m.sharpe)), kpi("Sortino", fmt.num(m.sortino)), kpi("Max drawdown", fmt.pct(m.max_drawdown), "bad"),
    kpi("Volatility", fmt.pct(m.volatility)), kpi("Trades", t.trades ?? 0), kpi("Win rate", fmt.pct(t.win_rate, 1)),
    kpi("Profit factor", fmt.num(t.profit_factor))));
  const series = [{ name: "Strategy", cls: "s0", fcls: "f0", points: r.equity }];
  if (r.benchmark) series.push({ name: "Equal-weight buy & hold", cls: "s1", fcls: "f1", points: r.benchmark });
  out.append(h("div", { class: "card" }, h("h2", null, "Equity"), lineChart(series, { yFmt: fmt.money, label: "equity curve" }),
    h("h3", { style: "margin-top:14px" }, "Drawdown"), lineChart([{ name: "Drawdown", cls: "neg", fcls: "fneg", points: r.drawdown }], { yFmt: (v) => fmt.pct(v, 1), fill: true, baseline: 0, small: true, label: "drawdown" })));
  const sig = r.significance;
  out.append(h("div", { class: "grid cols-2" },
    h("div", { class: "card" }, h("h2", null, "Performance"), table([{ key: "k", label: "Metric" }, { key: "v", label: "Value" }],
      Object.entries(m).map(([k, v]) => ({ k: k.replace(/_/g, " "), v: typeof v === "number" ? fmt.num(v, 4) : v })))),
    h("div", { class: "card" }, h("h2", null, "Trade statistics"), table([{ key: "k", label: "Metric" }, { key: "v", label: "Value" }],
      Object.entries(t).map(([k, v]) => ({ k: k.replace(/_/g, " "), v: typeof v === "number" ? fmt.num(v, 3) : v }))),
      sig ? h("p", { class: "hint" }, `Probability the true Sharpe > 0: ${fmt.pct(sig.probabilistic_sharpe_vs_0, 1)} · deflated for ${sig.n_trials} trial(s): ${fmt.pct(sig.deflated_sharpe, 1)}`) : null)));
  out.append(h("div", { class: "card" }, h("h2", null, `Trades (last ${r.trades.length})`),
    table([{ key: "symbol", label: "Symbol" }, { key: "direction", label: "Side", render: (d) => d > 0 ? "Long" : "Short" },
      { key: "quantity", label: "Qty" }, { key: "entry_price", label: "Entry", render: (v) => fmt.num(v) }, { key: "exit_price", label: "Exit", render: (v) => fmt.num(v) },
      { key: "pnl", label: "P&L", tone: true, render: (v) => fmt.num(v) }, { key: "return_pct", label: "Return", tone: true, render: (v) => fmt.pct(v) },
      { key: "exit_ts", label: "Closed", render: (v) => String(v).slice(0, 10) }], r.trades, "No closed trades.")));
  out.append(h("p", { class: "hint" }, `${r.orders} orders sent, ${r.rejected} rejected by risk. Data is synthetic: results illustrate mechanics, not real-market performance.`));
  return out;
}

function backtestView() {
  const root = h("div"), params = h("div", { class: "row" }), results = h("div"), df = dataFields();
  const sel = h("select");
  let getParams = () => ({}), list = [];
  const run = h("button", { class: "btn", type: "submit" }, "Run backtest");
  const doc = h("p", { class: "hint" });
  const apply = () => { const st = list.find((x) => x.name === sel.value); getParams = paramInputs(params, st); doc.textContent = st.doc; };
  sel.addEventListener("change", apply);
  strategies().then((l) => { list = l; l.forEach((x) => sel.append(h("option", { value: x.name }, x.name))); apply(); }).catch((e) => toast(e.message, true));
  root.append(h("form", { class: "card", onsubmit: (e) => { e.preventDefault(); busy(run, async () => {
    const r = await api("/api/backtest", { strategy: sel.value, params: getParams(), ...df.get() });
    results.replaceChildren(backtestResults(r));
  }); } }, h("h2", null, "Backtest a built-in strategy"),
    h("div", { class: "row" }, field("Strategy", sel), ...df.nodes), h("div", { class: "row", style: "margin-top:10px" }, params), doc,
    h("div", { style: "margin-top:12px" }, run)), results);
  return root;
}

// ----- strategy builder -----
const OPS = ["crosses_above", "crosses_below", ">", "<", ">=", "<=", "==", "!="];
const IND_TYPES = ["sma", "ema", "wma", "rsi", "roc", "zscore", "rolling_std", "rolling_max", "rolling_min", "atr", "bollinger", "macd", "donchian", "stochastic", "adx"];
const IND_HINT = { sma: "period=20", ema: "period=20", wma: "period=20", rsi: "period=14", roc: "period=10", zscore: "period=20", rolling_std: "period=20",
  rolling_max: "period=20", rolling_min: "period=20", atr: "period=14", bollinger: "period=20,k=2,output=lower", macd: "fast=12,slow=26,signal=9,output=hist",
  donchian: "period=20,output=upper", stochastic: "k=14,d=3,output=k", adx: "period=14,output=adx" };
const PRESET = { inds: [["fast", "sma", "period=10"], ["slow", "sma", "period=40"], ["rsi", "rsi", "period=14"], ["atr", "atr", "period=14"]],
  long_entry: "fast crosses_above slow\nrsi < 70", long_exit: "fast crosses_below slow", short_entry: "", short_exit: "", stop: "atr", mult: 2.5 };

function parseArgs(text) {
  const out = {};
  for (const part of text.split(",").map((x) => x.trim()).filter(Boolean)) {
    const [k, ...rest] = part.split("=");
    if (!rest.length) throw new Error(`Indicator argument "${part}" must look like name=value`);
    const v = rest.join("=").trim();
    out[k.trim()] = v !== "" && !isNaN(Number(v)) ? Number(v) : v;
  }
  return out;
}
function parseRules(text, label) {
  return text.split("\n").map((l) => l.trim()).filter(Boolean).map((line) => {
    const tok = line.split(/\s+/);
    if (tok.length !== 3) throw new Error(`${label}: "${line}" must be three words: left operator right`);
    return tok.map((t, i) => (i !== 1 && t !== "" && !isNaN(Number(t)) ? Number(t) : t));
  });
}

function builderView() {
  const root = h("div"), results = h("div"), df = dataFields();
  const name = h("input", { value: "my_strategy", style: "width:170px" });
  const weight = h("input", { type: "number", step: "0.05", min: "0.05", max: "1", value: "1", style: "width:80px" });
  const stopInd = h("input", { placeholder: "e.g. atr", style: "width:90px" });
  const stopMult = h("input", { type: "number", step: "0.1", value: "2.5", style: "width:80px" });
  const indBox = h("div");
  const rules = { long_entry: h("textarea", { "aria-label": "long entry rules" }), long_exit: h("textarea", { "aria-label": "long exit rules" }),
    short_entry: h("textarea", { "aria-label": "short entry rules" }), short_exit: h("textarea", { "aria-label": "short exit rules" }) };
  const preview = h("div", { class: "code" }, "");
  function addInd(n = "", t = "sma", a = "") {
    const nm = h("input", { value: n, placeholder: "name", "aria-label": "indicator name" });
    const ty = h("select", { "aria-label": "indicator type" }, IND_TYPES.map((x) => h("option", { value: x }, x)));
    ty.value = t;
    const ar = h("input", { value: a, placeholder: IND_HINT[t], "aria-label": "indicator arguments" });
    ty.addEventListener("change", () => { ar.placeholder = IND_HINT[ty.value]; });
    const row = h("div", { class: "indrow" }, nm, ty, ar, h("button", { class: "btn ghost", type: "button", onclick: () => row.remove(), "aria-label": "remove indicator" }, "✕"));
    row.get = () => ({ name: nm.value.trim(), type: ty.value, args: ar.value || ar.placeholder });
    indBox.append(row);
  }
  function load(p) {
    indBox.replaceChildren();
    p.inds.forEach((i) => addInd(...i));
    for (const k of Object.keys(rules)) rules[k].value = p[k];
    stopInd.value = p.stop; stopMult.value = p.mult;
  }
  function spec() {
    const indicators = {};
    for (const row of indBox.children) {
      const { name: n, type, args } = row.get();
      if (!n) throw new Error("Every indicator needs a name");
      indicators[n] = { type, ...parseArgs(args) };
    }
    const sp = { name: name.value.trim() || "custom", params: {}, indicators, weight: Number(weight.value) };
    for (const [k, ta] of Object.entries(rules)) { const r = parseRules(ta.value, k.replace("_", " ")); if (r.length) sp[k] = r; }
    if (stopInd.value.trim()) sp.stop_atr = { indicator: stopInd.value.trim(), multiple: Number(stopMult.value) };
    return sp;
  }
  const show = h("button", { class: "btn ghost", type: "button" }, "Show JSON");
  const run = h("button", { class: "btn", type: "submit" }, "Validate & backtest");
  show.addEventListener("click", () => { try { preview.textContent = JSON.stringify(spec(), null, 2); } catch (e) { toast(e.message, true); } });
  load(PRESET);
  root.append(h("form", { class: "card", onsubmit: (e) => { e.preventDefault(); busy(run, async () => {
    const sp = spec();
    preview.textContent = JSON.stringify(sp, null, 2);
    const r = await api("/api/backtest", { spec: sp, ...df.get() });
    results.replaceChildren(backtestResults(r));
  }); } },
    h("h2", null, "Build a strategy without code"),
    h("p", { class: "hint" }, "Define indicators, then rules. A rule is three words: left operator right, one per line; lines in a box are AND-ed. Operands are indicator names, close/open/high/low/volume, numbers, or name@1 for the value one bar ago."),
    h("div", { class: "row" }, field("Strategy name", name), field("Position weight", weight), ...df.nodes),
    h("h3", { style: "margin-top:16px" }, "Indicators"), indBox,
    h("button", { class: "btn ghost", type: "button", onclick: () => addInd() }, "+ Add indicator"),
    h("div", { class: "grid cols-2", style: "margin-top:16px" },
      field("Long entry", rules.long_entry), field("Long exit", rules.long_exit), field("Short entry", rules.short_entry), field("Short exit", rules.short_exit)),
    h("div", { class: "row", style: "margin-top:10px" }, field("Trailing stop indicator (ATR)", stopInd), field("Stop multiple", stopMult)),
    h("p", { class: "hint" }, "Operators: " + OPS.join("  ")),
    h("div", { class: "row", style: "margin-top:12px" }, run, show, h("button", { class: "btn ghost", type: "button", onclick: () => load(PRESET) }, "Reset to example")),
    preview), results);
  return root;
}

// ----- optimiser -----
function optimizeView() {
  const root = h("div"), results = h("div"), df = dataFields();
  df.bars.value = 500;
  const sel = h("select"), method = h("select", null, h("option", { value: "random" }, "random"), h("option", { value: "genetic" }, "genetic"));
  const n = h("input", { type: "number", value: 20, min: 5, max: 60, style: "width:80px" });
  const metric = h("select", null, ["sharpe", "sortino", "calmar", "total_return", "cagr"].map((x) => h("option", { value: x }, x)));
  const run = h("button", { class: "btn", type: "submit" }, "Optimise");
  strategies().then((l) => l.filter((x) => Object.keys(x.bounds).length).forEach((x) => sel.append(h("option", { value: x.name }, x.name)))).catch((e) => toast(e.message, true));
  root.append(h("form", { class: "card", onsubmit: (e) => { e.preventDefault(); busy(run, async () => {
    const r = await api("/api/optimize", { strategy: sel.value, method: method.value, n_iter: Number(n.value), metric: metric.value, ...df.get() });
    const keys = Object.keys(r.summary.best_params);
    const pts = r.scores.map((v, i) => [String(i + 1), v]);
    let bestSoFar = -Infinity;
    const running = pts.map(([i, v]) => { bestSoFar = Math.max(bestSoFar, v); return [i, bestSoFar]; });
    results.replaceChildren(
      h("div", { class: "kpis" }, kpi("Best " + metric.value, fmt.num(r.summary.best_score)), kpi("Trials", r.summary.trials), kpi("Failed", r.summary.failed),
        kpi("Plateau score", r.plateau == null ? "–" : fmt.num(r.plateau), r.plateau == null ? "" : (r.plateau > 0.7 ? "good" : "warn")), kpi("Seconds", fmt.num(r.summary.seconds, 1))),
      h("div", { class: "card" }, h("h2", null, "Best parameters"), h("div", { class: "code" }, JSON.stringify(r.summary.best_params, null, 2)),
        h("p", { class: "hint" }, "Plateau score near 1 means neighbouring parameters score similarly (robust); near 0 means a lone spike, a classic sign of overfitting. Test the winner out-of-sample before trusting it.")),
      h("div", { class: "card" }, h("h2", null, "Best score so far"), lineChart([{ name: "best", cls: "s0", fcls: "f0", points: running }], { small: true, label: "optimisation progress" })),
      h("div", { class: "card" }, h("h2", null, "Top trials"), table([...keys.map((k) => ({ key: k, label: k })), { key: "score", label: metric.value, render: (v) => fmt.num(v, 3) }], r.top)));
  }); } }, h("h2", null, "Optimise strategy parameters"),
    h("div", { class: "row" }, field("Strategy", sel), field("Method", method), field("Trials", n), field("Objective", metric), ...df.nodes),
    h("p", { class: "hint" }, "Each trial is a full backtest. Parameter sets that break the strategy's rules are recorded as failed trials rather than aborting the search."),
    h("div", { style: "margin-top:12px" }, run)), results);
  return root;
}

// ----- live paper trading -----
let autoTimer = null;
function stopAuto() { if (autoTimer) { clearInterval(autoTimer); autoTimer = null; } }

function liveView() {
  const root = h("div");
  const draw = (snap) => root.replaceChildren(snap && snap.open ? liveDashboard(snap, draw) : liveOpen(draw));
  api("/api/session").then(draw).catch((e) => { toast(e.message, true); draw(null); });
  return root;
}

function liveOpen(draw) {
  const symbols = h("input", { value: "AAA,BBB", style: "width:150px" });
  const sel = h("select", null, h("option", { value: "" }, "None (manual trading only)"));
  strategies().then((l) => l.filter((x) => x.name !== "pairs_trading" && x.name !== "momentum_rotation").forEach((x) => sel.append(h("option", { value: x.name }, x.name)))).catch(() => {});
  const btn = h("button", { class: "btn", type: "submit" }, "Open paper session");
  return h("form", { class: "card", onsubmit: (e) => { e.preventDefault(); busy(btn, async () => {
    draw(await api("/api/session/open", { symbols: symbols.value.split(",").map((x) => x.trim()).filter(Boolean), strategy: sel.value || undefined }));
  }); } }, h("h2", null, "Paper trading session"),
    h("p", { class: "hint" }, "A simulated broker and a synthetic random-walk price feed. Every order goes through the same risk gate, order manager and kill switch as the backtester. No real money or real market data is involved."),
    h("div", { class: "row" }, field("Symbols", symbols), field("Run a strategy", sel)), h("div", { style: "margin-top:12px" }, btn));
}

function meter(value, limit, label) {
  const frac = Math.max(0, Math.min(1, limit ? Math.abs(Math.min(value, 0)) / limit : 0));
  const cls = frac > 0.8 ? "crit" : frac > 0.5 ? "hot" : "";
  const bar = h("span");
  bar.style.width = (frac * 100).toFixed(0) + "%";
  return h("div", null, h("div", { class: "row" }, h("span", { class: "muted" }, label), h("span", { class: "spacer" }), h("span", null, fmt.pct(value) + " of −" + fmt.pct(limit, 0) + " limit")),
    h("div", { class: "meter " + cls, role: "progressbar", "aria-valuenow": (frac * 100).toFixed(0), "aria-valuemin": 0, "aria-valuemax": 100 }, bar));
}

function liveDashboard(snap, draw) {
  const p = snap.portfolio, ks = snap.kill_switch, halted = ks.state === "TRIGGERED";
  const act = (btn, path, body) => busy(btn, async () => { draw(await api(path, body)); });
  const step = (n) => { const b = h("button", { class: "btn ghost" }, "Step +" + n); b.addEventListener("click", () => act(b, "/api/session/step", { n })); return b; };
  const auto = h("button", { class: "btn ghost" }, autoTimer ? "Stop auto" : "Auto-step");
  auto.addEventListener("click", () => {
    if (autoTimer) { stopAuto(); draw(snap); return; }
    autoTimer = setInterval(async () => { try { draw(await api("/api/session/step", { n: 1 })); } catch (e) { stopAuto(); toast(e.message, true); } }, 1000);
    auto.textContent = "Stop auto";
  });
  const closeBtn = h("button", { class: "btn ghost" }, "Close session");
  closeBtn.addEventListener("click", () => { stopAuto(); busy(closeBtn, async () => { draw(await api("/api/session/close", {})); }); });

  const sym = h("select", null, snap.symbols.map((x) => h("option", { value: x }, x)));
  const side = h("select", null, h("option", { value: "BUY" }, "Buy"), h("option", { value: "SELL" }, "Sell"));
  const qty = h("input", { type: "number", min: 1, value: 10, style: "width:90px" });
  const type = h("select", null, h("option", { value: "MARKET" }, "Market"), h("option", { value: "LIMIT" }, "Limit"));
  const lim = h("input", { type: "number", step: "0.01", placeholder: "limit price", style: "width:110px" });
  const send = h("button", { class: "btn", type: "submit" }, "Send order");
  const ticket = h("form", { class: "card", onsubmit: (e) => { e.preventDefault(); busy(send, async () => {
    const r = await api("/api/session/order", { symbol: sym.value, side: side.value, quantity: Number(qty.value), type: type.value, limit_price: lim.value || null });
    toast(`Order ${r.order.status}${r.order.reason ? ": " + r.order.reason : ""}`, r.order.status === "REJECTED");
    draw(r);
  }); } }, h("h2", null, "Order ticket"),
    h("div", { class: "row" }, field("Symbol", sym), field("Side", side), field("Qty", qty), field("Type", type), field("Limit", lim), send),
    h("p", { class: "hint" }, "Market orders fill at the next bar's open. Orders failing a risk check are rejected, never sent."));

  const reason = h("input", { placeholder: "reason (required to reset)", style: "min-width:220px" });
  const trip = h("button", { class: "btn danger", type: "button" }, "TRIP kill switch");
  const reset = h("button", { class: "btn ghost", type: "button" }, "Reset");
  trip.addEventListener("click", () => act(trip, "/api/session/killswitch", { action: "trip", reason: reason.value }));
  reset.addEventListener("click", () => act(reset, "/api/session/killswitch", { action: "reset", reason: reason.value }));
  const cancelAll = h("button", { class: "btn ghost", type: "button" }, "Cancel all orders");
  cancelAll.addEventListener("click", () => act(cancelAll, "/api/session/cancel_all", {}));

  const posRows = Object.entries(p.positions).map(([k, v]) => ({ symbol: k, ...v }));
  return h("div", null,
    h("div", { class: "banner" + (halted ? " halt" : "") },
      halted ? h("strong", { class: "bad" }, "TRADING HALTED") : h("strong", { class: "good" }, "Kill switch armed"),
      halted ? h("span", null, ks.reason + " (" + ks.source + ")") : h("span", { class: "muted" }, `${snap.bars} bars processed`),
      h("span", { class: "spacer" }), step(1), step(10), step(50), auto, closeBtn),
    h("div", { class: "kpis" }, kpi("Equity", fmt.money(p.equity)), kpi("Cash", fmt.money(p.cash)), kpi("Realized P&L", fmt.money(p.realized), fmt.tone(p.realized)),
      kpi("Unrealized P&L", fmt.money(p.unrealized), fmt.tone(p.unrealized)), kpi("Gross exposure", fmt.money(p.gross)), kpi("Strategy errors", snap.strategy_errors, snap.strategy_errors ? "bad" : "")),
    h("div", { class: "grid cols-2" },
      h("div", { class: "card" }, h("h2", null, "Equity"), lineChart([{ name: "Equity", cls: "s0", fcls: "f0", points: snap.equity_curve }], { yFmt: fmt.money, label: "live equity" })),
      h("div", { class: "card" }, h("h2", null, "Prices"), h("div", { class: "grid" }, snap.symbols.map((x) => h("div", null, h("div", { class: "row" }, h("strong", null, x), h("span", { class: "spacer" }), h("span", null, fmt.num(snap.prices[x]))),
        lineChart([{ name: x, cls: "s0", fcls: "f0", points: snap.history[x].map((v, i) => [String(i), v]) }], { small: true, label: x + " price" })))))),
    ticket,
    h("div", { class: "grid cols-2" },
      h("div", { class: "card" }, h("h2", null, "Risk"), meter(snap.risk.daily_pnl_pct, snap.risk.max_daily_loss_pct, "Daily P&L"), h("div", { style: "height:10px" }),
        meter(snap.risk.drawdown, snap.risk.max_drawdown_pct, "Drawdown"),
        h("p", { class: "hint" }, "Size multiplier from drawdown de-risking: " + fmt.num(snap.risk.exposure_scalar, 2) + (Object.keys(snap.risk.rejections).length ? " · rejections: " + JSON.stringify(snap.risk.rejections) : ""))),
      h("div", { class: "card" }, h("h2", null, "Kill switch"), h("div", { class: "row" }, reason, trip, reset, cancelAll),
        h("p", { class: "hint" }, "Tripping cancels resting orders, flattens positions and blocks new orders. Resetting needs the Risk Manager or Admin role and a written reason (a trader will be refused)."))),
    h("div", { class: "card" }, h("h2", null, "Positions"), table([{ key: "symbol", label: "Symbol" }, { key: "qty", label: "Qty" }, { key: "avg", label: "Avg", render: (v) => fmt.num(v) },
      { key: "last", label: "Last", render: (v) => fmt.num(v) }, { key: "upl", label: "Unrealized", tone: true, render: (v) => fmt.num(v) }], posRows, "Flat.")),
    h("div", { class: "card" }, h("h2", null, "Orders"), table([{ key: "id", label: "ID", render: (v) => v.slice(-8) }, { key: "symbol", label: "Symbol" }, { key: "side", label: "Side" }, { key: "qty", label: "Qty" },
      { key: "type", label: "Type" }, { key: "status", label: "Status", render: (v) => h("span", { class: "badge " + v }, v) }, { key: "avg", label: "Avg fill", render: (v) => v ? fmt.num(v) : "–" },
      { key: "strategy", label: "Source" }, { key: "reason", label: "Reason" }], snap.orders, "No orders yet.")));
}

// ----- admin -----
function adminView() {
  const root = h("div"), perms = store.me.permissions;
  const auditBox = h("div"), usersBox = h("div");
  api("/api/audit").then((rows) => auditBox.replaceChildren(table([{ key: "ts", label: "Time", render: (v) => String(v).replace("T", " ").slice(0, 19) }, { key: "actor", label: "Actor" }, { key: "action", label: "Action" },
    { key: "details", label: "Details", render: (v) => JSON.stringify(v).slice(0, 110) }], rows, "No audit entries."))).catch((e) => auditBox.replaceChildren(h("p", { class: "hint" }, e.message)));
  root.append(h("div", { class: "card" }, h("h2", null, "Audit log (latest 150)"), auditBox));
  if (perms.includes("users:manage")) {
    const load = async () => {
      const users = await api("/api/users");
      usersBox.replaceChildren(table([{ key: "username", label: "User" }, { key: "role", label: "Role", render: (v, r) => {
        const sel = h("select", { "aria-label": "role for " + r.username }, ["TRADER", "RISK_MANAGER", "VIEWER", "ADMIN"].map((x) => h("option", { value: x }, x)));
        sel.value = v;
        sel.addEventListener("change", async () => { try { await api("/api/users/role", { user_id: r.id, role: sel.value }); toast("Role updated for " + r.username); } catch (e) { toast(e.message, true); sel.value = v; } });
        return sel; } }, { key: "active", label: "Active", render: (v) => v ? "yes" : "no" }], users));
    };
    load().catch((e) => toast(e.message, true));
    root.append(h("div", { class: "card" }, h("h2", null, "Users and roles"), usersBox,
      h("p", { class: "hint" }, "Give a second account the Risk Manager role to try resetting the kill switch. Role changes apply on the user's next request.")));
  }
  return root;
}

// ---------- boot ----------
async function boot() {
  if (!store.token) return mount(renderLogin());
  try { store.me = await api("/api/me"); renderApp(); }
  catch (_) { mount(renderLogin()); }
}
boot();
