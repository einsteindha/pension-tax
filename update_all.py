import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. CSS 추가 (wd-table + lm-cur)
css_add = """
/* ── WITHDRAWAL TABLE ── */
.wd-table { width:100%; border-collapse:collapse; font-size:12px; margin-top:8px; }
.wd-table th { background:var(--accent-bg); color:var(--gold-light); padding:7px 8px; text-align:center; font-weight:500; border:1px solid var(--bg3); font-size:10px; letter-spacing:.06em; text-transform:uppercase; }
.wd-table td { padding:6px 8px; border:1px solid var(--bg3); vertical-align:middle; }
.wd-table tbody tr:nth-child(even) td { background:var(--bg2); }
.wd-table tfoot td { background:var(--bg3); font-weight:600; font-size:12px; border:1px solid var(--bg3); padding:7px 8px; }
.wd-inp { width:100%; padding:4px 6px; border:1px solid var(--bg3); border-radius:var(--radius); background:var(--bg); color:var(--text); font-size:13px; font-family:inherit; text-align:right; }
.wd-inp:focus { outline:none; border-color:var(--gold); }
.wd-add-btn { display:inline-flex; align-items:center; gap:5px; padding:6px 14px; background:var(--accent-bg); color:var(--gold-light); border:none; border-radius:var(--radius); cursor:pointer; font-size:12px; font-family:inherit; margin-top:10px; letter-spacing:.03em; }
.wd-add-btn:hover { opacity:.85; }
.wd-del-btn { background:none; border:none; cursor:pointer; color:var(--red); font-size:14px; line-height:1; padding:2px 6px; }
"""
content = content.replace('</style>', css_add + '</style>', 1)

# ── 2. ps_amountR range 버그 수정 (updateKR 누락)
content = content.replace(
    "oninput=\"syncR('ps_amount','ps_amountR');calcPS()\"",
    "oninput=\"syncR('ps_amount','ps_amountR');updateKR('ps_amount');calcPS()\""
)

# ── 3. Tab 3: 현재나이/계좌구분/평가액 입력 추가
old_age = """      <div class="form-group">
        <label class="form-label" for="ps_age">수령 시작 나이</label>
        <div class="inp-wrap">
          <input type="number" id="ps_age" value="65" min="55" max="100" oninput="calcPS()">
          <span class="inp-unit">세</span>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">연금 유형</label>"""

new_age = """      <div class="form-group">
        <label class="form-label" for="ps_age">수령 시작 나이</label>
        <div class="inp-wrap">
          <input type="number" id="ps_age" value="65" min="55" max="100" oninput="calcPS()">
          <span class="inp-unit">세</span>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label" for="ps_cur_age">현재 나이 (연차 계산)</label>
        <div class="inp-wrap">
          <input type="number" id="ps_cur_age" value="65" min="55" max="100" oninput="calcPS()">
          <span class="inp-unit">세</span>
        </div>
        <div class="form-hint" id="ps_yr_info">수령 연차: 1년차</div>
      </div>

      <div class="form-group">
        <label class="form-label">계좌 개설 기준</label>
        <div class="radio-group">
          <div class="radio-opt">
            <input type="radio" name="ps_acct_type" id="ps_post2013" value="post2013" checked onchange="calcPS()">
            <label for="ps_post2013">2013년 이후 (10년)</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="ps_acct_type" id="ps_pre2013" value="pre2013" onchange="calcPS()">
            <label for="ps_pre2013">2013년 이전 (5년)</label>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label" for="ps_balance">연금계좌 현재 평가액</label>
        <div class="kr-num" id="ps_balance_kr"></div>
        <div class="inp-wrap">
          <input type="number" id="ps_balance" value="200000000" min="0" step="1000000"
            oninput="syncI('ps_balance','ps_balanceR');updateKR('ps_balance');calcPS()">
          <span class="inp-unit">원</span>
        </div>
        <input type="range" id="ps_balanceR" min="0" max="1000000000" step="5000000" value="200000000"
          oninput="syncR('ps_balance','ps_balanceR');updateKR('ps_balance');calcPS()">
        <div class="range-row"><span>0원</span><span>10억원</span></div>
        <div class="form-hint">연금수령한도 계산 기준</div>
      </div>

      <div class="form-group">
        <label class="form-label">연금 유형</label>"""

content = content.replace(old_age, new_age, 1)

# ── 4. Tab 3: 수령한도 매트릭스 카드 추가 (overSection 뒤, 결과 앞)
old_result = """    </div>
  </div>

  <!-- 결과 -->
  <div>
    <div class="card" id="ps_resultCard">"""

new_result = """    </div>

    <div class="card" style="margin-top:14px">
      <div class="card-title">연금수령한도 연차별 매트릭스</div>
      <div class="alert alert-info" style="font-size:11px;margin-bottom:10px">현재 평가액 기준 연차별 최대 인출 한도. 한도 초과 시 기타소득세 16.5%.</div>
      <div id="ps_limit_matrix"></div>
    </div>
  </div>

  <!-- 결과 -->
  <div>
    <div class="card" id="ps_resultCard">"""

content = content.replace(old_result, new_result, 1)

