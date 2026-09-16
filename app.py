import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="病院実習 症例進捗チェッカー", layout="centered", initial_sidebar_state="collapsed")
st.title("🩺 病院実習 症例進捗チェッカー")

# Google Sheets接続
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(ttl=0)

try:
    df = load_data()
except Exception as e:
    st.error("データの読み込みに失敗しました。Secretsの設定やスプレッドシートの共有設定を確認してください。")
    st.stop()

# タブの作成（進捗確認 と 設定・編集）
tab1, tab2 = st.tabs(["📊 進捗確認", "⚙️ 科目の追加・編集"])

# --- タブ1: 進捗確認 ---
with tab1:
    st.subheader("現在の進捗状況")
    
    total_target = df["目標ケース"].sum()
    total_current = df["現在ケース"].sum()
    total_progress = (total_current / total_target) if total_target > 0 else 0.0

    st.metric("全体の達成率", f"{int(total_progress * 100)}%", f"{total_current} / {total_target} ケース")
    st.progress(min(total_progress, 1.0))
    st.divider()

    for idx, row in df.iterrows():
        dept = row["科名"]
        target = int(row["目標ケース"])
        current = int(row["現在ケース"])
        progress = (current / target) if target > 0 else 0.0

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{dept}** ({current} / {target})")
            st.progress(min(progress, 1.0))
        with col2:
            if st.button("＋1", key=f"btn_{idx}"):
                df.at[idx, "現在ケース"] = current + 1
                conn.update(data=df)
                st.rerun()

# --- タブ2: 科目の追加・編集 ---
with tab2:
    st.subheader("新しい科目を追加")
    with st.form("add_dept_form", clear_on_submit=True):
        new_dept = st.text_input("科名（例: 矯正科、小児歯科など）")
        new_target = st.number_input("目標ケース数", min_value=1, value=5, step=1)
        submitted = st.form_submit_button("科目を追加する")
        
        if submitted and new_dept:
            new_row = {"科名": new_dept, "目標ケース": new_target, "現在ケース": 0}
            df = df._append(new_row, ignore_index=True)
            conn.update(data=df)
            st.success(f"「{new_dept}」を追加しました！")
            st.rerun()

    st.divider()
    st.subheader("登録済みの科目を編集・削除")
    
    for idx, row in df.iterrows():
        col_a, col_b, col_c = st.columns([2, 2, 1])
        with col_a:
            st.write(f"**{row['科名']}**")
        with col_b:
            new_val = st.number_input(f"目標数", min_value=0, value=int(row["目標ケース"]), key=f"target_{idx}")
            if new_val != row["目標ケース"]:
                df.at[idx, "目標ケース"] = new_val
                conn.update(data=df)
                st.rerun()
        with col_c:
            if st.button("削除", key=f"del_{idx}"):
                df = df.drop(idx)
                conn.update(data=df)
                st.rerun()
