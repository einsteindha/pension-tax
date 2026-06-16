content = open('index.html', encoding='utf-8').read()

# ── 1. wdAccs 데이터: IRP에 retirePensionYr 추가 ──────────────────────────
content = content.replace(
    "{ type: 'irp', openYear: 2015, balance: 300000000, src1: 10000000, src2: 200000000, src3: 90000000, withdrawal: 12000000 }",
    "{ type: 'irp', openYear: 2015, balance: 300000000, src1: 10000000, src2: 200000000, src3: 90000000, withdrawal: 12000000, retirePensionYr: 1 }",
    1
)

# ── 2. renderWdAccs 맵 콜백: py/pyDisc/pyColor 변수 추가 ─────────────────
content = content.replace(
    "    var color = isIRP ? 'var(--blue)' : 'var(--gold)';\n    return [",
    "    var color = isIRP ? 'var(--blue)' : 'var(--gold)';\n"
    "    var py = acc.retirePensionYr || 1;\n"
    "    var pyDisc = py <= 10 ? '30%↓' : py <= 20 ? '40%↓' : '50%↓';\n"
    "    var pyColor = py <= 10 ? 'var(--blue)' : py <= 20 ? 'var(--green)' : 'var(--gold)';\n"
    "    return [",
    1
)

# ── 3. ② 이연퇴직소득 행: 수령연차 입력 추가 ───────────────────────────────
old_src2_row = (
    "              '<input type=\"number\" value=\"' + acc.src2 + '\" min=\"0\" step=\"1000000\" style=\"width:120px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                '<span style=\"font-size:11px;color:var(--text3)\">원</span>',\n"
    "              '</div>'"
)
new_src2_row = (
    "              '<input type=\"number\" value=\"' + acc.src2 + '\" min=\"0\" step=\"1000000\" style=\"width:120px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                '<span style=\"font-size:11px;color:var(--text3)\">원</span>',\n"
    "                '<span style=\"font-size:11px;color:var(--border2);padding:0 3px\">|</span>',\n"
    "                '<span style=\"font-size:11px;color:var(--text2)\">수령</span>',\n"
    "                '<input type=\"number\" value=\"' + py + '\" min=\"1\" max=\"50\" style=\"width:42px;padding:3px 4px;border:1px solid var(--border2);border-radius:2px;font-size:12px;text-align:center\" oninput=\"wdAccs[' + i + '].retirePensionYr=parseInt(this.value)||1;calcWD()\">',\n"
    "                '<span id=\"wd_py_lbl_' + i + '\" style=\"font-size:10px;font-weight:600;color:' + pyColor + '\">' + py + '년차 (' + pyDisc + ')</span>',\n"
    "              '</div>'"
)
assert old_src2_row in content, "② src2 행 없음!"
content = content.replace(old_src2_row, new_src2_row, 1)

# ── 4. HTML 라디오 버튼 그룹 → 안내 메시지로 교체 ──────────────────────────
old_radio = (
    '        <div class="form-group" style="margin-top:8px">\n'
    '          <label class="form-label">이번 인출 연차 (감면율 결정)</label>\n'
    '          <div class="radio-group">\n'
    '            <div class="radio-opt">\n'
    '              <input type="radio" name="wd_rtPY" id="wd_rtpy_u10" value="u10" checked onchange="calcWD()">\n'
    '              <label for="wd_rtpy_u10">10년 이하 수령 (30%↓)</label>\n'
    '            </div>\n'
    '            <div class="radio-opt">\n'
    '              <input type="radio" name="wd_rtPY" id="wd_rtpy_u20" value="u20" onchange="calcWD()">\n'
    '              <label for="wd_rtpy_u20">10~20년 수령 (40%↓)</label>\n'
    '            </div>\n'
    '            <div class="radio-opt">\n'
    '              <input type="radio" name="wd_rtPY" id="wd_rtpy_o20" value="o20" onchange="calcWD()">\n'
    '              <label for="wd_rtpy_o20">20년 초과 수령 (50%↓)</label>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="form-hint">실제 인출한 해를 카운팅. 수령 기간이 총 몇 년에 걸치는지가 감면율을 결정합니다.</div>\n'
    '        </div>'
)
new_radio = (
    '        <div class="form-group" style="margin-top:8px">\n'
    '          <div class="form-hint">감면율(30/40/50%)은 위 IRP 계좌 카드의 ② 이연퇴직소득 행에서 수령연차를 직접 입력하여 설정합니다. (10년 이하→30%↓ / 11~20년→40%↓ / 21년+→50%↓)</div>\n'
    '        </div>'
)
assert old_radio in content, "라디오 버튼 그룹 없음!"
content = content.replace(old_radio, new_radio, 1)

# ── 5. calcWD: 글로벌 rtDiscount 제거 ─────────────────────────────────────
content = content.replace(
    "  var rtDiscount = $('wd_rtpy_u10').checked ? 0.30 : ($('wd_rtpy_u20').checked ? 0.40 : 0.50);\n",
    "",
    1
)

# ── 6. calcWD forEach: tax2 계산을 계좌별 수령연차 기반으로 변경 ─────────────
old_tax2 = "    var tax2 = (wd2 > 0 && totalSrc2 > 0) ? (wd2 / totalSrc2) * rtTotalTax * (1 - rtDiscount) : 0;"
new_tax2 = (
    "    var accPY = isIRP ? (acc.retirePensionYr || 1) : 1;\n"
    "    var accDiscount = accPY <= 10 ? 0.30 : accPY <= 20 ? 0.40 : 0.50;\n"
    "    var tax2 = (wd2 > 0 && totalSrc2 > 0) ? (wd2 / totalSrc2) * rtTotalTax * (1 - accDiscount) : 0;"
)
assert old_tax2 in content, "tax2 계산 없음!"
content = content.replace(old_tax2, new_tax2, 1)

# ── 7. calcWD forEach 라벨 업데이트: wd_py_lbl 추가 ──────────────────────
old_lbl_end = (
    "    var wdLblEl = $('wd_wd_lbl_' + i);\n"
    "    if (wdLblEl) wdLblEl.textContent = '원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '');\n"
    "  });"
)
new_lbl_end = (
    "    var wdLblEl = $('wd_wd_lbl_' + i);\n"
    "    if (wdLblEl) wdLblEl.textContent = '원' + (acc.withdrawal > 0 ? ' · ' + toKorean(acc.withdrawal) : '');\n"
    "    var pyLblEl = $('wd_py_lbl_' + i);\n"
    "    if (pyLblEl && isIRP) {\n"
    "      var curPY = acc.retirePensionYr || 1;\n"
    "      pyLblEl.textContent = curPY + '년차 (' + (curPY <= 10 ? '30%↓' : curPY <= 20 ? '40%↓' : '50%↓') + ')';\n"
    "      pyLblEl.style.color = curPY <= 10 ? 'var(--blue)' : curPY <= 20 ? 'var(--green)' : 'var(--gold)';\n"
    "    }\n"
    "  });"
)
assert old_lbl_end in content, "calcWD 라벨 끝 없음!"
content = content.replace(old_lbl_end, new_lbl_end, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ('retirePensionYr', 'retirePensionYr 필드'),
    ('wd_py_lbl_', '수령연차 라벨 ID'),
    ('accDiscount', '계좌별 discount'),
    ('pyDisc', 'pyDisc 변수'),
    ('wd_rtpy_u10', '라디오버튼 잔존여부'),
]
for k, label in checks:
    print(label + ':', k in content)
