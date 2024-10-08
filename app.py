from flask import Flask, render_template
from blueprints.gacha_simulation import gacha_simulation_bp
from blueprints.gacha_per_simulation import gacha_per_simulation_bp


def create_app():
    app = Flask(__name__)

    # Blueprint 등록
    app.register_blueprint(gacha_simulation_bp, url_prefix='/gacha')
    app.register_blueprint(gacha_per_simulation_bp,
                           url_prefix='/per_simulation')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
