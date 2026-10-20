import streamlit as st

st.set_page_config(page_title="見学ケース必要項目数チェック", layout="wide")

# 余白をスッキリさせ、クリックした文字に変化をつけやすくするCSS
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
    </style>
""", unsafe_allow_html=True)

st.title("📋 見学ケース必要項目数早見表")

if "checks" not in st.session_state:
    st.session_state.checks = {}

def render_html_section(title, items, max_cols=15):
    st.markdown(f"### ★ {title}")
    
    html = '<div class="table-scroll"><table class="custom-table">'
    html += '<tr><th>項目</th><th>必要</th>'
    for i in range(max_cols):
        html += f'<th>{i+1}</th>'
    html += '</tr>'
    
    for row in items:
        item_name = row[0]
        need_count = row[1]
        
        html += f'<tr><td>{item_name}</td><td>{need_count}</td>'
        for i in range(max_cols):
            if i < need_count:
                key = f"{title}_{item_name}_{i}"
                checked = "checked" if st.session_state.checks.get(key, False) else ""
                html += f'<td><input type="checkbox" name="{key}" {checked} onchange="this.form.submit()"></td>'
            else:
                html += '<td class="empty-cell"></td>'
        html += '</tr>'
    
    html += '</table></div>'
    st.markdown(html, unsafe_allow_html=True)

with st.form("check_form"):
    
    # ==========================================
    # 1. 保存・治療科（CR修復の全体15マスを削除し内訳のみに）
    # ==========================================
    hozon_items = [
        ("覆髄法", 2), 
        ("抜髄法", 2), 
        ("感染根管治療", 5), 
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
    # 4. 咀嚼補綴科（F・Pはそれぞれ1つずつで計2マスに）
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
        ("専門外来(顎顔面補綴)", 1),
    ]
    render_html_section("咀嚼補綴科", soshaku_items, max_cols=3)

    # ==========================================
    # 5. 予防歯科
    # ==========================================
    render_html_section("予防歯科", [("見学実習(10-1月)", 2), ("当番(2-10月)", 5)], max_cols=5)

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
    render_html_section("小児歯科", shoni_items, max_cols=5)

    # ==========================================
    # 7. 放射線科（撮影見学を追加し、文字クリックでチェックできるように）
    # ==========================================
    houshasen_items = [
        ("口内法スケッチ", 5), ("口外法スケッチ", 5),
        ("口外法スケッチ(CT/MRI)", 5), ("口内法デンタル撮影", 10),
    ]
    render_html_section("放射線科", houshasen_items, max_cols=10)

    st.markdown("### ★ 放射線科：撮影見学")
    st.caption("※ 項目名（文字）をタップするとチェックが入り、文字色が変わります。")
    
    kengaku_list = [
        "パノラマXp", "セファロ撮影", "顎関節撮影", "頭頸部撮影", 
        "MBCT", "CBCT", "MRI 顎関節", "MRI 頭頸部", "放射線治療"
    ]
    
    # 3列に並べて、文字（ラベル付きチェックボックス）で直感的に押せるようにする
    k_cols = st.columns(3)
    for idx, name in enumerate(kengaku_list):
        with k_cols[idx % 3]:
            key = f"放射線科_撮影見学_{name}"
            checked = st.session_state.checks.get(key, False)
            # 文字をタップしてチェックON/OFFできるようにする
            new_val = st.checkbox(name, key=key)
            # チェックが入ったら文字色が変わるようなスタイルを適用
            if new_val:
                st.markdown(f"<style>div[data-testid='stCheckbox'] label span {{ color: #1565c0; font-weight: bold; }}</style>", unsafe_allow_html=True)

    # ==========================================
    # 8. その他各科・当番系
    # ==========================================
    render_html_section("歯科麻酔科", [("入院患者全身麻酔", 1), ("精神鎮静法", 1), ("ペインクリニック", 1)], max_cols=3)
    render_html_section("顎口腔機能治療部", [("見学", 10), ("ドライマウスdisc.", 1), ("嚥下disc.", 1), ("SASdisc.", 1), ("発音・構音disc.", 1)], max_cols=10)
    render_html_section("障害者歯科", [("見学", 5)], max_cols=5)
    render_html_section("矯正科", [("配当", 3), ("EW以外の装置", 2), ("EW見学", 1)], max_cols=3)

    submitted = st.form_submit_button("🔄 入力内容を更新・保存する")
    if submitted:
        st.success("更新しました！")
