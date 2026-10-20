import streamlit as st

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

# 余白を極限まで詰め、紙の表のような見た目を完全再現するCSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    h2, h3 {
        margin-top: 0.4rem !important;
        margin-bottom: 0.1rem !important;
        font-size: 0.95rem !important;
        color: #111;
    }
    hr {
        margin: 0.3rem 0 !important;
    }
    .custom-table-header {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
    }
    .custom-table-header th {
        border: 1px solid #999;
        padding: 3px 5px;
        text-align: center;
        background-color: #f7f7f7;
        height: 24px;
    }
    .custom-table-header th:first-child {
        text-align: left;
        min-width: 160px;
        padding-left: 6px;
    }
    .custom-table-header th:nth-child(2) {
        min-width: 50px;
        font-size: 0.75rem;
        color: #555;
    }
    .empty-cell {
        background-color: #eaeaea;
        border: 1px solid #999;
        height: 28px;
    }
    .header-row {
        background-color: #f1f3f4;
        font-weight: bold;
        padding: 4px 8px;
        border: 1px solid #999;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 見学ケース必要項目数早見表")

# セッション状態の初期化
if "checks" not in st.session_state:
    st.session_state.checks = {}

def update_check(key):
    st.session_state.checks[key] = st.session_state[key]

def render_section(title, items, max_cols=15):
    st.markdown(f"### ★ {title}")
    
    # 1. ヘロダー行の描画
    header_html = f'<table class="custom-table-header"><tr><th>項目</th><th>必要</th>'
    for i in range(max_cols):
        header_html += f'<th>{i+1}</th>'
    header_html += '</tr></table>'
    st.markdown(header_html, unsafe_allow_html=True)
    
    # 2. 各行の描画
    for row in items:
        item_name = row[0]
        need_count = row[1]
        is_header = row[2] if len(row) > 2 else False
        
        if is_header:
            st.markdown(f'<div class="header-row"><b>{item_name}</b></div>', unsafe_allow_html=True)
        else:
            cols = st.columns([160, 50] + [35] * max_cols)
            with cols[0]:
                st.markdown(f"<div style='font-size:0.8rem; font-weight:bold; padding-top:4px;'>{item_name}</div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"<div style='font-size:0.75rem; color:#555; text-align:center; padding-top:4px;'>{need_count}</div>", unsafe_allow_html=True)
            
            for i in range(max_cols):
                with cols[2 + i]:
                    if i < need_count:
                        key = f"{title}_{item_name}_{i}"
                        if key not in st.session_state.checks:
                            st.session_state.checks[key] = False
                        # チェックを入れた瞬間に自動保存される仕組み
                        st.checkbox("", key=key, value=st.session_state.checks[key], on_change=update_check, args=(key,), label_visibility="collapsed")
                    else:
                        st.markdown("<div class='empty-cell'></div>", unsafe_allow_html=True)

# ==========================================
# 1. 保存・治療科
# ==========================================
hozon_items = [
    ("覆髄法", 2), 
    ("抜髄法", 2), 
    ("感染根管治療", 5), 
    ("★ CR修復 (合計15点)", 0, True),
    (" └ 2級窩洞以外", 13),
    (" └ 2級窩洞", 2),
    ("インレー修復", 2),
    ("感染チェア", 1),
    ("マイクロの使用", 2),
    ("歯周外科症例見学", 2),
]
render_section("保存・治療科", hozon_items, max_cols=15)

# ==========================================
# 2. 第一・第二口腔外科
# ==========================================
render_section("第一口腔外科", [("抜歯症例", 2), ("外科外来症例", 2), ("入院患者症例", 2)], max_cols=5)
render_section("第二口腔外科", [("抜歯症例", 2), ("外科外来症例", 3), ("入院患者症例", 1)], max_cols=5)

# ==========================================
# 3. 口腔補綴科
# ==========================================
hotetsu_items = [
    ("医療面接", 3), ("資料獲得", 3), ("診断・カウンセリング", 3),
    ("補綴前処置", 3), ("補綴物除去", 3), ("暫間補綴", 3),
    ("支台築造", 3), ("形成", 3), ("印象・咬合採得", 3),
    ("試適装着", 3), ("インプラント補綴", 3), ("IOS実習", 1),
    ("その他・受付・余剰分", 11), ("補綴難処置", 1),
    ("TMD症例", 1), ("インプラント症例", 1), ("デジタルデンティストリ", 1),
]
render_section("口腔補綴科", hotetsu_items, max_cols=11)

# ==========================================
# 4. 咀嚼補綴科
# ==========================================
soshaku_items = [
    ("口腔内検査・概形印象 (F)", 1), ("口腔内検査・概形印象 (P)", 1),
    ("筋圧形成・最終印象 (F)", 1), ("筋圧形成・最終印象 (P)", 1),
    ("咬合採得 (F)", 1), ("咬合採得 (P)", 1),
    ("ゴシックアーチ (F)", 1),
    ("人工歯配列試適 (F)", 1),
    ("装着・患者指導 (F)", 1), ("装着・患者指導 (P)", 1),
    ("調整・経過観察 (F)", 1), ("調整・経過観察 (P)", 1),
    ("補綴前処置 (P)", 1),
    ("支台装置・義歯試適 (P)", 1),
    ("義歯修理・リライン(各1必須)", 3),
    ("リコール", 2),
    ("専門外来 (顎顔面補綴、口唇口蓋裂)", 1),
]
render_section("咀嚼補綴科", soshaku_items, max_cols=3)

# ==========================================
# 5. 予防歯科
# ==========================================
render_section("予防歯科", [("見学実習(10-1月)", 2), ("当番(2-10月)", 5)], max_cols=5)

# ==========================================
# 6. 小児歯科
# ==========================================
shoni_items = [
    ("リコール (12月まで)", 2), ("リコール (3月まで)", 3), ("リコール (6月まで)", 3), ("リコール (8月まで)", 2),
    ("CR修復 (12月まで)", 2), ("CR修復 (3月まで)", 3), ("CR修復 (6月まで)", 3), ("CR修復 (8月まで)", 2),
    ("断髄・抜髄・RCT (12月まで)", 2), ("断髄・抜髄・RCT (3月まで)", 3), ("断髄・抜髄・RCT (6月まで)", 3), ("断髄・抜髄・RCT (8月まで)", 2),
    ("乳歯冠・義歯 (12月まで)", 2), ("乳歯冠・義歯 (3月まで)", 3), ("乳歯冠・義歯 (6月まで)", 3), ("乳歯冠・義歯 (8月まで)", 2),
    ("外科処置・抜歯 (12月まで)", 2), ("外科処置・抜歯 (3月まで)", 3), ("外科処置・抜歯 (6月まで)", 3), ("外科処置・抜歯 (8月まで)", 2),
]
render_section("小児歯科", shoni_items, max_cols=5)

# ==========================================
# 7. 放射線科
# ==========================================
render_section("放射線科", [("口内法スケッチ", 5), ("口外法スケッチ", 5), ("口外法スケッチ(CT/MRI)", 5), ("口内法デンタル撮影", 10)], max_cols=10)

st.markdown("### ★ 放射線科：撮影見学")
kengaku_list = [
    "パノラマXp", "セファロ撮影", "顎関節撮影", "頭頸部撮影", 
    "MBCT", "CBCT", "MRI 顎関節", "MRI 頭頸部", "放射線治療"
]
k_cols = st.columns(3)
for idx, name in enumerate(kengaku_list):
    with k_cols[idx % 3]:
        key = f"放射線科_撮影見学_{name}"
        if key not in st.session_state.checks:
            st.session_state.checks[key] = False
        st.checkbox(name, key=key, value=st.session_state.checks[key], on_change=update_check, args=(key,))

# ==========================================
# 8. その他各科・当番系
# ==========================================
render_section("歯科麻酔科", [("入院患者全身麻酔", 1), ("精神鎮静法", 1), ("ペインクリニック", 1)], max_cols=3)
render_section("顎口腔機能治療部", [("見学", 10), ("ドライマウスdisc.", 1), ("嚥下disc.", 1), ("SASdisc.", 1), ("発音・構音disc.", 1)], max_cols=10)
render_section("障害者歯科", [("見学", 5)], max_cols=5)
render_section("矯正科", [("配当", 3), ("EW以外の装置", 2), ("EW見学", 1)], max_cols=3)

st.markdown("### ★ 当番・研修関連")
toban_items = [
    ("検査部（1回）", 1, "toban_kensa"),
    ("口腔総合診療部（7回）", 7, "toban_sougou"),
    ("医学部病院（2回）", 2, "toban_med")
]
for label, count, prefix in toban_items:
    st.markdown(f"・**{label}**")
    cols = st.columns(max(count, 1))
    for i in range(count):
        key = f"{prefix}_{i}"
        if key not in st.session_state.checks:
            st.session_state.checks[key] = False
        with cols[i]:
            st.checkbox(f"{i+1}回", key=key, value=st.session_state.checks[key], on_change=update_check, args=(key,))
