#!/usr/bin/env python3
# fix_layout2.py
# 1. 생년월일 → inp-row (inp-wrap 좌, kr-num 우)
# 2. 1500만원 섹션 amount fields → swap (inp-wrap 좌, kr-num 우)
# 3. renderWdAccs() JS amount inp-rows → swap
# 4. 1500만원 섹션 → 고정 card (접고펴기 제거)

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original = html

# ═══════════════════════════════════════════════════
# 1. 생년월일 inp-row 추가
# ═══════════════════════════════════════════════════
old = (
    '        <label class="form-label" for="wd_birth">생년월일</label>\n'
    '<div class="inp-wrap">\n'
    '          <input type="date" id="wd_birth" value="1961-01-01" oninput="calcWD()">\n'
    '        </div>\n'
    '        <div id="wd_age_display" class="kr-num"></div>\n'
    '      </div>'
)
new = (
    '        <label class="form-label" for="wd_birth">생년월일</label>\n'
    '        <div class="inp-row">\n'
    '          <div class="inp-wrap">\n'
    '            <input type="date" id="wd_birth" value="1961-01-01" oninput="calcWD()">\n'
    '          </div>\n'
    '          <div id="wd_age_display" class="kr-num"></div>\n'
    '        </div>\n'
    '      </div>'
)
if old in html:
    html = html.replace(old, new); print('[OK] 생년월일 inp-row')
else:
    print('[MISS] 생년월일 inp-row')

# ═══════════════════════════════════════════════════
# 2. 1500만원 정적 HTML — kr-num ↔ inp-wrap swap
# ═══════════════════════════════════════════════════
# 패턴: 10칸 들여쓰기 inp-row, 12칸 kr-num, 12칸 inp-wrap
pattern_static = (
    r'([ ]{10}<div class="inp-row">\n)'
    r'([ ]{12}<div class="kr-num" id="wd_[^"]+_kr"></div>\n)'
    r'([ ]{12}<div class="inp-wrap">\n'
    r'[ ]{14}<input [^\n]+\n'
    r'[ ]{14}<span class="inp-unit">원</span>\n'
    r'[ ]{12}</div>\n)'
    r'([ ]{10}</div>)'
)

def swap_static(m):
    return m.group(1) + m.group(3) + m.group(2) + m.group(4)

html, n = re.subn(pattern_static, swap_static, html)
print(f'[OK] 정적 HTML swap: {n}개')

# ═══════════════════════════════════════════════════
# 3. renderWdAccs() JS — wd_bal
# ═══════════════════════════════════════════════════
old = (
    "                '<div class=\"inp-row\">',\n"
    "                  '<div id=\"wd_bal_lbl_' + i + '\" class=\"kr-num\">' + (acc.balance > 0 ? toKorean(acc.balance) : '') + '</div>',\n"
    "                  '<div class=\"inp-wrap\">',\n"
    "                    '<input id=\"wd_bal_input_' + i + '\" type=\"number\" value=\"' + acc.balance + '\" min=\"0\" step=\"1000000\" oninput=\"wdAccs[' + i + '].balance=parseFloat(this.value)||0;updateWdAccLabel(' + i + ');calcWD()\">',\n"
    "                    '<span class=\"inp-unit\">원</span>',\n"
    "                  '</div>',\n"
    "                '</div>',"
)
new = (
    "                '<div class=\"inp-row\">',\n"
    "                  '<div class=\"inp-wrap\">',\n"
    "                    '<input id=\"wd_bal_input_' + i + '\" type=\"number\" value=\"' + acc.balance + '\" min=\"0\" step=\"1000000\" oninput=\"wdAccs[' + i + '].balance=parseFloat(this.value)||0;updateWdAccLabel(' + i + ');calcWD()\">',\n"
    "                    '<span class=\"inp-unit\">원</span>',\n"
    "                  '</div>',\n"
    "                  '<div id=\"wd_bal_lbl_' + i + '\" class=\"kr-num\">' + (acc.balance > 0 ? toKorean(acc.balance) : '') + '</div>',\n"
    "                '</div>',"
)
if old in html:
    html = html.replace(old, new); print('[OK] JS wd_bal')
else:
    print('[MISS] JS wd_bal')

# wd_op (구법 계좌 연간 수령 금액)
old = (
    "              '<div class=\"inp-row\">',\n"
    "                '<div id=\"wd_op_kr_' + i + '\" class=\"kr-num\">' + ((acc.withdrawal||0) > 0 ? toKorean(acc.withdrawal) : '') + '</div>',\n"
    "                '<div class=\"inp-wrap\">',\n"
    "                  '<input type=\"number\" value=\"' + (acc.withdrawal||0) + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].withdrawal=parseFloat(this.value)||0;calcWD()\">',\n"
    "                  '<span class=\"inp-unit\">원</span>',\n"
    "                '</div>',\n"
    "              '</div>',"
)
new = (
    "              '<div class=\"inp-row\">',\n"
    "                '<div class=\"inp-wrap\">',\n"
    "                  '<input type=\"number\" value=\"' + (acc.withdrawal||0) + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].withdrawal=parseFloat(this.value)||0;calcWD()\">',\n"
    "                  '<span class=\"inp-unit\">원</span>',\n"
    "                '</div>',\n"
    "                '<div id=\"wd_op_kr_' + i + '\" class=\"kr-num\">' + ((acc.withdrawal||0) > 0 ? toKorean(acc.withdrawal) : '') + '</div>',\n"
    "              '</div>',"
)
if old in html:
    html = html.replace(old, new); print('[OK] JS wd_op')