# ── 5. Tab 4: "연금 수령 기간" 카드 → 인출 계획 테이블
old_period = """    <div class="card">
      <div class="card-title">연금 수령 기간</div>
      <div class="form-group">
        <label class="form-label" for="rt_pensionYears">IRP 연금 수령 기간</label>
        <div class="radio-group">
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_u10" value="u10" checked onchange="calcRT()">
            <label for="rtpy_u10">10년 이하</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_u20" value="u20" onchange="calcRT()">
            <label for="rtpy_u20">10 ~ 20년</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_o20" value="o20" onchange="calcRT()">
            <label for="rtpy_o20">20년 초과</label>
          </div>
        </div>
        <div class="form-hint">10년 이하: 30% 감면 / 10~20년: 40% 감면 / 20년 초과: 50% 감면 (2026년 신설)</div>
      </div>
    </div>"""

new_period = """    <div class="card">
      <div class="card-title">인출 계획</div>
      <div class="form-group">
        <label class="form-label">총 수령 기간 (감면율 결정)</label>
        <div class="radio-group">
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_u10" value="u10" checked onchange="calcRT()">
            <label for="rtpy_u10">10년 이하 (30%↓)</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_u20" value="u20" onchange="calcRT()">
            <label for="rtpy_u20">10~20년 (40%↓)</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="rtPY" id="rtpy_o20" value="o20" onchange="calcRT()">
            <label for="rtpy_o20">20년 초과 (50%↓)</label>
          </div>
        </div>
        <div class="form-hint">2026년 기준. 총 수령 기간에 따라 감면율 결정.</div>
      </div>
      <hr class="divider">
      <div class="sub-title">연차별 인출 금액</div>
      <div class="alert alert-info" style="font-size:11px;margin-bottom:10px">
        각 연차 인출 세금 = 퇴직소득세 × (인출액 ÷ 총 퇴직금) × (1 − 감면율)
      </div>
      <table class="wd-table">
        <thead>
          <tr><th>수령 연차</th><th>인출금액 (원)</th><th>퇴직소득세</th><th>세후 수령액</th><th></th></tr>
        </thead>
        <tbody id="wd_tbody"></tbody>
        <tfoot id="wd_tfoot"></tfoot>
      </table>
      <button class="wd-add-btn" onclick="addWdRow()">+ 연차 추가</button>
      <div class="form-hint" style="margin-top:8px" id="wd_remaining"></div>
    </div>"""

content = content.replace(old_period, new_period, 1)

# ── 6. Tab nav: ⑤ 통합 계산 버튼 추가
content = content.replace(
    '  <button class="tab-btn" onclick="switchTab(3)">④ 퇴직금 IRP</button>',
    '  <button class="tab-btn" onclick="switchTab(3)">④ 퇴직금 IRP</button>\n  <button class="tab-btn" onclick="switchTab(4)">⑤ 통합 계산</button>'
)

