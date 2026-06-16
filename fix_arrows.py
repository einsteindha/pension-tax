content = open('index.html', encoding='utf-8').read()

# ══════════════════════════════════════════════════════════════════════
# Tab1 IRP : 외부컨테이너 flex → block, flex:1 제거 (margin-bottom:14px 로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '        <div style="display:flex;gap:6px;align-items:flex-start;margin-bottom:14px">\n'
    '          <div style="flex:1;border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
new = (
    '        <div style="margin-bottom:14px">\n'
    '          <div style="border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
assert old in content, 'Tab1 IRP outer 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab1 IRP : 외부유입 ← 두 개 → ↑ 하나 (뒤에 오는 <!-- 연금저축 으로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '          <!-- 외부 유입 -->\n'
    '          <div style="display:flex;flex-direction:column;gap:5px;padding-top:24px">\n'
    '            <div style="display:flex;align-items:center;gap:3px">\n'
    '              <span style="font-size:13px;color:var(--text3)">←</span>\n'
    '              <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '                <div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">ISA 만기</div>\n'
    '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div style="display:flex;align-items:center;gap:3px">\n'
    '              <span style="font-size:13px;color:var(--text3)">←</span>\n'
    '              <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '                <div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">주택다운사이징</div>\n'
    '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '              </div>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <!-- 연금저축 (자기부담금만) -->'
)
new = (
    '          <!-- 외부 유입 -->\n'
    '          <div style="display:flex;align-items:center;gap:4px;margin-top:6px">\n'
    '            <span style="font-size:14px;color:var(--text3)">↑</span>\n'
    '            <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '              <div style="font-size:10px;font-weight:600;color:var(--text2)">ISA·다운사이징</div>\n'
    '              <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <!-- 연금저축 (자기부담금만) -->'
)
assert old in content, 'Tab1 IRP 외부유입 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab1 연금저축 : 외부컨테이너 flex → block, flex:1 제거 (margin-bottom:12px 로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '        <div style="display:flex;gap:6px;align-items:flex-start;margin-bottom:12px">\n'
    '          <div style="flex:1;border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
new = (
    '        <div style="margin-bottom:12px">\n'
    '          <div style="border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
assert old in content, 'Tab1 연금저축 outer 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab1 연금저축 : 외부유입 ← 두 개 → ↑ 하나 (뒤에 alert-warn 인출순서로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '          <!-- 외부 유입 -->\n'
    '          <div style="display:flex;flex-direction:column;gap:5px;padding-top:24px">\n'
    '            <div style="display:flex;align-items:center;gap:3px">\n'
    '              <span style="font-size:13px;color:var(--text3)">←</span>\n'
    '              <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '                <div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">ISA 만기</div>\n'
    '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div style="display:flex;align-items:center;gap:3px">\n'
    '              <span style="font-size:13px;color:var(--text3)">←</span>\n'
    '              <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '                <div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">주택다운사이징</div>\n'
    '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '              </div>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <div class="alert alert-warn" style="margin-bottom:0;font-size:11px">'
)
new = (
    '          <!-- 외부 유입 -->\n'
    '          <div style="display:flex;align-items:center;gap:4px;margin-top:6px">\n'
    '            <span style="font-size:14px;color:var(--text3)">↑</span>\n'
    '            <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '              <div style="font-size:10px;font-weight:600;color:var(--text2)">ISA·다운사이징</div>\n'
    '              <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <div class="alert alert-warn" style="margin-bottom:0;font-size:11px">'
)
assert old in content, 'Tab1 연금저축 외부유입 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab3 IRP : 외부컨테이너 flex → block, flex:1 제거 (헤더 텍스트 "IRP (퇴직금 포함)"으로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '      <div style="font-size:10px;font-weight:700;color:var(--text2);letter-spacing:.08em;margin-bottom:5px">IRP (퇴직금 포함)</div>\n'
    '      <div style="display:flex;gap:6px;align-items:flex-start">\n'
    '        <div style="flex:1;border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
