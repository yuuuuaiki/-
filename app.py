import streamlit as st

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

# 紙の表のようなコンパクトさと、マスの横並びを綺麗に保つCSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    h3 {
        margin-top: 0.8rem !important;
        margin-bottom: 0.1rem !important;
        font-size: 1.05rem !important;
        background-color: #f0f2f6;
        padding: 4px 8px;
        border-radius: 4px;
    }
    hr {
        margin: 0.5rem 0 !important;
    }
    /* 行の要素を中央揃え＆隙間を詰める */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 0.1rem !important;
        margin-bottom: 1px !important;
    }
    div[data-testid="stColumn"] {
        padding: 0px !important;
        text-align: center;
    }
    p {
        margin-bottom: 0px !important;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 見学ケース必要項目数早見表")

def render_table_section(title, items, total_slots=15):
    """紙の表と同じように、項目の右側にマスを横一列に並べる関数"""
    st.subheader(f"★ {title}")
    
    for item_name, need_count in items:
        # [項目名(幅4), 必要数(幅1.5)] + [マス用カラム×総スロット数]
        cols = st.columns([3.5, 1.2] + [1] * total_slots)
        
        with cols[0]:
            st.write(f"**{item_name}**")
        with cols[1]:
            st.caption(f"必要:{need_count}")
            
        # 必要な数だけチェックボックスを置き、残りは空欄（プレースホルダー）にする
        for i in range(total_slots):
            with cols[2 + i]:
                if i < need_count:
                    key = f"{title}_{item_name}_{i}"
                    st.checkbox("", key=key, label_visibility="collapsed")
                else:
                    # 必要数を超えたマスは薄く非活性っぽくするか空白にする
                    st.write("")
    st.divider()

# ==========================================
# 1. 保存・治療科 (最大15マス)
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
render_table_section("保存・治療科", hozon_items, total_slots=15)

# ==========================================
# 2. 第一・第二口腔外科 (最大3マス)
# ==========================================
render_table_section("第一口腔外科", [("抜歯症例", 2), ("外科外来症例", 2), ("入院患者症例", 2)], total_slots=3)
render_table_section("第二口腔外科", [("抜歯症例", 2), ("外科外来症例", 3), ("入院患者症例", 1)], total_slots=3)

# ==========================================
# 3. 口腔補綴科 (最大11マス)
# ==========================================
hotetsu_items = [
    ("医療面接", 3), ("資料獲得", 3), ("診断・カウンセリング", 3),
    ("補綴前処置", 3), ("補綴物除去", 3), ("暫間補綴", 3),
    ("支台築造", 3), ("形成", 3), ("印象・咬合採得", 3),
    ("試適装着", 3), ("インプラント補綴", 3), ("IOS実習", 1),
    ("その他・受付・余剰分", 11), ("補綴難処置", 1),
    ("TMD症例", 1), ("インプラント症例", 1), ("デジタルデンティストリ", 1),
]
render_table_section("口腔補綴科", hotetsu_items, total_slots=11)

# ==========================================
# 4. 咀嚼補綴科 (最大3マス)
# ==========================================
st.subheader("★ 咀嚼補綴科")
soshaku_items = [
    ("口腔内検査・概形印象", 1, "F・P"), ("筋圧形成・最終印象", 1, "F・P"),
    ("咬合採得", 1, "F・P"), ("ゴシックアーチ", 1, "F"),
    ("人工歯配列試適", 1, "F"), ("装着・患者指導", 1, "F・P"),
    ("調整・経過観察", 1, "F・P"), ("補綴前処置", 1, "P"),
    ("支台装置・義歯試適", 1, "P"), ("義歯修理・リライン(各1必須)", 3, ""),
    ("リコール", 2, ""), ("専門外来(顎顔面補綴)", 1, ""),
]
for item_name, need_count, note in soshaku_items:
    cols = st.columns([3, 1, 1.2] + [1] * 3)
    with cols[0]:
        st.write(f"**{item_name}**")
    with cols[1]:
        st.caption(f"必要:{need_count}")
    with cols[2]:
        if note:
            st.caption(f"({note})")
    for i in range(3):
        with cols[3 + i]:
            if i < need_count:
                st.checkbox("", key=f"咀嚼補綴科_{item_name}_{i}", label_visibility="collapsed")
st.divider()

# ==========================================
# 5. 予防歯科 (最大5マス)
# ==========================================
render_table_section("予防歯科", [("見学実習(10-1月)", 2), ("当番(2-10月)", 5)], total_slots=5)

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
    st.write(f"・**【{sub_title}】**")
    for period, need_count in sub_items:
        cols = st.columns([3, 1.2] + [1] * 3)
        with cols[0]:
            st.write(f" {period}")
        with cols[1]:
            st.caption(f"必要:{need_count}")
        for i in range(3):
            with cols[2 + i]:
                if i < need_count:
                    st.checkbox("", key=f"小児歯科_{sub_title}_{period}_{i}", label_visibility="collapsed")
st.divider()

# ==========================================
# 7. 放射線科
# ==========================================
st.subheader("★ 放射線科")
for item_name, need_count in [("口内法スケッチ", 5), ("口外法スケッチ", 5), ("口外法スケッチ(CT/MRI)", 5), ("口内法デンタル撮影", 10)]:
    cols = st.columns([3, 1.2] + [1] * 10)
    with cols[0]:
        st.write(f"**{item_name}**")
    with cols[1]:
        st.caption(f"必要:{need_count}")
    for i in range(10):
        with cols[2 + i]:
            if i < need_count:
                st.checkbox("", key=f"放射線科_{item_name}_{i}", label_visibility="collapsed")

st.write("・**撮影見学**")
kengaku_list = ["パノラマXp", "セファロ", "顎関節", "頭頸部", "MBCT", "CBCT", "MRI顎関節", "MRI頭頸部", "放射線治療"]
kengaku_cols = st.columns(3)
for idx, name in enumerate(kengaku_list):
    with kengaku_cols[idx % 3]:
        st.checkbox(name, key=f"放射線科_見学_{name}")
st.divider()

# ==========================================
# 8. その他各科・当番系
# ==========================================
render_table_section("歯科麻酔科", [("入院患者全身麻酔", 1), ("精神鎮静法", 1), ("ペインクリニック", 1)], total_slots=3)
render_table_section("顎口腔機能治療部", [("見学", 10), ("ドライマウスdisc.", 1), ("嚥下disc.", 1), ("SASdisc.", 1), ("発音・構音disc.", 1)], total_slots=10)
render_table_section("障害者歯科", [("見学", 5)], total_slots=5)
render_table_section("矯正科", [("配当", 3), ("EW以外の装置", 2), ("EW見学", 1)], total_slots=3)

st.subheader("★ 当番・研修関連")
st.write("・**検査部**（1回）")
st.checkbox("検査部完了", key="toban_kensa")
st.write("・**口腔総合診療部**（7回）")
sogou_cols = st.columns(7)
for i in range(7):
    with sogou_cols[i]:
        st.checkbox(f"{i+1}回", key=f"toban_sougou_{i}")
st.write("・**医学部病院**（2回）")
med_cols = st.columns(2)
for i in range(2):
    with med_cols[i]:
        st.checkbox(f"{i+1}回", key=f"toban_med_{i}")
