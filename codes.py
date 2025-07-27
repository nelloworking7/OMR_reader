SUBJECT_CODES = {
    1: {
        "name": "국어",
        "type": "객관식",
        "questions": list(range(1, 46))  # 1~45
    },
    2: {
        "name": "수학",
        "type": "혼합",  # 객관식 + 주관식
        "questions": {
            "객관식1": list(range(1, 16)),     # 1~15
            "주관식1": list(range(16, 23)),    # 16~22
            "객관식2": list(range(23, 29)),    # 23~28
            "주관식2": list(range(29, 31))     # 29~30
        }
    },
    3: {
        "name": "영어",
        "type": "객관식",
        "questions": list(range(1, 46))  # 1~45
    },
    4: {
        "name": "한국사",
        "type": "객관식",
        "questions": list(range(1, 21))  # 1~20
    },
    5: {
        "name": "탐구",
        "type": "복수과목",
        "questions": {
            "제1과목": list(range(1, 21)),    # 1~20
            "제2과목": list(range(1, 21))     # 1~20
        }
    },
    6: {
        "name": "제2외국어",
        "type": "객관식",
        "questions": list(range(1, 31))  # 예시로 30문항
    }
}
