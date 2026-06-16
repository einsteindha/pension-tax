
content = open('index.html', encoding='utf-8').read()

# ══ Fix 7: 실질 세율 → 실효세율 ══════════════════════════════════════════════
content = content.replace('<span class="rrow-label">실질 세율</span>',
                          '<span class="rrow-label">실효세율</span>', 1)

# ══ Fix 5: 모의계산 레이블 ════════════════════════════════════════════════════
content = content.replace('<span>1,500만원 초과 — 종합과세 비교 입력</span>',
                          '<span>1,500만원 초과 — 종합과세 모의계산</span>', 1)
content = content.replace('<div class="card-title">과세 방법 비교 (1,500만원 초과)</div>',
                          '<div class="card-title">과세 방법 모의계산 (1,500만원 초과)</div>', 1)

# ══ Fix 8a: Tab4 table 3-column ═══════════════════════════════════════════════
old_tab4 = '        <table style="width:100%;font-size:11px;border-collapse:collapse">\n          <thead>\n            <tr style="background:var(--bg3)">\n              <th style="padding:6px 8px;text-align:left;border:1px solid var(--border2);font-weight:600">수령 방법</th>\n              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">감면율</th>\n              <th style="padding:6px 8px;text-align:right;border:1px solid var(--border2);font-weight:600">납부 세금</th>\n              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">실효세율</th>\n              <th style="padding:6px 8px;text-align:right;border:1px solid var(--border2);font-weight:600">세후 수령</th>\n            </tr>\n          </thead>\n          <tbody>\n            <tr>\n              <td style="padding:6px 8px;border:1px solid var(--border2)">일시금 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--text3)">없음</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--red)" id="rt_lump_tax">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center" id="rt_lump_eff">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600" id="rt_lump_net">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.04)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">10년 이하 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">30%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d30_tax">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d30_eff">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d30_net">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.07)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">10~20년 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">40%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d40_tax">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d40_eff">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d40_net">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.11)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">20년 초과 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">50%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;color:var(--green)" id="rt_d50_tax">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d50_eff">—</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:right;font-weight:600;color:var(--green)" id="rt_d50_net">—</td>\n            </tr>\n          </tbody>\n        </table>'
new_tab4 = '        <table style="width:100%;font-size:11px;border-collapse:collapse">\n          <thead>\n            <tr style="background:var(--bg3)">\n              <th style="padding:6px 8px;text-align:left;border:1px solid var(--border2);font-weight:600">수령 방법</th>\n              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">감면율</th>\n              <th style="padding:6px 8px;text-align:center;border:1px solid var(--border2);font-weight:600">실효세율</th>\n            </tr>\n          </thead>\n          <tbody>\n            <tr>\n              <td style="padding:6px 8px;border:1px solid var(--border2)">일시금 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--text3)">없음</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center" id="rt_lump_eff">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.04)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">10년 이하 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">30%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d30_eff">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.07)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">10~20년 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">40%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d40_eff">—</td>\n            </tr>\n            <tr style="background:rgba(42,124,111,.11)">\n              <td style="padding:6px 8px;border:1px solid var(--border2)">20년 초과 수령</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;font-weight:700;color:var(--green)">50%↓</td>\n              <td style="padding:6px 8px;border:1px solid var(--border2);text-align:center;color:var(--green)" id="rt_d50_eff">—</td>\n            </tr>\n          </tbody>\n        </table>'
assert old_tab4 in content, 'Tab4 table 없음!'
content = content.replace(old_tab4, new_tab4, 1)

# ══ Fix 8b: calcRT — only set eff IDs ════════════════════════════════════════
old_calcRT = "  if ($('rt_lump_tax'))  $('rt_lump_tax').textContent  = fmt(Math.round(totalTax));\n  if ($('rt_lump_eff'))  $('rt_lump_eff').textContent  = rate.toFixed(2) + '%';\n  if ($('rt_lump_net'))  $('rt_lump_net').textContent  = fmt(Math.round(pay - totalTax));\n  if ($('rt_d30_tax'))   $('rt_d30_tax').textContent   = fmt(Math.round(totalTax * 0.70));\n  if ($('rt_d30_eff'))   $('rt_d30_eff').textContent   = (rate * 0.70).toFixed(2) + '%';\n  if ($('rt_d30_net'))   $('rt_d30_net').textContent   = fmt(Math.round(pay - totalTax * 0.70));\n  if ($('rt_d40_tax'))   $('rt_d40_tax').textContent   = fmt(Math.round(totalTax * 0.60));\n  if ($('rt_d40_eff'))   $('rt_d40_eff').textContent   = (rate * 0.60).toFixed(2) + '%';\n  if ($('rt_d40_net'))   $('rt_d40_net').textContent   = fmt(Math.round(pay - totalTax * 0.60));\n  if ($('rt_d50_tax'))   $('rt_d50_tax').textContent   = fmt(Math.round(totalTax * 0.50));\n  if ($('rt_d50_eff'))   $('rt_d50_eff').textContent   = (rate * 0.50).toFixed(2) + '%';\n  if ($('rt_d50_net'))   $('rt_d50_net').textContent   = fmt(Math.round(pay - totalTax * 0.50));"
new_calcRT = "  if ($('rt_lump_eff'))  $('rt_lump_eff').textContent  = rate.toFixed(2) + '%';\n  if ($('rt_d30_eff'))   $('rt_d30_eff').textContent   = (rate * 0.70).toFixed(2) + '%';\n  if ($('rt_d40_eff'))   $('rt_d40_eff').textContent   = (rate * 0.60).toFixed(2) + '%';\n  if ($('rt_d50_eff'))   $('rt_d50_eff').textContent   = (rate * 0.50).toFixed(2) + '%';"
assert old_calcRT in content, 'calcRT rates block 없음!'
content = content.replace(old_calcRT, new_calcRT, 1)

