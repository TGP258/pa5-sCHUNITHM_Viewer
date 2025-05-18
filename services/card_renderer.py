from PIL import Image, ImageDraw, ImageFont
import os
from flask import current_app

from services.data_loader import load_combined_data


# class CardRenderer:
#     def __init__(self):
#         self.font_cache = {}
#         self.output_dir = os.path.join(current_app.static_folder, 'images/cards')
#         os.makedirs(self.output_dir, exist_ok=True)
#
#     def render_card(self, card_data):
#         # 渲染逻辑...
#         image = self._create_image(card_data)
#         output_path = os.path.join(self.output_dir, f"{card_data['id']}.jpg")
#         image.save(output_path)
#         return output_path


# 单例实例
class CardRenderer:
    def __init__(self, app=None):
        self.font_cache = {}
        self.output_dir = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """延迟初始化，在应用上下文中设置输出目录"""
        self.output_dir = os.path.join(app.static_folder, 'images/cards')
        os.makedirs(self.output_dir, exist_ok=True)

    def render_card(self, card_data):
        """渲染单张卡片"""
        if self.output_dir is None:
            raise RuntimeError("渲染器未初始化，请先调用 init_app()")

        # 创建图像
        image = self._create_card_image(card_data)

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

        # 保存图片
        output_path = os.path.join(self.output_dir, f"{card_data['id']}.jpg")
        image.save(output_path)
        return output_path

    def _create_card_image(self, card_data):
        """实际创建卡片图像的逻辑"""
        # 加载模板或创建新图像
        template_path = os.path.join(current_app.config['TEMPLATES_FOLDER'],
                                     current_app.config.get('CARD_TEMPLATE', 'card_template.png'))

        try:
            if os.path.exists(template_path):
                image = Image.open(template_path).convert('RGB')
            else:
                # 默认背景
                image = Image.new('RGB', current_app.config['OUTPUT_IMAGE_SIZE'], (240, 240, 240))
        except Exception as e:
            current_app.logger.error(f"无法加载模板: {e}")
            image = Image.new('RGB', current_app.config['OUTPUT_IMAGE_SIZE'], (240, 240, 240))

        draw = ImageDraw.Draw(image)

        # 获取字体
        font = self._get_font(
            current_app.config['CARD_FONT'],
            current_app.config['CARD_FONT_SIZE']
        )

        # 绘制文本
        draw.text((50, 50), card_data['title'], fill=(0, 0, 0), font=font)
        # 添加其他绘制逻辑...

        return image

    def _get_font(self, font_path, font_size):
        """获取字体对象，带缓存"""
        cache_key = f"{font_path}_{font_size}"
        if cache_key not in self.font_cache:
            try:
                full_path = os.path.join(current_app.static_folder, 'fonts', font_path)
                self.font_cache[cache_key] = ImageFont.truetype(full_path, font_size)
            except Exception as e:
                current_app.logger.warning(f"无法加载字体 {font_path}: {e}")
                self.font_cache[cache_key] = ImageFont.load_default()
        return self.font_cache[cache_key]


# 创建未初始化的实例

card_renderer = CardRenderer()


def render_cards(card_ids):
    data = load_combined_data()
    for card in filter(lambda x: x['id'] in card_ids, data):
        card_renderer.render_card(card)