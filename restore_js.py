content = open('index.html', encoding='utf-8').read()

rt_js = r"""
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

function renderMatrix(tblId, legId) {
  var pays  = [30000000,50000000,100000000,200000000,300000000,500000000,700000000,1000000000];
  var years = [5,10,15,20,25,30];
  var payLabels = ['3천만','5천만','1억','2억','3억','5억','7억','10억'];
  var tbl = $(tblId || 'rt_matrix');
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
  var legend = $(legId || 'rt_legend');
  if (!legend) return;
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

"""

# INIT 바로 앞에 삽입
target = '/* ══════════════════════════════════════\n   INIT'
content = content.replace(target, rt_js + target, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

# 검증
checks = [
    'function calcRT',
    'function renderMatrix',
    'function setRtMode',
    'function renderWdTable',
    'function rateColor',
]
for fn in checks:
    print(fn + ':', fn in content)