# ══ Fix 6a: cmp-card — add id to sepDetail ═══════════════════════════════════
content = content.replace('          <div class="cmp-detail">세율 16.5%</div>',
                          '          <div class="cmp-detail" id="wd_sepDetail">—</div>', 1)

# ══ Fix 6b: breakdown HTML — rename + add natpen/otherinc ════════════════════
old_bdr = '          <div class="breakdown-row"><span>연금소득금액</span><span id="wd_b_pension">—</span></div>\n          <div class="breakdown-row"><span>근로소득금액</span><span id="wd_b_earned">—</span></div>\n          <div class="breakdown-row"><span>사업소득금액</span><span id="wd_b_biz">—</span></div>\n          <div class="breakdown-row"><span>이자·배당(합산분)</span><span id="wd_b_intdiv">—</span></div>\n          <div class="breakdown-row total"><span>종합소득금액</span><span id="wd_b_total">—</span></div>'
new_bdr = '          <div class="breakdown-row"><span>사적연금소득금액 (③)</span><span id="wd_b_pension">—</span></div>\n          <div class="breakdown-row"><span>공적연금소득금액</span><span id="wd_b_natpen">—</span></div>\n          <div class="breakdown-row"><span>근로소득금액</span><span id="wd_b_earned">—</span></div>\n          <div class="breakdown-row"><span>사업소득금액</span><span id="wd_b_biz">—</span></div>\n          <div class="breakdown-row"><span>이자·배당(합산분)</span><span id="wd_b_intdiv">—</span></div>\n          <div class="breakdown-row"><span>기타소득금액</span><span id="wd_b_otherinc">—</span></div>\n          <div class="breakdown-row total"><span>종합소득금액</span><span id="wd_b_total">—</span></div>'
assert old_bdr in content, 'breakdown rows 없음!'
content = content.replace(old_bdr, new_bdr, 1)

# ══ Fix 4: natPen/otherInc 입력 추가 (이자배당 뒤) ════════════════════════════
old_af_intdiv = '          <div class="form-hint">2,000만원 초과분만 종합소득 합산</div>\n        </div>\n        <hr class="divider">\n        <div class="sub-title">소득공제</div>'
new_af_intdiv = '          <div class="form-hint">2,000만원 초과분만 종합소득 합산</div>\n        </div>\n        <div class="form-group">\n          <label class="form-label" for="wd_natPen">공적연금소득 (국민연금 등 수령액)</label>\n          <div class="kr-num" id="wd_natPen_kr"></div>\n          <div class="inp-wrap">\n            <input type="number" id="wd_natPen" value="0" min="0" step="100000" oninput="updateKR(\'wd_natPen\');calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n          <div class="form-hint">연금소득공제(최대 900만원) 자동 적용 후 합산</div>\n        </div>\n        <div class="form-group">\n          <label class="form-label" for="wd_otherInc">기타소득금액 (필요경비 공제 후)</label>\n          <div class="kr-num" id="wd_otherInc_kr"></div>\n          <div class="inp-wrap">\n            <input type="number" id="wd_otherInc" value="0" min="0" step="100000" oninput="updateKR(\'wd_otherInc\');calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n        </div>\n        <hr class="divider">\n        <div class="sub-title">소득공제</div>'
assert old_af_intdiv in content, '이자배당→소득공제 구분선 없음!'
content = content.replace(old_af_intdiv, new_af_intdiv, 1)

