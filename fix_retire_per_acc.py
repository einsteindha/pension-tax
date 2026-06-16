content = open('index.html', encoding='utf-8').read()

# ── 1. wdAccs IRP 데이터: retireMode/retirePay/retireYears/retireManRate 추가
content = content.replace(
    "{ type: 'irp', openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0, retirePensionYr: 1 }",
    "{ type: 'irp', openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0, retirePensionYr: 1, retireMode: 'auto', retirePay: 0, retireYears: 20, retireManRate: 10 }",
    1
)

# ── 2. 전역 wd_rt_section HTML 블록 제거 (계좌 목록 뒤 ~ 1500만원섹션 앞)
old_rt_section = (
    '    <!-- 퇴직급여 섹션 (IRP+이연퇴직소득 있을 때 노출) -->\n'
    '    <div id="wd_rt_section" style="display:none;margin-top:10px">\n'
    '      <div class="card">\n'
    '        <div class="card-title">퇴직급여 (이연퇴직소득) 정보</div>\n'
    '        <div class="alert alert-info" style="font-size:11px;margin-bottom:12px">IRP 계좌의 이연퇴직소득 인출 시 퇴직소득세 계산에 사용됩니다.</div>\n'
    '\n'
    '        <div class="mode-toggle">\n'
    "          <button class=\"mode-btn active\" id=\"wd_rt_mAuto\" onclick=\"setWdRtMode('auto')\">자동 계산 (근속연수)</button>\n"
    "          <button class=\"mode-btn\" id=\"wd_rt_mManual\" onclick=\"setWdRtMode('manual')\">실효세율 직접 입력</button>\n"
    '        </div>\n'
    '\n'
    '        <div class="mode-panel active" id="wd_rt_autoPanel">\n'
    '          <div class="form-group">\n'
    '            <label class="form-label" for="wd_rt_pay">총 퇴직금(퇴직급여)</label>\n'
    '            <div class="kr-num" id="wd_rt_pay_kr"></div>\n'
    '            <div class="inp-wrap">\n'
    "              <input type=\"number\" id=\"wd_rt_pay\" value=\"200000000\" min=\"0\" step=\"1000000\" oninput=\"updateKR('wd_rt_pay');calcWD()\">\n"
    '              <span class="inp-unit">원</span>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="form-group">\n'
    '            <label class="form-label" for="wd_rt_years">근속연수</label>\n'
    '            <div class="inp-wrap">\n'
    '              <input type="number" id="wd_rt_years" value="20" min="1" max="50" oninput="calcWD()">\n'
    '              <span class="inp-unit">년</span>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <div class="mode-panel" id="wd_rt_manualPanel">\n'
    '          <div class="form-group">\n'
    '            <label class="form-label" for="wd_rt_pay2">총 퇴직금(퇴직급여)</label>\n'
    '            <div class="kr-num" id="wd_rt_pay2_kr"></div>\n'
    '            <div class="inp-wrap">\n'
    "              <input type=\"number\" id=\"wd_rt_pay2\" value=\"200000000\" min=\"0\" step=\"1000000\" oninput=\"updateKR('wd_rt_pay2');calcWD()\">\n"
    '              <span class="inp-unit">원</span>\n'
    '            </div>\n'
    '          </div>\n'
    '          <div class="form-group">\n'
    '            <label class="form-label" for="wd_rt_manRate">퇴직소득세 실효세율 (%)</label>\n'
    '            <div class="inp-wrap">\n'
    '              <input type="number" id="wd_rt_manRate" value="10" min="0" max="50" step="0.1" oninput="calcWD()">\n'
    '              <span class="inp-unit">%</span>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <div class="form-group" style="margin-top:8px">\n'
    '          <div class="form-hint">감면율(30/40/50%)은 위 IRP 계좌 카드의 ② 이연퇴직소득 행에서 수령연차를 직접 입력하여 설정합니다. (10년 이하→30%↓ / 11~20년→40%↓ / 21년+→50%↓)</div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '\n'
)
assert old_rt_section in content, 'wd_rt_section HTML 블록 없음!'
content = content.replace(old_rt_section, '', 1)

