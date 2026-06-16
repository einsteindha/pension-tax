content = open('index.html', encoding='utf-8').read()

# ================================================================
# Fix 0: 퇴직급여 블록 항상 렌더 (src2=0 시 display:none)
# ================================================================
old_rt_open = (
    "              ((acc.src2 || 0) > 0 ? [\n"
    "                '<div style=\"margin:6px 0 4px 24px;padding:8px 10px;background:rgba(43,94,167,.06);border-radius:var(--radius);border:1px solid rgba(43,94,167,.2)\">',"
)
new_rt_open = (
    "              [\n"
    "                '<div id=\"wd_rt_block_' + i + '\" style=\"display:' + ((acc.src2||0) > 0 ? '' : 'none') + ';margin:6px 0 4px 24px;padding:8px 10px;background:rgba(43,94,167,.06);border-radius:var(--radius);border:1px solid rgba(43,94,167,.2)\">',"
)
assert old_rt_open in content, 'Fix0: rt_block open 패턴 없음!'
content = content.replace(old_rt_open, new_rt_open, 1)

old_rt_close = (
    "                '</div>'\n"
    "              ].join('') : ''),\n"
)
new_rt_close = (
    "                '</div>'\n"
    "              ].join(''),\n"
)
assert old_rt_close in content, 'Fix0: rt_block close 패턴 없음!'
content = content.replace(old_rt_close, new_rt_close, 1)

# calcWD forEach: rtBlock display 업데이트
old_rtblock_upd = "    var rtResEl = $('wd_rt_result_' + i);"
new_rtblock_upd = (
    "    var rtBlock = $('wd_rt_block_' + i);\n"
    "    if (rtBlock && isIRP) rtBlock.style.display = src2 > 0 ? '' : 'none';\n"
    "    var rtResEl = $('wd_rt_result_' + i);"
)
assert old_rtblock_upd in content, 'Fix0: rtResEl 삽입점 없음!'
content = content.replace(old_rtblock_upd, new_rtblock_upd, 1)

# ================================================================
# Fix 1: accRtPay 기본값 → src2 (총 퇴직금 미입력 시 이연퇴직소득 원금으로 계산)
# ================================================================
old_accrtpay = "    var accRtPay = isIRP ? (acc.retirePay || 0) : 0;"
new_accrtpay = "    var accRtPay = isIRP ? (acc.retirePay || acc.src2 || 0) : 0;"
assert old_accrtpay in content, 'Fix1: accRtPay 없음!'
content = content.replace(old_accrtpay, new_accrtpay, 1)

# ================================================================
# Fix 2: 종신수령 설명 간소화 (4.4% 고정만 표시)
# ================================================================
old_ann = "'종신수령 <span style=\"font-size:10px;color:var(--text3)\">(4.4% 고정 · 80세+ 시 확정기간형보다 불리)</span>'"
new_ann = "'종신수령 <span style=\"font-size:10px;color:var(--text3)\">(4.4% 고정)</span>'"
assert old_ann in content, 'Fix2: 종신수령 라벨 없음!'
content = content.replace(old_ann, new_ann, 1)

# ================================================================
# Fix 3: Tab 0 — 7개 카드 접기/펼치기 (existing toggleSection 재사용)
# ================================================================
def tog_title(key, text, color=None):
    span = f'<span style="color:{color}">{text}</span>' if color else f'<span>{text}</span>'
    return (
        f'        <div class="card-title" style="cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none" onclick="toggleSection(\'{key}\')">'
        f'{span}'
        f'<i id="{key}_chev" style="font-size:10px;transition:transform .2s;font-style:normal">▼</i></div>\n'
        f'        <div id="{key}_body" class="stoggle-body hidden" style="padding:0">\n'
    )

# Card 1: 납입한도 vs 세액공제한도
c = ('        <div class="card-title">납입한도 vs 세액공제한도</div>\n', 1)
assert c[0] in content, 'Fix3/C1: title'
content = content.replace(c[0], tog_title('t0_limit', '납입한도 vs 세액공제한도'), 1)

