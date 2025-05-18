from flask import Flask
from blueprints.views import views_blueprint
from blueprints.api import api_blueprint
from config import Config
from services.card_renderer import card_renderer


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化卡片渲染器
    card_renderer.init_app(app)

    # 加载配置
    app.config.from_object(Config)

    # 注册蓝图
    app.register_blueprint(views_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # 初始化服务
    with app.app_context():
        from services.database import init_db
        init_db(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)