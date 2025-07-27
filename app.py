# app.py
import streamlit as st
from config import SUBJECT_CODES
from grading import grade_answers
from omr_processing import detect_markings, generate_x_grids, generate_y_grids, calculate_timing_belt_spacing
import cv2
import numpy as np

def main():
    st.title("OMR 채점 시스템")

    # 1페이지: 과목 선택
    st.header("1. 채점할 과목을 선택하세요")
    math_obj = st.checkbox("수학 객관식")
    math_sub = st.checkbox("수학 주관식")
    kor = st.checkbox("국어")
    eng = st.checkbox("영어")
    his = st.checkbox("한국사")
    exam = st.checkbox("탐구")
    lang2 = st.checkbox("제2외국어")

    if st.button("입력완료"):
        st.session_state['selected_subjects'] = {
            'math_obj': math_obj,
            'math_sub': math_sub,
            'kor': kor,
            'eng': eng,
            'his': his,
            'exam': exam,
            'lang2': lang2,
        }
        st.session_state['page'] = 2
        st.experimental_rerun()

    # 2페이지: 정답 및 배점 입력 (간단히 예시)
    if 'page' in st.session_state and st.session_state['page'] == 2:
        st.header("2. 정답과 배점을 입력하세요")

        # 예시: 국어 1~45 문제 정답 입력 (오지선다)
        kor_answers = []
        for i in range(1, 46):
            kor_answers.append(st.selectbox(f"국어 {i}번 문제 정답", [1, 2, 3, 4, 5], key=f"kor{i}"))
        if st.button("입력완료_2"):
            # 여기서 각 과목별로 정답/배점 데이터 저장하면 됨
            st.session_state['kor_answers'] = kor_answers
            st.session_state['page'] = 3
            st.experimental_rerun()

    # 3페이지: OMR 이미지 업로드 + 채점
    if 'page' in st.session_state and st.session_state['page'] == 3:
        st.header("3. OMR 이미지 업로드")
        uploaded_file = st.file_uploader("OMR 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 임시처리

            # TODO: 타이밍 벨트 인식 및 마킹 추출
            # TODO: grading 함수 호출

            st.write("채점 기능은 구현 중입니다.")

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state['page'] = 1
    main()