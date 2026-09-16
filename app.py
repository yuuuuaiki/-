import streamlit as st
import pandas as pd

st.set_page_config(page_title="病院実習 症例進捗チェッカー", page_icon="🩺", layout="centered")

st.title("🩺 病院実習 症例進捗チェッカー")

# Streamlit SecretsからスプレッドシートのURLを取得
if "sheet_url" in st.secrets:
    sheet_url = st.secrets["sheet_url"]
else:
    st.info("👈 左側のサイドバーにスプレッドシートの共有URLを設定してください。")
    st.stop()

# スプレッドシートIDの抽出とCSV URLの作成
try:
    if "/d/" in sheet_url:
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    else:
        sheet_id = sheet_url
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(csv_url)
    
    # 列名（1行目）に含まれる余計な空白を自動削除
    df.columns = df.columns.str.strip()
    
    # 見出し表記が「B列 (name)」などの場合にも対応させる処理
    col_map = {}
    for col in df.columns:
        if 'name' in col: col_map['name'] = col
        elif 'target' in col: col_map['target'] = col
        elif 'current' in col: col_map['current'] = col
        elif 'deadline' in col: col_map['deadline'] = col
    
except Exception as e:
    st.error("スプレッドシートの読み込みに失敗しました。URLと共有設定（リンクを知っている全員：編集者）を確認してください。")
    st.stop()

# タブの作成（進捗チェック / 期限・目標の編集）
tab1, tab2 = st.tabs(["📊 進捗一覧・カウント", "⚙️ 期限・目標の編集"])

with tab1:
    st.subheader("現在の進捗状況")
    
    name_col = col_map.get('name', df.columns[1] if len(df.columns) > 1 else df.columns[0])
    target_col = col_map.get('target', df.columns[2] if len(df.columns) > 2 else df.columns[0])
    current_col = col_map.get('current', df.columns[3] if len(df.columns) > 3 else df.columns[0])
    deadline_col = col_map.get('deadline', df.columns[4] if len(df.columns) > 4 else df.columns[0])

    for idx, row in df.iterrows():
        with st.container():
            cols = st.columns([3, 2, 2])
            cols[0].markdown(f"**{row[name_col]}**")
            cols[1].caption(f"期限: {row[deadline_col]}")
            
            try:
                target = int(row[target_col])
                current = int(row[current_col])
            except:
                target, current = 1, 0
                
            progress = min(current / target, 1.0) if target > 0 else 0
            
            st.progress(progress)
            st.write(f"進捗: **{current} / {target}** 件")
            st.divider()

with tab2:
    st.subheader("⚙️ 項目・期限・目標数の編集")
    st.info("科目や目標数・期限を変更したいときは、以下のリンクからスプレッドシートを開いて編集してください。")
    
    # Googleスプレッドシートへの直接リンク
    st.markdown(f"[👉 Googleスプレッドシートを開いて編集する](https://docs.google.com/spreadsheets/d/{sheet_id}/edit)")
    
    st.dataframe(df, use_container_width=True)
