content = open('index.html', encoding='utf-8').read()

# ── 1. wdAccs 기본값 0으로 ─────────────────────────────────────────────
content = content.replace(
    "{ type: 'irp', openYear: 2015, balance: 300000000, src1: 10000000, src2: 200000000, src3: 90000000, withdrawal: 12000000, retirePensionYr: 1 }",
    "{ type: 'irp', openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0, retirePensionYr: 1 }",
    1
)
content = content.replace(
    "{ type: 'ps',  openYear: 2010, balance: 100000000, src1: 5000000,  src2: 0,         src3: 95000000, withdrawal: 8000000  }",
    "{ type: 'ps',  openYear: 2020, balance: 0, src1: 0, src2: 0, src3: 0, withdrawal: 0 }",
    1
)

# ── 2. 원 서클 안 숫자: 폰트 일관성 (Unicode 기호 → 일반 숫자) ─────────────
# ① 서클
content = content.replace(
    'background:var(--purple);color:#fff;font-size:9px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">①</span>',
    'background:var(--purple);color:#fff;font-size:10px;font-style:normal;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0">1</span>',
    1
)
# ② 서클
content = content.replace(
    'background:var(--blue);color:#fff;font-size:9px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">②</span>',
    'background:var(--blue);color:#fff;font-size:10px;font-style:normal;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0">2</span>',
    1
)
# ③ 서클
content = content.replace(
    'background:var(--gold);color:#fff;font-size:9px;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">③</span>',
    'background:var(--gold);color:#fff;font-size:10px;font-style:normal;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0">3</span>',
    1
)

# ── 3. ② 라벨: "이연퇴직소득" → "이연퇴직소득 원금" ─────────────────────────
content = content.replace(
    "'<span style=\"font-size:11px;color:var(--text2);min-width:108px\">이연퇴직소득</span>',",
    "'<span style=\"font-size:11px;color:var(--text2);min-width:108px\">이연퇴직소득 원금</span>',",
    1
)

# ── 4. 재원 구성 헤더 아래 힌트 추가 ─────────────────────────────────────
old_src_header = "'<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:6px\">재원 구성 (인출 순서: ①→②→③)</div>',"
new_src_header = (
    "'<div style=\"font-size:11px;font-weight:700;color:var(--text2);margin-bottom:4px\">재원 구성 (인출 순서: ①→②→③)</div>',\n"
    "          '<div style=\"font-size:10px;color:var(--text3);margin-bottom:6px;line-height:1.5\">"
    "② 이연퇴직소득은 원금만 입력(운용수익은 ③에 포함) · "
    "ISA 이전분: 세액공제 받은 금액→③, 미적용 금액→①</div>',"
)
assert old_src_header in content, "재원 구성 헤더 없음!"
content = content.replace(old_src_header, new_src_header, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('done, lines:', content.count('\n'))

checks = [
    ("balance: 0, src1: 0", "기본값 0"),
    ("이연퇴직소득 원금", "② 라벨"),
    ("운용수익은 ③에 포함", "힌트 텍스트"),
    ("ISA 이전분", "ISA 힌트"),
    ('font-family:inherit', "폰트 통일"),
    ('>1</span>', "① 숫자"),
    ('>2</span>', "② 숫자"),
    ('>3</span>', "③ 숫자"),
]
for k, label in checks:
    print(label + ':', k in content)
