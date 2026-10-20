import streamlit as st

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

st.title("📋 見学ケース必要項目数早見表")
st.caption("各項目の四角（マス）をタップ・クリックしてチェックを入れる／外すことができます。")

# CSSでチェックボックスを大きめのボタン風にスタイリング
st.markdown("""
    <style>
    .stCheckbox {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

def render_grid_section(section_title, items, max_cols=15):
    """標準的なチェックボックスグリッドを描画する関数"""
    st.subheader(f"★ {section_title}")
    for item_name, count in items:
        cols = st.columns([3, 1.5] + [1] * max_cols)
        with cols[0]:
            st.write(f"**{item_name}**")
        with cols[1]:
            st.caption(f"必要: {count}")
        for i in range(count):
            with cols[2 + i]:
                key = f"{section_title}_{item_name}_{i}"
                st.checkbox("", key=key, label_visibility="collapsed")
    st.divider()

# ==========================================
# 1. 保存・治療科
# ==========================================
hozon_items = [
    ("覆髄法", 2),
    ("抜髄法", 2),
    ("感染根管治療", 5),
    ("CR修復", 15),
    ("2級窩洞以外", 13),
    ("2級窩洞", 2),
    ("インレー修復", 2),
    ("感染チェア", 1),
    ("マイクロの使用", 2),
    ("歯周外科症例見学", 2),
]
render_grid_section("保存・治療科", hozon_items, max_cols=15)

# ==========================================
# 2. 第一口腔外科・第二口腔外科
# ==========================================
geka1_items = [
    ("抜歯症例", 2),
    ("外科外来症例", 2),
    ("入院患者症例", 2),
]
render_grid_section("第一口腔外科", geka1_items, max_cols=5)

geka2_items = [
    ("抜歯症例", 2),
    ("外科外来症例", 3),
    ("入院患者症例", 1),
]
render_grid_section("第二口腔外科", geka2_items, max_cols=5)

# ==========================================
# 3. 口腔補綴科
# ==========================================
hotetsu_items = [
    ("医療面接", 3),
    ("資料獲得", 3),
    ("診断・カウンセリング", 3),
    ("補綴前処置", 3),
    ("補綴物除去", 3),
    ("暫間補綴", 3),
    ("支台築造", 3),
    ("形成", 3),
    ("印象・咬合採得", 3),
    ("試適装着", 3),
    ("インプラント補綴", 3),
    ("IOS実習", 1),
    ("その他・受付・余剰分", 11),
    ("補綴難処置", 1),
    ("TMD症例", 1),
    ("インプラント症例", 1),
    ("デジタルデンティストリ", 1),
]
render_grid_section("口腔補綴科", hotetsu_items, max_cols=11)

# ==========================================
# 4. 咀嚼補綴科
# ==========================================
st.subheader("★ 咀嚼補綴科")
soshaku_items = [
    ("口腔内検査・概形印象", 1, "F・P"),
    ("筋圧形成・最終印象", 1, "F・P"),
    ("咬合採得", 1, "F・P"),
    ("ゴシックアーチ", 1, "F"),
    ("人工歯配列試適", 1, "F"),
    ("装着・患者指導", 1, "F・P"),
    ("調整・経過観察", 1, "F・P"),
    ("補綴前処置", 1, "P"),
    ("支台装置・義歯試適", 1, "P"),
    ("義歯修理・リライン（最低各1個必須）", 3, ""),
    ("リコール", 2, ""),
    ("専門外来（顎顔面補綴）", 1, ""),
]

for item_name, count, note in soshaku_items:
    cols = st.columns([3.5, 1.5, 1.5] + [1] * 5)
    with cols[0]:
        st.write(f"**{item_name}**")
    with cols[1]:
        st.caption(f"必要: {count}")
    with cols[2]:
        if note:
            st.caption(f"({note})")
    for i in range(count):
        with cols[3 + i]:
            key = f"咀嚼補綴科_{item_name}_{i}"
            st.checkbox("", key=key, label_visibility="collapsed")
st.divider()

# ==========================================
# 5. 予防歯科
# ==========================================
yobou_items = [
    ("見学実習（10-1月まで）", 2),
    ("当番（2-10月まで）", 5),
]
render_grid_section("予防歯科", yobou_items, max_cols=5)

# ==========================================
# 6. 小児歯科
# ==========================================
st.subheader("★ 小児歯科")
shoni_sections = [
    ("リコール", [("12月まで", 2), ("3月まで", 3), ("6月まで", 3), ("8月まで", 2)]),
    ("CR修復", [("12月まで", 2), ("3月まで", 3), ("6月まで", 3), ("8月まで", 2)]),
    ("断髄・抜髄・RCT", [("12月まで", 2), ("3月まで", 3), ("6月まで", 3), ("8月まで", 2)]),
    ("乳歯冠・義歯", [("12月まで", 2), ("3月まで", 3), ("6月まで", 3), ("8月まで", 2)]),
    ("外科処置・抜歯", [("12月まで", 2), ("3月まで", 3), ("6月まで", 3), ("8月まで", 2)]),
]

for sub_title, sub_items in shoni_sections:
    st.write(f"**【{sub_title}】**")
    for period, count in sub_items:
        cols = st.columns([3, 1.5] + [1] * 5)
        with cols[0]:
            st.write(f"・{period}")
        with cols[1]:
            st.caption(f"必要: {count}")
        for i in range(count):
            with cols[2 + i]:
                key = f"小児歯科_{sub_title}_{period}_{i}"
                st.checkbox("", key=key, label_visibility="collapsed")
st.divider()

# ==========================================
# 7. 放射線科
# ==========================================
st.subheader("★ 放射線科")
houshasen_items = [
    ("口内法スケッチ", 5),
    ("口外法スケッチ", 5),
    ("口外法スケッチ（CT・MRI含む）", 5),
    ("口内法デンタル撮影", 10),
]
for item_name, count in houshasen_items:
    cols = st.columns([4, 1.5] + [1] * 10)
    with cols[0]:
        st.write(f"**{item_name}**")
    with cols[1]:
        st.caption(f"必要: {count}")
    for i in range(count):
        with cols[2 + i]:
            key = f"放射線科_{item_name}_{i}"
            st.checkbox("", key=key, label_visibility="collapsed")

st.write("**撮影見学**")
houshasen_kengaku = ["パノラマXp", "セファロ撮影", "顎関節撮影", "頭頸部撮影", "MBCT", "CBCT", "MRI 顎関節", "MRI 頭頸部", "放射線治療"]
kengaku_cols = st.columns(3)
for idx, name in enumerate(houshasen_kengaku):
    with kengaku_cols[idx % 3]:
        key = f"放射線科_撮影見学_{name}"
        st.checkbox(name, key=key)
st.divider()

# ==========================================
# 8. 歯科麻酔科・顎口腔機能治療部・障害者歯科・矯正科・当番系
# ==========================================
masui_items = [
    ("入院患者全身麻酔", 1),
    ("精神鎮静法", 1),
    ("ペインクリニック", 1),
]
render_grid_section("歯科麻酔科", masui_items, max_cols=3)

kinou_items = [
    ("見学", 10),
    ("ドライマウスdisc.", 1),
    ("嚥下disc.", 1),
    ("SASdisc.", 1),
    ("発音・構音disc.", 1),
]
render_grid_section("顎口腔機能治療部", kinou_items, max_cols=10)

shougai_items = [
    ("見学", 5),
]
render_grid_section("障害者歯科", shougai_items, max_cols=5)

kyousei_items = [
    ("配当", 3),
    ("EW以外の装置", 2),
    ("EW見学", 1),
]
render_grid_section("矯正科", kyousei_items, max_cols=3)

st.subheader("★ 当番・研修関連")
st.write("・**検査部**： 1回 当番組んでくれる")
st.checkbox("検査部 当番完了", key="toban_kensa")
st.write("・**口腔総合診療部**： 7回 当番組んでくれる")
toban_cols = st.columns(7)
for i in range(7):
    with toban_cols[i]:
        st.checkbox(f"{i+1}回目", key=f"toban_sougou_{i}")
st.write("・**医学部病院**： 2回 当番組んでくれる")
toban_med_cols = st.columns(2)
for i in range(2):
    with toban_med_cols[i]:
        st.checkbox(f"{i+1}回目", key=f"toban_med_{i}")
