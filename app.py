import streamlit as st
import json

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

# セッション状態の初期化
if "user_checks" not in st.session_state:
    st.session_state.user_checks = {}

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
        ("外科処置・抜歯 (12月まで)", 2), ("外科処置・抜歯 (3月まで)", 3), ("外科処置・抜歯 (6月まで)", 3), ("外科処置・抜歯 (8月まで)", 2),
        ("保隙・咬合誘導 (12月まで)", 2), ("保隙・咬合誘導 (3月まで)", 3), ("保隙・咬合誘導 (6月まで)", 3), ("保隙・咬合誘導 (8月まで)", 2)
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

sections_json = json.dumps(SECTIONS, ensure_ascii=False)

component_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    .table-scroll { overflow-x: auto; width: 100%; margin-bottom: 0.4rem; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; font-family: sans-serif; }
    .custom-table th, .custom-table td { border: 1px solid #999; padding: 3px 5px; text-align: center; white-space: nowrap; height: 24px; }
    .custom-table th:first-child, .custom-table td:first-child { text-align: left; font-weight: bold; background-color: #f7f7f7; min-width: 160px; }
    .custom-table th:nth-child(2), .custom-table td:nth-child(2) { text-align: center; background-color: #f7f7f7; min-width: 50px; font-size: 0.75rem; color: #555; }
    .empty-cell { background-color: #eaeaea; }
    .header-row { background-color: #f1f3f4; font-weight: bold; text-align: left !important; padding-left: 8px !important; }
    h3 { margin-top: 0.4rem !important; margin-bottom: 0.1rem !important; font-size: 0.95rem !important; color: #111; }
</style>
</head>
<body>
<div id="app"></div>

<script>
const sections = """ + sections_json + """;

function render() {
    let saved = JSON.parse(localStorage.getItem('kengaku_data_v2') || '{}');
    let html = '';

    for (const [title, items] of Object.entries(sections)) {
        let max_cols = 15;
        if (["第一口腔外科", "第二口腔外科", "予防歯科", "小児歯科", "障害者歯科"].includes(title)) max_cols = 5;
        else if (title === "口腔補綴科") max_cols = 11;
        else if (["咀嚼補綴科", "歯科麻酔科", "矯正科"].includes(title)) max_cols = 3;
        else if (["放射線科", "顎口腔機能治療部"].includes(title)) max_cols = 10;
        else if (title === "放射線科
