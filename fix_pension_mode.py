content = open('index.html', encoding='utf-8').read()

# ── 1. wdAccs: 연금저축에 lifeAnnuity 필드 추가 ──────────────────────────
content = content.replace(
    "{ type: 'ps',  openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0 }",
    "{ type: 'ps',  openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0, lifeAnnuity: false }",
    1
)

# ── 2. HTML: "수령 방법" radio 제거 ─────────────────────────────────────
old_method = (
    '\n      <div class="form-group">\n'
    '        <label class="form-label">수령 방법</label>\n'
    '        <div class="radio-group">\n'
    '          <div class="radio-opt">\n'
    '            <input type="radio" name="wd_method" id="wd_pension" value="pension" checked onchange="calcWD()">\n'
    '            <label for="wd_pension">연금 수령</label>\n'
    '          </div>\n'
    '          <div class="radio-opt">\n'
    '            <input type="radio" name="wd_method" id="wd_lump" value="lump" onchange="calcWD()">\n'
    '            <label for="wd_lump">일시금 (해지)</label>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="form-hint">일시금 선택 시 ③ 재원에 기타소득세 16.5% 적용</div>\n'
    '      </div>\n'
)
assert old_method in content, '수령 방법 radio 없음!'
content = content.replace(old_method, '\n', 1)

# ── 3. HTML: "연금 유형" 라디오(wd_pension_opts) 제거 ────────────────────
old_ptype = (
    '\n      <div id="wd_pension_opts">\n'
    '        <div class="form-group">\n'
    '          <label class="form-label">연금 유형</label>\n'
    '          <div class="radio-group">\n'
    '            <div class="radio-opt">\n'
    '              <input type="radio" name="wd_ptype" id="wd_fixed" value="fixed" checked onchange="calcWD()">\n'
    '              <label for="wd_fixed">확정기간형</label>\n'
    '            </div>\n'
    '            <div class="radio-opt">\n'
    '              <input type="radio" name="wd_ptype" id="wd_life" value="life" onchange="calcWD()">\n'
    '              <label for="wd_life">종신수령</label>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="form-hint">종신수령: 나이와 무관하게 4.4% 고정</div>\n'
    '        </div>\n'
    '\n'
    '      </div>\n'
)
assert old_ptype in content, '연금 유형 radio 없음!'
content = content.replace(old_ptype, '\n', 1)

# ── 4. renderWdAccs 카드 헤더: 자격 뱃지 추가 ────────────────────────────
old_hdr = (
    "'<span style=\"font-size:12px;font-weight:700;color:var(--text2)\">계좌 ' + (i+1) + ' <span style=\"color:' + color + '\">' + (isIRP ? 'IRP' : '연금저축') + '</span></span>',\n"
    "          '<div style=\"display:flex;gap:8px;align-items:center\">',"
)
new_hdr = (
    "'<span style=\"font-size:12px;font-weight:700;color:var(--text2)\">계좌 ' + (i+1) + ' <span style=\"color:' + color + '\">' + (isIRP ? 'IRP' : '연금저축') + '</span></span>',\n"
    "          '<span id=\"wd_elig_badge_' + i + '\" style=\"font-size:9px;padding:2px 6px;border-radius:10px;background:var(--bg2);color:var(--text3)\">—</span>',\n"
    "          '<div style=\"display:flex;gap:8px;align-items:center\">',"
)
assert old_hdr in content, '카드 헤더 없음!'
content = content.replace(old_hdr, new_hdr, 1)

# ── 5. renderWdAccs: 연금저축 종신수령 체크박스 (인출금액 헤더 바로 전) ──────
old_before_src = (
    "          '</div>',\n"
    "          '<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:4px\">인출금액 (순서: ①→②→③)</div>',"
)
new_before_src = (
    "          '</div>',\n"
    "          (!isIRP ? '<div style=\"display:flex;align-items:center;gap:6px;margin-bottom:8px;padding:5px 8px;background:var(--bg3);border-radius:var(--radius)\">' +\n"
    "            '<label style=\"font-size:11px;color:var(--text2);display:flex;align-items:center;gap:5px;cursor:pointer\">' +\n"
    "            '<input type=\"checkbox\" ' + (acc.lifeAnnuity ? 'checked' : '') + ' style=\"cursor:pointer\" onchange=\"wdAccs[' + i + '].lifeAnnuity=this.checked;calcWD()\">' +\n"
    "            '종신수령 <span style=\"font-size:10px;color:var(--text3)\">(4.4% 고정 · 80세+ 시 확정기간형보다 불리)</span>' +\n"
    "            '</label></div>' : ''),\n"
    "          '<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:4px\">인출금액 (순서: ①→②→③)</div>',"
)
assert old_before_src in content, '인출금액 헤더 바로 전 없음!'
content = content.replace(old_before_src, new_before_src, 1)

