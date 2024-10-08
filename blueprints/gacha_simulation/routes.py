# blueprints/gacha_simulation/routes.py
from flask import Blueprint, request, jsonify
from .simulation import gacha_simulation, evaluate_luck

gacha_simulation_bp = Blueprint('gacha_simulation', __name__)


@gacha_simulation_bp.route('/simulate', methods=['POST'])
def simulate_gacha():
    try:
        gacha_type = request.form['gacha_type']
        pulls = int(request.form['pulls'])

        if pulls <= 0:
            raise ValueError("가챠 횟수는 1 이상이어야 합니다.")
        if pulls > 1000:
            raise ValueError("가챠 횟수는 1000 이하로 입력 해 주세요.")

        stats, details = gacha_simulation(pulls, gacha_type)

        return jsonify(stats=stats, details=details)
    except Exception as e:
        return jsonify(error=str(e)), 400
