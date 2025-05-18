import pymysql.cursors
from flask import current_app, g


# def get_db():
#     if 'db' not in g:
#         g.db = pymysql.connect(
#             host=current_app.config['DB_HOST'],
#             port=current_app.config.get('DB_PORT', 3308),
#             user=current_app.config['DB_USER'],
#             password=current_app.config['DB_PASSWORD'],
#             database=current_app.config['DB_NAME'],
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#     return g.db
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()
#
#

import pymysql
from flask import current_app, g
def init_db(app):
    app.teardown_appcontext(close_db)
def get_db():
    """
    获取数据库连接
    """
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config.get('DB_HOST', 'localhost'),
            user=current_app.config.get('DB_USER', 'User'),
            password=current_app.config.get('DB_PASSWORD', 'user'),
            database=current_app.config.get('DB_NAME', 'chunithm_db'),
            port=current_app.config.get('DB_PORT', 3308),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def close_db(e=None):
    """
    关闭数据库连接
    """
    db = g.pop('db', None)
    if db is not None:
        try:
            if db.open:  # 检查连接是否仍然打开
                db.close()
        except:
            pass  # 如果关闭时出错，忽略错误