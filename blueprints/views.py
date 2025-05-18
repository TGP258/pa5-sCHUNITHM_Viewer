from flask import Blueprint, render_template, send_from_directory, current_app, abort
from services.data_loader import load_combined_data
from services.card_renderer import card_renderer, render_cards
from services.database import get_db

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def index():
    return render_template('base.html')

@views_blueprint.route('/cards')
def show_cards():
    data = load_combined_data()

    # 在请求上下文中渲染卡片
    rendered_cards = []
    for card in data:
        try:
            card_renderer.render_card(card)
            rendered_cards.append(card)
        except Exception as e:
            current_app.logger.error(f"渲染卡片 {card.get('id')} 失败: {e}")

    return render_template('card.html', cards=rendered_cards)

@views_blueprint.route('/card/<int:card_id>')
def get_card_image(card_id):
    # 渲染并返回单张卡片图片
    render_cards([card_id])
    return send_from_directory('static/images/cards', f'{card_id}.jpg')


@views_blueprint.route('/music/<int:song_id>')
def song_detail(song_id):
    # 获取歌曲信息
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # 获取基础信息
        cursor.execute("""
            SELECT * FROM songs WHERE id = %s
        """, (song_id,))
        song = cursor.fetchone()

        if not song:
            abort(404)

        # 获取难度信息
        cursor.execute("""
            SELECT * FROM difficulties 
            WHERE song_id = %s
            ORDER BY level_value
        """, (song_id,))
        song['difficulties'] = cursor.fetchall()

        # 获取玩家成绩
        cursor.execute("""
            SELECT s.*, d.level_display 
            FROM scores s
            JOIN difficulties d ON s.level_index = d.chart_id
            WHERE s.id = %s AND d.song_id = %s
            ORDER BY d.level_value
        """, (song_id, song_id))
        scores = cursor.fetchall()

        return render_template('music_detail.html',
                               song=song,
                               scores=scores)


    finally:
        cursor.close()
@views_blueprint.route('/music/search')
def music_search():
    """音乐搜索页面"""
    return render_template('music_search.html')