from sqlalchemy.testing import db

from services.data_loader import load_song_data, load_combined_data, load_score_data
from flask import Blueprint, request, jsonify
from services.database import get_db
from math import ceil
import pymysql.cursors


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/songs')
def get_songs():
    return jsonify(load_song_data())

@api_blueprint.route('/scores')
def get_scores():
    return jsonify(load_score_data())

@api_blueprint.route('/card/<int:card_id>')
def get_card_data(card_id):
    data = load_combined_data()
    card = next((item for item in data if item['id'] == card_id), None)
    return jsonify(card) if card else ('Not found', 404)

@api_blueprint.route('/music/search')
def search_music():
    try:
        # 获取参数
        query = request.args.get('q', '').strip()
        level = request.args.get('level', '').strip()
        genre = request.args.get('genre', '').strip()

        print(f"收到搜索请求 - 查询: '{query}', 难度: '{level}', 流派: '{genre}'")

        # 初始化数据库连接和游标
        db_conn = None
        cursor = None

        try:
            db_conn = get_db()
            # 添加调试信息
            print(f"数据库连接对象类型: {type(db_conn)}")
            if callable(db_conn):
                print("错误: get_db()返回的是可调用对象而不是连接")
                return jsonify({
                    'success': False,
                    'error': "数据库配置错误"
                }), 500

            cursor = db_conn.cursor(pymysql.cursors.DictCursor)

            sql = """
                SELECT s.id, s.title, s.artist, s.genre, s.bpm,
                       d.level_value, d.level_display, d.difficulty_type
                FROM songs s
                JOIN difficulties d ON s.id = d.song_id
                WHERE 1=1
            """
            params = []

            if query:
                sql += " AND (s.title LIKE %s OR s.artist LIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])

            if level:
                # 确保level可以转换为float
                try:
                    level_float = float(level)
                    sql += " AND d.level_value = %s"
                    params.append(level_float)
                except ValueError:
                    pass

            if genre:
                sql += " AND s.genre = %s"
                params.append(genre)

            sql += " GROUP BY s.id, d.id ORDER BY s.title ASC"

            print("执行SQL:", sql, "参数:", params)
            cursor.execute(sql, params)
            results = cursor.fetchall()

            return jsonify({
                'success': True,
                'results': results,
                'count': len(results)
            })

        except Exception as e:
            print("数据库查询出错:", str(e))
            import traceback
            traceback.print_exc()  # 打印完整的堆栈跟踪
            return jsonify({
                'success': False,
                'error': f"数据库查询出错: {str(e)}"
            }), 500

        finally:
            # 确保资源被正确释放
            if cursor:
                cursor.close()
            if db_conn:
                db_conn.close()

    except Exception as e:
        print("请求处理出错:", str(e))
        import traceback
        traceback.print_exc()  # 打印完整的堆栈跟踪
        return jsonify({
            'success': False,
            'error': f"请求处理出错: {str(e)}"
        }), 500
# @api_blueprint.route('/music/search')
# def search_music():
#     global cursor, db
#     try:
#         # 获取参数
#         query = request.args.get('q', '').strip()
#         level = request.args.get('level', '').strip()
#         genre = request.args.get('genre', '').strip()
#
#         print(f"收到搜索请求 - 查询: '{query}', 难度: '{level}', 流派: '{genre}'")
#
#         # 数据库查询
#         db = get_db()
#         # cursor = db.cursor(dictionary=True)
#         cursor = db.cursor(pymysql.cursors.DictCursor)
#
#         sql = """
#             SELECT s.id, s.title, s.artist, s.genre, s.bpm,
#                    d.level_value, d.level_display, d.difficulty_type
#             FROM songs s
#             JOIN difficulties d ON s.id = d.song_id
#             WHERE 1=1
#         """
#         params = []
#
#         if query:
#             sql += " AND (s.title LIKE %s OR s.artist LIKE %s)"
#             params.extend([f"%{query}%", f"%{query}%"])
#
#         if level:
#             sql += " AND d.level_value = %s"
#             params.append(float(level))
#
#         if genre:
#             sql += " AND s.genre = %s"
#             params.append(genre)
#
#         sql += " GROUP BY s.id, d.id ORDER BY s.title ASC"
#
#         print("执行SQL:", sql, "参数:", params)
#         cursor.execute(sql, params)
#         results = cursor.fetchall()
#
#         return jsonify({
#             'success': True,
#             'results': results,
#             'count': len(results)
#         })
#
#     except Exception as e:
#         print("搜索出错:", str(e))
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
#
#     # finally:
#         # cursor.close()
#         # db.close()