import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="病院実習 症例進捗チェッカー", layout="centered", initial_sidebar_state="collapsed")
st.title("🩺 病院実習 症例進捗チェッカー")

API_URL = st.secrets.get("api_url", "")

if not API_URL:
    st.error("Secretsに api_url が設定されていません。")
    st.stop()

def load_data():
    res = requests.get(API_URL)
    data = res.json()
    return pd.DataFrame(data)

def save_data(df):
    records = df.to_dict(orient="records")
    requests.post(API_URL, json=records)

try:
    df = load_data()
    if df.empty:
        df = pd.DataFrame(columns=["id", "name", "target", "current", "deadline"])
    df["target"] = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int)
    df["current"] = pd.to_numeric(df["current"], errors="coerce").fillna(0).astype(int)
except Exception as e:
    st.error("データの読み込みに失敗しました。")
    st.write(e)
    st.stop()

tab1, tab2 = st.tabs(["📊 進捗確認", "⚙️ 科目の追加・編集"])

# --- タブ1: 進捗確認 ---
with tab1:
    st.subheader("現在の進捗状況")
    
    total_target = df["target"].sum()
    total_current = df["current"].sum()
    total_progress = (total_current / total_target) if total_target > 0 else 0.0

    st.metric("全体の達成率", f"{int(total_progress * 100)}%", f"{total_current} / {total_target} ケース")
    st.progress(min(total_progress, 1.0))
    st.divider()

    for idx, row in df.iterrows():
        dept = row.get("name", f"科目{idx}")
        target = int(row["target"])
        current = int(row["current"])
        deadline = row.get("deadline", "")
        progress = (current / target) if target > 0 else 0.0

        col1, col2 = st.columns([3, 1])
        with col1:
            deadline_str = f" (締切: {deadline})" if pd.notna(deadline) and str(deadline).strip() != "" else ""
            st.write(f"**{dept}**{deadline_str} ({current} / {target})")
            st.progress(min(progress, 1.0))
        with col2:
            if st.button("＋1", key=f"btn_{idx}"):
                df.at[idx, "current"] = current + 1
                save_data(df)
                st.rerun()

# --- タブ2: 科目の追加・編集 ---
with tab2:
    st.subheader("新しい科目を追加")
    with st.form("add_dept_form", clear_on_submit=True):
        new_name = st.text_input("科名（例: 矯正科、小児歯科など）")
        new_target = st.number_input("目標ケース数", min_value=1, value=5, step=1)
        new_deadline = st.text_input("締切（任意 例: 10/31）")
        submitted = st.form_submit_button("科目を追加する")
        
        if submitted and new_name:
            next_id = int(df["id"].max() + 1) if "id" in df.columns and pd.notna(df["id"].max()) and len(df) > 0 else 1
            new_row = {
                "id": next_id,
                "name": new_name,
                "target": new_target,
                "current": 0,
                "deadline": new_deadline
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"「{new_name}」を追加しました！")
            st.rerun()

    st.divider()
    st.subheader("登録済みの科目を編集・削除")
    
    for idx, row in df.iterrows():
        col_a, col_b, col_c = st.columns([2, 2, 1])
        with col_a:
            st.write(f"**{row.get('name', '')}**")
        with col_b:
            new_val = st.number_input(f"目標数", min_value=0, value=int(row["target"]), key=f"target_{idx}")
            if new_val != row["target"]:
                df.at[idx, "target"] = new_val
                save_data(df)
                st.rerun()
        with col_c:
            if st.button("削除", key=f"del_{idx}"):
                df = df.drop(idx)
                save_data(df)
                st.rerun()
