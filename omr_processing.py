# omr_processing.py
import cv2
import numpy as np
from utils import preprocess_image, find_black_rects
from config import TIMING_BELT_X_START_MULTIPLIER

def calculate_timing_belt_spacing(timing_rects):
    """오른쪽 하단 타이밍 벨트 중 맨밑칸과 그 윗칸 간격 계산"""
    timing_rects = sorted(timing_rects, key=lambda r: r[1])  # y좌표 기준 정렬
    if len(timing_rects) < 2:
        raise ValueError("타이밍 벨트 직사각형이 충분하지 않음")
    spacing = timing_rects[1][1] - timing_rects[0][1]
    return spacing

def generate_x_grids(spacing, top_y):
    """기준길이(spacing)의 5.2배를 시작점으로 x축 평행 그리드 20개 생성"""
    start_y = top_y + spacing * TIMING_BELT_X_START_MULTIPLIER
    grids = [start_y + i*spacing for i in range(20)]
    return grids

def generate_y_grids(timing_rects, start_x):
    """상단 타이밍 벨트 기준으로 y축 그리드 생성"""
    # timing_rects는 x좌표 정렬 되어있음
    grids = []
    for rect in timing_rects:
        x, y, w, h = rect
        if x >= start_x:
            grids.append(x + w//2)
    return grids

def detect_markings(image, x_grids, y_grids):
    """마킹된 문제 번호, 선택지 번호 추출"""
    markings = []
    for i, x in enumerate(y_grids):
        for j, y in enumerate(x_grids):
            # 해당 위치 주변 픽셀 체크 (예: 5x5 영역)
            region = image[int(y-2):int(y+3), int(x-2):int(x+3)]
            if np.sum(region) > 255 * 10:  # 적당한 임계값
                markings.append((j+1, i+1))  # (문제번호, 선택지 번호)
    return markings