# ══ Fix 4: hi/taxCredit 입력 추가 (기타소득공제 뒤) ═══════════════════════════
old_af_oded = '        <div class="form-group">\n          <label class="form-label" for="wd_otherDed">기타 소득공제</label>\n          <div class="inp-wrap">\n            <input type="number" id="wd_otherDed" value="0" min="0" step="100000" oninput="calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n        </div>\n      </div>\n    </div>'
new_af_oded = '        <div class="form-group">\n          <label class="form-label" for="wd_otherDed">기타 소득공제</label>\n          <div class="inp-wrap">\n            <input type="number" id="wd_otherDed" value="0" min="0" step="100000" oninput="calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n        </div>\n        <div class="form-group">\n          <label class="form-label" for="wd_hi">건강보험료 납부액 (연간)</label>\n          <div class="kr-num" id="wd_hi_kr"></div>\n          <div class="inp-wrap">\n            <input type="number" id="wd_hi" value="0" min="0" step="100000" oninput="updateKR(\'wd_hi\');calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n          <div class="form-hint">건강보험료 공제 (소득공제)</div>\n        </div>\n        <hr class="divider">\n        <div class="sub-title">세액공제</div>\n        <div class="form-group">\n          <label class="form-label" for="wd_taxCredit">기타 세액공제 합계</label>\n          <div class="kr-num" id="wd_taxCredit_kr"></div>\n          <div class="inp-wrap">\n            <input type="number" id="wd_taxCredit" value="0" min="0" step="100000" oninput="updateKR(\'wd_taxCredit\');calcWD()">\n            <span class="inp-unit">원</span>\n          </div>\n          <div class="form-hint">의료비·교육비·기부금·보험료 등 세액공제 합산</div>\n        </div>\n      </div>\n    </div>'
assert old_af_oded in content, '기타소득공제→섹션끝 없음!'
content = content.replace(old_af_oded, new_af_oded, 1)

# ══ Fix 1a: wdAccs 초기화 openYear → openDate ═════════════════════════════════
content = content.replace("{ type: 'irp', openYear: 2020,", "{ type: 'irp', openDate: '2020-01-01',", 1)
content = content.replace("{ type: 'ps',  openYear: 2020,", "{ type: 'ps',  openDate: '2020-01-01',", 1)
content = content.replace("wdAccs.push({ type: 'ps', openYear: 2015,", "wdAccs.push({ type: 'ps', openDate: '2015-01-01',", 1)

# ══ Fix 1b: renderWdAccs 외부 div에 id 추가 ═══════════════════════════════════
content = content.replace(
    "'<div style=\"border:1.5px solid var(--border2);border-radius:var(--radius-lg);margin-bottom:10px;overflow:hidden\">',",
    "'<div id=\"wd_acc_card_' + i + '\" style=\"border:1.5px solid var(--border2);border-radius:var(--radius-lg);margin-bottom:10px;overflow:hidden;transition:border-color .3s,background .3s\">',",
    1
)

# ══ Fix 9: renderWdAccs 헤더에 자격뱃지 추가 ═════════════════════════════════
old_hdr = "          '<span style=\"font-size:12px;font-weight:700;color:var(--text2)\">계좌 ' + (i+1) + ' <span style=\"color:' + color + '\">' + (isIRP ? 'IRP' : '연금저축') + '</span></span>',\n          '<div style=\"display:flex;gap:8px;align-items:center\">',"
new_hdr = "          '<span style=\"font-size:12px;font-weight:700;color:var(--text2)\">계좌 ' + (i+1) + ' <span style=\"color:' + color + '\">' + (isIRP ? 'IRP' : '연금저축') + '</span></span>',\n          '<span id=\"wd_elig_badge_' + i + '\" style=\"font-size:9px;padding:2px 6px;border-radius:10px;background:var(--bg2);color:var(--text3)\">—</span>',\n          '<div style=\"display:flex;gap:8px;align-items:center\">',"
assert old_hdr in content, '계좌 헤더 없음!'
content = content.replace(old_hdr, new_hdr, 1)

# ══ Fix 1c: renderWdAccs openedYrs 계산 ══════════════════════════════════════
old_ry = "    var openedYrs = curYear - acc.openYear;\n    var yrLabel = openedYrs >= 0 ? '개설 ' + openedYrs + '년' : '';"
new_ry = "    var accOpenMs = acc.openDate ? (new Date() - new Date(acc.openDate)) : 0;\n    var openedYrs = Math.max(0, Math.floor(accOpenMs / (365.25 * 24 * 3600 * 1000)));\n    var yrLabel = '개설 ' + openedYrs + '년';"
assert old_ry in content, 'renderWdAccs openedYrs 없음!'
content = content.replace(old_ry, new_ry, 1)

