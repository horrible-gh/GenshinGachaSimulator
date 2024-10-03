from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

# Flask 라우트 설정


@app.route('/')
def index():
    return render_template('index_ajax.html')  # Ajax가 포함된 HTML 파일


@app.route('/simulate', methods=['POST'])
def simulate():
    # Ajax 요청에서 파라미터 받아오기
    gacha_type = request.form['gacha_type']
    pulls = int(request.form['pulls'])

    # 가챠 시뮬레이션 코드
    stats, details = gacha_simulation(pulls, gacha_type)

    return jsonify(stats=stats, details=details)  # 결과를 JSON으로 반환


def gacha_simulation(pulls_final, gacha_type):
    # 기본 가챠 정보 초기화
    if gacha_type == '1':
        pity = 80
        base_rate = 0.006
        special_rate = 0.55
    elif gacha_type == '2':
        pity = 70
        base_rate = 0.007
        special_rate = 0.75
    else:
        return "잘못된 가챠 유형입니다."

    # 시뮬레이션 실행
    acquired_specials = 0
    acquired_non_specials = 0
    pity_count = 0
    pulls_done = 0
    confirmed_next_special = False
    total_5_stars = 0
    results = []

    while pulls_done < pulls_final:
        pity_count += 1
        pulls_done += 1

        # 천장 도달 또는 기본 확률로 5성 획득
        if pity_count >= pity or random.random() < base_rate:
            total_5_stars += 1
            if confirmed_next_special or (acquired_specials % 2 == 0 and random.random() < special_rate):
                is_special = True
                confirmed_next_special = False
            else:
                is_special = False
                confirmed_next_special = True

            if is_special:
                acquired_specials += 1
                results.append(
                    f"{pulls_done}({pity_count}/{pity})회에 5성 한정 캐릭터/무기 획득! (누적 {acquired_specials}개)\n")
            else:
                acquired_non_specials += 1
                results.append(
                    f"{pulls_done}({pity_count}/{pity})회에 비한정 캐릭터/무기 획득. 다음 5성은 확정 (누적 {acquired_non_specials}개)\n")
            pity_count = 0

    # 통계 계산 및 결과 분석
    mean_value = pulls_final / pity
    std_dev = math.sqrt(mean_value * (1 - base_rate))

    # 전체 통계 결과 메시지 생성
    stats = (
        f"총 {pulls_done}회 사용하여 5성 한정 캐릭터/무기 {acquired_specials}개, "
        f"비한정 캐릭터/무기 {acquired_non_specials}개 획득!\n"
        f"총 5성 획득 횟수: {total_5_stars} (기대값: {mean_value:.2f}, 표준편차: {std_dev:.2f})\n"
        # f"확정 + 비확정 획득 횟수 기준으로 평가: {evaluate_luck(total_5_stars, mean_value, std_dev)}\n"
        # f"한정 캐릭터/무기 획득 횟수 기준으로 평가: {evaluate_luck(acquired_specials, mean_value, std_dev, special_rate)}\n"
    )

    # 결과 반환 (상위 통계 및 상세 내역)
    return stats, "\n".join(results)

# 운의 평가 함수


def evaluate_luck(obtained, expected, std_dev, rate=1):
    best = int(round((expected + 2.5 * std_dev) * rate))
    good = int(round((expected + 2 * std_dev) * rate))
    bad = int(round((expected + 1 * std_dev) * rate))
    worst = int(round((expected - 0.5 * std_dev) * rate))
    normal = int(round(best + good + bad + worst) / 4)
    if obtained <= worst:
        return f"매우 운이 나쁜 결과 (기준: {worst})"
    elif obtained <= bad:
        return f"평균보다 운이 나쁨 (기준: {bad})"
    elif obtained >= best:
        return f"매우 운이 좋은 결과 (기준: {best})"
    elif obtained >= good:
        return f"평균보다 운이 좋음 (기준: {good})"
    else:
        return f"평균적인 결과 (기준: {normal})"


if __name__ == "__main__":
    app.run(debug=True)