old_c1e = ('          <strong>DC형</strong> — 납입 자체 한도 없음. 세액공제는 IRP와 동일하게 900만원 한도 내 적용.\n'
           '        </div>\n      </div>')
new_c1e = ('          <strong>DC형</strong> — 납입 자체 한도 없음. 세액공제는 IRP와 동일하게 900만원 한도 내 적용.\n'
           '        </div>\n        </div>\n      </div>')
assert old_c1e in content, 'Fix3/C1: end'
content = content.replace(old_c1e, new_c1e, 1)

# Card 2: ISA 만기금 연금계좌 이전
c2t = '        <div class="card-title" style="color:var(--purple)">ISA 만기금 연금계좌 이전</div>\n'
assert c2t in content, 'Fix3/C2: title'
content = content.replace(c2t, tog_title('t0_isa', 'ISA 만기금 연금계좌 이전', 'var(--purple)'), 1)

old_c2e = ('        <div class="alert alert-info" style="margin-top:10px;font-size:11px">예) ISA 3,000만원 이전 → 300만원 추가 세액공제</div>\n'
           '      </div>')
new_c2e = ('        <div class="alert alert-info" style="margin-top:10px;font-size:11px">예) ISA 3,000만원 이전 → 300만원 추가 세액공제</div>\n'
           '        </div>\n      </div>')
assert old_c2e in content, 'Fix3/C2: end'
content = content.replace(old_c2e, new_c2e, 1)

# Card 3: 주택 다운사이징 차액 납입
c3t = '        <div class="card-title" style="color:var(--amber)">주택 다운사이징 차액 납입</div>\n'
assert c3t in content, 'Fix3/C3: title'
content = content.replace(c3t, tog_title('t0_down', '주택 다운사이징 차액 납입', 'var(--amber)'), 1)

old_c3e = ('        <div class="alert alert-warn" style="margin-top:10px;font-size:11px">세무사 또는 CFP 상담 권장</div>\n'
           '      </div>\n    </div>')
new_c3e = ('        <div class="alert alert-warn" style="margin-top:10px;font-size:11px">세무사 또는 CFP 상담 권장</div>\n'
           '        </div>\n      </div>\n    </div>')
assert old_c3e in content, 'Fix3/C3: end'
content = content.replace(old_c3e, new_c3e, 1)

# Card 4: 미국 배당 원천징수 주의 (card style="margin-top:14px")
c4t = '        <div class="card-title" style="color:var(--amber)">⚠ 미국 배당 원천징수 주의</div>\n'
assert c4t in content, 'Fix3/C4: title'
content = content.replace(c4t, tog_title('t0_div', '⚠ 미국 배당 원천징수 주의', 'var(--amber)'), 1)

old_c4e = (
    '              고배당 미국 ETF(S&P500 배당형 등)는 ISA·일반계좌 활용이 세후 수익률에 유리할 수 있음\n'
    '            </div>\n          </div>\n        </div>\n      </div>\n    </div>'
)
new_c4e = (
    '              고배당 미국 ETF(S&P500 배당형 등)는 ISA·일반계좌 활용이 세후 수익률에 유리할 수 있음\n'
    '            </div>\n          </div>\n        </div>\n        </div>\n      </div>\n    </div>'
)
assert old_c4e in content, 'Fix3/C4: end'
content = content.replace(old_c4e, new_c4e, 1)

# Card 5: 수령 조건 & 연금수령한도
c5t = '        <div class="card-title">수령 조건 & 연금수령한도</div>\n'
assert c5t in content, 'Fix3/C5: title'
content = content.replace(c5t, tog_title('t0_cond', '수령 조건 & 연금수령한도'), 1)

old_c5e = ('        <div style="font-size:11px;color:var(--text3);margin-top:5px">한도 초과 인출 시 기타소득세 16.5%</div>\n'
           '      </div>')
new_c5e = ('        <div style="font-size:11px;color:var(--text3);margin-top:5px">한도 초과 인출 시 기타소득세 16.5%</div>\n'
           '        </div>\n      </div>')
