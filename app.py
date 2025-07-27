import streamlit as st
from data.codes import SUBJECT_CODES
from data.subjects import SUBJECT_LIST
from utils.grading import grade_answers
from utils.grid_generation import generate_grids
from utils.marking_detection import detect_markings

def main():
    st.title("OMR 채점 웹앱")

    # 1페이지: 과목 선택
    st.header("1. 채점할 과목을 선택하세요")
    
    # 수학(객관식+주관식) 별도 처리
    math_selected = st.checkbox("2. 수학 (객관식+주관식)")
    # 일반 과목
    general_subjects = ["1. 국어", "3. 영어", "4. 한국사", "5. 탐구", "6. 제2외국어"]
    selected_general = st.multiselect("일반 과목 선택", general_subjects)
    
    if st.button("입력완료"):
        st.session_state['math_selected'] = math_selected
        st.session_state['selected_general'] = selected_general
        st.session_state['page'] = 2

    # 2페이지: 정답 및 배점 입력
    if st.session_state.get('page', 1) == 2:
        st.header("2. 답과 배점을 입력하세요")
        # 선택된 과목에 따라 입력창 생성
        answers = {}
        scores = {}
        
        if st.session_state.get('math_selected', False):
            st.subheader("수학")
            # 수학 답안 및 배점 입력 UI (단답형, 주관식 섞어서)
            answers['math'] = st.text_area("수학 답안 (단답형 1~15, 주관식 16~30)")
            scores['math'] = st.text_area("수학 배점 (콤마로 구분)")
            
        for subj in st.session_state.get('selected_general', []):
            subj_code = subj.split('.')[0]
            subj_name = SUBJECT_LIST.get(subj_code, subj)
            st.subheader(subj_name)
            answers[subj_code] = st.text_area(f"{subj_name} 답안")
            scores[subj_code] = st.text_area(f"{subj_name} 배점")
        
        if st.button("입력완료(답안)"):
            st.session_state['answers'] = answers
            st.session_state['scores'] = scores
            st.session_state['page'] = 3

    # 3페이지: OMR 업로드 및 채점
    if st.session_state.get('page', 3) == 3:
        st.header("3. OMR 사진을 업로드하세요")
        uploaded_file = st.file_uploader("OMR 이미지 파일 선택", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            # 이미지 처리 및 채점 로직 실행
            # (실제 함수는 utils에 구현해두었으니 호출)
            
            # 예시: 
            image = uploaded_file.read()
            
            # 1) 타이밍 벨트 기준 좌측 10칸 이후 데이터 추출
            grids = generate_grids(image)
            markings = detect_markings(image, grids)
            
            # 2) 입력된 정답과 비교해서 채점
            result = grade_answers(markings, st.session_state.get('answers', {}))
            
            st.write("채점 결과:")
            st.json(result)


if __name__ == "__main__":
    # 페이지 상태 초기화
    if 'page' not in st.session_state:
        st.session_state['page'] = 1
    main()
