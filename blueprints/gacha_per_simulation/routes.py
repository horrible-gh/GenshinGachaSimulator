# blueprints/gacha_per_simulation/routes.py
from flask import Blueprint, request, jsonify
from .simulation import simulate_gacha, estimate_probability

gacha_per_simulation_bp = Blueprint('gacha_per_simulation', __name__)


@gacha_per_simulation_bp.route('/simulate', methods=['POST'])
def simulate_per_simulation():
    try:
        pulls = int(request.form['pulls'])
        target_character = int(request.form['target_character'])
        target_weapon = int(request.form['target_weapon'])

        if pulls <= 0:
            raise ValueError("가챠 횟수는 1 이상이어야 합니다.")
        if target_character <= 0 and target_weapon < 0:
            raise ValueError("목표 캐릭터 수 또는 무기수는 1 이상이어야 합니다.")
        if pulls > 1000:
            raise ValueError("가챠 횟수는 1000 이하로 입력 해 주세요.")

        # 시뮬레이션 횟수를 정의 (예: 10000번)
        trials = 1000

        probability = estimate_probability(
            trials, pulls, target_character, target_weapon)

        return jsonify(probability=probability)
    except Exception as e:
        return jsonify(error=str(e)), 400
