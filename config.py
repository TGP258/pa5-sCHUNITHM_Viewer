import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件


class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3308))
    DB_USER = os.getenv('DB_USER', 'User')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'user')
    DB_NAME = os.getenv('DB_NAME', 'chunithm_db')

    # 文件路径
    CSV_PATH = os.getenv('CSV_PATH', 'data/scores.csv')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'static/images/cards')

    # 渲染配置
    OUTPUT_IMAGE_SIZE = (800, 600)  # 卡片尺寸
    CARD_TEMPLATE = 'card_template.png'  # 模板文件名
    CARD_FONT = 'NotoSansCJK-Regular.ttc'  # 字体文件
    CARD_FONT_SIZE = 24  # 基础字体大小
    DRAW_CONFIG = {
        'title': (100, 50, 36, (0, 0, 0), 'NotoSansCJK-Regular.ttc'),
        # 其他配置...
    }