# ══ Fix 1d: renderWdAccs date input ══════════════════════════════════════════
old_oi = "              '<div style=\"font-size:11px;color:var(--text3);margin-bottom:3px\">계좌 개설 연도</div>',\n              '<div style=\"display:flex;align-items:center;gap:5px\">',\n                '<input type=\"number\" value=\"' + acc.openYear + '\" min=\"1990\" max=\"2026\" style=\"width:72px;padding:4px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].openYear=parseInt(this.value)||2015;updateWdAccLabel(' + i + ');calcWD()\">',\n                '<span id=\"wd_yr_lbl_' + i + '\" style=\"font-size:11px;color:var(--text3)\">년 · ' + yrLabel + '</span>',\n              '</div>',"
new_oi = "              '<div style=\"font-size:11px;color:var(--text3);margin-bottom:3px\">계좌 개설일</div>',\n              '<div style=\"display:flex;align-items:center;gap:5px\">',\n                '<input type=\"date\" value=\"' + (acc.openDate||'2020-01-01') + '\" style=\"padding:4px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].openDate=this.value;updateWdAccLabel(' + i + ');calcWD()\">',\n                '<span id=\"wd_yr_lbl_' + i + '\" style=\"font-size:11px;color:var(--text3)\">' + yrLabel + '</span>',\n              '</div>',"
assert old_oi in content, 'renderWdAccs date input 없음!'
content = content.replace(old_oi, new_oi, 1)

# ══ Fix 9: 계좌별 5년 미만 경고 div 삽입 ═════════════════════════════════════
old_5yr_html = "          (!isIRP ? '<div style=\"display:flex;align-items:center;gap:6px;margin-bottom:8px;padding:5px 8px;background:var(--bg3);border-radius:var(--radius)\">' +\n            '<label style=\"font-size:11px;color:var(--text2);display:flex;align-items:center;gap:5px;cursor:pointer\">' +\n            '<input type=\"checkbox\" ' + (acc.lifeAnnuity ? 'checked' : '') + ' style=\"cursor:pointer\" onchange=\"wdAccs[' + i + '].lifeAnnuity=this.checked;calcWD()\">' +\n            '종신수령 <span style=\"font-size:10px;color:var(--text3)\">(4.4% 고정)</span>' +\n            '</label></div>' : ''),\n          '<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:4px\">인출금액 (순서: ①→②→③)</div>',"
new_5yr_html = "          (!isIRP ? '<div style=\"display:flex;align-items:center;gap:6px;margin-bottom:8px;padding:5px 8px;background:var(--bg3);border-radius:var(--radius)\">' +\n            '<label style=\"font-size:11px;color:var(--text2);display:flex;align-items:center;gap:5px;cursor:pointer\">' +\n            '<input type=\"checkbox\" ' + (acc.lifeAnnuity ? 'checked' : '') + ' style=\"cursor:pointer\" onchange=\"wdAccs[' + i + '].lifeAnnuity=this.checked;calcWD()\">' +\n            '종신수령 <span style=\"font-size:10px;color:var(--text3)\">(4.4% 고정)</span>' +\n            '</label></div>' : ''),\n          '<div id=\"wd_under5yr_warn_' + i + '\" style=\"display:none;margin-bottom:8px;padding:8px 10px;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.25);border-radius:var(--radius);font-size:11px;line-height:1.5\">' +\n            '<strong>개설 5년 미만 — 연금수령 요건 미충족</strong><br>' +\n            '③ 세액공제O+수익 재원에 <strong>기타소득세 16.5%</strong> 적용. ①은 비과세, ②는 퇴직소득세 유지.' +\n          '</div>',\n          '<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:4px\">인출금액 (순서: ①→②→③)</div>',"
assert old_5yr_html in content, '종신수령→인출금액 헤더 없음!'
content = content.replace(old_5yr_html, new_5yr_html, 1)

# ══ Fix 1e: updateWdAccLabel ══════════════════════════════════════════════════
old_ual = "function updateWdAccLabel(i) {\n  var acc = wdAccs[i];\n  var curYear = 2026;\n  var yrLbl = $('wd_yr_lbl_' + i);\n  if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear || curYear)) + '년';\n  var balLbl = $('wd_bal_lbl_' + i);\n  if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';\n}"
new_ual = "function updateWdAccLabel(i) {\n  var acc = wdAccs[i];\n  var yrLbl = $('wd_yr_lbl_' + i);\n  if (yrLbl) {\n    var ms = acc.openDate ? (new Date() - new Date(acc.openDate)) : 0;\n    var yrs = Math.max(0, Math.floor(ms / (365.25 * 24 * 3600 * 1000)));\n    yrLbl.textContent = '개설 ' + yrs + '년';\n  }\n  var balLbl = $('wd_bal_lbl_' + i);\n  if (balLbl) balLbl.textContent = acc.balance > 0 ? toKorean(acc.balance) : '';\n}"
assert old_ual in content, 'updateWdAccLabel 없음!'
content = content.replace(old_ual, new_ual, 1)

# ══ Fix 1f: calcWD isPre2013 ══════════════════════════════════════════════════
content = content.replace(
    "  var isPre2013 = wdAccs.some(function(a) { return (a.openYear||2015) <= 2013; });",
    "  var isPre2013 = wdAccs.some(function(a) { return a.openDate && a.openDate <= '2013-02-28'; });",
    1
)

