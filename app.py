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
    res = requests.get(API_URL, allow_redirects=True)
    data = res.json()
    return pd.DataFrame(data)

def save_data(df):
    records = df.to_dict(orient="records")
    requests.post(API_URL, json=records, allow_redirects=True)

def format_deadline(val):
    if pd.isna(val) or str(val).strip() == "":
        return ""
    return str(val).split("T")[0]

try:
    df = load_data()
    if df.empty:
        df = pd.DataFrame(columns=["id", "name", "target", "current", "deadline"])
    if "deadline" not in df.columns:
        df["deadline"] = ""
    df["target"] = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int)
    df["current"] = pd.to_numeric(df["current"], errors="coerce").fillna(0).astype(int)
except Exception as e:
    st.error("データの読み込みに失敗しました。")
    st.write("エラー詳細:", e)
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

    # 「診療科：処置名」の形式でグループ分け
    df["category"] = df["name"].apply(lambda x: str(x).split("：")[0] if "：" in str(x) else (str(x).split(":")[0] if ":" in str(x) else "その他"))
    df["sub_name"] = df["name"].apply(lambda x: str(x).split("：")[1] if "：" in str(x) else (str(x).split(":")[1] if ":" in str(x) else str(x)))

    categories = df["category"].unique()

    for cat in categories:
        cat_df = df[df["category"] == cat]
        
        # グループごとのアコーディオン表示（タップで開閉）
        with st.expander(f"📌 {cat}（{cat_df['current'].sum()} / {cat_df['target'].sum()}）", expanded=True):
            for idx, row in cat_df.iterrows():
                dept = row["sub_name"]
                target = int(row["target"])
                current = int(row["current"])
                raw_deadline = row.get("deadline", "")
                deadline = format_deadline(raw_deadline)
                progress = (current / target) if target > 0 else 0.0

                st.write(f"**{dept}**" + (f" 🕒 締切: {deadline}" if deadline else "") + f" ({current} / {target})")
                st.progress(min(progress, 1.0))

                col_plus, col_minus, _ = st.columns([1, 1, 2])
                with col_plus:
                    if st.button("＋1", key=f"btn_plus_{idx}"):
                        df.at[idx, "current"] = current + 1
                        save_data(df.drop(columns=["category", "sub_name"], errors="ignore"))
                        st.rerun()
                with col_minus:
                    if st.button("ー1", key=f"btn_minus_{idx}"):
                        if current > 0:
                            df.at[idx, "current"] = current - 1
                            save_data(df.drop(columns=["category", "sub_name"], errors="ignore"))
                            st.rerun()
                st.divider()

# --- タブ2: 科目の追加・編集 ---
with tab2:
    st.subheader("新しい科目を追加")
    st.caption("※「小児歯科：CR修復」のように『科名：処置名』で入力するとグループ分けされます！")
    
    with st.form("add_dept_form", clear_on_submit=True):
        new_name = st.text_input("科名・処置名（例: 小児歯科：CR修復）")
        new_target = st.number_input("目標ケース数", min_value=1, value=2, step=1)
        new_deadline = st.text_input("時期・締切（例: 12月まで / 2026-12-31）")
        submitted = st.form_submit_button("科目を追加する")
        
        if submitted and new_name:
            clean_df = df.drop(columns=["category", "sub_name"], errors="ignore")
            next_id = int(clean_df["id"].max() + 1) if "id" in clean_df.columns and pd.notna(clean_df["id"].max()) and len(clean_df) > 0 else 1
            new_row = {
                "id": next_id,
                "name": new_name,
                "target": new_target,
                "current": 0,
                "deadline": new_deadline
            }
            clean_df = pd.concat([clean_df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(clean_df)
            st.success(f"「{new_name}」を追加しました！")
            st.rerun()

    st.divider()
    st.subheader("登録済みの科目を編集・削除")
    
    clean_df = df.drop(columns=["category", "sub_name"], errors="ignore")
    for idx, row in clean_df.iterrows():
        st.write(f"**{row.get('name', '')}**")
        col_target, col_dead, col_del = st.columns([2, 3, 1])
        
        with col_target:
            new_target_val = st.number_input("目標数", min_value=0, value=int(row["target"]), key=f"target_{idx}")
        
        with col_dead:
            current_dead = format_deadline(row.get("deadline", ""))
            new_dead_val = st.text_input("締切・時期", value=str(current_dead), key=f"dead_{idx}")
            
        with col_del:
            st.write("") # スペース調整
            st.write("")
            if st.button("削除", key=f"del_{idx}"):
                clean_df = clean_df.drop(idx)
                save_data(clean_df)
                st.rerun()

        # 目標数か締切が変更されたら保存
        if new_target_val != row["target"] or new_dead_val != current_dead:
            clean_df.at[idx, "target"] = new_target_val
            clean_df.at[idx, "deadline"] = new_dead_val
            save_data(clean_df)
            st.rerun()

        st.divider()
