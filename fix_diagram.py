content = open('index.html', encoding='utf-8').read()

# ── 1. IRP 이연퇴직소득 수익 행: ② 퇴직소득세 → ③ 연금소득세 ────────────────
# (두 탭에 동일 패턴, 묽은 파란 배경으로 구별)
# 탭1: 멀티라인, 탭3: 인라인 — 공통 분모 부분만 교체
old_rt_return_1 = 'background:rgba(43,94,167,.05);border-left:3px solid var(--blue);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">'
new_rt_return_1 = 'background:var(--gold-pale);border-left:3px solid var(--gold);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">'

# 교체 후 내부 ②→③, blue→amber/gold 도 바꿔야 함
# 하지만 바로 옆에 오는 ② span도 바꿔야 하므로 전체 셀 교체
# 탭1과 탭3에 정확히 2번 나타남
count = content.count(old_rt_return_1)
print(f'이연퇴직소득 수익 셀 배경 발견: {count}개')
content = content.replace(old_rt_return_1, new_rt_return_1)

# 위 교체 후 해당 위치에 ② 퇴직소득세 → ③ 연금소득세
# 이 ② 셀들만 있는 gold-pale 컨텍스트를 타겟하기 어려우니
# 묽은 파란 배경이었던 자리에 오는 ② 뱃지와 텍스트를 교체
# (gold-pale 뒤에 오는 ②blue span은 다른 셀들과 구별됨 — 단 이 패턴은 다른 셀과 겹칠 수 있음)
# 안전한 방법: 이연퇴직소득 수익 특유의 연속 패턴으로 교체

# 탭3 인라인 버전: gold-pale로 바꾼 후 내부 ②→③
old_rt_badge_inline = (
    'background:var(--gold-pale);border-left:3px solid var(--gold);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">'
    '<span style="width:18px;height:18px;border-radius:50%;background:var(--blue);color:#fff;font-size:10px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">②</span>'
    '<span style="font-size:10px;color:var(--blue);font-weight:600">퇴직소득세</span></div>'
)
new_rt_badge_inline = (
    'background:var(--gold-pale);border-left:3px solid var(--gold);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">'
    '<span style="width:18px;height:18px;border-radius:50%;background:var(--gold);color:#fff;font-size:10px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">③</span>'
    '<span style="font-size:10px;color:var(--amber);font-weight:600">연금소득세</span></div>'
)

# 탭1 멀티라인 버전
old_rt_badge_multi = (
    'background:var(--gold-pale);border-left:3px solid var(--gold);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">\n'
    '                <span style="width:18px;height:18px;border-radius:50%;background:var(--blue);color:#fff;font-size:10px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">②</span>\n'
    '                <span style="font-size:10px;color:var(--blue);font-weight:600">퇴직소득세</span>\n'
    '              </div>'
)
new_rt_badge_multi = (
    'background:var(--gold-pale);border-left:3px solid var(--gold);display:flex;align-items:center;gap:5px;border-top:1px solid var(--bg3)">\n'
    '                <span style="width:18px;height:18px;border-radius:50%;background:var(--gold);color:#fff;font-size:10px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">③</span>\n'
    '                <span style="font-size:10px;color:var(--amber);font-weight:600">연금소득세</span>\n'
    '              </div>'
)

c1 = content.count(old_rt_badge_inline)
c2 = content.count(old_rt_badge_multi)
print(f'수익행 ② 뱃지 인라인: {c1}개, 멀티라인: {c2}개')

content = content.replace(old_rt_badge_inline, new_rt_badge_inline)
content = content.replace(old_rt_badge_multi, new_rt_badge_multi)

# ── 2. ISA 만기 패널: 원금→① 단순 → 공제 여부 분기 ────────────────────────
# 탭1 (멀티라인)
old_isa_tab1 = '                <div style="font-size:9px;color:var(--text3);margin-top:2px">원금→① · 수익→③</div>'
new_isa_tab1 = '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div>'

# 탭3 (인라인)
old_isa_tab3 = '<div style="font-size:9px;color:var(--text3);margin-top:2px">원금→① · 수익→③</div>'
new_isa_tab3 = '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X 원금→① / 공제O 원금·수익→③</div>'

c3 = content.count(old_isa_tab1)
c4 = content.count(old_isa_tab3)
print(f'ISA 만기 탭1: {c3}개, 탭3: {c4}개')

content = content.replace(old_isa_tab1, new_isa_tab1)
content = content.replace(old_isa_tab3, new_isa_tab3)

# ── 3. 주택다운사이징 패널: ①비과세만 → ①③ 분기 ─────────────────────────
# 탭1 (멀티라인)
old_down_tab1 = (
    '                <div style="display:inline-flex;align-items:center;gap:3px;margin-top:2px">\n'
    '                  <span style="width:14px;height:14px;border-radius:50%;background:var(--purple);color:#fff;font-size:8px;display:inline-flex;align-items:center;justify-content:center;font-weight:700">①</span>\n'
    '                  <span style="font-size:9px;color:var(--text3)">비과세</span>\n'
    '                </div>'
)
new_down_tab1 = '                <div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>'

# 탭3 (인라인)
old_down_tab3 = (
    '<div style="display:inline-flex;align-items:center;gap:3px;margin-top:2px">'
    '<span style="width:14px;height:14px;border-radius:50%;background:var(--purple);color:#fff;font-size:8px;display:inline-flex;align-items:center;justify-content:center;font-weight:700">①</span>'
    '<span style="font-size:9px;color:var(--text3)">비과세</span>'
    '</div>'
)
new_down_tab3 = '<div style="font-size:9px;color:var(--text3);margin-top:2px">공제X→① / 공제O→③</div>'

c5 = content.count(old_down_tab1)
c6 = content.count(old_down_tab3)
print(f'주택다운사이징 탭1: {c5}개, 탭3: {c6}개')

content = content.replace(old_down_tab1, new_down_tab1)
content = content.replace(old_down_tab3, new_down_tab3)

# ── 4. "재원 구성" → "인출금액" (계좌 카드 헤더) ─────────────────────────
content = content.replace(
    '"재원 구성 (인출 순서: ①→②→③)"',
    '"인출금액 (순서: ①→②→③)"',
    1
)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

# 최종 검증
print('이연퇴직소득 수익 ② 잔존:', 'rgba(43,94,167,.05)' in content)
print('ISA 원금→① 단순 잔존:', '>원금→① · 수익→③<' in content)
print('주택다운 ①비과세only 잔존(inline):', '>비과세</span></div>' in content)
print('인출금액 헤더:', '"인출금액 (순서: ①→②→③)"' in content)
