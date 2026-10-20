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
    except Exception as e:
        return None

def load_data_from_sheet(sheet_name="見学ケースデータ"):
    client = get_gspread_client()
    if not client:
        return {}
    try:
        sh = client.open(sheet_name).sheet1
        records = sh.get_all_records()
        data = {}
        for row in records:
            data[row["key"]] = row["val"] == "1"
        return data
    except Exception:
        return {}

def save_key_to_sheet(key, value, sheet_name="見学ケースデータ"):
    client = get_gspread_client()
    if not client:
        return
    try:
        sh = client.open(sheet_name).sheet1
        cell = sh.find(key)
        val_str = "1" if value else "0"
        if cell:
            sh.update_cell(cell.row, 2, val_str)
        else:
            sh.append_row([key, val_str])
    except Exception as e:
        pass

# セッション状態の初期化（初回起動時にスプレッドシートから読み込む）
if "checks" not in st.session_state:
    st.session_state.checks = load_data_from_sheet()

# チェックボックス変更時の保存関数
if "submitted_key" in st.query_params:
    changed_key = st.query_params["submitted_key"]
    new_val = st.query_params.get(changed_key) == "1"
    st.session_state.checks[changed_key] = new_val
    save_key_to_sheet(changed_key, new_val)
    st.query_params.clear()

def render_html_section(title, items, max_cols=15):
    st.markdown(f"### ★ {title}")
    
    html = f'<div class="table-scroll"><table class="custom-table">'
    html += '<tr><th>項目</th><th>必要</th>'
    for i in range(max_cols):
        html += f'<th>{i+1}</th>'
    html += '</tr>'
    
    for row in items:
        item_name = row[0]
        need_count = row[1]
        is_header = row[2] if len(row) > 2 else False
        
        if is_header:
            html += f'<tr class="header-row"><td colspan="{max_cols + 2}"><b>{item_name}</b></td></tr>'
        else:
            html += f'<tr><td>{item_name}</td><td>{need_count}</td>'
            for i in range(max_cols):
                if i < need_count:
                    key = f"{title}_{item_name}_{i}"
                    is_checked = st.session_state.checks.get(key, False)
                    checked_attr = "checked" if is_checked else ""
                    next_val = "0" if is_checked else "1"
                    
                    # タップしたらURLクエリ経由で自動保存を発動させる処理
                    html += f'<td><input type="checkbox" {checked_attr} onchange="window.location.href=\'?submitted_key={key}&{key}={next_val}\'"></td>'
                else:
                    html += '<td class="empty-cell"></td>'
            html += '</tr>'
    
    html += '</table></div>'
    st.markdown(html, unsafe_allow_html=True)

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
render_html_section("保存・治療科", hozon_items, max_cols=15)

# ==========================================
# 2. 第一・第二口腔外科
# ==========================================
render_html_section("第一口腔外科", [("抜歯症例", 2), ("外科外来症例", 2), ("入院患者症例", 2)], max_cols=5)
render_html_section("第二口腔外科", [("抜歯症例", 2), ("外科外来症例", 3), ("入院患者症例", 1)], max_cols=5)

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
render_html_section("口腔補綴科", hotetsu_items, max_cols=11)

# ==========================================
# 4. 咀嚼補綴科
# ==========================================
soshaku_items = [
    ("口腔内検査・概形印象 (F)", 1), ("口腔内検査・概形印象 (P)", 1),
    ("筋圧形成・最終印象 (F)", 1), ("筋圧形成・最終印象 (P)", 1),
    ("咬合採得 (F)", 1), ("咬合採得