assert old_c5e in content, 'Fix3/C5: end'
content = content.replace(old_c5e, new_c5e, 1)

# Card 6: 나이별 연금소득세율
c6t = '        <div class="card-title">나이별 연금소득세율</div>\n'
assert c6t in content, 'Fix3/C6: title'
content = content.replace(c6t, tog_title('t0_rate', '나이별 연금소득세율'), 1)

old_c6e = ('        <div style="font-size:11px;color:var(--text3);margin-top:6px">종신수령은 80세 이상도 4.4% 고정 — 80세 이상은 확정기간형이 유리</div>\n'
           '      </div>')
new_c6e = ('        <div style="font-size:11px;color:var(--text3);margin-top:6px">종신수령은 80세 이상도 4.4% 고정 — 80세 이상은 확정기간형이 유리</div>\n'
           '        </div>\n      </div>')
assert old_c6e in content, 'Fix3/C6: end'
content = content.replace(old_c6e, new_c6e, 1)

# Card 7: 재원별 인출 순서 (Tab 0 버전 - 소득세법 시행령으로 구별)
old_c7t = ('        <div class="card-title">재원별 인출 순서</div>\n'
           '        <div style="font-size:11px;color:var(--text3);margin-bottom:12px">소득세법 시행령 제40조의2')
new_c7t = (tog_title('t0_ord', '재원별 인출 순서') +
           '        <div style="font-size:11px;color:var(--text3);margin-bottom:12px">소득세법 시행령 제40조의2')
assert old_c7t in content, 'Fix3/C7: title'
content = content.replace(old_c7t, new_c7t, 1)

old_c7e = (
    '          <strong>인출 순서:</strong> ① 세액공제X 원금(비과세, ISA 원금·다운사이징 포함) → ② 이연퇴직소득(퇴직소득세, IRP만) → ③ 세액공제O 원금+운용수익(연금소득세, ISA 수익분 포함)\n'
    '        </div>\n      </div>\n    </div>\n\n  </div><!-- /flow-wrap -->'
)
new_c7e = (
    '          <strong>인출 순서:</strong> ① 세액공제X 원금(비과세, ISA 원금·다운사이징 포함) → ② 이연퇴직소득(퇴직소득세, IRP만) → ③ 세액공제O 원금+운용수익(연금소득세, ISA 수익분 포함)\n'
    '        </div>\n        </div>\n      </div>\n    </div>\n\n  </div><!-- /flow-wrap -->'
)
assert old_c7e in content, 'Fix3/C7: end'
content = content.replace(old_c7e, new_c7e, 1)

# ================================================================
# Fix 4: 탭4 제목 변경 → "퇴직소득 실효세율"
# ================================================================
old_tab4 = '>④ 퇴직급여 계산</button>'
new_tab4 = '>④ 퇴직소득 실효세율</button>'
assert old_tab4 in content, 'Fix4: tab4 title'
content = content.replace(old_tab4, new_tab4, 1)

