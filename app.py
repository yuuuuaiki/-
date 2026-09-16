import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="病院実習 症例進捗チェッカー", layout="centered", initial_sidebar_state="collapsed")
st.title("🩺 病院実習 症例進捗チェッカー")

# Google Sheets接続
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(ttl=0)

try:
    df = load_data()
    
    # 列名の空白除去＆小文字化マップを作成
    col_map = {str(c).strip().lower(): c for c in df.columns}
    
    # 柔軟な列名マッピング
    name_col = col_map.get("name") or col_map.get("科名") or col_map.get("科") or df.columns[1] if len(df.columns) > 1 else df.columns[0]
    target_col = col_map.get("target") or col_map.get("目標ケース") or col_map.get("目標") or df.columns[2] if len(df.columns) > 2 else df.columns[0]
    current_col = col_map.get("current") or col_map.get("現在ケース") or col_map.get("現在") or df.columns[3] if len(df.columns) > 3 else df.columns[0]
    deadline_col = col_map.get("deadline") or col_map.get("締切")

    # 標準の列名に統一
    df = df.rename(columns={
        name_col: "name",
        target_col: "target",
        current_col: "current"
    })
    if deadline_col:
        df = df.rename(columns={deadline_col: "deadline"})
    else:
        df["deadline"] = ""

    # 数値型に変換
    df["target"] = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int)
    df["current"] = pd.to_numeric(df["current"], errors="coerce").fillna(0).astype(int)

except Exception as e:
    st.error("データの読み込み・変換に失敗しました。")
    st.write("エラー詳細:", e)
    if 'df' in locals():
        st.write("読み込まれた列名一覧:", list(df.columns))
    st.stop()

# タブの作成（進捗確認 と 設定・編集）
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
                conn.update(data=df)
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
            next_id = int(df["id"].max() + 1) if "id" in df.columns and pd.notna(df["id"].max()) else len(df) + 1
            new_row = {
                "name": new_name,
                "target": new_target,
                "current": 0,
                "deadline": new_deadline
            }
            if "id" in df.columns:
                new_row["id"] = next_id
                
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            conn.update(data=df)
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
                conn.update(data=df)
                st.rerun()
        with col_c:
            if st.button("削除", key=f"del_{idx}"):
                df = df.drop(idx)
                conn.update(data=df)
                st.rerun()
