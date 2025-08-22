# 0. 필요한 라이브러리를 가져옵니다.
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

#-----------------------------------------------------------------
# 1. 화면 구성 (UI: User Interface)
#-----------------------------------------------------------------

st.set_page_config(page_title="오늘의 발표자 뽑기", page_icon="🎯")
st.title("🎯 오늘의 발표자 뽑기")
st.divider()
total_students = st.number_input("전체 학생 수를 입력하세요.", min_value=1, value=25, step=1)
allow_duplicates = st.checkbox("중복 추첨 허용")
st.divider()

#-----------------------------------------------------------------
# 2-1. 발표자 뽑기 로직 (Session State 미사용 버전)
#-----------------------------------------------------------------
# [문제점] 
# 이 리스트는 버튼을 누르거나 다른 위젯을 조작할 때마다 스크립트가 재실행되어 항상 빈 리스트로 초기화됩니다.
# picked_numbers = [] 

# start_button = st.button("🔍 발표자 뽑기")
# if start_button:
#     picked_number = random.randint(1, total_students + 1)
#     # 뽑힌 번호를 리스트에 추가합니다.
#     picked_numbers.append(picked_number)
#     st.header(f"🎉 {picked_number}번! 발표해주세요!  🎉")

#-----------------------------------------------------------------
# 3. 추첨 이력 표시
#-----------------------------------------------------------------
# st.header("")
# st.subheader("📜 **뽑힌 번호**")
# st.subheader(picked_numbers) # picked_numbers는 매번 초기화됩니다.

#-----------------------------------------------------------------
# [해결책] Session State 초기화
# 앱의 '기억 저장소'인 st.session_state에 'picked_numbers'가 없으면, 딱 한 번만 빈 리스트로 만들어주며, 페이지를 닫기 전까지 초기화되지 않습니다.
#-----------------------------------------------------------------

if 'picked_numbers' not in st.session_state:
    st.session_state.picked_numbers = []

#-----------------------------------------------------------------
# 2-2. 발표자 뽑기 로직 (Session State 사용 버전)
#-----------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    start_button = st.button("🔍 발표자 뽑기", key = 'start_button')
with col2:
    if start_button:
        # --- 중복 추첨을 허용하지 않는 경우 ---
        if not allow_duplicates:
            all_numbers = list(range(1, total_students + 1))
            # 전체 번호 중 아직 뽑히지 않은 번호들만 available_numbers 리스트에 담습니다.
            available_numbers = [num for num in all_numbers if num not in st.session_state.picked_numbers]

            if available_numbers:
                picked_number = random.choice(available_numbers)
                # 뽑힌 번호를 '초기화되지 않는' 세션 상태 리스트에 추가합니다.
                st.session_state.picked_numbers.append(picked_number)
                st.header(f"🎉 {picked_number}번! 당첨!  🎉")
                st.balloons()
            else:
                st.warning("모든 학생이 발표를 완료했습니다! 🥳")

        # --- 중복 추첨을 허용하는 경우 ---
        else:
            picked_number = random.randint(1, total_students)
            # 뽑힌 번호를 세션 상태 리스트에 추가합니다.
            st.session_state.picked_numbers.append(picked_number)
            st.header(f"🎉 {picked_number}번! 당첨!  🎉")
            st.balloons()

#-----------------------------------------------------------------
# 3. 추첨 이력 표시
#-----------------------------------------------------------------

st.divider()
st.subheader("📜 **추첨된 번호**")
st.subheader(str(st.session_state.picked_numbers))
reset_buttion = st.button("⚠️ 추첨 이력 초기화", key="reset_button")
if reset_buttion:
    st.session_state.picked_numbers = []
    st.success("추첨 이력이 초기화되었습니다.")