new = (
    '      <div style="font-size:10px;font-weight:700;color:var(--text2);letter-spacing:.08em;margin-bottom:5px">IRP (퇴직금 포함)</div>\n'
    '      <div>\n'
    '        <div style="border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
assert old in content, 'Tab3 IRP outer 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab3 IRP : 외부유입 ← 두 개 → ↑ 하나 (뒤에 <!-- 연금저축 --> 으로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '        <div style="display:flex;flex-direction:column;gap:5px;padding-top:24px">\n'
    '          <div style="display:flex;align-items:center;gap:3px"><span style="font-size:13px;color:var(--text3)">←</span>'
    '<div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">'
    '<div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">ISA 만기</div>'
    '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div></div></div>\n'
    '          <div style="display:flex;align-items:center;gap:3px"><span style="font-size:13px;color:var(--text3)">←</span>'
    '<div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">'
    '<div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">주택다운사이징</div>'
    '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div></div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '    <!-- 연금저축 -->'
)
new = (
    '        <div style="display:flex;align-items:center;gap:4px;margin-top:6px">\n'
    '          <span style="font-size:14px;color:var(--text3)">↑</span>\n'
    '          <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '            <div style="font-size:10px;font-weight:600;color:var(--text2)">ISA·다운사이징</div>\n'
    '            <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '          </div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '    <!-- 연금저축 -->'
)
assert old in content, 'Tab3 IRP 외부유입 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab3 연금저축 : 외부컨테이너 flex → block, flex:1 제거 ("연금저축 (자기부담금만)"으로 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '      <div style="font-size:10px;font-weight:700;color:var(--text2);letter-spacing:.08em;margin-bottom:5px">연금저축 (자기부담금만)</div>\n'
    '      <div style="display:flex;gap:6px;align-items:flex-start">\n'
    '        <div style="flex:1;border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
new = (
    '      <div style="font-size:10px;font-weight:700;color:var(--text2);letter-spacing:.08em;margin-bottom:5px">연금저축 (자기부담금만)</div>\n'
    '      <div>\n'
    '        <div style="border:1.5px solid var(--bg3);border-radius:var(--radius-lg);overflow:hidden">'
)
assert old in content, 'Tab3 연금저축 outer 없음!'
content = content.replace(old, new, 1)

# ══════════════════════════════════════════════════════════════════════
# Tab3 연금저축 : 외부유입 ← 두 개 → ↑ 하나 (앞에 <!-- 외부 유입 --> 있어서 유일)
# ══════════════════════════════════════════════════════════════════════
old = (
    '        <!-- 외부 유입 -->\n'
    '        <div style="display:flex;flex-direction:column;gap:5px;padding-top:24px">\n'
    '          <div style="display:flex;align-items:center;gap:3px"><span style="font-size:13px;color:var(--text3)">←</span>'
    '<div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">'
    '<div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">ISA 만기</div>'
    '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div></div></div>\n'
    '          <div style="display:flex;align-items:center;gap:3px"><span style="font-size:13px;color:var(--text3)">←</span>'
    '<div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">'
    '<div style="font-size:10px;font-weight:600;color:var(--text2);white-space:nowrap">주택다운사이징</div>'
    '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div></div></div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '  <div class="alert alert-warn" style="margin-top:10px'
)
new = (
    '        <!-- 외부 유입 -->\n'
    '        <div style="display:flex;align-items:center;gap:4px;margin-top:6px">\n'
    '          <span style="font-size:14px;color:var(--text3)">↑</span>\n'
    '          <div style="border:1px solid var(--bg3);border-radius:var(--radius);padding:5px 8px;background:var(--bg2)">\n'
    '            <div style="font-size:10px;font-weight:600;color:var(--text2)">ISA·다운사이징</div>\n'
    '            <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>\n'
    '          </div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '  <div class="alert alert-warn" style="margin-top:10px'
)
assert old in content, 'Tab3 연금저축 외부유입 없음!'
content = content.replace(old, new, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = ['ISA·다운사이징', '↑', 'margin-top:6px', '<!-- 외부 유입 -->']
for k in checks:
    print(k + ':', content.count(k))
