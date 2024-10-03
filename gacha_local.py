import random
import math

pity = 80
base_rate = 0.006  # 0.6%
special_rate = 0.55  # 한정 캐릭터 획득 확률
input_choice = 0
primogems_input = 0
pulls_final = 0  # 원석을 가챠 횟수로 변환
primogems_final = 0  # 최종 사용 원석 계산


def input():
    global pity, base_rate, special_rate, input_choice, primogems_input, pulls_final, primogems_final
    # 1. 가챠 종류 선택
    gacha_type = input("1. 캐릭터 가챠 or 2. 무기 가챠를 선택하세요 (1/2): ")

    # 2. 가챠 정보 초기화
    if gacha_type == '1':
        pity = 80
        base_rate = 0.006  # 0.6%
        special_rate = 0.55  # 한정 캐릭터 획득 확률
        print("캐릭터 가챠가 선택되었습니다.")
    elif gacha_type == '2':
        pity = 70
        base_rate = 0.007  # 0.7%
        special_rate = 0.75  # 픽업 무기 확률
        print("무기 가챠가 선택되었습니다.")
    else:
        print("잘못된 입력입니다.")
        return False

    # 3. 제원 입력 방식 선택
    input_choice = input("제원 입력 방식을 선택하세요 (1: 원석으로 입력, 2: 횟수로 입력): ")
    if input_choice == '1':
        # 원석으로 입력
        primogems_input = int(input("사용 가능한 원석 수를 입력하세요: "))
        pulls_final = primogems_input // 160  # 원석을 가챠 횟수로 변환
        primogems_final = pulls_final * 160  # 최종 사용 원석 계산
    elif input_choice == '2':
        # 횟수로 입력
        pulls_final = int(input("가챠 횟수를 입력하세요: "))
        primogems_final = pulls_final * 160  # 가챠 횟수를 원석으로 변환
    else:
        print("잘못된 입력입니다. 1 또는 2 중에서 선택하세요.")
        return False

    print(f"\n총 {pulls_final}회({primogems_final} 원석)로 가챠를 시작합니다.\n")
    return True


def gacha_simulation(log_gacha_step=True):
    global pity, base_rate, special_rate, input_choice, primogems_input, pulls_final, primogems_final

    # 4. 가챠 시뮬레이션
    acquired_specials = 0
    acquired_non_specials = 0  # 비한정 캐릭터/무기 획득 횟수
    pity_count = 0
    pulls_done = 0
    confirmed_next_special = False  # 비한정 획득 후, 다음 5성에서 확정 여부
    total_5_stars = 0  # 총 5성 획득 횟수

    while pulls_done < pulls_final:
        pity_count += 1
        pulls_done += 1

        # 천장 도달 또는 기본 확률로 5성 획득
        if pity_count >= pity or random.random() < base_rate:
            total_5_stars += 1  # 5성 획득 누적
            # 확정 획득 여부 확인
            if confirmed_next_special or (acquired_specials % 2 == 0 and random.random() < special_rate):
                is_special = True
                confirmed_next_special = False  # 확정 획득 후 리셋
            else:
                is_special = False
                confirmed_next_special = True  # 다음 5성은 확정 한정 캐릭터/무기

            if is_special:
                acquired_specials += 1
                if log_gacha_step:
                    print(
                        f"{pulls_done}({pity_count}/{pity})회에 5성 한정 캐릭터/무기 획득! (누적 {acquired_specials}개)\n")
            else:
                acquired_non_specials += 1
                if log_gacha_step:
                    print(
                        f"{pulls_done}({pity_count}/{pity})회에 비한정 캐릭터/무기 획득. 다음 5성은 확정\n")

            pity_count = 0
        else:
            continue

    # 5. 통계 계산 및 결과 분석
    mean_value = pulls_final / pity  # 평균적으로 획득해야 하는 5성 수
    std_dev = math.sqrt(mean_value * (1 - base_rate))  # 표준편차 계산

    # 운의 평가
    def evaluate_luck(obtained, expected, std_dev):
        best = int(round(expected + 12 * std_dev))
        good = int(round(expected + 9 * std_dev))
        bad = int(round(expected + 6 * std_dev))
        worst = int(round(expected + 3 * std_dev))
        normal = int(round((best + good + bad + worst) / 4))
        print()
        print(f"운이 아주좋음:{best}")
        print(f"운이 좋음:{good}")
        print(f"운이 보통:{normal}")
        print(f"운이 나쁨:{bad}")
        print(f"운이 매우나쁨:{worst}")

        # if obtained <= worst:
        #    return f"매우 운이 나쁜 결과(기준:{worst})"
        # elif obtained <= bad:
        #    return f"평균보다 운이 나쁨(기준:{bad})"
        # elif obtained >= best:
        #    return f"매우 운이 좋은 결과(기준:{best})"
        # elif obtained >= good:
        #    return f"평균보다 운이 좋음(기준:{good})"
        # else:
        #    return f"평균적인 결과(기준:{normal})"

    # 결과 메시지 표시
    print(f"총 {pulls_done}회 ({primogems_final} 원석) 사용하여 5성 한정 캐릭터/무기 {acquired_specials}개, 비한정 {acquired_non_specials}개 획득!")
    print(
        f"총 5성 획득 횟수: {total_5_stars} (기대값: {mean_value:.2f}, 표준편차: {std_dev:.2f})")
    print(
        f"확정 + 비확정 획득 횟수 기준으로 평가: {evaluate_luck(total_5_stars, mean_value, std_dev)}")
    print(
        f"한정 캐릭터/무기 획득 횟수 기준으로 평가: {evaluate_luck(acquired_specials, mean_value, std_dev)}")


if __name__ == "__main__":
    gacha_simulation()
