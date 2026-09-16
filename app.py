import datetime
import streamlit as st

st.set_page_config(
    page_title="実習症例チェッカー", layout="centered", initial_sidebar_state="collapsed"
)

st.title("🩺 病院実習 症例進捗チェッカー")

# 初期データの登録（セッションに保持）
if "departments" not in st.session_state:
  st.session_state.departments = [
      {
          "科名": "保存科",
          "目標ケース": 5,
          "現在ケース": 0,
          "期限": datetime.date(2026, 10, 31),
      },
      {
          "科名": "口腔外科",
          "目標ケース": 3,
          "現在ケース": 0,
          "期限": datetime.date(2026, 11, 15),
      },
      {
          "科名": "補綴科",
          "目標ケース": 4,
          "現在ケース": 0,
          "期限": datetime.date(2026, 10, 15),
      },
      {
          "科名": "小児歯科",
          "目標ケース": 2,
          "現在ケース": 0,
          "期限": datetime.date(2026, 12, 1),
      },
  ]

today = datetime.date.today()

# --- 全体サマリー ---
total_target = sum(d["目標ケース"] for d in st.session_state.departments)
total_current = sum(d["現在ケース"] for d in st.session_state.departments)
total_progress = (
    total_current / total_target if total_target > 0 else 0
)

st.subheader("📊 全体の進捗状況")
col_s1, col_s2 = st.columns(2)
col_s1.metric("全体の収集状況", f"{total_current} / {total_target} ケース")
col_s2.metric("全体達成率", f"{int(total_progress * 100)}%")
st.progress(total_progress)

st.divider()

# --- 各科の進捗リスト ---
st.subheader("📋 各科の症例一覧")

for idx, dept in enumerate(st.session_state.departments):
  days_left = (dept["期限"] - today).days

  with st.expander(
      f"**{dept['科名']}** （{dept['現在ケース']} / {dept['目標ケース']} ケース）",
      expanded=True,
  ):
    c1, c2, c3 = st.columns([1.2, 1.2, 1])

    prog = (
        min(dept["現在ケース"] / dept["目標ケース"], 1.0)
        if dept["目標ケース"] > 0
        else 0
    )

    with c1:
      st.write(f"**目標:** {dept['目標ケース']} ケース")
      st.write(f"**現在:** {dept['現在ケース']} ケース")

    with c2:
      st.write(f"**提出期限:** {dept['期限'].strftime('%Y/%m/%d')}")
      if days_left < 0:
        st.error(f"⚠️ 期限切れ ({abs(days_left)}日経過)")
      elif days_left <= 7:
        st.warning(f"⏳ 残り {days_left} 日（急ぎ！）")
      else:
        st.info(f"🗓️ 残り {days_left} 日")

    with c3:
      if st.button("➕ 1ケース追加", key=f"add_{idx}"):
        st.session_state.departments[idx]["現在ケース"] += 1
        st.rerun()
      if st.button("➖ 1ケース減らす", key=f"sub_{idx}"):
        if st.session_state.departments[idx]["現在ケース"] > 0:
          st.session_state.departments[idx]["現在ケース"] -= 1
          st.rerun()

    st.progress(prog)
    if dept["現在ケース"] >= dept["目標ケース"]:
      st.caption("🎉 **必要ケース数達成！**")

st.divider()

# --- 新しい科の追加フォーム ---
with st.expander("➕ 新しい科を追加する"):
  with st.form("add_dept_form"):
    new_name = st.text_input("科の名前 (例: 小児歯科、矯正歯科)")
    new_target = st.number_input("必要目標ケース数", min_value=1, value=3)
    new_deadline = st.date_input("提出期限", value=today)

    submitted = st.form_submit_button("追加する")
    if submitted and new_name:
      st.session_state.departments.append({
          "科名": new_name,
          "目標ケース": new_target,
          "現在ケース": 0,
          "期限": new_deadline,
      })
      st.success(f"{new_name}を追加したで！")
      st.rerun()