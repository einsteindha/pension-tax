content = open('index.html', encoding='utf-8').read()

# ── 1. renderMatrix: 타겟 ID 파라미터 추가 ──────────────────────────────
content = content.replace(
    "function renderMatrix() {",
    "function renderMatrix(tblId, legId) {",
    1
)
content = content.replace(
    "  var tbl = $('rt_matrix');",
    "  var tbl = $(tblId || 'rt_matrix');",
    1
)
content = content.replace(
    "  var legend = $('rt_legend');",
    "  var legend = $(legId || 'rt_legend');",
    1
)

# ── 2. syncWdSrc 함수 추가 ─────────────────────────────────────────────
sync_fn = """function syncWdSrc(i) {
  var acc = wdAccs[i];
  acc.withdrawal = (acc.src1||0) + (acc.src2||0) + (acc.src3||0);
  var el = $('wd_wd_inp_' + i);
  if (el) el.value = acc.withdrawal;
  calcWD();
}

"""
content = content.replace('function renderWdAccs() {', sync_fn + 'function renderWdAccs() {', 1)

# ── 3. renderWdAccs: 동적 라벨 ID, src oninput → syncWdSrc, 수령금액 ID ─

# year label ID
content = content.replace(
    """'<span style="font-size:11px;color:var(--text3)">년 · ' + yrLabel + '</span>'""",
    """'<span id="wd_yr_lbl_' + i + '" style="font-size:11px;color:var(--text3)">년 · ' + yrLabel + '</span>'""",
    1
)

# balance KR label ID
content = content.replace(
    """'<div style="font-size:10px;color:var(--text3);margin-top:2px">' + (acc.balance > 0 ? toKorean(acc.balance) : '') + '</div>'""",
    """'<div id="wd_bal_lbl_' + i + '" style="font-size:10px;color:var(--text3);margin-top:2px">' + (acc.balance > 0 ? toKorean(acc.balance) : '') + '</div>'""",
    1
)

# src1 oninput → syncWdSrc
content = content.replace(
    "oninput=\"wdAccs[' + i + '].src1=parseFloat(this.value)||0;calcWD()\"",
    "oninput=\"wdAccs[' + i + '].src1=parseFloat(this.value)||0;syncWdSrc(' + i + ')\"",
    1
)

# src2 oninput → syncWdSrc
content = content.replace(
    "oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;calcWD()\"",
    "oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;syncWdSrc(' + i + ')\"",
    1
)

# src3 oninput → syncWdSrc
content = content.replace(
    "oninput=\"wdAccs[' + i + '].src3=parseFloat(this.value)||0;calcWD()\"",
    "oninput=\"wdAccs[' + i + '].src3=parseFloat(this.value)||0;syncWdSrc(' + i + ')\"",
    1
)

# withdrawal input ID 추가
content = content.replace(
    """'<input type="number" value="' + acc.withdrawal + '" min="0" step="500000" style="width:130px;padding:4px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px" oninput="wdAccs[' + i + '].withdrawal=parseFloat(this.value)||0;calcWD()">',""",
    """'<input type="number" id="wd_wd_inp_' + i + '" value="' + acc.withdrawal + '" min="0" step="500000" style="width:130px;padding:4px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px" oninput="wdAccs[' + i + '].withdrawal=parseFloat(this.value)||0;calcWD()">',""",
    1
)

# ── 4. calcWD: isPre2013 자동 계산 ────────────────────────────────────────
content = content.replace(
    "  var isPre2013 = $('wd_pre2013') && $('wd_pre2013').checked;",
    "  var isPre2013 = wdAccs.some(function(a) { return (a.openYear||2015) <= 2013; });",
    1
)

# ── 5. calcWD: 동적 라벨 업데이트 (루프 내 accResults.push 직후) ───────────
old_push = "    accResults.push({ label: '계좌 ' + (i+1) + ' ' + (isIRP ? 'IRP' : '연금저축'), gross: wd1+wd2+wd3, tax: tax2+tax3, eligPS: eligPS });\n  });"
new_push = """    accResults.push({ label: '계좌 ' + (i+1) + ' ' + (isIRP ? 'IRP' : '연금저축'), gross: wd1+wd2+wd3, tax: tax2+tax3, eligPS: eligPS });
    var yrLbl = $('wd_yr_lbl_' + i);
    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + (curYear - (acc.openYear||curYear)) + '년';
    var balLbl = $('wd_bal_lbl_' + i);
    if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';
  });"""
content = content.replace(old_push, new_push, 1)

# ── 6. calcWD: 매트릭스 카드 표시/숨김 + 렌더링 ─────────────────────────
content = content.replace(
    "  if ($('wd_rt_section')) $('wd_rt_section').style.display = hasRetirement ? '' : 'none';",
    """  if ($('wd_rt_section')) $('wd_rt_section').style.display = hasRetirement ? '' : 'none';
  if ($('wd_rt_matrix_card')) {
    $('wd_rt_matrix_card').style.display = hasRetirement ? '' : 'none';
    if (hasRetirement) renderMatrix('wd_rt_matrix', 'wd_rt_legend');
  }""",
    1
)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

# 검증
checks = [
    ('syncWdSrc', 'syncWdSrc 함수'),
    ('wd_yr_lbl_', '연도 라벨 ID'),
    ('wd_bal_lbl_', '잔액 라벨 ID'),
    ('wd_wd_inp_', '수령금액 입력 ID'),
    ('syncWdSrc(' , 'src oninput 연결'),
    ('wd_rt_matrix', '매트릭스 카드'),
    ('tblId || ', 'renderMatrix 파라미터'),
    ('isPre2013 = wdAccs', 'isPre2013 자동계산'),
]
for k, label in checks:
    print(label + ':', k in content)
