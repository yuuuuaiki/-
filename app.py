import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

# 余白を極限まで詰め、紙の表の見た目を完全に再現するCSS
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
    .table-scroll {
        overflow-x: auto;
        width: 100%;
        margin-bottom: 0.4rem;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8rem;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #999;
        padding: 3px 5px;
        text-align: center;
        white-space: nowrap;
        height: 24px;
    }
    .custom-table th:first-child, .custom-table td:first-child {
        text-align: left;
        font-weight: bold;
        background-color: #f7f7f7;
        min-width: 160px;
    }
    .custom-table th:nth-child(2), .custom-table td:nth-child(2) {
        text-align: center;
        background-color: #f7f7f7;
        min-width: 50px;
        font-size: 0.75rem;
        color: #555;
    }
    .empty-cell {
        background-color: #eaeaea;
    }
    .header-row {
        background-color: #f1f3f4;
        font-weight: bold;
        text-align: left !important;
        padding-left: 8px !important;
    }
    /* Streamlit標準チェックボックスの余白調整 */
    div[data-testid="stCheckbox"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stCheckbox"] > label {
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 見学ケース必要項目数早見表")

# --- Google スプレッドシート連携処理 ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_resource
def get_gspread_client():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        return gspread.authorize(credentials)
    except Exception:
        return None

def load_data_from_sheet(sheet_name="見学ケースデータ"):
    data = {}
    client = get_gspread_client()
    if not client:
        return data
    try:
        sh = client.open(sheet_name).sheet1
        records = sh.get_all_records()
        for row in records:
            k = row.get("key")
            v = row.get("val")
            if k:
                data[k] = (v == 1 or v == "1" or v is True)
    except Exception:
        pass
    return data

def save_key_to_sheet(key, value, sheet_name="見学ケースデータ"):
    client = get_gspread_client()
    if not client:
        return
    try:
        sh = client.open(sheet_name).sheet1
        val_str = "1" if value else "0"
        cell = None
        try:
            cell = sh.find(key)
        except Exception:
            pass
            
        if cell:
            sh.update_cell(cell.row, 2, val_str)
        else:
            try:
                if not sh.row_values(1):
                    sh.append_row(["key", "val"])
            except Exception:
                pass
            sh.append_row([key, val_str])
    except Exception:
        pass

# 初回起動時にスプレッドシートから全データをロード
if "checks" not in st.session_state:
    st.session_state.checks = load_data_from_sheet()

def on_check_change(key):
    # チェック状態変更時に自動でスプレッドシート更新
    new_val = st.session_state[key]
    st.session_state.checks[key] = new_val
    save_key_to_sheet(key, new_val)

def render_table_section(title, items, max_cols=15):
    st.markdown(f"### ★ {title}")
    
    # テーブルヘッダー
    header_cols = st.columns([3, 1] + [1] * max_cols)
    with header_cols[0]:
        st.markdown("**項目**")
    with header_cols[1]:
        st.markdown("**必要**")
    for i in range(max_cols):
        with header_cols[i + 2]:
            st.markdown(f"**{i+1}**")
            
    st.markdown("<hr style='margin:2px 0;'>", unsafe_allow_html=True)

    # テーブル各行
    for row in items:
        item_name = row[0]
        need_count = row[1]
        is_header = row[2] if len(row) > 2 else False
        
        cols = st.columns([3, 1] + [1] * max_cols)
        if is_header:
            with cols[0]:
                st.markdown(f"**{item_name}**")
        else:
            with cols[0]:
                st.write(item_name)
            with cols[1]:
                st.write(str(need_count))
            for i in range(max_cols):
                with cols[i + 2]:
                    if i < need_count:
                        key = f"{title}_{item_name}_{i}"
                        default_val = st.session_state.checks.get(key, False)
                        st.checkbox(
                            "", 
                            key=key, 
                            value=default_val, 
                            on_change=on_check_change, 
                            args=(key,),
                            label_visibility="collapsed"
                        )
                    else:
                        st.markdown("<div style='background-color:#eaeaea; height:24px; border-radius:3px;'></div>", unsafe_allow_html=True)

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
render_table_section("保存・治療科", hozon_items, max_cols=15)

# ==========================================
# 2. 第一・第二口腔外科
# ==========================================
render_table_section("第一口腔外科", [("抜歯症例", 2), ("外科外来症例", 2), ("入院患者症例", 2)], max_cols=5)
render_table_section("第二口腔外科", [("抜歯症例", 2), ("外科外来症例", 3), ("入院患者症例", 1)], max_cols=5)

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
render_table_section("口腔補綴科", hotetsu_items, max_cols=11)

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
render_table_section("咀嚼補綴科", soshaku_items, max_cols=3)

# ==========================================
# 5. 予防歯科
# ==========================================
render_table_section("予防歯科", [("見学実習(10-1月)", 2), ("当番(2-10月)", 5)], max_cols=5)

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
render_table_section("小児歯科", shoni_items, max_cols=5)

# ==========================================
# 7. 放射線科
# ==========================================
render_table_section("放射線科", [("口内法スケッチ", 5), ("口外法スケッチ", 5), ("口外法スケッチ(CT/MRI)", 5), ("口内法デンタル撮影", 10)], max_cols=10)

st.markdown("### ★ 放射線科：撮影見学")
kengaku_list = [
    "パノラマXp", "セファロ撮影", "顎関節撮影", "頭頸部撮影", 
    "MBCT", "CBCT", "MRI 顎関節", "MRI 頭頸部", "放射線治療"
]
k_cols = st.columns(3)
for idx, name in enumerate(kengaku_list):
    with k_cols[idx % 3]:
        key = f"放射線科_撮影見学_{name}"
        default_val = st.session_state.checks.get(key, False)
        st.checkbox(
            name, 
            key=key, 
            value=default_val, 
            on_change=on_check_change, 
            args=(key,)
        )

# ==========================================
# 8. その他各科・当番系
# ==========================================
render_table_section("歯科麻酔科", [("入院患者全身麻酔", 1), ("精神鎮静法", 1), ("ペインクリニック", 1)], max_cols=3)
render_table_section("顎口腔機能治療部", [("見学", 10), ("ドライマウスdisc.", 1), ("嚥下disc.", 1), ("SASdisc.", 1), ("発音・構音disc.", 1)], max_cols=10)
render_table_section("障害者歯科", [("見学", 5)], max_cols=5)
render_table_section("矯正科", [("配当", 3), ("EW以外の装置", 2), ("EW見学", 1)], max_cols=3)

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
        default_val = st.session_state.checks.get(key, False)
        with cols[i]:
            st.checkbox(
                f"{i+1}回", 
                key=key, 
                value=default_val, 
                on_change=on_check_change, 
                args=(key,)
            )