# ══ Fix 1g: calcWD earliestOpen → _accOpenYrs ════════════════════════════════
old_elig = "  var earliestOpen = wdAccs.reduce(function(mn, a) { return Math.min(mn, a.openYear || curYear); }, 9999);\n  if (earliestOpen === 9999) earliestOpen = curYear;\n  var openedYrs = curYear - earliestOpen;\n  var elig55 = age >= 55;\n  var elig5yr = openedYrs >= 5;\n\n  var eligMsg = '나이 ' + age + '세: ' + (elig55 ? '✓ 55세 이상' : '✗ 55세 미만') + ' · 가장 오래된 계좌 개설 ' + openedYrs + '년: ' + (elig5yr ? '✓ 5년 이상' : '✗ 5년 미만');"
new_elig = "  var _accOpenYrs = function(a) {\n    if (!a.openDate) return 0;\n    return Math.max(0, (new Date() - new Date(a.openDate)) / (365.25 * 24 * 3600 * 1000));\n  };\n  var openedYrs = wdAccs.reduce(function(mx, a) { return Math.max(mx, _accOpenYrs(a)); }, 0);\n  var elig55 = age >= 55;\n  var elig5yr = openedYrs >= 5;\n\n  var eligMsg = '나이 ' + age + '세: ' + (elig55 ? '✓ 55세 이상' : '✗ 55세 미만') + ' · 가장 오래된 계좌 개설 ' + Math.floor(openedYrs) + '년: ' + (elig5yr ? '✓ 5년 이상' : '✗ 5년 미만');"
assert old_elig in content, 'earliestOpen block 없음!'
content = content.replace(old_elig, new_elig, 1)

# ══ Fix 1h: accOpenedYrs ═════════════════════════════════════════════════════
content = content.replace(
    "    var accOpenedYrs = curYear - (acc.openYear || curYear);",
    "    var accOpenedYrs = _accOpenYrs(acc);",
    1
)

# ══ Fix 1i: yrLbl textContent ════════════════════════════════════════════════
content = content.replace(
    "    if (yrLbl) yrLbl.textContent = '년 · 개설 ' + Math.max(0, curYear - (acc.openYear||curYear)) + '년';",
    "    if (yrLbl) yrLbl.textContent = '개설 ' + Math.floor(accOpenedYrs) + '년';",
    1
)

# ══ Fix 1j: pensionYr 버그 수정 ══════════════════════════════════════════════
old_pyr = "  var eligibleAge = Math.max(55, earliestOpen + 5);\n  var pensionYr = age >= eligibleAge ? Math.max(1, Math.round(age - eligibleAge + 1)) : 0;"
new_pyr = "  var pensionYr = (elig55 && elig5yr) ? Math.max(1, Math.round(age - 55 + 1)) : 0;"
assert old_pyr in content, 'pensionYr 없음!'
content = content.replace(old_pyr, new_pyr, 1)

# ══ Fix 9: calcWD forEach — eligBadge + 5년경고 토글 ═════════════════════════
old_acc_push = "    accResults.push({ label: '계좌 ' + (i+1) + ' ' + (isIRP ? 'IRP' : '연금저축'), gross: wd1+wd2+wd3, tax: tax2+tax3, eligPS: eligPS });\n    var yrLbl = $('wd_yr_lbl_' + i);"
new_acc_push = "    accResults.push({ label: '계좌 ' + (i+1) + ' ' + (isIRP ? 'IRP' : '연금저축'), gross: wd1+wd2+wd3, tax: tax2+tax3, eligPS: eligPS });\n    var eligBadge = $('wd_elig_badge_' + i);\n    if (eligBadge) {\n      eligBadge.textContent = eligPS ? '연금소득세 ✓' : '기타소득세 16.5%';\n      eligBadge.style.background = eligPS ? 'rgba(76,175,80,.12)' : 'rgba(239,68,68,.08)';\n      eligBadge.style.color = eligPS ? 'var(--green)' : 'var(--red)';\n    }\n    var under5yr = accOpenedYrs < 5;\n    var acc5yrWarn = $('wd_under5yr_warn_' + i);\n    if (acc5yrWarn) acc5yrWarn.style.display = under5yr ? '' : 'none';\n    var accCard = $('wd_acc_card_' + i);\n    if (accCard) {\n      accCard.style.borderColor = under5yr ? 'rgba(239,68,68,.5)' : '';\n      accCard.style.background  = under5yr ? 'rgba(239,68,68,.02)' : '';\n    }\n    var yrLbl = $('wd_yr_lbl_' + i);"
assert old_acc_push in content, 'accResults push anchor 없음!'
content = content.replace(old_acc_push, new_acc_push, 1)

