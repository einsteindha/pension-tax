content = open('index.html', encoding='utf-8').read()

# ── 1. 수령정보·계좌정보 순서 교체 + 수령정보 카드에 id·경고 div 추가 ────────
old_layout = (
    '    <!-- 계좌 목록 -->\n'
    '    <div class="card">\n'
    '      <div class="card-title" style="display:flex;justify-content:space-between;align-items:center">\n'
    '        <span>계좌 정보</span>\n'
    '        <button onclick="addWdAcc()" style="font-size:11px;padding:4px 10px;background:var(--blue);color:#fff;border:none;border-radius:var(--radius);cursor:pointer">+ 계좌 추가</button>\n'
    '      </div>\n'
    '      <div id="wd_accs"></div>\n'
    '    </div>\n'
    '\n'
    '    <!-- 공통 수령 정보 -->\n'
    '    <div class="card" style="margin-top:10px">\n'
    '      <div class="card-title">수령 정보</div>\n'
    '\n'
    '      <div class="form-group">\n'
    '        <label class="form-label" for="wd_age">현재 나이 (수령 나이)</label>\n'
    '        <div class="inp-wrap">\n'
    '          <input type="number" id="wd_age" value="65" min="18" max="100" oninput="calcWD()">\n'
    '          <span class="inp-unit">세</span>\n'
    '        </div>\n'
    '      </div>\n'
    '\n'
    '\n'
    '    </div>\n'
)
new_layout = (
    '    <!-- 공통 수령 정보 -->\n'
    '    <div class="card" id="wd_age_card" style="transition:background .3s,border-color .3s;border:1.5px solid transparent">\n'
    '      <div class="card-title">수령 정보</div>\n'
    '\n'
    '      <div class="form-group">\n'
    '        <label class="form-label" for="wd_age">현재 나이 (수령 나이)</label>\n'
    '        <div class="inp-wrap">\n'
    '          <input type="number" id="wd_age" value="65" min="18" max="100" oninput="calcWD()">\n'
    '          <span class="inp-unit">세</span>\n'
    '        </div>\n'
    '      </div>\n'
    '\n'
    '      <div id="wd_under55_warn" style="display:none;margin-top:6px" class="alert alert-warn">\n'
    '        <strong>55세 미만 — 연금 수령 불가</strong><br>\n'
    '        연금계좌 인출 요건(만 55세 이상)을 충족하지 않습니다.<br>\n'
    '        ③ 세액공제O+수익 재원에 <strong>기타소득세 16.5%</strong> 적용, 연금소득세 감면 혜택 없음.\n'
    '      </div>\n'
    '\n'
    '    </div>\n'
    '\n'
    '    <!-- 계좌 목록 -->\n'
    '    <div class="card" style="margin-top:10px">\n'
    '      <div class="card-title" style="display:flex;justify-content:space-between;align-items:center">\n'
    '        <span>계좌 정보</span>\n'
    '        <button onclick="addWdAcc()" style="font-size:11px;padding:4px 10px;background:var(--blue);color:#fff;border:none;border-radius:var(--radius);cursor:pointer">+ 계좌 추가</button>\n'
    '      </div>\n'
    '      <div id="wd_accs"></div>\n'
    '    </div>\n'
)
assert old_layout in content, '레이아웃 블록 없음!'
content = content.replace(old_layout, new_layout, 1)

# ── 2. 결과 패널: wd_eligibility 아래에 55세 미만 안내 추가 ────────────────
old_result_top = (
    '      <div id="wd_eligibility" class="alert alert-info" style="font-size:11px;margin-bottom:10px"></div>\n'
    '\n'
    '      <div class="result-hero">'
)
new_result_top = (
    '      <div id="wd_eligibility" class="alert alert-info" style="font-size:11px;margin-bottom:10px"></div>\n'
    '\n'
    '      <div id="wd_under55_notice" style="display:none;margin-bottom:10px" class="alert alert-warn">\n'
    '        <strong>연금 외 수령만 가능</strong> — 55세 미만으로 연금수령 요건 미충족.<br>\n'
    '        ③ 재원은 기타소득세 16.5% 적용. ①은 비과세, ②는 퇴직소득세 그대로 적용.\n'
    '      </div>\n'
    '\n'
    '      <div class="result-hero">'
)
assert old_result_top in content, '결과 패널 상단 없음!'
content = content.replace(old_result_top, new_result_top, 1)

# ── 3. calcWD JS: 55세 미만 경고 토글 추가 ──────────────────────────────────
old_elig_block = (
    "  if ($('wd_eligibility')) {\n"
    "    $('wd_eligibility').textContent = eligMsg;\n"
    "    $('wd_eligibility').className = (elig55 && elig5yr) ? 'alert alert-info' : 'alert alert-warn';\n"
    "  }"
)
new_elig_block = (
    "  if ($('wd_eligibility')) {\n"
    "    $('wd_eligibility').textContent = eligMsg;\n"
    "    $('wd_eligibility').className = (elig55 && elig5yr) ? 'alert alert-info' : 'alert alert-warn';\n"
    "  }\n"
    "  var ageCard = $('wd_age_card');\n"
    "  if (ageCard) {\n"
    "    ageCard.style.background = elig55 ? '' : 'rgba(239,68,68,.04)';\n"
    "    ageCard.style.borderColor = elig55 ? 'transparent' : 'rgba(239,68,68,.35)';\n"
    "  }\n"
    "  var u55w = $('wd_under55_warn');   if (u55w) u55w.style.display = elig55 ? 'none' : '';\n"
    "  var u55n = $('wd_under55_notice'); if (u55n) u55n.style.display = elig55 ? 'none' : '';"
)
assert old_elig_block in content, 'wd_eligibility JS 블록 없음!'
content = content.replace(old_elig_block, new_elig_block, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    'wd_age_card',
    'wd_under55_warn',
    'wd_under55_notice',
    'u55w',
    'ageCard.style.background',
]
for k in checks:
    print(k + ':', k in content)