# ================================================================
# Fix 5: 탭4 인출계획 카드 제거 + switchTab에서 renderWdTable 제거
# ================================================================
old_plan = (
    '\n    <div class="card">\n'
    '      <div class="card-title">인출 계획</div>\n'
    '      <div class="form-group">\n'
    '        <label class="form-label">총 수령 기간 (감면율 결정)</label>\n'
    '        <div class="radio-group">\n'
    '          <div class="radio-opt">\n'
    '            <input type="radio" name="rtPY" id="rtpy_u10" value="u10" checked onchange="calcRT()">\n'
    '            <label for="rtpy_u10">10년 이하 (30%↓)</label>\n'
    '          </div>\n'
    '          <div class="radio-opt">\n'
    '            <input type="radio" name="rtPY" id="rtpy_u20" value="u20" onchange="calcRT()">\n'
    '            <label for="rtpy_u20">10~20년 (40%↓)</label>\n'
    '          </div>\n'
    '          <div class="radio-opt">\n'
    '            <input type="radio" name="rtPY" id="rtpy_o20" value="o20" onchange="calcRT()">\n'
    '            <label for="rtpy_o20">20년 초과 (50%↓)</label>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="form-hint">2026년 기준. 총 수령 기간에 따라 감면율 결정.</div>\n'
    '      </div>\n'
    '      <hr class="divider">\n'
    '      <div class="sub-title">연차별 인출 금액</div>\n'
    '      <div class="alert alert-info" style="font-size:11px;margin-bottom:10px">\n'
    '        각 연차 인출 세금 = 퇴직소득세 × (인출액 ÷ 총 퇴직금) × (1 − 감면율)\n'
    '      </div>\n'
    '      <table class="wd-table">\n'
    '        <thead>\n'
    '          <tr><th>수령 연차</th><th>인출금액 (원)</th><th>퇴직소득세</th><th>세후 수령액</th><th></th></tr>\n'
    '        </thead>\n'
    '        <tbody id="wd_tbody"></tbody>\n'
    '        <tfoot id="wd_tfoot"></tfoot>\n'
    '      </table>\n'
    '      <button class="wd-add-btn" onclick="addWdRow()">+ 연차 추가</button>\n'
    '      <div class="form-hint" style="margin-top:8px" id="wd_remaining"></div>\n'
    '    </div>\n'
    '  </div>'
)
new_plan = '\n  </div>'
assert old_plan in content, 'Fix5: 인출계획 카드 없음!'
content = content.replace(old_plan, new_plan, 1)

# switchTab에서 renderWdTable 호출 제거
content = content.replace(
    'if (idx === 3) { renderMatrix(); renderWdTable(); }',
    'if (idx === 3) { renderMatrix(); calcRT(); }',
    1
)
# 초기화 코드에서 renderWdTable 제거
content = content.replace('\nrenderWdTable();\n', '\n', 1)

# ================================================================
# Fix 6a: 탭4 결과 HTML — 3개 rrow 제거 + cmp-grid 제거 + 감면율 테이블 추가
# ================================================================
old_result_rows = (
    '      <div class="rrow">\n'
    '        <span class="rrow-label">연금 수령 시 납부세액</span>\n'
    '        <span class="rrow-val blue" id="rt_pensionTax">—</span>\n'
    '      </div>\n'
    '      <div class="rrow">\n'
    '        <span class="rrow-label">연금 전환으로 절감되는 세금</span>\n'
    '        <span class="rrow-val green" id="rt_saved">—</span>\n'
    '      </div>\n'
    '      <div class="rrow">\n'
    '        <span class="rrow-label">절세율</span>\n'
    '        <span class="rrow-val green" id="rt_savedRate">—</span>\n'
    '      </div>\n'
    '\n'
    '      <div class="breakdown" id="rt_breakdown" style="display:none">'
)
new_result_rows = '      <div class="breakdown" id="rt_breakdown" style="display:none">'
assert old_result_rows in content, 'Fix6a: rrow 제거 대상 없음!'
content = content.replace(old_result_rows, new_result_rows, 1)