# ── 3. renderWdAccs: ② IRP 블록 끝에 퇴직급여 정보 서브섹션 추가
# 모드 토글을 setAccRtMode(i, isManual) 함수로 처리 (onclick 내 문자열 따옴표 충돌 방지)
old_irp_end = (
    "                '<span id=\"wd_py_lbl_' + i + '\" style=\"font-size:10px;font-weight:600;color:' + pyColor + '\">' + py + '년차 (' + pyDisc + ')</span>',\n"
    "              '</div>'\n"
    "            ].join('') : ''),"
)
new_irp_end = (
    "                '<span id=\"wd_py_lbl_' + i + '\" style=\"font-size:10px;font-weight:600;color:' + pyColor + '\">' + py + '년차 (' + pyDisc + ')</span>',\n"
    "              '</div>',\n"
    "              ((acc.src2 || 0) > 0 ? [\n"
    "                '<div style=\"margin:6px 0 4px 24px;padding:8px 10px;background:rgba(43,94,167,.06);border-radius:var(--radius);border:1px solid rgba(43,94,167,.2)\">',\n"
    "                  '<div style=\"font-size:10px;font-weight:700;color:var(--blue);margin-bottom:6px\">퇴직급여 세금 정보</div>',\n"
    "                  '<div style=\"display:flex;gap:4px;margin-bottom:7px\">',\n"
    "                    '<button style=\"' + (acc.retireMode !== 'manual' ? 'background:var(--blue);color:#fff' : 'background:var(--bg3);color:var(--text2)') + ';font-size:10px;padding:3px 9px;border:1px solid var(--border2);border-radius:var(--radius);cursor:pointer\" onclick=\"setAccRtMode(' + i + ',0)\">자동 (근속연수)</button>',\n"
    "                    '<button style=\"' + (acc.retireMode === 'manual' ? 'background:var(--blue);color:#fff' : 'background:var(--bg3);color:var(--text2)') + ';font-size:10px;padding:3px 9px;border:1px solid var(--border2);border-radius:var(--radius);cursor:pointer\" onclick=\"setAccRtMode(' + i + ',1)\">실효세율 직접입력</button>',\n"
    "                  '</div>',\n"
    "                  '<div style=\"display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end\">',\n"
    "                    '<div>',\n"
    "                      '<div style=\"font-size:10px;color:var(--text3);margin-bottom:2px\">총 퇴직금</div>',\n"
    "                      '<div style=\"display:flex;align-items:center;gap:3px\">',\n"
    "                        '<input type=\"number\" value=\"' + (acc.retirePay || 0) + '\" min=\"0\" step=\"1000000\" style=\"width:120px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].retirePay=parseFloat(this.value)||0;calcWD()\">',\n"
    "                        '<span style=\"font-size:11px;color:var(--text3)\">원</span>',\n"
    "                      '</div>',\n"
    "                    '</div>',\n"
    "                    (acc.retireMode !== 'manual' ? [\n"
    "                      '<div>',\n"
    "                        '<div style=\"font-size:10px;color:var(--text3);margin-bottom:2px\">근속연수</div>',\n"
    "                        '<div style=\"display:flex;align-items:center;gap:3px\">',\n"
    "                          '<input type=\"number\" value=\"' + (acc.retireYears || 20) + '\" min=\"1\" max=\"50\" style=\"width:55px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px;text-align:center\" oninput=\"wdAccs[' + i + '].retireYears=parseInt(this.value)||1;calcWD()\">',\n"
    "                          '<span style=\"font-size:11px;color:var(--text3)\">년</span>',\n"
    "                        '</div>',\n"
    "                      '</div>',\n"
    "                    ].join('') : [\n"
    "                      '<div>',\n"
    "                        '<div style=\"font-size:10px;color:var(--text3);margin-bottom:2px\">실효세율</div>',\n"
    "                        '<div style=\"display:flex;align-items:center;gap:3px\">',\n"
    "                          '<input type=\"number\" value=\"' + (acc.retireManRate || 10) + '\" min=\"0\" max=\"50\" step=\"0.1\" style=\"width:55px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px;text-align:center\" oninput=\"wdAccs[' + i + '].retireManRate=parseFloat(this.value)||0;calcWD()\">',\n"
    "                          '<span style=\"font-size:11px;color:var(--text3)\">%</span>',\n"
    "                        '</div>',\n"
    "                      '</div>',\n"
    "                    ].join('')),\n"
    "                  '</div>',\n"
    "                  '<div id=\"wd_rt_result_' + i + '\" style=\"font-size:10px;color:var(--text3);margin-top:6px;padding-top:5px;border-top:1px solid rgba(43,94,167,.15)\">퇴직소득세: —</div>',\n"
    "                '</div>'\n"
    "              ].join('') : ''),\n"
    "            ].join('') : ''),"
)
assert old_irp_end in content, '② IRP 블록 끝 패턴 없음!'
content = content.replace(old_irp_end, new_irp_end, 1)

