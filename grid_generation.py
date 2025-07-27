import numpy as np

def generate_x_grid(start_y, spacing, num_lines=20):
    return [int(start_y + i * spacing) for i in range(num_lines)]

def generate_y_grid(start_x, spacing, num_grids):
    return [int(start_x + i * spacing) for i in range(num_grids)]

def get_question_number(i, j, subject_code):
    # i: x축 그리드 인덱스 (문제 순서용)
    # j: y축 그리드 인덱스 (선지 1~5 위치용)

    if subject_code in [1, 3, 4]:  # 국어, 영어, 한국사
        if j < 15:
            return i + 1 + (j * 20)
        elif j < 20:
            return i + 1 + 20 + ((j - 15) * 20)
        elif j < 25:
            return i + 1 + 40 + ((j - 20) * 20)
        else:
            return None
    elif subject_code == 5:  # 탐구
        if j < 15:
            return ("탐구1", i + 1 + (j * 20))
        elif j < 20:
            return ("탐구2", i + 1 + ((j - 15) * 20))
        else:
            return None
    else:
        return i + 1 + (j * 20)