old_cmp_grid = (
    '      <div style="margin-top:14px">\n'
    '        <div class="cmp-grid">\n'
    '          <div class="cmp-card" id="rt_lumpCard">\n'
    '            <div class="cmp-label">일시금 수령</div>\n'
    '            <div class="cmp-value" id="rt_lumpNet">—</div>\n'
    '            <div class="cmp-detail">세금 전액 납부</div>\n'
    '          </div>\n'
    '          <div class="cmp-card winner" id="rt_pensionCard">\n'
    '            <div class="cmp-label">연금 수령</div>\n'
    '            <div class="cmp-value" id="rt_pensionNet">—</div>\n'
    '            <div class="cmp-detail" id="rt_pensionDetail">—</div>\n'
    '            <div class="badge-win" id="rt_discountBadge">—</div>\n'
    '          </div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '\n'
    '</div>'
)
new_cmp_grid = (
    '      <div style="margin-top:14px">\n'
    '        <div class="sub-title" style="margin-bottom:8px">수령 기간별 실효세율 비교</div>\n'
    '        <table style="width:100%;font-size:11px;border-collapse:collapse">\n'
    '          <thead>\n'
    '            <tr style="background:var(--bg3)">\n'
    '              <th style="padding:6px 8px;text-align:left;border:1px solid var(--border2);font-weight:600">수령 방법</th>\n'
    '              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">감면율</th>\n'
    '              <th style="padding:6px 8px;text-align:right;border:1px solid var(--border2);font-weight:600">납부 세금</th>\n'
    '              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">실효세율</th>\n'
    '              <th style="padding:6px 8px;text-align:right;border:1px solid var(--border2);font-weight:600">세후 수령</th>\n'
    '            </tr>\n'
    '          </thead>\n'
    '          <tbody>\n'
    '            <tr>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2)">일시금 수령</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--text3)">없음</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--red)" id="rt_lump_tax">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center" id="rt_lump_eff">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600" id="rt_lump_net">—</td>\n'
    '            </tr>\n'
    '            <tr style="background:rgba(42,124,111,.04)">\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2)">10년 이하 수령</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">30%↓</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d30_tax">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d30_eff">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d30_net">—</td>\n'
    '            </tr>\n'
    '            <tr style="background:rgba(42,124,111,.07)">\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2)">10~20년 수령</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">40%↓</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d40_tax">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d40_eff">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d40_net">—</td>\n'
    '            </tr>\n'
    '            <tr style="background:rgba(42,124,111,.11)">\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2)">20년 초과 수령</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">50%↓</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d50_tax">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d50_eff">—</td>\n'
    '              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d50_net">—</td>\n'
    '            </tr>\n'
    '          </tbody>\n'
    '        </table>\n'
    '        <div class="form-hint" style="margin-top:6px">감면율은 실제 수령 기간 합산 기준 적용. 연금수령한도 초과 시 해당 부분은 감면 소멸.</div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '\n'
    '</div>'
)
assert old_cmp_grid in content, 'Fix6a: cmp-grid 없음!'
content = content.replace(old_cmp_grid, new_cmp_grid, 1)