else:
    print('[MISS] JS wd_op')

# wd_src1
old = (
    "                  '<div class=\"inp-row\">',\n"
    "                    '<div id=\"wd_src1_kr_' + i + '\" class=\"kr-num\">' + (acc.src1 > 0 ? toKorean(acc.src1) : '') + '</div>',\n"
    "                    '<div class=\"inp-wrap\">',\n"
    "                      '<input type=\"number\" value=\"' + acc.src1 + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].src1=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                      '<span class=\"inp-unit\">원</span>',\n"
    "                    '</div>',\n"
    "                  '</div>',"
)
new = (
    "                  '<div class=\"inp-row\">',\n"
    "                    '<div class=\"inp-wrap\">',\n"
    "                      '<input type=\"number\" value=\"' + acc.src1 + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].src1=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                      '<span class=\"inp-unit\">원</span>',\n"
    "                    '</div>',\n"
    "                    '<div id=\"wd_src1_kr_' + i + '\" class=\"kr-num\">' + (acc.src1 > 0 ? toKorean(acc.src1) : '') + '</div>',\n"
    "                  '</div>',"
)
if old in html:
    html = html.replace(old, new); print('[OK] JS wd_src1')
else:
    print('[MISS] JS wd_src1')

# wd_src2
old = (
    "                    '<div class=\"inp-row\">',\n"
    "                      '<div id=\"wd_src2_kr_' + i + '\" class=\"kr-num\">' + (acc.src2 > 0 ? toKorean(acc.src2) : '') + '</div>',\n"
    "                      '<div class=\"inp-wrap\">',\n"
    "                        '<input type=\"number\" value=\"' + acc.src2 + '\" min=\"0\" step=\"1000000\" oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                        '<span class=\"inp-unit\">원</span>',\n"
    "                      '</div>',\n"
    "                    '</div>',"
)
new = (
    "                    '<div class=\"inp-row\">',\n"
    "                      '<div class=\"inp-wrap\">',\n"
    "                        '<input type=\"number\" value=\"' + acc.src2 + '\" min=\"0\" step=\"1000000\" oninput=\"wdAccs[' + i + '].src2=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                        '<span class=\"inp-unit\">원</span>',\n"
    "                      '</div>',\n"
    "                      '<div id=\"wd_src2_kr_' + i + '\" class=\"kr-num\">' + (acc.src2 > 0 ? toKorean(acc.src2) : '') + '</div>',\n"
    "                    '</div>',"
)
if old in html:
    html = html.replace(old, new); print('[OK] JS wd_src2')
else:
    print('[MISS] JS wd_src2')

# wd_src3
old = (
    "                  '<div class=\"inp-row\">',\n"
    "                    '<div id=\"wd_src3_kr_' + i + '\" class=\"kr-num\">' + (acc.src3 > 0 ? toKorean(acc.src3) : '') + '</div>',\n"
    "                    '<div class=\"inp-wrap\">',\n"
    "                      '<input type=\"number\" value=\"' + acc.src3 + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].src3=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                      '<span class=\"inp-unit\">원</span>',\n"
    "                    '</div>',\n"
    "                  '</div>',"
)
new = (
    "                  '<div class=\"inp-row\">',\n"
    "                    '<div class=\"inp-wrap\">',\n"
    "                      '<input type=\"number\" value=\"' + acc.src3 + '\" min=\"0\" step=\"500000\" oninput=\"wdAccs[' + i + '].src3=parseFloat(this.value)||0;syncWdSrc(' + i + ')\">',\n"
    "                      '<span class=\"inp-unit\">원</span>',\n"
    "                    '</div>',\n"
    "                    '<div id=\"wd_src3_kr_' + i + '\" class=\"kr-num\">' + (acc.src3 > 0 ? toKorean(acc.src3) : '') + '</div>',\n"
    "                  '</div>',"
)
if old in html:
    html = html.replace(old, new); print('[OK] JS wd_src3')
else:
    print('[MISS] JS wd_src3')

# ═══════════════════════════════════════════════════
# 4. 1500만원 섹션 → 고정 card (toggleable 제거)
# ═══════════════════════════════════════════════════
old = (
    '    <div id="wd_overSection" class="section-toggle" style="margin-top:10px">\n'
    '      <button class="stoggle-header" onclick="toggleSection(\'wd_over\')">\n'
    '        <span>1,500만원 초과 — 종합과세 모의계산</span>\n'
    '        <i class="chev" id="wd_over_chev">▼</i>\n'
    '      </button>\n'
    '      <div class="stoggle-body hidden" id="wd_over_body">'
)
new = (
    '    <div id="wd_overSection" class="card section-toggle" style="margin-top:10px">\n'
    '      <div class="card-title">종합과세 모의계산</div>\n'
    '      <div id="wd_over_body">'
)
if old in html:
    html = html.replace(old, new); print('[OK] wd_overSection → card')
else:
    print('[MISS] wd_overSection → card')

# ═══════════════════════════════════════════════════
if html != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n파일 저장 완료.')
else:
    print('\n변경 없음.')
