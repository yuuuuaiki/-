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
except Exception as e:
    st.error("スプレッドシートの読み込みに失敗しました。URLと共有設定（リンクを知っている全員：編集者）を確認してください。")
    st.stop()

# タブの作成（進捗チェック / 期限・目標の編集）
tab1, tab2 = st.tabs(["📊 進捗一覧・カウント", "⚙️ 期限・目標の編集"])

with tab1:
    st.subheader("現在の進捗状況")
    for idx, row in df.iterrows():
        with st.container():
            cols = st.columns([3, 2, 2])
            cols[0].markdown(f"**{row['name']}**")
            cols[1].caption(f"期限: {row['deadline']}")
            
            target = int(row['target'])
            current = int(row['current'])
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