# ================================================================
# Fix 6b: calcRT() 재작성 — discount 라디오 제거, wdRows forEach 제거, 새 테이블 업데이트
# ================================================================
old_calcRT = (
    'function calcRT() {\n'
    '  var isAuto = $(\'rt_mAuto\').classList.contains(\'active\');\n'
    '  var discount = $(\'rtpy_u10\').checked ? 0.30 : ($(\'rtpy_u20\').checked ? 0.40 : 0.50);\n'
    '  var pay, totalTax, rate, showBreakdown;\n'
    '\n'
    '  if (isAuto) {\n'
    '    pay = v(\'rt_pay\');\n'
    '    var years = v(\'rt_years\');\n'
    '    var res = calcRetirementTax(pay, years);\n'
    '    totalTax = res.total; rate = res.rate; showBreakdown = true;\n'
    '    $(\'rt_b_pay\').textContent  = fmt(pay);\n'
    '    $(\'rt_b_ysd\').textContent  = fmt(res.ysD);\n'
    '    $(\'rt_b_conv\').textContent = fmt(res.conv);\n'
    '    $(\'rt_b_cd\').textContent   = fmt(res.cD);\n'
    '    $(\'rt_b_base\').textContent = fmt(res.taxBase);\n'
    '    $(\'rt_b_tax\').textContent  = fmt(res.total);\n'
    '  } else {\n'
    '    pay = v(\'rt_pay2\');\n'
    '    totalTax = pay * (v(\'rt_manRate\') / 100);\n'
    '    rate = v(\'rt_manRate\');\n'
    '    showBreakdown = false;\n'
    '  }\n'
    '\n'
    '  $(\'rt_breakdown\').style.display = showBreakdown ? \'\' : \'none\';\n'
    '\n'
    '  var totalWd = 0, totalWdTax = 0;\n'
    '  wdRows.forEach(function(r, i) {\n'
    '    var rowTax = pay > 0 ? (r.amt / pay) * totalTax * (1 - discount) : 0;\n'
    '    var rowNet = r.amt - rowTax;\n'
    '    totalWd += r.amt; totalWdTax += rowTax;\n'
    '    var tEl = $(\'wd_tax_\' + i), nEl = $(\'wd_net_\' + i);\n'
    '    if (tEl) tEl.textContent = r.amt > 0 ? fmt(rowTax) : \'—\';\n'
    '    if (nEl) nEl.textContent = r.amt > 0 ? fmt(rowNet) : \'—\';\n'
    '  });\n'
    '\n'
    '  var tfoot = $(\'wd_tfoot\');\n'
    '  if (tfoot && wdRows.length > 0) {\n'
    '    tfoot.innerHTML = \'<tr><td style="text-align:center">합계</td><td style="text-align:right">\' + fmt(totalWd) + \'</td><td style="text-align:right;color:var(--red)">\' + fmt(totalWdTax) + \'</td><td style="text-align:right;color:var(--green)">\' + fmt(totalWd - totalWdTax) + \'</td><td></td></tr>\';\n'
    '  }\n'
    '\n'
    '  var remEl = $(\'wd_remaining\');\n'
    '  if (remEl && pay > 0) {\n'
    '    var remaining = pay - totalWd;\n'
    '    remEl.textContent = \'총 퇴직금 미계획 잔액: \' + fmt(Math.max(0, remaining));\n'
    '    remEl.style.color = remaining < 0 ? \'var(--red)\' : \'var(--text3)\';\n'
    '  }\n'
    '\n'
    '  var pensionTax = totalTax * (1 - discount);\n'
    '  var saved = totalTax - pensionTax;\n'
    '  $(\'rt_lumpTax\').textContent    = fmt(totalTax);\n'
    '  $(\'rt_lumpRate\').textContent   = rate.toFixed(2) + \'%\';\n'
    '  $(\'rt_pensionTax\').textContent = fmt(pensionTax);\n'
    '  $(\'rt_saved\').textContent      = fmt(saved);\n'
    '  $(\'rt_savedRate\').textContent  = (discount * 100).toFixed(0) + \'% 감면\';\n'
    '  $(\'rt_lumpNet\').textContent    = fmt(pay - totalTax);\n'
    '  $(\'rt_pensionNet\').textContent = fmt(pay - pensionTax);\n'
    '  var detailMap = { u10:\'10년 이하 수령 (30% 감면)\', u20:\'10~20년 수령 (40% 감면)\', o20:\'20년 초과 수령 (50% 감면)\' };\n'
    '  var pyVal = document.querySelector(\'input[name="rtPY"]:checked\').value;\n'
    '  $(\'rt_pensionDetail\').textContent = detailMap[pyVal];\n'
    '  $(\'rt_discountBadge\').textContent = (discount * 100).toFixed(0) + \'% 절세\';\n'
    '}'
)
new_calcRT = (
    'function calcRT() {\n'
    '  var isAuto = $(\'rt_mAuto\').classList.contains(\'active\');\n'
    '  var pay, totalTax, rate, showBreakdown;\n'
    '\n'
    '  if (isAuto) {\n'
    '    pay = v(\'rt_pay\');\n'
    '    var years = v(\'rt_years\');\n'
    '    var res = calcRetirementTax(pay, years);\n'
    '    totalTax = res.total; rate = res.rate; showBreakdown = true;\n'
    '    $(\'rt_b_pay\').textContent  = fmt(pay);\n'
    '    $(\'rt_b_ysd\').textContent  = fmt(res.ysD);\n'
    '    $(\'rt_b_conv\').textContent = fmt(res.conv);\n'
    '    $(\'rt_b_cd\').textContent   = fmt(res.cD);\n'
    '    $(\'rt_b_base\').textContent = fmt(res.taxBase);\n'
    '    $(\'rt_b_tax\').textContent  = fmt(res.total);\n'
    '  } else {\n'
    '    pay = v(\'rt_pay2\');\n'
    '    totalTax = pay * (v(\'rt_manRate\') / 100);\n'
    '    rate = v(\'rt_manRate\');\n'
    '    showBreakdown = false;\n'
    '  }\n'
    '\n'
    '  $(\'rt_breakdown\').style.display = showBreakdown ? \'\' : \'none\';\n'
    '  $(\'rt_lumpTax\').textContent  = fmt(totalTax);\n'
    '  $(\'rt_lumpRate\').textContent = rate.toFixed(2) + \'%\';\n'
    '\n'
    '  // 수령 기간별 실효세율 비교 테이블\n'
    '  if ($(\'rt_lump_tax\'))  $(\'rt_lump_tax\').textContent  = fmt(Math.round(totalTax));\n'
    '  if ($(\'rt_lump_eff\'))  $(\'rt_lump_eff\').textContent  = rate.toFixed(2) + \'%\';\n'
    '  if ($(\'rt_lump_net\'))  $(\'rt_lump_net\').textContent  = fmt(Math.round(pay - totalTax));\n'
    '  if ($(\'rt_d30_tax\'))   $(\'rt_d30_tax\').textContent   = fmt(Math.round(totalTax * 0.70));\n'
    '  if ($(\'rt_d30_eff\'))   $(\'rt_d30_eff\').textContent   = (rate * 0.70).toFixed(2) + \'%\';\n'
    '  if ($(\'rt_d30_net\'))   $(\'rt_d30_net\').textContent   = fmt(Math.round(pay - totalTax * 0.70));\n'
    '  if ($(\'rt_d40_tax\'))   $(\'rt_d40_tax\').textContent   = fmt(Math.round(totalTax * 0.60));\n'
    '  if ($(\'rt_d40_eff\'))   $(\'rt_d40_eff\').textContent   = (rate * 0.60).toFixed(2) + \'%\';\n'
    '  if ($(\'rt_d40_net\'))   $(\'rt_d40_net\').textContent   = fmt(Math.round(pay - totalTax * 0.60));\n'
    '  if ($(\'rt_d50_tax\'))   $(\'rt_d50_tax\').textContent   = fmt(Math.round(totalTax * 0.50));\n'
    '  if ($(\'rt_d50_eff\'))   $(\'rt_d50_eff\').textContent   = (rate * 0.50).toFixed(2) + \'%\';\n'
    '  if ($(\'rt_d50_net\'))   $(\'rt_d50_net\').textContent   = fmt(Math.round(pay - totalTax * 0.50));\n'
    '}'
)
assert old_calcRT in content, 'Fix6b: calcRT 함수 없음!'
content = content.replace(old_calcRT, new_calcRT, 1)