# ── 4. setAccRtMode 헬퍼 함수 추가 (setWdRtMode 뒤에)
old_set_mode = (
    "function setWdRtMode(mode) {\n"
    "  $('wd_rt_mAuto').classList.toggle('active', mode === 'auto');\n"
    "  $('wd_rt_mManual').classList.toggle('active', mode === 'manual');\n"
    "  $('wd_rt_autoPanel').classList.toggle('active', mode === 'auto');\n"
    "  $('wd_rt_manualPanel').classList.toggle('active', mode === 'manual');\n"
    "  calcWD();\n"
    "}"
)
new_set_mode = (
    "function setAccRtMode(i, isManual) {\n"
    "  wdAccs[i].retireMode = isManual ? 'manual' : 'auto';\n"
    "  renderWdAccs();\n"
    "  calcWD();\n"
    "}"
)
assert old_set_mode in content, 'setWdRtMode 함수 없음!'
content = content.replace(old_set_mode, new_set_mode, 1)

# ── 5. calcWD: 전역 퇴직소득세 블록 → 제거, totalSrc2/hasRetirement 만 유지
old_calc_rt_block = (
    "  // 퇴직소득세\n"
    "  var isWdRtAuto = $('wd_rt_mAuto') && $('wd_rt_mAuto').classList.contains('active');\n"
    "  var rtPayTotal = 0, rtTotalTax = 0;\n"
    "  if (isWdRtAuto) {\n"
    "    rtPayTotal = parseFloat($('wd_rt_pay').value) || 0;\n"
    "    var rtRes = calcRetirementTax(rtPayTotal, parseFloat($('wd_rt_years').value) || 20);\n"
    "    rtTotalTax = rtRes.total;\n"
    "  } else {\n"
    "    rtPayTotal = parseFloat($('wd_rt_pay2').value) || 0;\n"
    "    rtTotalTax = rtPayTotal * ((parseFloat($('wd_rt_manRate').value) || 0) / 100);\n"
    "  }\n"
    "\n"
    "  var totalSrc2 = wdAccs.reduce(function(s, a) { return s + (a.type === 'irp' ? (a.src2 || 0) : 0); }, 0);\n"
    "  var hasRetirement = totalSrc2 > 0;\n"
    "  if ($('wd_rt_section')) $('wd_rt_section').style.display = hasRetirement ? '' : 'none';\n"
    "  if ($('wd_rt_matrix_card')) {\n"
    "    $('wd_rt_matrix_card').style.display = hasRetirement ? '' : 'none';\n"
    "    if (hasRetirement) renderMatrix('wd_rt_matrix', 'wd_rt_legend');\n"
    "  }"
)
new_calc_rt_block = (
    "  var totalSrc2 = wdAccs.reduce(function(s, a) { return s + (a.type === 'irp' ? (a.src2 || 0) : 0); }, 0);\n"
    "  var hasRetirement = totalSrc2 > 0;\n"
    "  if ($('wd_rt_matrix_card')) {\n"
    "    $('wd_rt_matrix_card').style.display = hasRetirement ? '' : 'none';\n"
    "    if (hasRetirement) renderMatrix('wd_rt_matrix', 'wd_rt_legend');\n"
    "  }"
)
assert old_calc_rt_block in content, 'calcWD 전역 퇴직소득세 블록 없음!'
content = content.replace(old_calc_rt_block, new_calc_rt_block, 1)