# ── 7. Tab 5 HTML 추가
tab5 = """
<!-- ════════════════════════════════════════════
     TAB 5 : 통합 계산
     ════════════════════════════════════════════ -->
<div id="tab4" class="tab-content">
<div class="container">
<div class="split split-55">

  <!-- 입력 -->
  <div>
    <div class="card">
      <div class="card-title">개인납입 연금 수령</div>
      <div class="alert alert-info" style="font-size:11px;margin-bottom:12px">Tab ③의 개인납입 연금소득 (연금저축·IRP 개인납입분 + 운용수익).</div>
      <div class="form-group">
        <label class="form-label" for="it_ps_amount">연간 개인납입 연금 수령액</label>
        <div class="kr-num" id="it_ps_amount_kr"></div>
        <div class="inp-wrap">
          <input type="number" id="it_ps_amount" value="12000000" min="0" step="100000"
            oninput="syncI('it_ps_amount','it_ps_amountR');updateKR('it_ps_amount');calcIT()">
          <span class="inp-unit">원</span>
        </div>
        <input type="range" id="it_ps_amountR" min="0" max="60000000" step="100000" value="12000000"
          oninput="syncR('it_ps_amount','it_ps_amountR');updateKR('it_ps_amount');calcIT()">
        <div class="range-row"><span>0원</span><span>6,000만원</span></div>
      </div>
      <div class="form-group">
        <label class="form-label" for="it_age">수령 나이</label>
        <div class="inp-wrap">
          <input type="number" id="it_age" value="65" min="55" max="100" oninput="calcIT()">
          <span class="inp-unit">세</span>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">연금 유형</label>
        <div class="radio-group">
          <div class="radio-opt">
            <input type="radio" name="itType" id="it_fixed" value="fixed" checked onchange="calcIT()">
            <label for="it_fixed">확정기간형</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="itType" id="it_life" value="life" onchange="calcIT()">
            <label for="it_life">종신수령</label>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">퇴직금 IRP 연금 수령</div>
      <div class="alert alert-info" style="font-size:11px;margin-bottom:12px">Tab ④의 퇴직소득세 계산 결과를 아래에 입력하세요.</div>
      <div class="form-group">
        <label class="form-label" for="it_rt_annual">연간 IRP 인출액 (퇴직금 재원)</label>
        <div class="kr-num" id="it_rt_annual_kr"></div>
        <div class="inp-wrap">
          <input type="number" id="it_rt_annual" value="10000000" min="0" step="500000"
            oninput="syncI('it_rt_annual','it_rt_annualR');updateKR('it_rt_annual');calcIT()">
          <span class="inp-unit">원</span>
        </div>
        <input type="range" id="it_rt_annualR" min="0" max="100000000" step="500000" value="10000000"
          oninput="syncR('it_rt_annual','it_rt_annualR');updateKR('it_rt_annual');calcIT()">
        <div class="range-row"><span>0원</span><span>1억원</span></div>
      </div>
      <div class="form-group">
        <label class="form-label" for="it_rt_total">총 퇴직금</label>
        <div class="kr-num" id="it_rt_total_kr"></div>
        <div class="inp-wrap">
          <input type="number" id="it_rt_total" value="200000000" min="0" step="1000000"
            oninput="updateKR('it_rt_total');calcIT()">
          <span class="inp-unit">원</span>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label" for="it_rt_lump_tax">퇴직소득세 — 일시금 기준 (Tab ④에서 확인)</label>
        <div class="kr-num" id="it_rt_lump_tax_kr"></div>
        <div class="inp-wrap">
          <input type="number" id="it_rt_lump_tax" value="0" min="0" step="100000"
            oninput="updateKR('it_rt_lump_tax');calcIT()">
          <span class="inp-unit">원</span>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">연금 수령 기간 (감면율)</label>
        <div class="radio-group">
          <div class="radio-opt">
            <input type="radio" name="itPY" id="itpy_u10" value="u10" checked onchange="calcIT()">
            <label for="itpy_u10">10년 이하 (30%↓)</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="itPY" id="itpy_u20" value="u20" onchange="calcIT()">
            <label for="itpy_u20">10~20년 (40%↓)</label>
          </div>
          <div class="radio-opt">
            <input type="radio" name="itPY" id="itpy_o20" value="o20" onchange="calcIT()">
            <label for="itpy_o20">20년 초과 (50%↓)</label>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 결과 -->
  <div>
    <div class="card">
      <div class="card-title">통합 수령 현황</div>
      <div class="result-hero">
        <div class="result-hero-label">세후 월 수령액 합계</div>
        <div class="result-hero-value" id="it_net_monthly">—</div>
        <div class="result-hero-sub" id="it_net_sub"></div>
      </div>
      <div class="rrow">
        <span class="rrow-label">합산 연간 수령액</span>
        <span class="rrow-val blue" id="it_total_gross">—</span>
      </div>
      <div class="rrow">
        <span class="rrow-label">합산 연간 세금</span>
        <span class="rrow-val red" id="it_total_tax">—</span>
      </div>
      <div class="rrow">
        <span class="rrow-label">합산 세후 연간</span>
        <span class="rrow-val green" id="it_total_net">—</span>
      </div>
      <div class="rrow">
        <span class="rrow-label">실질 세율</span>
        <span class="rrow-val" id="it_eff_rate">—</span>
      </div>
      <hr class="divider">
      <div class="breakdown">
        <div class="breakdown-title">항목별 세금 내역</div>
        <div class="breakdown-row">
          <span>개인납입 연금 세금</span>
          <span id="it_ps_tax_d">—</span>
        </div>
        <div class="breakdown-row">
          <span>퇴직금 IRP 세금 (감면 후)</span>
          <span id="it_rt_tax_d">—</span>
        </div>
        <div class="breakdown-row total">
          <span>합산 세금</span>
          <span id="it_tax_sum">—</span>
        </div>
      </div>
      <div id="it_limit_warn" class="alert alert-warn" style="margin-top:12px;display:none"></div>
      <div class="breakdown" style="margin-top:12px">
        <div class="breakdown-title">월별 수령 구성</div>
        <div class="breakdown-row">
          <span>개인납입 연금 (세후 월)</span>
          <span id="it_ps_net_m">—</span>
        </div>
        <div class="breakdown-row">
          <span>퇴직금 IRP (세후 월)</span>
          <span id="it_rt_net_m">—</span>
        </div>
        <div class="breakdown-row total">
          <span>합계 (세후 월)</span>
          <span id="it_total_net_m">—</span>
        </div>
      </div>
    </div>
  </div>

</div>
</div>
</div>

"""
content = content.replace('</main>', tab5 + '</main>', 1)