# ══ Fix 3: 총 퇴직금 한글 단위 div ════════════════════════════════════════════
old_rtp = "                      '<div style=\"display:flex;align-items:center;gap:3px\">',\n                        '<input type=\"number\" value=\"' + (acc.retirePay || 0) + '\" min=\"0\" step=\"1000000\" style=\"width:120px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].retirePay=parseFloat(this.value)||0;calcWD()\">',\n                        '<span style=\"font-size:11px;color:var(--text3)\">원</span>',\n                      '</div>',\n                    '</div>',"
new_rtp = "                      '<div style=\"display:flex;align-items:center;gap:3px\">',\n                        '<input type=\"number\" value=\"' + (acc.retirePay || 0) + '\" min=\"0\" step=\"1000000\" style=\"width:120px;padding:3px 6px;border:1px solid var(--border2);border-radius:2px;font-size:12px\" oninput=\"wdAccs[' + i + '].retirePay=parseFloat(this.value)||0;calcWD()\">',\n                        '<span style=\"font-size:11px;color:var(--text3)\">원</span>',\n                      '</div>',\n                      '<div id=\"wd_rt_pay_kr_' + i + '\" style=\"font-size:10px;color:var(--text3);margin-top:2px\">' + (acc.retirePay > 0 ? toKorean(acc.retirePay) : '') + '</div>',\n                    '</div>',"
assert old_rtp in content, '퇴직금 input 없음!'
content = content.replace(old_rtp, new_rtp, 1)

# ══ Fix 3: calcWD rtPayKrEl 업데이트 ═════════════════════════════════════════
old_rtres = "      rtResEl.textContent = '퇴직소득세 기준: ' + fmt(Math.round(accRtTax)) + ' (실효 ' + effRate + '%) · 이번 인출분: ' + fmt(Math.round(tax2));\n      } else {\n        rtResEl.textContent = '총 퇴직금 금액을 입력해주세요';\n      }\n    }\n  });"
new_rtres = "      rtResEl.textContent = '퇴직소득세 기준: ' + fmt(Math.round(accRtTax)) + ' (실효 ' + effRate + '%) · 이번 인출분: ' + fmt(Math.round(tax2));\n      } else {\n        rtResEl.textContent = '총 퇴직금 금액을 입력해주세요';\n      }\n    }\n    var rtPayKrEl = $('wd_rt_pay_kr_' + i);\n    if (rtPayKrEl && isIRP) rtPayKrEl.textContent = accRtPay > 0 ? toKorean(accRtPay) : '';\n  });"
assert old_rtres in content, 'rtResEl block 없음!'
content = content.replace(old_rtres, new_rtres, 1)

# ══ Fix 2: 계좌별 내역 실효세율 ═══════════════════════════════════════════════
old_ar = "      html += '<div class=\"breakdown-row\"><span>' + r.label + '</span><span>수령 ' + fmt(r.gross) + ' · 세금 ' + fmt(r.tax) + '</span></div>';"
new_ar = "      var rEff = r.gross > 0 ? (r.tax/r.gross*100).toFixed(1)+'%' : '—';\n      html += '<div class=\"breakdown-row\"><span>' + r.label + '</span><span>수령 ' + fmt(r.gross) + ' · 세금 ' + fmt(r.tax) + ' <span style=\"color:var(--text3)\">(실효 ' + rEff + ')</span></span></div>';"
assert old_ar in content, '계좌별 내역 row 없음!'
content = content.replace(old_ar, new_ar, 1)

