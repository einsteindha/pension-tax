#!/usr/bin/env python3
# fix_inprow_1500.py — 1500만원 섹션 inp-row 변환 + wd_otherDed kr-num 추가

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 공통 변환 함수 ──────────────────────────────────────────────────────────
def to_inprow_no_hint(fid, label_tag, inp_tag, unit='원'):
    """kr-num 있고 form-hint 없는 필드"""
    old = (
        label_tag + '\n'
        '<div class="inp-wrap">\n'
        '            ' + inp_tag + '\n'
        '            <span class="inp-unit">' + unit + '</span>\n'
        '          </div>\n'
        '\n'
        '          <div class="kr-num" id="' + fid + '_kr"></div>\n'
        '        </div>'
    )
    new = (
        label_tag + '\n'
        '          <div class="inp-row">\n'
        '            <div class="kr-num" id="' + fid + '_kr"></div>\n'
        '            <div class="inp-wrap">\n'
        '              ' + inp_tag + '\n'
        '              <span class="inp-unit">' + unit + '</span>\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>'
    )
    return old, new

def to_inprow_with_hint(fid, label_tag, inp_tag, hint_html, unit='원'):
    """kr-num 있고 form-hint 있는 필드"""
    old = (
        label_tag + '\n'
        '<div class="inp-wrap">\n'
        '            ' + inp_tag + '\n'
        '            <span class="inp-unit">' + unit + '</span>\n'
        '          </div>\n'
        '\n'
        '          <div class="kr-num" id="' + fid + '_kr"></div>\n'
        '          ' + hint_html + '\n'
        '        </div>'
    )
    new = (
        label_tag + '\n'
        '          <div class="inp-row">\n'
        '            <div class="kr-num" id="' + fid + '_kr"></div>\n'
        '            <div class="inp-wrap">\n'
        '              ' + inp_tag + '\n'
        '              <span class="inp-unit">' + unit + '</span>\n'
        '            </div>\n'
        '          </div>\n'
        '          ' + hint_html + '\n'
        '        </div>'
    )
    return old, new

# ── 각 필드 변환 ────────────────────────────────────────────────────────────

fields_no_hint = [
    # (fid, label_content, input_tag)
    ('wd_salary', '근로소득 — 총급여',
     '<input type="number" id="wd_salary" value="0" min="0" step="1000000" oninput="updateKR(\'wd_salary\');calcWD()">'),
    ('wd_bizRev', '사업소득 — 총수입금액',
     '<input type="number" id="wd_bizRev" value="0" min="0" step="1000000" oninput="updateKR(\'wd_bizRev\');calcWD()">'),
    ('wd_bizExp', '사업소득 — 필요경비',
     '<input type="number" id="wd_bizExp" value="0" min="0" step="1000000" oninput="updateKR(\'wd_bizExp\');calcWD()">'),
    ('wd_otherInc', '기타소득금액 (필요경비 공제 후)',
     '<input type="number" id="wd_otherInc" value="0" min="0" step="100000" oninput="updateKR(\'wd_otherInc\');calcWD()">'),
    ('wd_np', '국민연금 보험료공제',
     '<input type="number" id="wd_np" value="0" min="0" step="100000" oninput="updateKR(\'wd_np\');calcWD()">'),
]

fields_with_hint = [
    ('wd_intDiv', '이자 · 배당소득',
     '<input type="number" id="wd_intDiv" value="0" min="0" step="100000" oninput="updateKR(\'wd_intDiv\');calcWD()">',
     '<div class="form-hint">2,000만원 초과분만 종합소득 합산</div>'),
    ('wd_natPen', '공적연금소득 (국민연금 등 수령액)',
     '<input type="number" id="wd_natPen" value="0" min="0" step="100000" oninput="updateKR(\'wd_natPen\');calcWD()">',
     '<div class="form-hint">연금소득공제(최대 900만원) 자동 적용 후 합산</div>'),
    ('wd_hi', '건강보험료 납부액 (연간)',
     '<input type="number" id="wd_hi" value="0" min="0" step="100000" oninput="updateKR(\'wd_hi\');calcWD()">',
     '<div class="form-hint">건강보험료 공제 (소득공제) · 근로소득자·은퇴자 해당<br>자영업자·프리랜서는 사업소득 필요경비로 처리하므로 여기 입력 불필요</div>'),
    ('wd_taxCredit', '기타 세액공제 합계 <span style="font-weight:400;color:var(--text3)">(자녀·의료비·교육비 등)</span>',
     '<input type="number" id="wd_taxCredit" value="0" min="0" step="100000" oninput="updateKR(\'wd_taxCredit\');calcWD()">',
     '<div class="form-hint">의료비·교육비·기부금·보험료 등 세액공제 합산</div>'),
]

original = html

# no-hint 필드
for fid, label_text, inp_tag in fields_no_hint:
    label_tag = '          <label class="form-label" for="' + fid + '">' + label_text + '</label>'
    old, new = to_inprow_no_hint(fid, label_tag, inp_tag)
    if old in html:
        html = html.replace(old, new)
        print(f'[OK] {fid}')
    else:
        print(f'[MISS] {fid}')

# with-hint 필드
for fid, label_text, inp_tag, hint_html in fields_with_hint:
    label_tag = '          <label class="form-label" for="' + fid + '">' + label_text + '</label>'
    old, new = to_inprow_with_hint(fid, label_tag, inp_tag, hint_html)
    if old in html:
        html = html.replace(old, new)
        print(f'[OK] {fid}')
    else:
        print(f'[MISS] {fid}')

# ── wd_otherDed: kr-num 추가 + updateKR 추가 ──────────────────────────────
old_otherded = (
    '          <label class="form-label" for="wd_otherDed">기타 소득공제</label>\n'
    '<div class="inp-wrap">\n'
    '            <input type="number" id="wd_otherDed" value="0" min="0" step="100000" oninput="calcWD()">\n'
    '            <span class="inp-unit">원</span>\n'
    '          </div>\n'
    '        </div>'
)
new_otherded = (
    '          <label class="form-label" for="wd_otherDed">기타 소득공제</label>\n'
    '          <div class="inp-row">\n'
    '            <div class="kr-num" id="wd_otherDed_kr"></div>\n'
    '            <div class="inp-wrap">\n'
    '              <input type="number" id="wd_otherDed" value="0" min="0" step="100000" oninput="updateKR(\'wd_otherDed\');calcWD()">\n'
    '              <span class="inp-unit">원</span>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>'
)
if old_otherded in html:
    html = html.replace(old_otherded, new_otherded)
    print('[OK] wd_otherDed')
else:
    print('[MISS] wd_otherDed')

if html != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n파일 저장 완료.')
else:
    print('\n변경 없음.')
