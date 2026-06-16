#!/usr/bin/env python3
# fix_flowchart.py — 종합과세 모의계산 섹션을 흐름도 레이아웃으로 재구성

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original = html

# ═══════════════════════════════════════════════════
# 1. CSS 추가 (SECTION TOGGLE 블록 앞에 삽입)
# ═══════════════════════════════════════════════════
CSS_NEW = '''\
/* ── TAX FLOW (종합과세 흐름도) ── */
.tax-flow { display: flex; flex-direction: column; gap: 0; }
.tf-box { border: 1.5px solid var(--bg3); border-radius: var(--radius); padding: 12px 14px; background: var(--bg); }
.tf-box-title { font-size: 10px; font-weight: 700; color: var(--text3); letter-spacing: .06em; text-transform: uppercase; margin-bottom: 8px; }
.tf-auto-row { display: flex; justify-content: space-between; align-items: center; }
.tf-auto-badge { background: var(--bg3); color: var(--text3); font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 600; margin-left: 5px; vertical-align: middle; }
.tf-result { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--border); }
.tf-result-label { font-size: 11px; font-weight: 700; color: var(--text2); }
.tf-result-value { font-family: 'DM Serif Display', serif; font-size: 15px; color: var(--gold); }
.tf-arrow { text-align: center; font-size: 11px; color: var(--text3); padding: 4px 0; line-height: 1.4; }
.tf-step { border-radius: var(--radius); padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; }
.tf-step.neutral { background: var(--bg2); border: 1.5px solid var(--bg3); }
.tf-step.final   { background: rgba(43,94,167,.06); border: 1.5px solid rgba(43,94,167,.3); }
.tf-step-label { font-size: 12px; font-weight: 600; color: var(--text1); }
.tf-step-value { font-family: 'DM Serif Display', serif; font-size: 17px; color: var(--gold); }

'''

CSS_ANCHOR = '/* ── SECTION TOGGLE ── */'
if CSS_ANCHOR in html:
    html = html.replace(CSS_ANCHOR, CSS_NEW + CSS_ANCHOR)
    print('[OK] CSS 추가')
else:
    print('[MISS] CSS anchor')

# ═══════════════════════════════════════════════════
# 2. wd_over_body 내용 전체 교체 (흐름도 구조로)
# ═══════════════════════════════════════════════════
NEW_BODY = '''\
      <div id="wd_over_body">
        <div class="alert alert-warn" style="margin-bottom:12px">연간 사적연금소득(③ 재원 합산)이 1,500만원을 초과하면 분리과세(16.5%) 또는 종합과세 중 선택할 수 있습니다.</div>
        <div class="tax-flow">

          <!-- ① 소득금액 합산 -->
          <div class="tf-box">
            <div class="tf-box-title">① 소득금액 합산</div>
            <div class="form-group">
              <div class="tf-auto-row">
                <span class="form-label" style="margin-bottom:0">사적연금소득 ③ <span class="tf-auto-badge">자동</span></span>
                <span class="kr-num" id="wd_fl_pension" style="min-height:auto;font-size:15px">—</span>
              </div>
              <div class="form-hint" style="margin-top:2px">계좌 수령액 기준 · 연금소득공제 자동 적용</div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_salary">근로소득 — 총급여</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_salary" value="0" min="0" step="1000000" oninput="updateKR('wd_salary');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_salary_kr"></div>
              </div>
              <div class="form-hint">근로소득공제 자동 적용</div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_bizRev">사업소득 — 총수입금액</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_bizRev" value="0" min="0" step="1000000" oninput="updateKR('wd_bizRev');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_bizRev_kr"></div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_bizExp">사업소득 — 필요경비</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_bizExp" value="0" min="0" step="1000000" oninput="updateKR('wd_bizExp');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_bizExp_kr"></div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_intDiv">금융소득 (이자·배당)</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_intDiv" value="0" min="0" step="100000" oninput="updateKR('wd_intDiv');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_intDiv_kr"></div>
              </div>
              <div class="form-hint">2,000만원 초과분만 종합소득 합산</div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_natPen">공적연금소득 (국민연금 등 수령액)</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_natPen" value="0" min="0" step="100000" oninput="updateKR('wd_natPen');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_natPen_kr"></div>
              </div>
              <div class="form-hint">연금소득공제(최대 900만원) 자동 적용 후 합산</div>
            </div>
            <div class="form-group" style="margin-bottom:0">
              <label class="form-label" for="wd_otherInc">기타소득금액 (필요경비 공제 후)</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_otherInc" value="0" min="0" step="100000" oninput="updateKR('wd_otherInc');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_otherInc_kr"></div>
              </div>
            </div>
            <div class="tf-result">
              <span class="tf-result-label">종합소득금액</span>
              <span class="tf-result-value" id="wd_fl_total">—</span>
            </div>
          </div>

          <div class="tf-arrow">▼ 소득공제</div>

          <!-- ② 소득공제 -->
          <div class="tf-box">
            <div class="tf-box-title">② 소득공제</div>
            <div class="form-group">
              <label class="form-label" for="wd_dep">부양가족 수 (본인 제외)</label>
              <div class="inp-wrap"><input type="number" id="wd_dep" value="0" min="0" max="20" oninput="calcWD()"><span class="inp-unit">명</span></div>
              <div class="form-hint">기본공제: (1 + 부양가족) × 150만원</div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_np">국민연금 보험료공제</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_np" value="0" min="0" step="100000" oninput="updateKR('wd_np');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_np_kr"></div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="wd_hi">건강보험료 납부액 (연간)</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_hi" value="0" min="0" step="100000" oninput="updateKR('wd_hi');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_hi_kr"></div>
              </div>
              <div class="form-hint">근로소득자·은퇴자 해당 · 자영업자는 사업소득 필요경비 처리</div>
            </div>
            <div class="form-group" style="margin-bottom:0">
              <label class="form-label" for="wd_otherDed">기타 소득공제</label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_otherDed" value="0" min="0" step="100000" oninput="updateKR('wd_otherDed');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_otherDed_kr"></div>
              </div>
            </div>
            <div class="tf-result">
              <span class="tf-result-label">소득공제 합계</span>
              <span class="tf-result-value" id="wd_fl_ded">—</span>
            </div>
          </div>

          <div class="tf-arrow">▼</div>

          <!-- 과세표준 -->
          <div class="tf-step neutral">
            <span class="tf-step-label">과세표준</span>
            <span class="tf-step-value" id="wd_fl_base">—</span>
          </div>

          <div class="tf-arrow">▼ 세율 6%~45% 적용</div>

          <!-- 종합소득세 -->
          <div class="tf-step neutral">
            <span class="tf-step-label">종합소득세 <span style="font-size:10px;font-weight:400;color:var(--text3)">(지방세 포함)</span></span>
            <span class="tf-step-value" id="wd_fl_comptax">—</span>
          </div>

          <div class="tf-arrow">▼ 세액공제</div>

          <!-- ③ 세액공제 -->
          <div class="tf-box">
            <div class="tf-box-title">③ 세액공제</div>
            <div class="form-group" style="margin-bottom:0">
              <label class="form-label" for="wd_taxCredit">기타 세액공제 합계 <span style="font-weight:400;color:var(--text3)">(자녀·의료비·교육비 등)</span></label>
              <div class="inp-row">
                <div class="inp-wrap"><input type="number" id="wd_taxCredit" value="0" min="0" step="100000" oninput="updateKR('wd_taxCredit');calcWD()"><span class="inp-unit">원</span></div>
                <div class="kr-num" id="wd_taxCredit_kr"></div>
              </div>
              <div class="form-hint">의료비·교육비·기부금·보험료 등 세액공제 합산</div>
            </div>
          </div>

          <div class="tf-arrow">▼</div>

          <!-- 결정세액 -->
          <div class="tf-step final">
            <span class="tf-step-label">종합과세 결정세액 <span style="font-size:10px;font-weight:400;color:var(--text3)">(전체 소득 기준)</span></span>
            <span class="tf-step-value" id="wd_fl_final">—</span>
          </div>

        </div>
      </div>'''