# ================================================================
# 저장 및 검증
# ================================================================
open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ('wd_rt_block_', 'Fix0: rtBlock id'),
    ("acc.retirePay || acc.src2", 'Fix1: accRtPay fallback'),
    ('4.4% 고정)</span>', 'Fix2: 종신수령 간소화'),
    ('t0_limit_chev', 'Fix3: 납입한도 토글'),
    ('t0_isa_chev', 'Fix3: ISA 토글'),
    ('t0_down_chev', 'Fix3: 주택다운 토글'),
    ('t0_div_chev', 'Fix3: 배당주의 토글'),
    ('t0_cond_chev', 'Fix3: 수령조건 토글'),
    ('t0_rate_chev', 'Fix3: 세율 토글'),
    ('t0_ord_chev', 'Fix3: 인출순서 토글'),
    ('퇴직소득 실효세율', 'Fix4: tab4 제목'),
    ('인출 계획', 'Fix5: 인출계획 잔존'),
    ('rtpy_u10', 'Fix5: rtpy 라디오 잔존'),
    ('rt_d30_tax', 'Fix6: 30% 테이블 셀'),
    ('rt_d50_net', 'Fix6: 50% 세후수령 셀'),
]
for k, label in checks:
    found = k in content
    should_absent = k in ('인출 계획', 'rtpy_u10')
    ok = not found if should_absent else found
    print(('OK' if ok else 'NG'), label + ':', found)
