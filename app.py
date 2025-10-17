import streamlit as st
import pandas as pd
import pathlib
from datetime import datetime

DATA_PATH = pathlib.Path("data/logs.csv")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# CSV読み込み
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["日付", "得点", "正タイプ(回)", "誤タイプ(回)","正確率(%)", "平均タイプ(回/秒)", "ランキング", "時間帯", "スタンドの有無","BGMの有無","何回目？", "備考" ])

df = load_data()

def cal_accuracy(correct, wrong):
    if correct + wrong == 0:
        return 0.0
    total = correct + wrong
    return (correct / total) * 100


st.title("タイピング練習ログ")

# form
st.subheader("ログ入力")
date = st.date_input("日付", datetime.now().date())
score = st.number_input("得点", 0)
correct_types = st.number_input("正タイプ(回)", 0)
wrong_types = st.number_input("誤タイプ(回)", 0)
accuracy = cal_accuracy(correct_types, wrong_types)
avg_types_per_sec = st.number_input("平均タイプ(回/秒)", 0.0)
ranking = st.number_input("ランキング", 0)
time_of_day = st.number_input("時間帯", 0)
use_stand = st.selectbox("スタンドの有無", ["有", "無"])
bgm = st.selectbox("BGMの有無", ["有", "無"])
session_count = st.number_input("何回目？", 1)
remarks = st.text_area("備考")

if st.button('ログを保存'):
    new_row = [date, score, correct_types, wrong_types, accuracy, avg_types_per_sec, ranking, time_of_day, use_stand, bgm, session_count, remarks]
    df.loc[len(df)] = new_row
    df.to_csv(DATA_PATH, index=False)
    st.success("ログを保存しました！")

    st.subheader("記録一覧")
st.dataframe(df, use_container_width=True)