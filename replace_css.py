import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """\
<style>
:root {
  --bg: #faf8f4;
  --bg2: #f2efe9;
  --bg3: #e8e4db;
  --text: #1a1814;
  --text2: #3d3a35;
  --text3: #7a776f;
  --border: rgba(0,0,0,.08);
  --border2: rgba(0,0,0,.13);
  --blue: #2b5ea7;
  --green: #2a7c6f;
  --amber: #b86e1a;
  --red: #943030;
  --purple: #5b4890;
  --gold: #c4933f;
  --gold-light: #f0d99a;
  --gold-pale: #fdf5e0;
  --accent-bg: #1a1814;
  --radius: 2px;
  --radius-lg: 4px;
  color-scheme: light;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Noto Sans KR', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  font-size: 15px;
  line-height: 1.65;
}

/* ── HEADER ── */
.site-header {
  background: var(--accent-bg);
  padding: 22px 32px;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  border-bottom: 1px solid rgba(255,255,255,.05);
}
.header-title h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 24px; font-weight: 400; color: #fff; letter-spacing: .01em;
}
.header-title h1 span { color: var(--gold); font-style: italic; }
.header-title p { font-size: 11px; color: rgba(255,255,255,.4); margin-top: 4px; letter-spacing: .1em; text-transform: uppercase; }
.header-badge {
  font-size: 11px; color: rgba(255,255,255,.5);
  border: 1px solid rgba(255,255,255,.14);
  padding: 4px 14px; border-radius: 2px; white-space: nowrap; letter-spacing: .08em;
}

/* ── TAB NAV ── */
.tab-nav {
  display: flex;
  background: var(--bg);
  border-bottom: 1px solid var(--bg3);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.tab-btn {
  flex: 1; min-width: 90px;
  padding: 14px 10px;
  border: none; background: transparent;
  cursor: pointer; font-size: 13px; font-weight: 400;
  color: var(--text3); font-family: inherit;
  white-space: nowrap; border-bottom: 2px solid transparent;
  transition: all .2s; letter-spacing: .03em;
}
.tab-btn:hover { color: var(--text2); }
.tab-btn.active { color: var(--text); border-bottom-color: var(--gold); }

/* ── LAYOUT ── */
.tab-content { display: none; }
.tab-content.active { display: block; }
.container { max-width: 1400px; margin: 0 auto; padding: 28px 32px; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }
.split-55 { grid-template-columns: 55% 1fr; }
@media (max-width: 860px) { .split, .split-55 { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .container { padding: 16px; } .site-header { padding: 16px 20px; } .site-footer { padding: 18px 16px; } }

/* ── CARD ── */
.card {
  background: var(--bg2);
  border: 1px solid var(--bg3);
  border-radius: var(--radius-lg);
  padding: 20px;
}
.card + .card { margin-top: 14px; }
.card-title {
  font-size: 11px; font-weight: 500; color: var(--text2);
  margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
  letter-spacing: .12em; text-transform: uppercase;
}
.card-title::before {
  content: ''; width: 2px; height: 13px;
  background: var(--gold); border-radius: 1px; flex-shrink: 0;
}

/* ── FORM ── */
.form-group { margin-bottom: 14px; }
.form-label {
  display: block; font-size: 10px; font-weight: 500;
  color: var(--text3); margin-bottom: 5px; letter-spacing: .14em;
  text-transform: uppercase;
}
.form-hint { font-size: 11px; color: var(--text3); margin-top: 4px; line-height: 1.55; }
.inp-wrap { position: relative; display: flex; align-items: center; }
.inp-wrap input[type="number"] {
  width: 100%; padding: 9px 38px 9px 11px;
  border: 1px solid var(--bg3); border-radius: var(--radius);
  background: var(--bg); color: var(--text);
  font-size: 14px; font-family: inherit; transition: border-color .2s;
}
.inp-wrap input[type="number"]:focus { outline: none; border-color: var(--gold); }
.inp-unit {
  position: absolute; right: 10px;
  font-size: 11px; color: var(--text3); pointer-events: none;
}
input[type="range"] { width: 100%; accent-color: var(--gold); cursor: pointer; height: 3px; margin-top: 6px; }
.range-row { display: flex; justify-content: space-between; font-size: 10px; color: var(--text3); margin-top: 3px; letter-spacing: .04em; }
.radio-group { display: flex; gap: 6px; flex-wrap: wrap; }
.radio-opt { flex: 1; min-width: 70px; }
.radio-opt input[type="radio"] { display: none; }
.radio-opt label {
  display: block; padding: 7px 10px; border: 1px solid var(--bg3);
  border-radius: var(--radius); cursor: pointer; font-size: 12px; font-weight: 400;
  text-align: center; color: var(--text3); transition: all .2s; white-space: nowrap;
}
.radio-opt input:checked + label { background: var(--accent-bg); color: var(--gold-light); border-color: var(--accent-bg); }
.divider { border: none; border-top: 1px solid var(--bg3); margin: 14px 0; }

/* ── RESULT ── */
.result-hero {
  background: var(--accent-bg); border-radius: var(--radius-lg);
  padding: 20px 22px; margin-bottom: 14px;
}
.result-hero-label { font-size: 10px; color: rgba(255,255,255,.45); margin-bottom: 6px; letter-spacing: .12em; text-transform: uppercase; }
.result-hero-value { font-family: 'DM Serif Display', serif; font-size: 34px; font-weight: 400; color: var(--gold-light); line-height: 1.2; }
.result-hero-sub { font-size: 12px; color: rgba(255,255,255,.4); margin-top: 6px; }

.rrow {
  display: flex; justify-content: space-between; align-items: center;
  padding: 9px 0; border-bottom: 1px solid var(--bg3); font-size: 13px;
}
.rrow:last-child { border-bottom: none; }
.rrow-label { color: var(--text3); }
.rrow-val { font-weight: 500; }
.rrow-val.green { color: var(--green); }
.rrow-val.red   { color: var(--red); }
.rrow-val.blue  { color: var(--blue); }
.rrow-val.gold  { color: var(--amber); }

.cmp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
.cmp-card {
  background: var(--bg3); border: 1px solid var(--bg3);
  border-radius: var(--radius); padding: 14px; text-align: center;
}
.cmp-card.winner { border-color: var(--green); background: rgba(42,124,111,.07); }
.cmp-label { font-size: 10px; font-weight: 500; color: var(--text3); margin-bottom: 6px; letter-spacing: .1em; text-transform: uppercase; }
.cmp-value { font-family: 'DM Serif Display', serif; font-size: 26px; font-weight: 400; color: var(--text); }
.cmp-card.winner .cmp-value { color: var(--green); }
.cmp-detail { font-size: 11px; color: var(--text3); margin-top: 4px; }
.badge-win {
  display: inline-block; background: var(--green); color: #fff;
  font-size: 10px; font-weight: 400; padding: 2px 8px; border-radius: 2px; margin-top: 5px; letter-spacing: .05em;
}

/* ── ALERT ── */
.alert {
  padding: 10px 14px; font-size: 12px; margin-bottom: 12px; line-height: 1.65;
  border-left: 2px solid; border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
}
.alert-info  { background: #edf2fc; color: var(--blue); border-color: var(--blue); border-top: 1px solid #c8d8f5; border-right: 1px solid #c8d8f5; border-bottom: 1px solid #c8d8f5; }
.alert-warn  { background: var(--gold-pale); color: var(--amber); border-color: var(--gold); border-top: 1px solid #f0d99a; border-right: 1px solid #f0d99a; border-bottom: 1px solid #f0d99a; }
.alert-green { background: rgba(42,124,111,.07); color: var(--green); border-color: var(--green); border-top: 1px solid rgba(42,124,111,.18); border-right: 1px solid rgba(42,124,111,.18); border-bottom: 1px solid rgba(42,124,111,.18); }

/* ── SECTION TOGGLE ── */
.section-toggle {
  display: none;
  border: 1px solid var(--bg3); border-radius: var(--radius-lg);
  margin-top: 14px; overflow: hidden;
}
.section-toggle.visible { display: block; }
.stoggle-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; background: var(--bg3); cursor: pointer;
  font-size: 11px; font-weight: 500; color: var(--text2);
  border: none; width: 100%; text-align: left; font-family: inherit;
  transition: background .2s; letter-spacing: .08em; text-transform: uppercase;
}
.stoggle-header:hover { background: #ddd8cf; }
.stoggle-header .chev { transition: transform .25s; font-style: normal; font-size: 11px; }
.stoggle-header.open .chev { transform: rotate(180deg); }
.stoggle-body { padding: 16px; border-top: 1px solid var(--bg3); }
.stoggle-body.hidden { display: none; }

.sub-title {
  font-size: 10px; font-weight: 500; color: var(--text3);
  text-transform: uppercase; letter-spacing: .14em;
  margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--bg3);
}

/* ── MODE TOGGLE ── */
.mode-toggle {
  display: flex; background: var(--bg3); border: 1px solid var(--bg3);
  border-radius: var(--radius); padding: 3px; margin-bottom: 16px;
}
.mode-btn {
  flex: 1; padding: 7px 12px; border: none; background: transparent;
  cursor: pointer; font-size: 12px; font-weight: 400; color: var(--text3);
  border-radius: var(--radius); transition: all .2s; font-family: inherit;
}
.mode-btn.active { background: var(--accent-bg); color: var(--gold-light); }
.mode-panel { display: none; }
.mode-panel.active { display: block; }

/* ── TAB 1: FLOW DIAGRAM ── */
.flow-wrap {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0 20px;
  align-items: start;
}
@media (max-width: 860px) { .flow-wrap { grid-template-columns: 1fr; } }
.flow-stage { }
.flow-head {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px; border-radius: var(--radius) var(--radius) 0 0;
  font-weight: 500; font-size: 16px; font-family: 'Noto Serif KR', serif;
}
.flow-head .num {
  width: 27px; height: 27px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 400; flex-shrink: 0; font-family: 'DM Serif Display', serif;
}
.flow-body {
  background: var(--bg2); border: 1px solid var(--bg3);
  border-top: none; border-radius: 0 0 var(--radius) var(--radius); padding: 14px;
}
.flow-arrow {
  display: flex; justify-content: center; align-items: center;
  height: 28px; font-size: 18px; color: var(--text3);
  display: none;
}
@media (max-width: 860px) { .flow-arrow { display: flex; } }

.fitem {
  display: flex; gap: 9px; padding: 10px 0;
  border-bottom: 1px solid var(--bg3); font-size: 13px;
  align-items: flex-start;
}
.fitem:last-child { border-bottom: none; padding-bottom: 0; }
.fitem-dot {
  width: 22px; height: 22px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 500; flex-shrink: 0; margin-top: 1px;
}
.fitem-body { flex: 1; }
.fitem-title { font-weight: 500; color: var(--text); font-size: 14px; font-family: 'Noto Serif KR', serif; }
.fitem-desc  { font-size: 12px; color: var(--text3); margin-top: 3px; line-height: 1.55; }
.fitem-rate  { font-size: 12px; font-weight: 500; white-space: nowrap; margin-top: 4px; }

.flow-blue .flow-head { background: rgba(43,94,167,.09); color: var(--blue); }
.flow-blue .flow-head .num { background: var(--blue); color: #fff; }
.flow-blue .fitem-dot { background: rgba(43,94,167,.1); color: var(--blue); }
.flow-purple .flow-head { background: rgba(91,72,144,.09); color: var(--purple); }
.flow-purple .flow-head .num { background: var(--purple); color: #fff; }
.flow-purple .fitem-dot { background: rgba(91,72,144,.1); color: var(--purple); }
.flow-green .flow-head { background: rgba(42,124,111,.09); color: var(--green); }
.flow-green .flow-head .num { background: var(--green); color: #fff; }
.flow-green .fitem-dot { background: rgba(42,124,111,.1); color: var(--green); }

.key-box {
  background: var(--gold-pale);
  border-left: 2px solid var(--gold);
  border-top: 1px solid #f0d99a; border-right: 1px solid #f0d99a; border-bottom: 1px solid #f0d99a;
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0; padding: 14px 18px;
  margin-top: 24px;
}
.key-box-title { font-size: 10px; font-weight: 500; color: var(--amber); margin-bottom: 10px; letter-spacing: .14em; text-transform: uppercase; }
.key-pt {
  font-size: 13px; color: var(--text2); padding: 4px 0;
  display: flex; gap: 8px; line-height: 1.6;
}
.key-pt::before { content: '✓'; color: var(--green); flex-shrink: 0; font-size: 11px; margin-top: 3px; }

/* ── MATRIX ── */
.matrix-wrap { overflow-x: auto; margin: 14px -20px 0; padding: 0 20px; }
table.matrix {
  border-collapse: collapse; width: 100%;
  font-size: 13px; min-width: 480px;
}
table.matrix th, table.matrix td {
  border: 1px solid var(--bg3); padding: 9px 11px;
  text-align: center; white-space: nowrap;
}
table.matrix th {
  background: var(--accent-bg); color: var(--gold-light); font-weight: 500;
}
table.matrix .rh {
  background: var(--bg3); font-weight: 500; color: var(--text2);
  text-align: left; padding-left: 12px;
}
.matrix-legend {
  display: flex; gap: 12px; flex-wrap: wrap;
  font-size: 11px; margin-top: 10px; color: var(--text2);
}
.legend-dot {
  width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; margin-top: 2px;
}

/* ── BREAKDOWN BOX ── */
.breakdown {
  background: var(--bg3); border-radius: var(--radius);
  padding: 12px 14px; margin-top: 12px;
}
.breakdown-title { font-size: 10px; font-weight: 500; color: var(--text3); margin-bottom: 8px; letter-spacing: .1em; text-transform: uppercase; }
.breakdown-row {
  display: flex; justify-content: space-between;
  font-size: 13px; padding: 3px 0; color: var(--text2);
}
.breakdown-row.total {
  border-top: 1px solid var(--bg3); margin-top: 6px;
  padding-top: 8px; font-weight: 500; color: var(--text);
}

/* ── STAGE OVERVIEW ── */
.t1-overview { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-bottom: 24px; }
@media (max-width: 860px) { .t1-overview { grid-template-columns: 1fr; } }
.isa-down-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 12px; }
@media (max-width: 600px) { .isa-down-grid { grid-template-columns: 1fr; } }

/* ── LIMIT DIAGRAM ── */
.limit-bar { display: flex; height: 48px; border-radius: var(--radius); overflow: hidden; margin: 12px 0 4px; }
.limit-seg { display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 4px 6px; font-size: 11px; font-weight: 500; text-align: center; line-height: 1.3; }
.ls-a { background: var(--accent-bg); color: var(--gold-light); }
.ls-b { background: rgba(43,94,167,.18); color: var(--blue); }
.ls-c { background: var(--bg3); color: var(--text3); }
.limit-ruler { display: flex; justify-content: space-between; font-size: 10px; color: var(--text3); letter-spacing: .04em; }

/* ── KR NUM DISPLAY ── */
.kr-num { font-family: 'DM Serif Display', serif; font-size: 20px; font-weight: 400; color: var(--gold); min-height: 24px; margin-bottom: 4px; line-height: 1.3; }

/* ── FOOTER ── */
.site-footer {
  margin-top: 48px; padding: 22px 32px;
  background: var(--bg2); border-top: 1px solid var(--bg3);
}
.disclaimer {
  font-size: 11px; color: var(--text3); line-height: 2;
  text-align: center; max-width: 800px; margin: 0 auto; letter-spacing: .03em;
}
</style>"""

content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('done')