# 교체 범위: <div id="wd_over_body"> ~ </div> (wd_over_body 닫는 태그)
START = '      <div id="wd_over_body">'
# 종료 앵커: wd_overSection 닫는 태그 바로 앞
END_ANCHOR = '\n    </div>\n\n  </div><!-- /left -->'

start_idx = html.find(START)
end_idx   = html.find(END_ANCHOR, start_idx)
if start_idx >= 0 and end_idx >= 0:
    # end_idx is at '\n    </div>' (wd_overSection close). wd_over_body's </div> is right before it.
    # We replace from START to (and including) the '      </div>' of wd_over_body
    # The actual closing tag of wd_over_body appears as '      </div>' just before '\n    </div>'
    body_close = '      </div>'
    body_close_idx = html.rfind(body_close, start_idx, end_idx)
    if body_close_idx >= 0:
        old_block = html[start_idx : body_close_idx + len(body_close)]
        html = html[:start_idx] + NEW_BODY + html[body_close_idx + len(body_close):]
        print('[OK] wd_over_body 교체')
    else:
        print('[MISS] wd_over_body closing tag')
else:
    print(f'[MISS] wd_over_body block (start={start_idx}, end={end_idx})')

# ═══════════════════════════════════════════════════
# 3. calcWD() 내부에 flowchart 업데이트 코드 추가
# ═══════════════════════════════════════════════════
JS_ANCHOR = '    var compTax = Math.max(0, compTaxBefore - earnTaxCredit - taxCredit);\n    var penCompTax'
JS_INSERT = '''    var compTax = Math.max(0, compTaxBefore - earnTaxCredit - taxCredit);
    // ── flowchart panel ──
    if ($('wd_fl_pension')) $('wd_fl_pension').textContent = fmt(totalEligWd3);
    if ($('wd_fl_total'))   $('wd_fl_total').textContent   = fmt(Math.round(totInc));
    if ($('wd_fl_ded'))     $('wd_fl_ded').textContent     = fmt(Math.round(totDed));
    if ($('wd_fl_base'))    $('wd_fl_base').textContent    = fmt(Math.max(0, Math.round(taxBase)));
    if ($('wd_fl_comptax')) $('wd_fl_comptax').textContent = fmt(Math.max(0, Math.round(compTaxBefore)));
    if ($('wd_fl_final'))   $('wd_fl_final').textContent   = fmt(Math.max(0, Math.round(compTax)));
    var penCompTax'''

if JS_ANCHOR in html:
    html = html.replace(JS_ANCHOR, JS_INSERT)
    print('[OK] JS flowchart 업데이트 추가')
else:
    print('[MISS] JS anchor')

# ═══════════════════════════════════════════════════
if html != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n파일 저장 완료.')
else:
    print('\n변경 없음.')