# ── 6. calcWD JS: isPension/isLife/pensionRate 글로벌 변수 제거 ─────────────
old_global = (
    "  var isPension = $('wd_pension').checked;\n"
    "  var isLife    = isPension && $('wd_life') && $('wd_life').checked;\n"
    "  var isPre2013 = wdAccs.some(function(a) { return (a.openYear||2015) <= 2013; });\n"
    "  var pensionRate = isLife ? 0.044 : (age >= 80 ? 0.033 : age >= 70 ? 0.044 : 0.055);"
)
new_global = (
    "  var isPre2013 = wdAccs.some(function(a) { return (a.openYear||2015) <= 2013; });"
)
assert old_global in content, 'isPension 글로벌 없음!'
content = content.replace(old_global, new_global, 1)

# ── 7. calcWD: totalEligWd3 집계 초기화 추가 ─────────────────────────────
old_totals = (
    "  var totalBal = 0, totalGross = 0;\n"
    "  var totalTax2 = 0, totalTax3 = 0;\n"
    "  var totalWd1 = 0, totalWd2 = 0, totalWd3 = 0;"
)
new_totals = (
    "  var totalBal = 0, totalGross = 0;\n"
    "  var totalTax2 = 0, totalTax3 = 0;\n"
    "  var totalWd1 = 0, totalWd2 = 0, totalWd3 = 0;\n"
    "  var totalEligWd3 = 0;"
)
assert old_totals in content, 'totals 초기화 없음!'
content = content.replace(old_totals, new_totals, 1)

# ── 8. calcWD forEach: tax3 계산을 계좌별로, eligWd3 집계 추가 ──────────────
old_tax3 = (
    "    totalWd1 += wd1; totalWd2 += wd2; totalWd3 += wd3;\n"
    "    totalGross += (wd1 + wd2 + wd3);\n"
    "    var accPY = isIRP ? (acc.retirePensionYr || 1) : 1;\n"
    "    var accDiscount = accPY <= 10 ? 0.30 : accPY <= 20 ? 0.40 : 0.50;\n"
    "    var tax2 = (wd2 > 0 && totalSrc2 > 0) ? (wd2 / totalSrc2) * rtTotalTax * (1 - accDiscount) : 0;\n"
    "    var tax3;\n"
    "    if (!isPension || !eligPS) { tax3 = wd3 * 0.165; }\n"
    "    else { tax3 = wd3 * pensionRate; }"
)
new_tax3 = (
    "    totalWd1 += wd1; totalWd2 += wd2; totalWd3 += wd3;\n"
    "    totalGross += (wd1 + wd2 + wd3);\n"
    "    var accPY = isIRP ? (acc.retirePensionYr || 1) : 1;\n"
    "    var accDiscount = accPY <= 10 ? 0.30 : accPY <= 20 ? 0.40 : 0.50;\n"
    "    var tax2 = (wd2 > 0 && totalSrc2 > 0) ? (wd2 / totalSrc2) * rtTotalTax * (1 - accDiscount) : 0;\n"
    "    var accIsLife = !isIRP && (acc.lifeAnnuity || false);\n"
    "    var accPensionRate = accIsLife ? 0.044 : (age >= 80 ? 0.033 : age >= 70 ? 0.044 : 0.055);\n"
    "    var tax3;\n"
    "    if (!eligPS) { tax3 = wd3 * 0.165; }\n"
    "    else { totalEligWd3 += wd3; tax3 = wd3 * accPensionRate; }"
)
assert old_tax3 in content, 'tax3 계산 없음!'
content = content.replace(old_tax3, new_tax3, 1)

# ── 9. calcWD forEach 라벨 업데이트: eligBadge 추가 ──────────────────────
old_badge = (
    "    var yrLbl = $('wd_yr_lbl_' + i);\n"
    "    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear||curYear)) + '년';"
)
new_badge = (
    "    var eligBadge = $('wd_elig_badge_' + i);\n"
    "    if (eligBadge) {\n"
    "      eligBadge.textContent = eligPS ? '연금소득세 ✓' : '기타소득세 16.5%';\n"
    "      eligBadge.style.background = eligPS ? 'rgba(76,175,80,.12)' : 'rgba(239,68,68,.08)';\n"
    "      eligBadge.style.color = eligPS ? 'var(--green)' : 'var(--red)';\n"
    "    }\n"
    "    var yrLbl = $('wd_yr_lbl_' + i);\n"
    "    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear||curYear)) + '년';"
)
assert old_badge in content, 'eligBadge 삽입점 없음!'
content = content.replace(old_badge, new_badge, 1)

# ── 10. over15 체크: isPension 제거 → totalEligWd3 기반 ──────────────────
content = content.replace(
    "var over15 = totalWd3 > 15000000 && isPension;",
    "var over15 = totalEligWd3 > 15000000;",
    1
)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ('lifeAnnuity', 'lifeAnnuity 필드'),
    ('wd_elig_badge_', '자격 뱃지'),
    ('accIsLife', '계좌별 종신수령'),
    ('accPensionRate', '계좌별 연금세율'),
    ('totalEligWd3', 'eligWd3 집계'),
    ('wd_pension', '수령방법 radio 잔존'),
    ('wd_pension_opts', '연금유형 div 잔존'),
]
for k, label in checks:
    found = k in content
    mark = '✓' if (found and k not in ['wd_pension','wd_pension_opts']) or (not found and k in ['wd_pension','wd_pension_opts']) else '✗'
    print(f'{mark} {label}: {found}')