# ── 6. calcWD forEach: tax2 전역 배분 → 계좌별 직접 계산
old_tax2 = "    var tax2 = (wd2 > 0 && totalSrc2 > 0) ? (wd2 / totalSrc2) * rtTotalTax * (1 - accDiscount) : 0;"
new_tax2 = (
    "    var accRtPay = isIRP ? (acc.retirePay || 0) : 0;\n"
    "    var accRtTax = 0;\n"
    "    if (isIRP && wd2 > 0 && accRtPay > 0) {\n"
    "      if ((acc.retireMode || 'auto') === 'manual') {\n"
    "        accRtTax = accRtPay * ((acc.retireManRate || 0) / 100);\n"
    "      } else {\n"
    "        var rtCalc = calcRetirementTax(accRtPay, acc.retireYears || 20);\n"
    "        accRtTax = rtCalc.total;\n"
    "      }\n"
    "    }\n"
    "    var tax2 = (wd2 > 0 && accRtPay > 0) ? (wd2 / accRtPay) * accRtTax * (1 - accDiscount) : 0;"
)
assert old_tax2 in content, 'tax2 계산 라인 없음!'
content = content.replace(old_tax2, new_tax2, 1)

# ── 7. calcWD forEach 라벨 끝: wd_rt_result_i 업데이트 추가
old_lbl_tail = (
    "    var pyLblEl = $('wd_py_lbl_' + i);\n"
    "    if (pyLblEl && isIRP) {\n"
    "      var curPY = acc.retirePensionYr || 1;\n"
    "      pyLblEl.textContent = curPY + '년차 (' + (curPY <= 10 ? '30%↓' : curPY <= 20 ? '40%↓' : '50%↓') + ')';\n"
    "      pyLblEl.style.color = curPY <= 10 ? 'var(--blue)' : curPY <= 20 ? 'var(--green)' : 'var(--gold)';\n"
    "    }\n"
    "  });"
)
new_lbl_tail = (
    "    var pyLblEl = $('wd_py_lbl_' + i);\n"
    "    if (pyLblEl && isIRP) {\n"
    "      var curPY = acc.retirePensionYr || 1;\n"
    "      pyLblEl.textContent = curPY + '년차 (' + (curPY <= 10 ? '30%↓' : curPY <= 20 ? '40%↓' : '50%↓') + ')';\n"
    "      pyLblEl.style.color = curPY <= 10 ? 'var(--blue)' : curPY <= 20 ? 'var(--green)' : 'var(--gold)';\n"
    "    }\n"
    "    var rtResEl = $('wd_rt_result_' + i);\n"
    "    if (rtResEl && isIRP) {\n"
    "      if (accRtPay > 0) {\n"
    "        var effRate = accRtTax > 0 ? (accRtTax / accRtPay * 100).toFixed(1) : '0.0';\n"
    "        rtResEl.textContent = '퇴직소득세 기준: ' + fmt(Math.round(accRtTax)) + ' (실효 ' + effRate + '%) · 이번 인출분: ' + fmt(Math.round(tax2));\n"
    "      } else {\n"
    "        rtResEl.textContent = '총 퇴직금 금액을 입력해주세요';\n"
    "      }\n"
    "    }\n"
    "  });"
)
assert old_lbl_tail in content, 'pyLblEl 블록 끝 없음!'
content = content.replace(old_lbl_tail, new_lbl_tail, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ("retirePay: 0", 'retirePay 필드'),
    ("retireMode: 'auto'", 'retireMode 필드'),
    ('setAccRtMode', 'setAccRtMode 함수'),
    ('wd_rt_result_', '퇴직결과 라벨 ID'),
    ('accRtPay', '계좌별 accRtPay'),
    ('accRtTax', '계좌별 accRtTax'),
    ('rtTotalTax', '전역 rtTotalTax 잔존'),
    ('wd_rt_section', 'wd_rt_section 잔존'),
    ('setWdRtMode', 'setWdRtMode 잔존'),
]
for k, label in checks:
    found = k in content
    should_absent = k in ('rtTotalTax', 'wd_rt_section', 'setWdRtMode')
    ok = not found if should_absent else found
    mark = 'OK' if ok else 'NG'
    print(mark, label + ':', found)