# ══ Fix 6c: over15 calcWD 블록 전체 교체 ═════════════════════════════════════
old_o15 = "  if (over15) {\n    var sepTax  = totalWd3 * 0.165;\n    var salary  = parseFloat($('wd_salary').value) || 0;\n    var bizRev  = parseFloat($('wd_bizRev').value) || 0;\n    var bizExp  = parseFloat($('wd_bizExp').value) || 0;\n    var intDiv  = parseFloat($('wd_intDiv').value) || 0;\n    var dep     = parseFloat($('wd_dep').value)    || 0;\n    var np      = parseFloat($('wd_np').value)     || 0;\n    var otherD  = parseFloat($('wd_otherDed').value) || 0;\n    var penAmt  = totalWd3 - pensionDeduction(totalWd3);\n    var earnAmt = salary > 0 ? Math.max(0, salary - earnedDeduction(salary)) : 0;\n    var bizAmt  = Math.max(0, bizRev - bizExp);\n    var intAmt  = Math.max(0, intDiv - 20000000);\n    var totInc  = penAmt + earnAmt + bizAmt + intAmt;\n    var totDed  = (1 + dep) * 1500000 + np + otherD;\n    var taxBase = Math.max(0, totInc - totDed);\n    var compTax = baseTax(taxBase) * 1.1;\n    var hasInput = salary>0||bizRev>0||intDiv>0||dep>0||np>0||otherD>0;\n    if ($('wd_sepTax'))    $('wd_sepTax').textContent   = fmt(sepTax);\n    if ($('wd_compTax'))   $('wd_compTax').textContent  = hasInput ? fmt(compTax) : '소득 정보 입력 필요';\n    if ($('wd_compDetail')) $('wd_compDetail').textContent = hasInput ? '과세표준 ' + fmtN(taxBase/10000) + '만원' : '위 항목 입력';\n    var rec = $('wd_recommendation'), sepCard = $('wd_sepCard'), compCard = $('wd_compCard');\n    if (hasInput && rec && sepCard && compCard) {\n      var better = compTax < sepTax ? 'comp' : 'sep';\n      sepCard.className  = 'cmp-card' + (better === 'sep'  ? ' winner' : '');\n      compCard.className = 'cmp-card' + (better === 'comp' ? ' winner' : '');\n      rec.style.display = '';\n      rec.className = better === 'sep' ? 'alert alert-info' : 'alert alert-green';\n      rec.innerHTML = better === 'sep'\n        ? '<strong>분리과세가 유리합니다.</strong> 종합과세 대비 약 ' + fmt(Math.abs(sepTax-compTax)) + ' 절세'\n        : '<strong>종합과세가 유리합니다.</strong> 분리과세 대비 약 ' + fmt(Math.abs(sepTax-compTax)) + ' 절세';\n      if ($('wd_compBreakdown')) {\n        $('wd_compBreakdown').style.display = '';\n        $('wd_b_pension').textContent = fmt(penAmt);\n        $('wd_b_earned').textContent  = earnAmt > 0 ? fmt(earnAmt) : '—';\n        $('wd_b_biz').textContent     = bizAmt  > 0 ? fmt(bizAmt)  : '—';\n        $('wd_b_intdiv').textContent  = intAmt  > 0 ? fmt(intAmt)  : '—';\n        $('wd_b_total').textContent   = fmt(totInc);\n        $('wd_b_ded').textContent     = fmt(totDed);\n        $('wd_b_base').textContent    = fmt(taxBase);\n        $('wd_b_comptax').textContent = fmt(compTax);\n      }\n    } else if (rec) { rec.style.display = 'none'; }\n  }"
new_o15 = "  if (over15) {\n    var sepTax   = totalEligWd3 * 0.165;\n    var salary   = parseFloat($('wd_salary').value)    || 0;\n    var bizRev   = parseFloat($('wd_bizRev').value)    || 0;\n    var bizExp   = parseFloat($('wd_bizExp').value)    || 0;\n    var intDiv   = parseFloat($('wd_intDiv').value)    || 0;\n    var natPen   = parseFloat($('wd_natPen').value)    || 0;\n    var otherInc = parseFloat($('wd_otherInc').value)  || 0;\n    var dep      = parseFloat($('wd_dep').value)       || 0;\n    var np       = parseFloat($('wd_np').value)        || 0;\n    var hi       = parseFloat($('wd_hi').value)        || 0;\n    var otherD   = parseFloat($('wd_otherDed').value)  || 0;\n    var taxCredit = parseFloat($('wd_taxCredit').value) || 0;\n    var penAmt     = totalEligWd3 - pensionDeduction(totalEligWd3);\n    var natPenAmt  = natPen > 0 ? Math.max(0, natPen - pensionDeduction(natPen)) : 0;\n    var earnAmt    = salary > 0 ? Math.max(0, salary - earnedDeduction(salary)) : 0;\n    var bizAmt     = Math.max(0, bizRev - bizExp);\n    var intAmt     = Math.max(0, intDiv - 20000000);\n    var totInc     = penAmt + natPenAmt + earnAmt + bizAmt + intAmt + otherInc;\n    var totDed     = (1 + dep) * 1500000 + np + hi + otherD;\n    var taxBase    = Math.max(0, totInc - totDed);\n    var compTaxBefore = baseTax(taxBase) * 1.1;\n    var earnTaxCredit = 0;\n    if (salary > 0 && totInc > 0 && compTaxBefore > 0) {\n      var earnShare = earnAmt / totInc;\n      var earnTaxPart = compTaxBefore * earnShare;\n      earnTaxCredit = earnTaxPart <= 700000 ? earnTaxPart * 0.55 : 385000 + (earnTaxPart - 700000) * 0.30;\n      var earnTCcap = salary <= 55000000 ? 740000 : salary <= 70000000 ? 660000 : 500000;\n      earnTaxCredit = Math.min(earnTaxCredit, earnTCcap);\n    }\n    var compTax = Math.max(0, compTaxBefore - earnTaxCredit - taxCredit);\n    var hasInput = salary>0||bizRev>0||intDiv>0||natPen>0||otherInc>0||dep>0||np>0||hi>0||otherD>0||taxCredit>0;\n    var sepEff  = '16.5';\n    var compEff = totInc > 0 ? (compTax / totInc * 100).toFixed(1) : '0.0';\n    if ($('wd_sepTax'))    $('wd_sepTax').textContent    = sepEff + '%';\n    if ($('wd_sepDetail')) $('wd_sepDetail').textContent  = '세금 ' + fmtN(Math.round(sepTax/10000)) + '만원';\n    if ($('wd_compTax'))   $('wd_compTax').textContent   = hasInput ? compEff + '%' : '—';\n    if ($('wd_compDetail')) $('wd_compDetail').textContent = hasInput ? '세금 ' + fmtN(Math.round(compTax/10000)) + '만원' : '위 항목 입력';\n    var rec = $('wd_recommendation'), sepCard = $('wd_sepCard'), compCard = $('wd_compCard');\n    if (sepCard)  { sepCard.className  = 'cmp-card'; sepCard.style.outline  = ''; }\n    if (compCard) { compCard.className = 'cmp-card'; compCard.style.outline = ''; }\n    if (hasInput && rec && sepCard && compCard) {\n      var better = compTax < sepTax ? 'comp' : 'sep';\n      sepCard.style.outline  = better === 'sep'  ? '2px solid var(--green)' : '';\n      compCard.style.outline = better === 'comp' ? '2px solid var(--green)' : '';\n      rec.style.display = '';\n      rec.className = 'alert alert-info';\n      rec.innerHTML = better === 'sep'\n        ? '<strong>분리과세 실효세율 16.5%</strong> — 종합과세(' + compEff + '%)보다 절세에 유리합니다.'\n        : '<strong>종합과세 실효세율 ' + compEff + '%</strong> — 분리과세(16.5%)보다 절세에 유리합니다.';\n      if ($('wd_compBreakdown')) {\n        $('wd_compBreakdown').style.display = '';\n        if ($('wd_b_pension'))  $('wd_b_pension').textContent  = fmt(penAmt);\n        if ($('wd_b_natpen'))   $('wd_b_natpen').textContent   = natPenAmt > 0 ? fmt(natPenAmt) : '—';\n        if ($('wd_b_earned'))   $('wd_b_earned').textContent   = earnAmt   > 0 ? fmt(earnAmt)   : '—';\n        if ($('wd_b_biz'))      $('wd_b_biz').textContent      = bizAmt    > 0 ? fmt(bizAmt)    : '—';\n        if ($('wd_b_intdiv'))   $('wd_b_intdiv').textContent   = intAmt    > 0 ? fmt(intAmt)    : '—';\n        if ($('wd_b_otherinc')) $('wd_b_otherinc').textContent = otherInc  > 0 ? fmt(otherInc)  : '—';\n        if ($('wd_b_total'))    $('wd_b_total').textContent    = fmt(totInc);\n        if ($('wd_b_ded'))      $('wd_b_ded').textContent      = fmt(totDed);\n        if ($('wd_b_base'))     $('wd_b_base').textContent     = fmt(taxBase);\n        if ($('wd_b_comptax'))  $('wd_b_comptax').textContent  = fmt(compTax);\n      }\n    } else if (rec) { rec.style.display = 'none'; }\n  }"
assert old_o15 in content, 'over15 block 없음!'
content = content.replace(old_o15, new_o15, 1)

