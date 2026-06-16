content = open('index.html', encoding='utf-8').read()

# ── 1. openYear oninput: updateWdAccLabel 추가 ─────────────────────────
content = content.replace(
    "].openYear=parseInt(this.value)||2015;calcWD()\">',",
    "].openYear=parseInt(this.value)||2015;updateWdAccLabel(' + i + ');calcWD()\">',",
    1
)

# ── 2. balance oninput: updateWdAccLabel 추가 ─────────────────────────
content = content.replace(
    "].balance=parseFloat(this.value)||0;calcWD()\">',",
    "].balance=parseFloat(this.value)||0;updateWdAccLabel(' + i + ');calcWD()\">',",
    1
)

# ── 3. 연간 수령 금액 섹션: input → readonly display ─────────────────────
old_wd = (
    "          '<div>',\n"
    "            '<div style=\"font-size:11px;color:var(--text3);margin-bottom:3px\">연간 수령 금액</div>',\n"
    "            '<div style=\"display:flex;align-items:center;gap:6px\">',\n"
    "              '<input type=\"number\" id=\"wd_wd_inp_' + i + '\" value=\"' + acc.withdrawal + '\" min=\"0\" step=\"500000\" style=\"width:130px;padding:4px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].withdrawal=parseFloat(this.value)||0;calcWD()\">',\n"
    "              '<span style=\"font-size:11px;color:var(--text3)\">원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '') + '</span>',\n"
    "            '</div>',\n"
    "          '</div>',"
)
new_wd = (
    "          '<div>',\n"
    "            '<div style=\"font-size:11px;color:var(--text3);margin-bottom:3px\">연간 수령 금액 <span style=\"font-size:10px;opacity:.7\">(①+②+③ 합산)</span></div>',\n"
    "            '<div style=\"display:flex;align-items:center;gap:6px\">',\n"
    "              '<div style=\"padding:5px 10px;background:var(--bg3);border:1.5px solid var(--border);border-radius:2px;font-size:13px;font-weight:600;color:var(--text1);min-width:130px\"><span id=\"wd_wd_num_' + i + '\">' + ((acc.withdrawal||0) > 0 ? (acc.withdrawal).toLocaleString() : '0') + '</span></div>',\n"
    "              '<span id=\"wd_wd_lbl_' + i + '\" style=\"font-size:11px;color:var(--text3)\">원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '') + '</span>',\n"
    "            '</div>',\n"
    "          '</div>',"
)
assert old_wd in content, "연간 수령 금액 섹션 없음!"
content = content.replace(old_wd, new_wd, 1)

# ── 4. syncWdSrc: el.value 대신 num/lbl span 업데이트 ───────────────────
old_sync = (
    "function syncWdSrc(i) {\n"
    "  var acc = wdAccs[i];\n"
    "  acc.withdrawal = (acc.src1||0) + (acc.src2||0) + (acc.src3||0);\n"
    "  var el = $('wd_wd_inp_' + i);\n"
    "  if (el) el.value = acc.withdrawal;\n"
    "  calcWD();\n"
    "}"
)
new_sync = (
    "function syncWdSrc(i) {\n"
    "  var acc = wdAccs[i];\n"
    "  acc.withdrawal = (acc.src1||0) + (acc.src2||0) + (acc.src3||0);\n"
    "  var numEl = $('wd_wd_num_' + i);\n"
    "  if (numEl) numEl.textContent = acc.withdrawal > 0 ? acc.withdrawal.toLocaleString() : '0';\n"
    "  var lblEl = $('wd_wd_lbl_' + i);\n"
    "  if (lblEl) lblEl.textContent = '원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '');\n"
    "  calcWD();\n"
    "}"
)
assert old_sync in content, "syncWdSrc 없음!"
content = content.replace(old_sync, new_sync, 1)

# ── 5. updateWdAccLabel 함수 추가 (syncWdSrc 뒤) ────────────────────────
update_fn = (
    "\nfunction updateWdAccLabel(i) {\n"
    "  var acc = wdAccs[i];\n"
    "  var curYear = 2026;\n"
    "  var yrLbl = $('wd_yr_lbl_' + i);\n"
    "  if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear || curYear)) + '년';\n"
    "  var balLbl = $('wd_bal_lbl_' + i);\n"
    "  if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';\n"
    "}\n"
)
content = content.replace(
    "\nfunction renderWdAccs() {",
    update_fn + "\nfunction renderWdAccs() {",
    1
)

# ── 6. calcWD 루프 내 라벨 업데이트: withdrawal도 포함 ────────────────────
old_lbl = (
    "    var yrLbl = $('wd_yr_lbl_' + i);\n"
    "    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + (curYear - (acc.openYear||curYear)) + '년';\n"
    "    var balLbl = $('wd_bal_lbl_' + i);\n"
    "    if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';\n"
    "  });"
)
new_lbl = (
    "    var yrLbl = $('wd_yr_lbl_' + i);\n"
    "    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear||curYear)) + '년';\n"
    "    var balLbl = $('wd_bal_lbl_' + i);\n"
    "    if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';\n"
    "    var wdNumEl = $('wd_wd_num_' + i);\n"
    "    if (wdNumEl) wdNumEl.textContent = (acc.withdrawal||0) > 0 ? (acc.withdrawal).toLocaleString() : '0';\n"
    "    var wdLblEl = $('wd_wd_lbl_' + i);\n"
    "    if (wdLblEl) wdLblEl.textContent = '원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '');\n"
    "  });"
)
assert old_lbl in content, "calcWD 라벨 업데이트 없음!"
content = content.replace(old_lbl, new_lbl, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ('updateWdAccLabel', 'updateWdAccLabel 함수'),
    ('wd_wd_num_', '수령금액 num span'),
    ('wd_wd_lbl_', '수령금액 lbl span'),
    ('①+②+③ 합산', 'read-only 합산 텍스트'),
    ('updateWdAccLabel(\' + i + \')', 'oninput 연결'),
]
for k, label in checks:
    print(label + ':', k in content)
