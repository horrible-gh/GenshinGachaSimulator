from flask import Flask, render_template
from blueprints.gacha_simulation import gacha_simulation_bp
from blueprints.gacha_per_simulation import gacha_per_simulation_bp

context = "/genshin_gacha_simulator"


def create_app():
    app = Flask(__name__)

    # Blueprint 등록
    app.register_blueprint(gacha_simulation_bp, url_prefix=f'{context}/gacha')
    app.register_blueprint(gacha_per_simulation_bp,
                           url_prefix=f'{context}/per_simulation')

    @app.route(f'{context}')
    def index():
        return render_template('index.html')

    @app.route(f'/')
    def root():
        return "Hello Horrible World!"

    return app


# Flask 애플리케이션을 전역 변수로 생성
app = create_app()

if __name__ == "__main__":
    # __main__으로 실행될 때만 app으로 실행
    app.run(debug=True)
