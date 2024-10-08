# blueprints/gacha_per_simulation/simulation.py
import random


# 가챠 시뮬레이션 함수
def simulate_gacha(pulls, target_character, target_weapon):
    pity = 0
    weapon_pity = 0
    guaranteed_character = False  # 캐릭터 한정 확정 여부
    guaranteed_weapon = False     # 무기 한정 확정 여부
    obtained_characters = 0       # 획득한 캐릭터 수
    obtained_weapons = 0          # 획득한 무기 수

    # 반복문으로 가챠 진행
    for _ in range(pulls):
        # 캐릭터 가챠 진행 (목표 캐릭터 수에 도달하지 않은 경우)
        if obtained_characters < target_character:
            pity += 1
            if pity >= 80 or random.random() < 0.006:  # 캐릭터 가챠: 0.6% 확률
                pity = 0
                if guaranteed_character or random.random() < 0.55:
                    obtained_characters += 1
                    guaranteed_character = False  # 확정 초기화
                else:
                    guaranteed_character = True  # 다음 5성은 확정 픽업 한정

        # 무기 가챠 진행 (캐릭터를 모두 획득한 후 무기 획득 시작)
        elif obtained_weapons < target_weapon:
            weapon_pity += 1
            if weapon_pity >= 70 or random.random() < 0.007:  # 무기 가챠: 0.7% 확률
                weapon_pity = 0
                if guaranteed_weapon or random.random() < 0.75:
                    obtained_weapons += 1
                    guaranteed_weapon = False  # 확정 초기화
                else:
                    guaranteed_weapon = True  # 다음 5성은 확정 픽업 무기

        # 캐릭터와 무기를 모두 얻었을 때 종료
        if obtained_characters >= target_character and obtained_weapons >= target_weapon:
            return True

    return False


# 확률 계산 함수
def estimate_probability(trials, pulls, target_character, target_weapon):
    success = 0
    for _ in range(trials):
        if simulate_gacha(pulls, target_character, target_weapon):
            success += 1
    return success / trials
