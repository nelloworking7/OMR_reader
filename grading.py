# grading.py

def grade_answers(markings, answer_key, points):
    """
    markings: list of (문제번호, 선택지)
    answer_key: dict {문제번호: 정답번호}
    points: dict {문제번호: 배점}
    """
    score = 0
    detailed = {}
    for q, sel in markings:
        correct = answer_key.get(q, None)
        if correct is None:
            detailed[q] = {'your': sel, 'correct': None, 'result': 'N/A'}
            continue
        if sel == correct:
            score += points.get(q, 0)
            detailed[q] = {'your': sel, 'correct': correct, 'result': 'O'}
        else:
            detailed[q] = {'your': sel, 'correct': correct, 'result': 'X'}
    return score, detailed