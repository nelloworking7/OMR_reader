# timing_belt.py
import cv2
import numpy as np

def preprocess_for_timing_belt(image):
    """
    타이밍 벨트 검출을 위한 전처리:
    - 그레이스케일 변환
    - 이진화 (흑색 직사각형만 남기기 위해 역이진화)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 임계값 조절 가능 (검은색 영역 검출 목적)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    return thresh

def find_timing_belt_rects(binary_img):
    """
    타이밍 벨트에 해당하는 직사각형(검은색) 탐색
    - contour 찾고
    - 너무 작거나 너무 크면 제외 (노이즈 제거용)
    - 직사각형 위치(x,y,w,h) 리스트 반환
    """
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # 크기 조건 필터링 (임계값은 OMR 이미지 크기에 따라 조정 가능)
        if 8 < w < 30 and 8 < h < 30:
            rects.append((x, y, w, h))
    # x좌표 기준 정렬(좌->우)
    rects = sorted(rects, key=lambda r: r[0])
    return rects

def get_right_bottom_timing_belt(rects, image_shape):
    """
    이미지 우측 하단에 위치한 타이밍 벨트 직사각형 리스트 반환
    - 우측 하단 영역 기준으로 필터링
    """
    height, width = image_shape[:2]
    candidates = []
    for r in rects:
        x, y, w, h = r
        # 우측 하단 영역 (예: 이미지의 오른쪽 20%, 아래쪽 20%)
        if x > width * 0.8 and y > height * 0.8:
            candidates.append(r)
    # y좌표 기준 오름차순 정렬 (아래쪽부터 위쪽)
    candidates = sorted(candidates, key=lambda r: r[1], reverse=True)
    return candidates

def calculate_spacing_from_timing_belt(timing_rects):
    """
    우측 하단 타이밍 벨트에서 맨 밑칸과 그 윗칸 간격 계산
    """
    if len(timing_rects) < 2:
        raise ValueError("타이밍 벨트 직사각형이 2개 이상이어야 합니다.")
    # y 좌표 내림차순 정렬 (아래->위)
    timing_rects = sorted(timing_rects, key=lambda r: r[1], reverse=True)
    bottom = timing_rects[0]
    second = timing_rects[1]
    spacing = abs(bottom[1] - second[1])
    return spacing

def find_top_timing_belt(rects, image_shape):
    """
    상단 타이밍 벨트 직사각형(좌측 10개는 인적사항 무시)
    - 좌측 상단 10개는 인적사항, 11번부터 마지막까지 마킹란 기준
    """
    height, width = image_shape[:2]
    candidates = []
    for r in rects:
        x, y, w, h = r
        # 상단 20% 영역
        if y < height * 0.2 and x < width * 0.8:
            candidates.append(r)
    # x좌표 기준 정렬
    candidates = sorted(candidates, key=lambda r: r[0])
    # 좌측 10개 무시
    top_timing = candidates[10:]
    return top_timing