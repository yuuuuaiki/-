import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

# 1. 余白を極限まで詰め、紙の表の見た目を完全に再現するCSS
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
    .save-bar {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: white;
        padding: 8px 0;
        border-bottom: 2px solid #ddd;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .save-btn {
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 8px 20px;
        font-size: 0.95rem;
        font-weight: bold;
        border-radius: 4px;
        cursor: pointer;
    }
    .save-btn:hover {
        background-color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

# --- Google スプレッドシート連携処理 ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TARGET_SHEET_NAME = "症例管理データ"

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

def load_data_from_sheet(sheet_name=TARGET_SHEET_NAME):
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
                data[str(k)] = (v == 1 or v == "1" or v is True)
    except Exception:
        pass
    return data

def save_all_to_sheet(checks_dict, sheet_name=TARGET_SHEET_NAME):
    client = get_gspread_client()
    if not client:
        return False
    try:
        sh = client.open(sheet_name).sheet1
        for k, v in checks_dict.items():
            val_str = "1" if v else "0"
            cell = None
            try:
                cell = sh.find(str(k))
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
                sh.append_row([str(k), val_str])
        return True
    except Exception:
        return False

# 初回起動時にスプレッドシートから読み込み
if "checks" not in st.session_state:
    st.session_state.checks = load_data_from_sheet()

# 項目定義の全リスト
SECTIONS = {
    "保存・治療科": [
        ("覆髄法", 2), ("抜髄法", 2), ("感染根管治療", 5), 
        ("★ CR修復 (合計15点)", 0, True), (" └ 2級窩洞以外", 13), (" └ 2級窩洞", 2),
        ("インレー修復", 2), ("感染チェア", 1), ("マイクロの使用", 2), ("歯周外科症例見学", 2)
    ],
    "第一口腔外科": [("抜歯症例", 2), ("外科外来症例", 2), ("入院患者症例", 2)],
    "第二口腔外科": [("抜歯症例", 2), ("外科外来症例", 3), ("入院患者症例", 1)],
    "口腔補綴科": [
        ("医療面接", 3), ("資料獲得", 3), ("診断・カウンセリング", 3),
        ("補綴前処置", 3), ("補綴物除去", 3), ("暫間補綴", 3),
        ("支台築造", 3), ("形成", 3), ("印象・咬合採得", 3),
        ("試適装着", 3), ("インプラント補綴", 3), ("IOS実習", 1),
        ("その他・受付・余剰分", 11), ("補綴難処置", 1),
        ("TMD症例", 1), ("インプラント症例", 1), ("デジタルデンティストリ", 1)
    ],
    "咀嚼補綴科": [
        ("口腔内検査・概形印象 (F)", 1), ("口腔内検査・概形印象 (P)", 1),
        ("筋圧形成・最終印象 (F)", 1), ("筋圧形成・最終印象 (P)", 1),
        ("咬合採得 (F)", 1), ("咬合採得 (P)", 1),
        ("ゴシックアーチ (F)", 1), ("人工歯配列試適 (F)", 1),
        ("装着・患者指導 (F)", 1), ("装着・患者指導 (P)", 1),
        ("調整・経過観察 (F)", 1), ("調整・経過観察 (P)", 1),
        ("補綴前処置 (P)", 1), ("支台装置・義歯試適 (P)", 1),
        ("義歯修理・リライン(各1必須)", 3), ("リコール", 2),
        ("専門外来 (顎顔面補綴、口唇口蓋裂)", 1)
    ],
    "予防歯科": [("見学実習(10-1月)", 2), ("当番(2-10月)", 5)],
    "小児歯科": [
        ("リコール (12月まで)", 2), ("リコール (3月まで)", 3), ("リコール (6月まで)", 3), ("リコール (8月まで)", 2),
        ("CR修復 (12月まで)", 2), ("CR修復 (3月まで)", 3), ("CR修復 (6月まで)", 3), ("CR修復 (8月まで)", 2),
        ("断髄・抜髄・RCT (12月まで)", 2), ("断髄・抜髄・RCT (3月まで)", 3), ("断髄・抜髄・RCT (6月まで)", 3), ("断髄・抜髄・RCT (8月まで)", 2),
        ("乳歯冠・義歯 (12月まで)", 2), ("乳歯冠・義歯 (3月まで)", 3), ("乳歯冠・義歯 (6月まで)", 3), ("乳歯冠・義歯 (8月まで)", 2),
        ("外科処置・抜歯 (12月まで)", 2), ("外科処置・抜歯 (3月まで)", 3), ("外科処置・抜歯 (6月まで)", 3), ("外科処置・抜歯 (8月まで)", 2)
    ],
    "放射線科": [("口内法スケッチ", 5), ("口外法スケッチ", 5), ("口外法スケッチ(CT/MRI)", 5), ("口内法デンタル撮影", 10)],
    "放射線科：撮影見学": [
        ("パノラマXp", 1), ("セファロ撮影", 1), ("顎関節撮影", 1),
        ("頭頸部撮影", 1), ("MBCT", 1), ("CBCT", 1),
        ("MRI 顎関節", 1), ("MRI 頭頸部", 1), ("放射線治療", 1)
    ],
    "歯科麻酔科": [("入院患者全身麻酔", 1), ("精神鎮静法", 1), ("ペインクリニック", 1)],
    "顎口腔機能治療部": [("見学", 10), ("ドライマウスdisc.", 1), ("嚥下disc.", 1), ("SASdisc.", 1), ("発音・構音disc.", 1)],
    "障害者歯科": [("見学", 5)],
    "矯正科": [("配当", 3), ("EW以外の装置", 2), ("EW見学", 1)],
    "当番・研修関連": [("検査部", 1), ("口腔総合診療部", 7), ("医学部病院", 2)]
}

# フォーム送信時の処理（チェックボックスデータを集計してスプレッドシート保存）
if "form_submitted" in st.query_params:
    new_checks = {}
    for title, items in SECTIONS.items():
        for row in items:
            item_name = row[0]
            need_count = row[1]
            is_header = row[2] if len(row) > 2 else False
            if not is_header:
                for i in range(need_count):
                    key = f"{title}_{item_name}_{i}".replace(" ", "_").replace("'", "").replace('"', '')
                    new_checks[key] = key in st.query_params

    st.session_state.checks = new_checks
    if save_all_to_sheet(new_checks):
        st.success("✨ 「症例管理データ」に正常に保存されました！")
    else:
        st.error("⚠️ 保存に失敗しました。接続を確認してください。")
    st.query_params.clear()

# HTMLフォーム開始（表とボタンのみを綺麗に配置）
html_content = '<form method="get">'
html_content += '<input type="hidden" name="form_submitted" value="1">'
html_content += '<div class="save-bar"><span>📋 見学ケース必要項目数早見表</span><input type="submit" class="save-btn" value="💾 変更を保存する"></div>'

def get_table_html(title, items, max_cols=15):
    h = f'<h3>★ {title}</h3>'
    h += '<div class="table-scroll"><table class="custom-table">'
    h += '<tr><th>項目</th><th>必要</th>'
    for i in range(max_cols):
        h += f'<th>{i+1}</th>'
    h += '</tr>'
    
    for row in items:
        item_name = row[0]
        need_count = row[1]
        is_header = row[2] if len(row) > 2 else False
        
        if is_header:
            h += f'<tr class="header-row"><td colspan="{max_cols + 2}"><b>{item_name}</b></td></tr>'
        else:
            h += f'<tr><td>{item_name}</td><td>{need_count}</td>'
            for i in range(max_cols):
                if i < need_count:
                    key = f"{title}_{item_name}_{i}".replace(" ", "_").replace("'", "").replace('"', '')
                    is_checked = st.session_state.checks.get(key, False)
                    checked_attr = "checked" if is_checked else ""
                    h += f'<td><input type="checkbox" name="{key}" value="1" {checked_attr}></td>'
                else:
                    h += '<td class="empty-cell"></td>'
            h += '</tr>'
    h += '</table></div>'
    return h

# 全セクションをHTML表として出力
html_content += get_table_html("保存・治療科", SECTIONS["保存・治療科"], max_cols=15)
html_content += get_table_html("第一口腔外科", SECTIONS["第一口腔外科"], max_cols=5)
html_content += get_table_html("第二口腔外科", SECTIONS["第二口腔外科"], max_cols=5)
html_content += get_table_html("口腔補綴科", SECTIONS["口腔補綴科"], max_cols=11)
html_content += get_table_html("咀嚼補綴科", SECTIONS["咀嚼補綴科"], max_cols=3)
html_content += get_table_html("予防歯科", SECTIONS["予防歯科"], max_cols=5)
html_content += get_table_html("小児歯科", SECTIONS["小児歯科"], max_cols=5)
html_content += get_table_html("放射線科", SECTIONS["放射線科"], max_cols=10)
html_content += get_table_html("放射線科：撮影見学", SECTIONS["放射線科：撮影見学"], max_cols=1)
html_content += get_table_html("歯科麻酔科", SECTIONS["歯科麻酔科"], max_cols=3)
html_content += get_table_html("顎口腔機能治療部", SECTIONS["顎口腔機能治療部"], max_cols=10)
html_content += get_table_html("障害者歯科", SECTIONS["障害者歯科"], max_cols=5)
html_content += get_table_html("矯正科", SECTIONS["矯正科"], max_cols=3)
html_content += get_table_html("当番・研修関連", SECTIONS["当番・研修関連"], max_cols=7)

html_content += '<div style="text-align: center; margin: 20px 0;"><input type="submit" class="save-btn" value="💾 変更を保存する" style="font-size: 1.1rem; padding: 10px 30px;"></div>'
html_content += '</form>'

st.markdown(html_content, unsafe_allow_html=True)
