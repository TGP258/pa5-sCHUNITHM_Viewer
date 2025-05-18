import pandas as pd
from services.database import get_db
# from services.data_loader import load_combined_data
import json
import os
from flask import current_app


def _load_from_json():
    """从JSON文件加载歌曲数据"""
    json_path = os.path.join(current_app.instance_path, 'data/songs.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 转换格式以保持与数据库返回结构一致
        formatted_data = []
        for song in data:
            for difficulty in song.get('difficulties', []):
                formatted_data.append({
                    'id': song['id'],
                    'title': song['title'],
                    'artist': song['artist'],
                    'genre': song['genre'],
                    'bpm': song['bpm'],
                    'origin_from': song['from'],
                    'difficulty_type': difficulty['type'],
                    'level_value': difficulty['level_value'],
                    'level_display': difficulty['level_display'],
                    'chart_id': difficulty['chart_id'],
                    'combo': difficulty['combo'],
                    'charter': difficulty['charter']
                })
        return formatted_data
    except Exception as e:
        current_app.logger.error(f"从JSON加载数据失败: {e}")
        return []


def load_combined_data():
    """合并歌曲数据和成绩数据"""
    songs = load_song_data()
    scores = load_score_data()

    # 按歌曲ID组织歌曲数据
    songs_dict = {}
    for song in songs:
        song_id = song['id']
        if song_id not in songs_dict:
            songs_dict[song_id] = {
                'id': song_id,
                'title': song['title'],
                'artist': song['artist'],
                'genre': song['genre'],
                'bpm': song['bpm'],
                'from': song['origin_from'],
                'difficulties': []
            }
        songs_dict[song_id]['difficulties'].append({
            'type': song['difficulty_type'],
            'level_value': song['level_value'],
            'level_display': song['level_display'],
            # 'chart_id': song['chart_id'],
            # 'combo': song['combo'],
            # 'charter': song['charter']
        })

    # 合并成绩数据
    combined = []
    for score in scores:
        song_id = score['id']
        if song_id in songs_dict:
            combined.append({
                **songs_dict[song_id],
                **score,
                # 添加计算字段
                'rating_display': f"{score['rating']:.2f}" if 'rating' in score else 'N/A',
                'clear_status': 'CLEAR' if score.get('clear') == 'clear' else '',
                'fc_status': 'FULL COMBO' if score.get('full_combo') == 'fullcombo' else ''
            })
        else:
            current_app.logger.warning(f"未找到歌曲ID {song_id} 的元数据")

    return combined
def load_song_data(source='db'):
    if source == 'db':
        return _load_from_db()
    else:
        return _load_from_json()


def _load_from_db():
    db = get_db()
    # cursor = db.cursor(dictionary=True)
    cursor = db.cursor(dictionary=True) if hasattr(db, 'cursor') and 'dictionary' in db.cursor.__code__.co_varnames else db.cursor()
    try:
        cursor.execute("""
            SELECT s.id, s.title, s.artist, s.genre, s.bpm, s.origin_from,
                   d.difficulty_type, d.level_value, d.level_display
            FROM songs s
            JOIN difficulties d ON s.id = d.song_id
        """)
        return cursor.fetchall()
    finally:
        cursor.close()


def load_score_data():
    try:
        df = pd.read_csv(current_app.config['CSV_PATH'])
        # 数据处理逻辑...
        return df.to_dict('records')
    except Exception as e:
        current_app.logger.error(f"加载成绩数据失败: {e}")
        return []


# def load_combined_data():
#     songs = load_song_data()
#     scores = load_score_data()
#     # 合并逻辑...
#     return combined_data