# ══ updateKR 초기화 목록 ════════════════════════════════════════════════════
content = content.replace(
    "['tc_salary','tc_ps','tc_irp','rt_pay','rt_pay2','wd_rt_pay','wd_rt_pay2'].forEach(updateKR);",
    "['tc_salary','tc_ps','tc_irp','rt_pay','rt_pay2','wd_rt_pay','wd_rt_pay2','wd_natPen','wd_otherInc','wd_hi','wd_taxCredit'].forEach(updateKR);",
    1
)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ('실효세율', True),
    ('openDate', True),
    ('openYear', False),  # 없어야 함
    ('wd_natPen', True),
    ('wd_otherInc', True),
    ('wd_hi', True),
    ('wd_taxCredit', True),
    ('wd_under5yr_warn_', True),
    ('wd_acc_card_', True),
    ('wd_elig_badge_', True),
    ('wd_b_natpen', True),
    ('wd_b_otherinc', True),
    ('wd_sepDetail', True),
    ('rt_lump_tax', False),  # 없어야 함
    ('type="date"', True),
    ('_accOpenYrs', True),
    ('totalEligWd3 * 0.165', True),
    ('wd_rt_pay_kr_', True),
    ("'실효 ' + rEff", True),
]
for k, want in checks:
    found = k in content
    ok = found == want
    mark = '✓' if ok else '✗'
    note = '있음' if found else '없음'
    expected = '있어야함' if want else '없어야함'
    if not ok:
        note += f' ({expected})'
    print(f'{mark} {k}: {note}')