# ── 8. 전체 JS 교체
new_script = r"""<script>
/* ══════════════════════════════════════
   HELPERS
══════════════════════════════════════ */
const $ = id => document.getElementById(id);
const v = id => parseFloat($(id).value) || 0;
const fmt = n => Math.round(n).toLocaleString('ko-KR') + '원';
const fmtN = n => Math.round(n).toLocaleString('ko-KR');
const fmtPct = n => n.toFixed(2) + '%';

function toKorean(n) {
  n = Math.round(Math.abs(parseFloat(n) || 0));
  if (!n) return '';
  const eok = Math.floor(n / 1e8);
  const man = Math.floor((n % 1e8) / 1e4);
  const won = n % 1e4;
  const parts = [];
  if (eok) parts.push(eok + '억');
  if (man) {
    const ch = Math.floor(man / 1000);
    const rem = man % 1000;
    parts.push((ch ? ch + '천' : '') + (rem || '') + '만');
  }
  if (won) parts.push(won + '원');
  return parts.join(' ');
}
function updateKR(id) {
  const el = $(id + '_kr');
  if (el) el.textContent = toKorean(v(id));
}
function syncR(inputId, rangeId) { $(inputId).value = $(rangeId).value; }
function syncI(inputId, rangeId) { $(rangeId).value = $(inputId).value; }

/* ══════════════════════════════════════
   TAB SWITCHING
══════════════════════════════════════ */
function switchTab(idx) {
  document.querySelectorAll('.tab-content').forEach((el, i) => el.classList.toggle('active', i === idx));
  document.querySelectorAll('.tab-btn').forEach((el, i) => el.classList.toggle('active', i === idx));
  if (idx === 3) { renderMatrix(); renderWdTable(); }
}

/* ══════════════════════════════════════
   SECTION TOGGLE
══════════════════════════════════════ */
function toggleSection(key) {
  const body = $(key + '_body');
  const chev = $(key + '_chev');
  const header = chev?.closest('.stoggle-header');
  const isOpen = !body.classList.contains('hidden');
  body.classList.toggle('hidden', isOpen);
  if (chev) chev.style.transform = isOpen ? '' : 'rotate(180deg)';
  if (header) header.classList.toggle('open', !isOpen);
}

/* ══════════════════════════════════════
   BASE TAX
══════════════════════════════════════ */
function baseTax(x) {
  x = Math.max(0, x);
  if (x <= 14000000)    return x * 0.06;
  if (x <= 50000000)    return 840000    + (x - 14000000) * 0.15;
  if (x <= 88000000)    return 6240000   + (x - 50000000) * 0.24;
  if (x <= 150000000)   return 15360000  + (x - 88000000) * 0.35;
  if (x <= 300000000)   return 37060000  + (x - 150000000) * 0.38;
  if (x <= 500000000)   return 94060000  + (x - 300000000) * 0.40;
  if (x <= 1000000000)  return 174060000 + (x - 500000000) * 0.42;
  return 384060000 + (x - 1000000000) * 0.45;
}
function earnedDeduction(salary) {
  if (salary <= 5000000)   return salary * 0.7;
  if (salary <= 15000000)  return 3500000  + (salary - 5000000)  * 0.4;
  if (salary <= 45000000)  return 7500000  + (salary - 15000000) * 0.15;
  if (salary <= 100000000) return 12000000 + (salary - 45000000) * 0.05;
  return Math.min(14750000 + (salary - 100000000) * 0.02, 20000000);
}
function pensionDeduction(total) {
  let d;
  if (total <= 3500000)       d = total;
  else if (total <= 7000000)  d = 3500000  + (total - 3500000) * 0.4;
  else if (total <= 14000000) d = 4900000  + (total - 7000000) * 0.2;
  else if (total <= 20000000) d = 6300000  + (total - 14000000) * 0.1;
  else                         d = 6900000  + (total - 20000000) * 0.05;
  return Math.min(d, 9000000);
}
function calcRetirementTax(pay, years) {
  years = Math.max(1, Math.round(years));
  pay = Math.max(0, pay);
  let ysD;
  if (years <= 5)       ysD = 1000000 * years;
  else if (years <= 10) ysD = 5000000  + 2000000 * (years - 5);
  else if (years <= 20) ysD = 15000000 + 2500000 * (years - 10);
  else                  ysD = 40000000 + 3000000 * (years - 20);
  ysD = Math.min(ysD, pay);
  const net  = Math.max(0, pay - ysD);
  const conv = net / years * 12;
  let cD;
  if (conv <= 8000000)        cD = conv;
  else if (conv <= 70000000)  cD = 8000000   + (conv - 8000000)  * 0.6;
  else if (conv <= 100000000) cD = 45200000  + (conv - 70000000) * 0.55;
  else if (conv <= 300000000) cD = 61700000  + (conv - 100000000)* 0.45;
  else                         cD = 151700000 + (conv - 300000000)* 0.35;
  const taxBase = Math.max(0, conv - cD);
  const retTax  = baseTax(taxBase) / 12 * years;
  const total   = retTax * 1.1;
  const rate    = pay > 0 ? total / pay * 100 : 0;
  return { ysD, conv, cD, taxBase, retTax, total, rate };
}

/* ══════════════════════════════════════
   납입 한도 연동
══════════════════════════════════════ */
function capIRP() {
  const maxIrp = Math.max(0, 18000000 - v('tc_ps'));
  $('tc_irp').max = maxIrp; $('tc_irpR').max = maxIrp;
  if (v('tc_irp') > maxIrp) { $('tc_irp').value = maxIrp; $('tc_irpR').value = maxIrp; updateKR('tc_irp'); }
}
function capPS() {
  const maxPs = Math.max(0, 18000000 - v('tc_irp'));
  $('tc_ps').max = maxPs; $('tc_psR').max = maxPs;
  if (v('tc_ps') > maxPs) { $('tc_ps').value = maxPs; $('tc_psR').value = maxPs; updateKR('tc_ps'); }
}

/* ══════════════════════════════════════
   TAB 2 : 세액공제
══════════════════════════════════════ */
function calcTC() {
  const isEarned = $('it_earned').checked;
  $('tc_earnedGroup').style.display = isEarned ? '' : 'none';
  $('tc_compGroup').style.display   = isEarned ? 'none' : '';
  const salary = v('tc_salary'), comp = v('tc_comp');
  const ps = v('tc_ps'), irp = v('tc_irp'), isa = v('tc_isa'), down = v('tc_down');
  const totalInput = ps + irp;
  const pct = Math.min(totalInput / 18000000 * 100, 100);
  $('tc_totalSum').innerHTML = '<strong>' + fmtN(Math.round(totalInput/10000)) + '만원</strong><span style="color:var(--text3);font-size:11px;margin-left:4px">/ 1,800만원</span>';
  $('tc_totalBarFill').style.width = pct + '%';
  $('tc_totalBarFill').style.background = totalInput > 14000000 ? 'var(--amber)' : 'var(--blue)';
  const rate = isEarned ? (salary <= 55000000 ? 0.165 : 0.132) : (comp <= 45000000 ? 0.165 : 0.132);
  const psElig  = Math.min(ps, 6000000);
  const irpRoom = 9000000 - psElig;
  const irpElig = Math.min(irp, irpRoom);
  const baseTotal = psElig + irpElig;
  const isaElig = Math.min(isa * 0.1, 3000000);
  const total  = baseTotal + isaElig;
  const credit = total * rate;
  const psOver = Math.max(0, ps - 6000000), irpOver = Math.max(0, irp - irpRoom);
  const rateStr = (rate * 100).toFixed(1) + '%';
  const income = isEarned ? salary : comp, thresh = isEarned ? 55000000 : 45000000;
  $('tc_rateAlert').innerHTML = '<strong>세액공제율 ' + rateStr + '</strong> — ' + (isEarned?'총급여':'종합소득금액') + ' ' + fmtN(thresh/10000) + '만원 ' + (income<=thresh?'이하':'초과') + ' 해당';
  $('tc_credit').textContent    = fmt(credit);
  $('tc_creditSub').textContent = '월 환산 ' + fmt(credit/12) + (isaElig>0 ? ' · ISA 추가 ' + fmt(isaElig*rate) + ' 포함' : '');
  $('tc_eligible').textContent  = fmt(total);
  $('tc_rate').textContent      = rateStr;
  $('tc_net').textContent       = fmt(total - credit);
  $('tc_monthly').textContent   = fmt((total - credit) / 12);
  $('tc_b_ps').textContent  = fmt(psElig);
  $('tc_b_irp').textContent = fmt(irpElig);
  if (isaElig > 0) { $('tc_b_isa_row').style.display = ''; $('tc_b_isa').textContent = '+' + fmt(isaElig); }
  else $('tc_b_isa_row').style.display = 'none';
  if (down > 0) { $('tc_b_down_row').style.display = ''; $('tc_b_down').textContent = fmt(down) + ' (비과세)'; }
  else $('tc_b_down_row').style.display = 'none';
  $('tc_b_total').textContent  = fmt(total);
  $('tc_psOver').textContent   = psOver  > 0 ? fmt(psOver)  : '없음';
  $('tc_irpOver').textContent  = irpOver > 0 ? fmt(irpOver) : '없음';
}

/* ══════════════════════════════════════
   TAB 3 : 연금 수령 + 수령한도 매트릭스
══════════════════════════════════════ */
function calcPS() {
  const amount  = v('ps_amount');
  const age     = v('ps_age') || 65;
  const curAge  = v('ps_cur_age') || age;
  const isLife  = $('ps_life').checked;
  const isPre   = $('ps_pre2013') && $('ps_pre2013').checked;
  const over15M = amount > 15000000;

  // 연금수령연차
  const yr    = Math.max(1, Math.round(curAge - age + 1));
  const maxYr = isPre ? 5 : 10;
  if ($('ps_yr_info')) {
    $('ps_yr_info').textContent = curAge > age
      ? '수령 시작(' + age + '세) → 현재(' + curAge + '세) = ' + yr + '년차' + (yr > maxYr ? ' (한도 없음 구간)' : '')
      : age + '세 수령 시작 → 1년차';
  }

  let rate;
  if (isLife) { rate = 0.044; }
  else { if (age >= 80) rate = 0.033; else if (age >= 70) rate = 0.044; else rate = 0.055; }

  const tax    = amount * rate;
  const netAnn = amount - tax;

  $('ps_rateInfo').innerHTML = '수령 나이 <strong>' + age + '세</strong> · ' + yr + '년차 · 세율 <strong>' + (rate*100).toFixed(1) + '%</strong>' +
    (isLife ? ' (종신 — 4.4% 고정)' : '') +
    (over15M ? ' · <span style="color:var(--amber)">1,500만원 초과 → 과세방법 선택</span>' : '');

  $('ps_tax').textContent        = fmt(tax);
  $('ps_taxSub').textContent     = '연금소득세 ' + (rate*100).toFixed(1) + '% (지방소득세 포함)';
  $('ps_rate').textContent       = (rate*100).toFixed(1) + '%';
  $('ps_monthly').textContent    = fmt(tax / 12);
  $('ps_netAnnual').textContent  = fmt(netAnn);
  $('ps_netMonthly').textContent = fmt(netAnn / 12);

  $('ps_overSection').classList.toggle('visible', over15M);
  $('ps_overResult').style.display = over15M ? '' : 'none';

  if (over15M) {
    const sepTax = amount * 0.165;
    const salary = v('ps_salary'), bizRev = v('ps_bizRev'), bizExp = v('ps_bizExp');
    const otherRev = v('ps_otherRev'), otherExpInput = v('ps_otherExp');
    const otherExp = otherExpInput > 0 ? otherExpInput : otherRev * 0.6;
    const intDiv = v('ps_intDiv'), dep = v('ps_dep') || 0;
    const np = v('ps_np'), hi = v('ps_hi'), otherDed = v('ps_otherDed');
    const pensionAmt = amount - pensionDeduction(amount);
    const earnedAmt  = salary > 0 ? Math.max(0, salary - earnedDeduction(salary)) : 0;
    const bizAmt     = Math.max(0, bizRev - bizExp);
    const otherAmt   = Math.max(0, otherRev - otherExp);
    const intDivAmt  = Math.max(0, intDiv - 20000000);
    const totalIncome = pensionAmt + earnedAmt + bizAmt + otherAmt + intDivAmt;
    const totalDed    = (1 + dep) * 1500000 + np + hi + otherDed;
    const taxBaseComp = Math.max(0, totalIncome - totalDed);
    const compTax     = baseTax(taxBaseComp) * 1.1;
    const hasInput    = salary>0||bizRev>0||otherRev>0||intDiv>0||dep>0||np>0||hi>0||otherDed>0;
    $('ps_sepTax').textContent  = fmt(sepTax);
    $('ps_compTax').textContent = hasInput ? fmt(compTax) : '소득 정보 입력 필요';
    $('ps_compDetail').textContent = hasInput ? '과세표준 ' + fmtN(taxBaseComp/10000) + '만원' : '위 항목 입력';
    const rec = $('ps_recommendation'), sepCard = $('ps_sepCard'), compCard = $('ps_compCard');
    if (hasInput) {
      const better = compTax < sepTax ? 'comp' : 'sep';
      sepCard.className  = 'cmp-card' + (better==='sep'  ? ' winner' : '');
      compCard.className = 'cmp-card' + (better==='comp' ? ' winner' : '');
      const diff = Math.abs(sepTax - compTax);
      rec.style.display = '';
      if (better === 'sep') { rec.className = 'alert alert-info'; rec.innerHTML = '<strong>분리과세가 유리합니다.</strong> 종합과세 대비 약 ' + fmt(diff) + ' 절세'; }
      else { rec.className = 'alert alert-green'; rec.innerHTML = '<strong>종합과세가 유리합니다.</strong> 분리과세 대비 약 ' + fmt(diff) + ' 절세'; }
      $('ps_compBreakdown').style.display = '';
      $('ps_b_pension').textContent = fmt(pensionAmt);
      $('ps_b_earned').textContent  = earnedAmt > 0 ? fmt(earnedAmt) : '—';
      $('ps_b_biz').textContent     = bizAmt > 0    ? fmt(bizAmt)    : '—';
      $('ps_b_other').textContent   = otherAmt > 0  ? fmt(otherAmt)  : '—';
      $('ps_b_intdiv').textContent  = intDivAmt > 0 ? fmt(intDivAmt) : '—';
      $('ps_b_total').textContent   = fmt(totalIncome);
      $('ps_b_ded').textContent     = fmt(totalDed);
      $('ps_b_base').textContent    = fmt(taxBaseComp);
      $('ps_b_tax').textContent     = fmt(compTax);
    } else {
      sepCard.className = compCard.className = 'cmp-card';
      rec.style.display = 'none';
      $('ps_compBreakdown').style.display = 'none';
    }
  }

  renderLimitMatrix(yr, isPre, v('ps_balance'));
}

function renderLimitMatrix(curYr, isPre, balance) {
  const el = $('ps_limit_matrix');
  if (!el) return;
  const maxYr = isPre ? 5 : 10;
  const denom0 = isPre ? 6 : 11;
  const note = isPre ? '2013년 이전 계좌 — 5년 기준 (6년차부터 한도 없음)' : '2013년 이후 계좌 — 10년 기준 (11년차부터 한도 없음)';

  let html = '<div style="font-size:11px;color:var(--text3);margin-bottom:8px">한도 = 평가액 ÷ (' + denom0 + ' − 연차) × 120% &nbsp;·&nbsp; ' + note + '</div>';
  html += '<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:12px;min-width:300px">';
  html += '<tr style="background:var(--accent-bg)">';
  html += '<th style="padding:6px 8px;border:1px solid var(--bg3);color:var(--gold-light);font-weight:500;text-align:center">연차</th>';
  html += '<th style="padding:6px 8px;border:1px solid var(--bg3);color:var(--gold-light);font-weight:500;text-align:center">한도율</th>';
  html += '<th style="padding:6px 8px;border:1px solid var(--bg3);color:var(--gold-light);font-weight:500;text-align:right">한도금액</th>';
  html += '</tr>';

  for (var n = 1; n <= maxYr; n++) {
    var denom = denom0 - n;
    var limitRate = denom > 0 ? (1 / denom * 1.2) : 1.2;
    var limitAmt = balance * limitRate;
    var isCur = (n === curYr) && curYr <= maxYr;
    var rowBg = isCur ? 'rgba(196,147,63,.2)' : (n % 2 === 0 ? 'var(--bg2)' : '');
    var fw = isCur ? 'font-weight:700;' : '';
    var color = isCur ? 'color:var(--amber);' : '';
    html += '<tr style="background:' + rowBg + '">';
    html += '<td style="padding:5px 8px;border:1px solid var(--bg3);text-align:center;' + fw + color + '">' + n + '년차' + (isCur ? ' ◀ 현재' : '') + (curYr > maxYr && n === maxYr ? '<span style="color:var(--green);font-size:10px;margin-left:4px">(현재는 한도없음)</span>' : '') + '</td>';
    html += '<td style="padding:5px 8px;border:1px solid var(--bg3);text-align:center;' + fw + color + '">' + (limitRate*100).toFixed(1) + '%</td>';
    html += '<td style="padding:5px 8px;border:1px solid var(--bg3);text-align:right;color:var(--blue);' + fw + '">' + (balance > 0 ? fmtN(Math.round(limitAmt/10000)) + '만원' : '—') + '</td>';
    html += '</tr>';
  }

  var unlimitYr = maxYr + 1;
  var isUnlimit = curYr >= unlimitYr;
  html += '<tr style="background:' + (isUnlimit ? 'rgba(42,124,111,.1)' : '') + '">';
  html += '<td style="padding:5px 8px;border:1px solid var(--bg3);text-align:center;' + (isUnlimit ? 'font-weight:700;color:var(--green);' : '') + '">' + unlimitYr + '년차~' + (isUnlimit ? ' ◀ 현재' : '') + '</td>';
  html += '<td colspan="2" style="padding:5px 8px;border:1px solid var(--bg3);text-align:center;color:var(--green);font-weight:600">한도 없음</td>';
  html += '</tr></table></div>';
  el.innerHTML = html;
}

/* ══════════════════════════════════════
   TAB 4 : 퇴직소득세 + 인출 계획
══════════════════════════════════════ */
var wdRows = [{ yr: 1, amt: 20000000 }];

function addWdRow() {
  var maxYr = wdRows.length > 0 ? Math.max.apply(null, wdRows.map(function(r){return r.yr;})) + 1 : 1;
  wdRows.push({ yr: maxYr, amt: 0 });
  renderWdTable();
  calcRT();
}
function removeWdRow(idx) {
  wdRows.splice(idx, 1);
  renderWdTable();
  calcRT();
}
function renderWdTable() {
  var tbody = $('wd_tbody');
  if (!tbody) return;
  tbody.innerHTML = wdRows.map(function(r, i) {
    return '<tr>' +
      '<td style="text-align:center"><input class="wd-inp" type="number" value="' + r.yr + '" min="1" max="50" style="width:55px;text-align:center" oninput="wdRows['+i+'].yr=parseInt(this.value)||1;calcRT()">년차</td>' +
      '<td><input class="wd-inp" type="number" value="' + r.amt + '" min="0" step="1000000" oninput="wdRows['+i+'].amt=parseFloat(this.value)||0;calcRT()"></td>' +
      '<td id="wd_tax_'+i+'" style="text-align:right;color:var(--red)">—</td>' +
      '<td id="wd_net_'+i+'" style="text-align:right;color:var(--green)">—</td>' +
      '<td style="text-align:center"><button class="wd-del-btn" onclick="removeWdRow('+i+')">✕</button></td>' +
    '</tr>';
  }).join('');
}

function setRtMode(mode) {
  $('rt_mAuto').classList.toggle('active', mode === 'auto');
  $('rt_mManual').classList.toggle('active', mode === 'manual');
  $('rt_autoPanel').classList.toggle('active', mode === 'auto');
  $('rt_manualPanel').classList.toggle('active', mode === 'manual');
  calcRT();
}

function calcRT() {
  var isAuto = $('rt_mAuto').classList.contains('active');
  var discount = $('rtpy_u10').checked ? 0.30 : ($('rtpy_u20').checked ? 0.40 : 0.50);
  var pay, totalTax, rate, showBreakdown;

  if (isAuto) {
    pay = v('rt_pay');
    var years = v('rt_years');
    var res = calcRetirementTax(pay, years);
    totalTax = res.total; rate = res.rate; showBreakdown = true;
    $('rt_b_pay').textContent  = fmt(pay);
    $('rt_b_ysd').textContent  = fmt(res.ysD);
    $('rt_b_conv').textContent = fmt(res.conv);
    $('rt_b_cd').textContent   = fmt(res.cD);
    $('rt_b_base').textContent = fmt(res.taxBase);
    $('rt_b_tax').textContent  = fmt(res.total);
  } else {
    pay = v('rt_pay2');
    totalTax = pay * (v('rt_manRate') / 100);
    rate = v('rt_manRate');
    showBreakdown = false;
  }

  $('rt_breakdown').style.display = showBreakdown ? '' : 'none';

  // 인출 계획 테이블 업데이트
  var totalWd = 0, totalWdTax = 0;
  wdRows.forEach(function(r, i) {
    var rowTax = pay > 0 ? (r.amt / pay) * totalTax * (1 - discount) : 0;
    var rowNet = r.amt - rowTax;
    totalWd += r.amt; totalWdTax += rowTax;
    var tEl = $('wd_tax_' + i), nEl = $('wd_net_' + i);
    if (tEl) tEl.textContent = r.amt > 0 ? fmt(rowTax) : '—';
    if (nEl) nEl.textContent = r.amt > 0 ? fmt(rowNet) : '—';
  });

  var tfoot = $('wd_tfoot');
  if (tfoot && wdRows.length > 0) {
    tfoot.innerHTML = '<tr><td style="text-align:center">합계</td><td style="text-align:right">' + fmt(totalWd) + '</td><td style="text-align:right;color:var(--red)">' + fmt(totalWdTax) + '</td><td style="text-align:right;color:var(--green)">' + fmt(totalWd - totalWdTax) + '</td><td></td></tr>';
  }

  var remEl = $('wd_remaining');
  if (remEl && pay > 0) {
    var remaining = pay - totalWd;
    remEl.textContent = '총 퇴직금 미계획 잔액: ' + fmt(Math.max(0, remaining));
    remEl.style.color = remaining < 0 ? 'var(--red)' : 'var(--text3)';
  }

  var pensionTax = totalTax * (1 - discount);
  var saved = totalTax - pensionTax;
  $('rt_lumpTax').textContent    = fmt(totalTax);
  $('rt_lumpRate').textContent   = rate.toFixed(2) + '%';
  $('rt_pensionTax').textContent = fmt(pensionTax);
  $('rt_saved').textContent      = fmt(saved);
  $('rt_savedRate').textContent  = (discount * 100).toFixed(0) + '% 감면';
  $('rt_lumpNet').textContent    = fmt(pay - totalTax);
  $('rt_pensionNet').textContent = fmt(pay - pensionTax);
  var detailMap = { u10:'10년 이하 수령 (30% 감면)', u20:'10~20년 수령 (40% 감면)', o20:'20년 초과 수령 (50% 감면)' };
  var pyVal = document.querySelector('input[name="rtPY"]:checked').value;
  $('rt_pensionDetail').textContent = detailMap[pyVal];
  $('rt_discountBadge').textContent = (discount * 100).toFixed(0) + '% 절세';
}

/* ══════════════════════════════════════
   TAB 4 : 매트릭스
══════════════════════════════════════ */
function renderMatrix() {
  var pays  = [30000000,50000000,100000000,200000000,300000000,500000000,700000000,1000000000];
  var years = [5,10,15,20,25,30];
  var payLabels = ['3천만','5천만','1억','2억','3억','5억','7억','10억'];
  var tbl = $('rt_matrix');
  if (!tbl) return;
  var html = '<tr><th>근속연수 \\ 퇴직금</th>';
  payLabels.forEach(function(l) { html += '<th>' + l + '원</th>'; });
  html += '</tr>';
  years.forEach(function(y) {
    html += '<tr><td class="rh">' + y + '년</td>';
    pays.forEach(function(p) {
      var res = calcRetirementTax(p, y);
      var r = res.rate;
      var bg = rateColor(r), fg = r > 10 ? '#fff' : '#1a1a2e';
      html += '<td style="background:' + bg + ';color:' + fg + ';font-weight:600">' + r.toFixed(1) + '%</td>';
    });
    html += '</tr>';
  });
  tbl.innerHTML = html;
  var legend = $('rt_legend');
  var stops = [{label:'0~3%',color:rateColor(1.5)},{label:'3~6%',color:rateColor(4.5)},{label:'6~10%',color:rateColor(8)},{label:'10~15%',color:rateColor(12.5)},{label:'15%+',color:rateColor(18)}];
  legend.innerHTML = stops.map(function(s) { return '<span style="display:flex;align-items:center;gap:5px"><span class="legend-dot" style="background:'+s.color+'"></span>'+s.label+'</span>'; }).join('');
}
function rateColor(r) {
  if (r < 3)  return '#c8e6c9';
  if (r < 6)  return '#81c784';
  if (r < 10) return '#ffcc02';
  if (r < 15) return '#ff9800';
  return '#e53935';
}

/* ══════════════════════════════════════
   TAB 5 : 통합 계산
══════════════════════════════════════ */
function calcIT() {
  var psAmount  = v('it_ps_amount');
  var age       = v('it_age') || 65;
  var isLife    = $('it_life') && $('it_life').checked;
  var rtAnnual  = v('it_rt_annual');
  var rtTotal   = v('it_rt_total');
  var rtLumpTax = v('it_rt_lump_tax');
  var itDiscount = $('itpy_u10').checked ? 0.30 : ($('itpy_u20').checked ? 0.40 : 0.50);

  var psRate;
  if (isLife) { psRate = 0.044; }
  else { if (age >= 80) psRate = 0.033; else if (age >= 70) psRate = 0.044; else psRate = 0.055; }

  var psTax = psAmount * psRate;
  var psNet = psAmount - psTax;
  var rtTax = rtTotal > 0 ? (rtAnnual / rtTotal) * rtLumpTax * (1 - itDiscount) : 0;
  var rtNet = rtAnnual - rtTax;

  var totalGross = psAmount + rtAnnual;
  var totalTax   = psTax + rtTax;
  var totalNet   = totalGross - totalTax;
  var effRate    = totalGross > 0 ? totalTax / totalGross * 100 : 0;

  $('it_net_monthly').textContent = fmt(totalNet / 12);
  $('it_net_sub').textContent     = '연간 ' + fmt(totalNet) + ' · 세금 ' + fmt(totalTax);
  $('it_total_gross').textContent = fmt(totalGross);
  $('it_total_tax').textContent   = fmt(totalTax);
  $('it_total_net').textContent   = fmt(totalNet);
  $('it_eff_rate').textContent    = effRate.toFixed(2) + '%';
  $('it_ps_tax_d').textContent    = fmt(psTax);
  $('it_rt_tax_d').textContent    = fmt(rtTax);
  $('it_tax_sum').textContent     = fmt(totalTax);
  $('it_ps_net_m').textContent    = fmt(psNet / 12);
  $('it_rt_net_m').textContent    = fmt(rtNet / 12);
  $('it_total_net_m').textContent = fmt(totalNet / 12);

  var warnEl = $('it_limit_warn');
  if (psAmount > 15000000) {
    warnEl.style.display = '';
    warnEl.textContent = '개인납입 연금소득 ' + fmtN(Math.round(psAmount/10000)) + '만원이 분리과세 한도(1,500만원)를 초과합니다. Tab ③에서 분리과세 vs 종합과세 비교를 확인하세요.';
  } else {
    warnEl.style.display = 'none';
  }
}

/* ══════════════════════════════════════
   INIT
══════════════════════════════════════ */
['tc_salary','tc_ps','tc_irp','ps_amount','ps_balance',
 'rt_pay','rt_pay2','it_ps_amount','it_rt_annual','it_rt_total','it_rt_lump_tax'].forEach(updateKR);
calcTC();
calcPS();
calcRT();
calcIT();
renderWdTable();
</script>"""

content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('done')
