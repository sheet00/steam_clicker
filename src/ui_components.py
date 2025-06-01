import pygame
import os
import random


class Particle:
    def __init__(self, x, y, color, radius, velocity, lifespan):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.velocity = velocity  # (vx, vy)
        self.lifespan = lifespan
        self.alpha = 255  # 透明度

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.lifespan -= dt
        self.alpha = max(0, int(255 * (self.lifespan / 0.5)))  # 0.5秒で消えるように調整

    def draw(self, screen):
        # パーティクルを直接画面に描画（より軽量）
        # アルファ値を適用するために、描画前に色を調整
        current_color = self.color
        # 色がタプルであることを確認し、アルファ値を追加
        if isinstance(current_color, tuple) and len(current_color) == 3:
            # アルファ値を適用した新しい色を作成
            adjusted_color = (
                current_color[0],
                current_color[1],
                current_color[2],
                self.alpha,
            )
        else:
            # 不明な形式の場合はデフォルト色とアルファ値を使用
            adjusted_color = (255, 255, 255, self.alpha)  # Fallback to white with alpha

        pygame.gfxdraw.aacircle(
            screen, int(self.x), int(self.y), int(self.radius), adjusted_color
        )
        pygame.gfxdraw.filled_circle(
            screen, int(self.x), int(self.y), int(self.radius), adjusted_color
        )


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, num_particles=10):
        for _ in range(num_particles):
            # ランダムな速度と寿命
            vx = (random.random() - 0.5) * 100
            vy = (random.random() - 0.5) * 100 - 50  # 上方向に少し強く
            lifespan = random.uniform(0.3, 0.8)
            radius = random.uniform(2, 5)
            self.particles.append(Particle(x, y, color, radius, (vx, vy), lifespan))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.lifespan > 0]
        for p in self.particles:
            p.update(dt)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def create_money_particles(self, x, y, amount):
        # お金の量に応じてパーティクルの数を調整
        num_particles = (
            min(20, amount // 100) + 5
        )  # 最低5個、100につき1個追加、最大20個
        # お金の色（緑色）
        money_color = (34, 197, 94)  # ACCENT_SUCCESSと同じ
        self.emit(x, y, money_color, num_particles)

    def create_success_particles(self, x, y):
        # 成功時のパーティクル（少なめ、緑色）
        num_particles = 10
        success_color = ACCENT_SUCCESS  # 成功時の色
        self.emit(x, y, success_color, num_particles)


# 色の定義
WHITE = (255, 255, 255)  # 基本の白
BLACK = (0, 0, 0)  # 基本の黒

# ベースカラー（ライト系）
BACKGROUND_PRIMARY = (248, 249, 250)  # #F8F9FA - メイン背景
BACKGROUND_SECONDARY = (255, 255, 255)  # #FFFFFF - カード背景
BACKGROUND_TERTIARY = (250, 251, 252)  # #FAFBFC - パネル背景

# アクセントカラー
ACCENT_PRIMARY = (59, 130, 246)  # #3B82F6 - メインブルー
ACCENT_SECONDARY = (139, 92, 246)  # #8B5CF6 - パープル
ACCENT_SUCCESS = (34, 197, 94)  # #22C55E - グリーン
ACCENT_WARNING = (251, 146, 60)  # #FB923C - オレンジ
ACCENT_ERROR = (239, 68, 68)  # #EF4444 - レッド

# グレースケール
GRAY_50 = (249, 250, 251)  # #F9FAFB - 最も薄い
GRAY_100 = (243, 244, 246)  # #F3F4F6
GRAY_200 = (229, 231, 235)  # #E5E7EB
GRAY_300 = (209, 213, 219)  # #D1D5DB
GRAY_400 = (156, 163, 175)  # #9CA3AF
GRAY_500 = (107, 114, 128)  # #6B7280 - 中間
GRAY_600 = (75, 85, 99)  # #4B5563
GRAY_700 = (55, 65, 81)  # #374151
GRAY_800 = (31, 41, 55)  # #1F2937
GRAY_900 = (17, 24, 39)  # #111827 - 最も濃い

# テキストカラー
TEXT_PRIMARY = (17, 17, 39)  # #111827 - メインテキスト
TEXT_SECONDARY = (75, 85, 99)  # #4B5563 - サブテキスト
TEXT_TERTIARY = (156, 163, 175)  # #9CA3AF - 補助テキスト
TEXT_INVERSE = (255, 255, 255)  # #FFFFFF - 反転テキスト

# UI要素の色マッピング
INFO_PANEL_BG = BACKGROUND_TERTIARY  # 情報パネルの背景
BUTTON_PANEL_BG = BACKGROUND_TERTIARY  # メインボタンパネルの背景
UPGRADE_PANEL_B极 = BACKGROUND_TERTIARY  # アップグレードパネルの背景

# ボタン色
BUTTON_NORMAL_WORK = ACCENT_PRIMARY  # 労働ボタンの通常色
BUTTON_CLICKED_WORK = (
    ACCENT_PRIMARY[0] - 20,
    ACCENT_PRIMARY[1] - 20,
    ACCENT_PRIMARY[2] - 20,
)  # 労働ボタンのクリック色
BUTTON_NORMAL_BUY = ACCENT_SUCCESS  # 購入ボタンの通常色
BUTTON_CLICKED_BUY = (
    ACCENT_SUCCESS[0] - 20,
    ACCENT_SUCCESS[1] - 20,
    ACCENT_SUCCESS[2] - 20,
)  # 購入ボタンのクリック色

UPGRADE_BUTTON_NORMAL = BACKGROUND_SECONDARY  # アップグレードボタンの通常色
UPGRADE_BUTTON_CLICKED = GRAY_100  # アップグレードボタンのクリック色

BORDER_COLOR = GRAY_200  # パネルの枠線
BORDER_COLOR_SECONDARY = GRAY_300  # セカンダリ境界線色 (必要に応じて使用)

# フィードバックテキストの色（統一感のある色調）
FEEDBACK_SUCCESS = ACCENT_SUCCESS  # 落ち着いたグリーン
FEEDBACK_POSITIVE = ACCENT_SUCCESS  # 深いグリーン
FEEDBACK_INFO = ACCENT_PRIMARY  # 落ち着いたブルー
FEEDBACK_EARNED = ACCENT_PRIMARY  # 深いブルー
FEEDBACK_WARNING = ACCENT_WARNING  # 落ち着いたオレンジ
FEEDBACK_BONUS = ACCENT_WARNING  # 深いオレンジ
FEEDBACK_ERROR = ACCENT_ERROR  # 落ち着いたレッド
FEEDBACK_RESET = ACCENT_ERROR  # 深いレッド
FEEDBACK_NEUTRAL = TEXT_SECONDARY  # 温かいグレー
FEEDBACK_SECONDARY = TEXT_TERTIARY  # 薄い温かいグレー


# フォント設定
pygame.init()
# フォント設定 (Interフォントがない場合はMeiryoを使用)
# 提案書ではInterフォントを使用していますが、環境にない場合を考慮し、Meiryoを代替としています。
# もしInterフォントを導入する場合は、パスを適宜変更してください。
FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"  # または "fonts/Inter-Regular.ttf" など


font_small = pygame.font.Font(FONT_PATH, 14)
font_nomal = pygame.font.Font(FONT_PATH, 16)
font_large = pygame.font.Font(FONT_PATH, 20)
font_x_large = pygame.font.Font(FONT_PATH, 32)

emoji_font = pygame.font.Font("C:/Windows/Fonts/seguiemj.ttf", 20)
emoji_font_large = pygame.font.Font("C:/Windows/Fonts/seguiemj.ttf", 32)


# アイコン関連の設定
def load_upgrade_icons():
    """アップグレードアイコンを読み込む関数"""
    upgrade_icons = []

    # 各アイコンのファイル名を直接指定
    icon_files = [
        "01_kabu_chart_woman.png",
        "02_shopping_omiyage_man.png",
        "03_ai_character01_smile.png",
        "04_shopping_cart.png",
        "05_computer_game_gaming_computer.png",
        "06_game_gamen.png",
    ]

    # アイコンを読み込む
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for icon_file in icon_files:
        try:
            icon_path = os.path.join(current_dir, icon_file)
            icon_image = pygame.image.load(icon_path)
            # アイコンのサイズを調整
            icon_image = pygame.transform.scale(icon_image, (100, 100))
            upgrade_icons.append(icon_image)
        except Exception as e:
            print(f"アイコン読み込みエラー: {icon_file} - {e}")
            # 画像が読み込めない場合は空の画像を作成
            empty_surface = pygame.Surface((70, 70), pygame.SRCALPHA)
            empty_surface.fill((0, 0, 0, 0))  # 透明な画像
            upgrade_icons.append(empty_surface)

    return upgrade_icons


# アップグレードアイコンを読み込む
upgrade_icons = load_upgrade_icons()


def format_number(number):
    """数値を3桁カンマ区切りでフォーマットする関数"""
    return f"{number:,}"


def format_japanese_unit(number, unit="円"):
    """数値を日本円の単位（万、億、兆など）でフォーマットする関数"""
    is_negative = number < 0
    abs_number = abs(number)

    if abs_number < 10000:  # 1万未満
        return f"{number:,}{unit}"

    units = [
        (10**4, "万"),
        (10**8, "億"),
        (10**12, "兆"),
        (10**16, "京"),
        (10**20, "垓"),
        (10**24, "𥝱"),  # または秭
        (10**28, "穣"),
        (10**32, "溝"),
        (10**36, "澗"),
        (10**40, "正"),
        (10**44, "載"),
        (10**48, "極"),
    ]

    for i in range(len(units) - 1, -1, -1):
        value, unit_name = units[i]
        if abs_number >= value:
            formatted_number = abs_number / value
            prefix = "-" if is_negative else ""
            if formatted_number == int(formatted_number):
                return f"{prefix}{int(formatted_number):,}{unit_name}{unit}"
            else:
                return f"{prefix}{formatted_number:.1f}{unit_name}{unit}".replace(
                    f".0{unit_name}{unit}", f"{unit_name}{unit}"
                )

    return f"{number:,}{unit}"  # 念のためのフォールバック


def format_purchase_count(purchase_count):
    """購入数を適切にフォーマットする関数"""
    if purchase_count == int(purchase_count):
        return format_number(int(purchase_count))
    else:
        return f"{purchase_count:.1f}".replace(".0", "")


def draw_stats_cards(screen, game_state):
    """統計カードを描画する関数"""
    screen_width = screen.get_width()
    card_width = (screen_width - 80 - 40) // 3  # 3枚のカードと余白 (20px x 2)
    card_height = 120
    start_x = 40
    start_y = 40
    padding_x = 20

    # カードのデータ (総資産、積みゲー、賃金の3要素)
    cards_data = [
        {
            "icon": "💼",
            "title": "賃金",
            "value": format_japanese_unit(
                int(
                    game_state.work_unit_price
                    * (
                        1.0
                        + (
                            game_state.gaming_pc_level
                            * game_state.gaming_pc_efficiency_bonus
                        )
                    )
                )
            ),
            "subtitle": "労働1回あたりの賃金",
        },
        {
            "icon": "💰",
            "title": "総資産",
            "value": format_japanese_unit(game_state.money),
            "subtitle": "資産すべて",
        },
        {
            "icon": "🎮",
            "title": "積みゲー",
            "value": f"{format_number(game_state.stock)}個",
            "subtitle": "購入したゲーム数",
        },
    ]

    for i, card_data in enumerate(cards_data):
        x = start_x + i * (card_width + padding_x)
        y = start_y
        draw_single_stats_card(screen, x, y, card_width, card_height, card_data)


def draw_single_stats_card(screen, x, y, width, height, card_data):
    """単一の統計カードを描画する関数（グラスモーフィズム風）"""
    # カード背景（グラスモーフィズム）
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # 背景色（単一色）
    pygame.draw.rect(
        card_surface,
        BACKGROUND_SECONDARY,
        (0, 0, width, height),
        border_radius=16,
    )

    # 境界線
    pygame.draw.rect(card_surface, GRAY_300, (0, 0, width, height), 2, border_radius=16)

    screen.blit(card_surface, (x, y))

    # アイコン
    icon_surface = emoji_font_large.render(card_data["icon"], True, TEXT_PRIMARY)
    screen.blit(icon_surface, (x + 20, y + 20))

    # タイトル
    title_surface = font_x_large.render(card_data["title"], True, TEXT_SECONDARY)
    screen.blit(title_surface, (x + 80, y + 20))

    # 値
    value_surface = font_large.render(card_data["value"], True, TEXT_PRIMARY)
    screen.blit(value_surface, (x + 20, y + 80))

    # サブタイトル
    if card_data["subtitle"]:
        subtitle_font = font_small
        subtitle_surface = subtitle_font.render(
            card_data["subtitle"], True, TEXT_TERTIARY
        )
        screen.blit(
            subtitle_surface,
            (
                x + width - subtitle_surface.get_width() - 20,
                y + height - subtitle_surface.get_height() - 10,
            ),
        )


def draw_main_buttons(screen, game_state, buttons, current_time, click_time):
    """メインボタン（労働、購入）を描画する関数（中段に配置）"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    animation_duration = 0.4

    clicked_button = buttons.get("clicked_button")
    work_button_rect = buttons.get("work_button")
    buy_button_rect = buttons.get("buy_button")

    # ボタンパネルの描画（中段に配置）
    panel_width = screen_width - 80  # 画面幅いっぱいを使う
    panel_height = 110  # パネルの高さを半分に調整
    button_panel = pygame.Rect(
        40,  # 左マージン
        180,  # 情報パネルの下 (40+120+20=180)
        panel_width,
        panel_height,
    )
    pygame.draw.rect(screen, BACKGROUND_TERTIARY, button_panel, border_radius=16)
    pygame.draw.rect(screen, GRAY_200, button_panel, 2, border_radius=16)

    # 労働ボタンと購入ボタンを横並びに配置
    button_width = (panel_width - 60) // 2  # 2つのボタンの幅（間に20pxの隙間）
    button_height = 40  # ボタンの高さを半分に調整

    # 労働ボタンの位置を更新
    work_button_rect.x = button_panel.x + 20
    work_button_rect.y = button_panel.y + (panel_height - button_height) // 2
    work_button_rect.width = button_width
    work_button_rect.height = button_height

    # 購入ボタンの位置を更新
    buy_button_rect.x = work_button_rect.right + 20
    buy_button_rect.y = work_button_rect.y
    buy_button_rect.width = button_width
    buy_button_rect.height = button_height

    # 労働ボタンを描画
    draw_modern_button(
        screen,
        work_button_rect,
        "労働",
        "primary",
        "large",
        clicked_button == "work" and current_time - click_time < animation_duration,
    )

    # 購入ボタンを描画
    draw_modern_button(
        screen,
        buy_button_rect,
        "ゲーム購入",
        "success",
        "large",
        clicked_button == "buy" and current_time - click_time < animation_duration,
    )

    # ゲーム価格の表示（購入ボタンの下中央に配置）
    game_price_surface = font_nomal.render(
        f"価格: {format_japanese_unit(int(game_state.game_price))}",
        True,
        TEXT_SECONDARY,
    )
    # 更新後のボタンRectを返す
    price_info_pos = (
        buy_button_rect.centerx - game_price_surface.get_width() // 2,
        buy_button_rect.bottom + 10,
    )
    screen.blit(game_price_surface, price_info_pos)

    # 更新後のボタンRectを返す
    return work_button_rect, buy_button_rect


def draw_modern_button(screen, rect, text, button_type, size, is_clicked):
    """モダンなボタンを描画する関数"""
    # サイズ設定
    sizes = {
        "small": {"height": 36, "font_size": 14},
        "medium": {"height": 44, "font_size": 16},
        "large": {"height": 56, "font_size": 18},
    }
    size_config = sizes[size]

    # タイプ別設定
    types = {
        "primary": {
            "background": ACCENT_PRIMARY,
            "text_color": TEXT_INVERSE,
            "hover_background": (
                ACCENT_PRIMARY[0] - 20,
                ACCENT_PRIMARY[1] - 20,
                ACCENT_PRIMARY[2] - 20,
            ),
        },
        "success": {
            "background": ACCENT_SUCCESS,
            "text_color": TEXT_INVERSE,
            "hover_background": (
                ACCENT_SUCCESS[0] - 20,
                ACCENT_SUCCESS[1] - 20,
                ACCENT_SUCCESS[2] - 20,
            ),
        },
        "secondary": {
            "background": GRAY_100,
            "text_color": TEXT_PRIMARY,
            "hover_background": GRAY_200,
        },
    }
    type_config = types[button_type]

    # ホバー状態の判定
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)

    # ボタンの色
    if is_clicked:
        bg_color = type_config["hover_background"]
    elif is_hovered:
        bg_color = type_config["hover_background"]
    else:
        bg_color = type_config["background"]

    # ボタン背景
    pygame.draw.rect(screen, bg_color, rect, border_radius=12)

    # テキスト
    font = {14: font_nomal, 16: font_nomal, 18: font_nomal}[size_config["font_size"]]
    text_surface = font.render(text, True, type_config["text_color"])
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_upgrade_panel(screen, game_state, buttons, current_time, click_time):
    """アップグレードパネルとカードを描画する関数（下段に配置）"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    animation_duration = 0.4

    clicked_upgrade = buttons.get("clicked_upgrade")
    upgrade_buttons_rects = buttons.get("upgrade_buttons", [])

    # アップグレードパネルの描画（下段に配置） - アップグレード情報パネルの下に配置
    panel_width = screen_width - 80
    panel_height = screen_height - 400  # 画面縦幅を大きくするため
    upgrade_panel = pygame.Rect(
        40,  # 左マージン
        560,  # アップグレード情報パネルの下
        panel_width,
        panel_height,
    )
    pygame.draw.rect(screen, BACKGROUND_TERTIARY, upgrade_panel, border_radius=16)
    pygame.draw.rect(screen, GRAY_200, upgrade_panel, 2, border_radius=16)

    # アップグレードカードの配置設定（3列表示に変更）
    card_width = (panel_width - 100) // 3  # 3列表示（間に隙間を確保）
    card_height = 180
    margin_top = 20
    margin_left = 20
    card_spacing_x = 20
    card_spacing_y = 20

    # アップグレードボタンのrectを再計算
    upgrade_buttons_rects = []
    for i in range(len(game_state.upgrades)):
        row = i // 3  # 3列なので行計算を変更
        col = i % 3  # 3列なので列計算を変更
        x = upgrade_panel.left + margin_left + col * (card_width + card_spacing_x)
        y = upgrade_panel.top + margin_top + row * (card_height + card_spacing_y)
        rect = pygame.Rect(x, y, card_width, card_height)
        upgrade_buttons_rects.append(rect)

    buttons["upgrade_buttons"] = upgrade_buttons_rects

    # 各アップグレードカードの描画
    for i, upgrade_rect in enumerate(upgrade_buttons_rects):
        draw_upgrade_card(
            screen,
            game_state,
            upgrade_rect,
            i,
            clicked_upgrade,
            current_time,
            click_time,
        )


def draw_upgrade_card(
    screen, game_state, rect, index, clicked_upgrade, current_time, click_time
):
    """単一のアップグレードカードを描画する関数（新しいレイアウト用に調整）"""
    animation_duration = 0.4
    upgrade = game_state.upgrades[index]

    # カード背景（グラスモーフィズム）
    card_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # 購入可能かどうかで色を変更
    is_affordable = game_state.money >= upgrade["cost"]

    # 背景色（半透明）
    bg_alpha = 180 if is_affordable else 100
    pygame.draw.rect(
        card_surface,
        (*BACKGROUND_SECONDARY, bg_alpha),
        (0, 0, rect.width, rect.height),
        border_radius=16,
    )

    # ホバー効果
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    if is_hovered:
        pygame.draw.rect(
            card_surface,
            (*ACCENT_PRIMARY, 30),
            (0, 0, rect.width, rect.height),
            border_radius=16,
        )

    # クリック時の色
    if clicked_upgrade == index and current_time - click_time < animation_duration:
        pygame.draw.rect(
            card_surface,
            (*GRAY_200, 100),
            (0, 0, rect.width, rect.height),
            border_radius=16,
        )

    # 境界線
    border_color = ACCENT_PRIMARY if is_affordable else GRAY_300
    pygame.draw.rect(
        card_surface, border_color, (0, 0, rect.width, rect.height), 2, border_radius=16
    )

    screen.blit(card_surface, (rect.x, rect.y))

    icon_size = 120
    icon_x = rect.x + 10
    icon_y = rect.y + 10

    if index < len(upgrade_icons):
        icon = pygame.transform.scale(upgrade_icons[index], (icon_size, icon_size))
        screen.blit(icon, (icon_x, icon_y))

    # タイトル
    display_name = upgrade["name"]
    title_surface = font_large.render(display_name, True, TEXT_PRIMARY)
    screen.blit(title_surface, (icon_x + icon_size + 20, icon_y))

    # 価格
    price_text = format_japanese_unit(upgrade["cost"])
    price_color = ACCENT_SUCCESS if is_affordable else TEXT_TERTIARY
    price_surface = font_large.render(price_text, True, price_color)
    screen.blit(price_surface, (icon_x + icon_size + 20, icon_y + 30))

    # 所持数/レベル
    if index == 4:  # ゲーミングPC
        count_text = (
            f"Lv.{game_state.gaming_pc_level}"
            if game_state.gaming_pc_level > 0
            else "未所持"
        )
    else:
        count_text = f"所持: {upgrade['count']}"
    count_surface = font_nomal.render(count_text, True, TEXT_SECONDARY)
    screen.blit(count_surface, (icon_x + icon_size + 20, icon_y + 60))

    # 説明文
    description_lines = upgrade["description"].split("\n")
    line_height = font_small.get_height()
    for i, line in enumerate(description_lines):
        desc_surface = font_small.render(line, True, TEXT_TERTIARY)
        screen.blit(
            desc_surface, (rect.x + 10, rect.y + rect.height - 50 + (i * line_height))
        )


def draw_upgrade_status_panel(screen, game_state):
    """アップグレード情報表示パネルを描画する関数"""
    # パネルの位置とサイズ
    panel_width = screen.get_width() - 80
    panel_height = 250  # 2列表示に対応するため高さを調整
    panel_x = 40
    panel_y = 300  # メインボタンの下

    # パネルの背景
    pygame.draw.rect(
        screen,
        BACKGROUND_TERTIARY,
        (panel_x, panel_y, panel_width, panel_height),
        border_radius=12,
    )
    pygame.draw.rect(
        screen,
        GRAY_200,
        (panel_x, panel_y, panel_width, panel_height),
        2,
        border_radius=12,
    )

    # 列と行の設定
    num_cols = 2
    num_rows = 3  # 1列3要素なので、合計6要素で2列3行
    col_width = panel_width // num_cols
    row_height = panel_height // num_rows

    # 各要素のパディング
    item_padding_y = 10

    # 1行目: 基本情報
    base_texts = [
        "💼 労働DX化",
        "🛒 同時購入",
        "🤖 労働自動化",
        "⚡ 購入自動化",
        "🎮 ゲーミングPC",
        "🚀 アーリーアクセス",
    ]

    # 2行目: 具体的効果
    effect_texts = [
        # 労働DX化
        f"{int(game_state.upgrades[0]['count'] * game_state.work_unit_up_percent)}%アップ",
        # 同時購入
        f"{format_purchase_count(game_state.purchase_count)}個/回",
        # 労働自動化
        f"毎秒{game_state.auto_clicks}回クリック",
        # 購入自動化
        f"{game_state.auto_purchase_interval}秒毎に{game_state.auto_purchases}回購入",
        # ゲーミングPC
        "",  # ゲーミングPCのテキストは描画時に特別処理するので空にする
        # アーリーアクセス
        "",  # アーリーアクセスは2行で表示するので、ここでは空にする
    ]

    # テキストを描画（絵文字とテキストを分離）
    for i, text in enumerate(base_texts):
        # 2列3行の配置を計算
        col = i // num_rows  # 0, 0, 0, 1, 1, 1
        row = i % num_rows  # 0, 1, 2, 0, 1, 2

        # 各要素の中心X座標を計算
        x_center = panel_x + col * col_width + col_width // 2

        # 各要素のY座標を計算
        y_base = panel_y + row * row_height + item_padding_y

        # 絵文字とテキストを分離（最初の1文字が絵文字）
        emoji_char = text[0]
        text_part = text[2:]  # 絵文字とスペースを除いた部分

        # 絵文字部分の描画
        emoji_surface = emoji_font.render(emoji_char, True, TEXT_PRIMARY)
        emoji_rect = emoji_surface.get_rect(
            midright=(x_center - 5, y_base + 10)
        )  # 調整
        screen.blit(emoji_surface, emoji_rect)

        # テキスト部分の描画
        text_surface = font_nomal.render(text_part, True, TEXT_PRIMARY)
        text_rect = text_surface.get_rect(midleft=(x_center, y_base + 10))  # 調整
        screen.blit(text_surface, text_rect)

    for i, text in enumerate(effect_texts):
        # 2列3行の配置を計算
        col = i // num_rows
        row = i % num_rows

        # 各要素の中心X座標を計算
        x_center = panel_x + col * col_width + col_width // 2

        # 各要素のY座標を計算
        y_effect = (
            panel_y + row * row_height + item_padding_y + 40
        )  # 効果テキストのY座標

        if i == 4:  # ゲーミングPCの場合
            # 1行目: 効率と購入間隔
            line1_text = (
                f"効率+{int(game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus * 100)}% "
                f"購入間隔-{int(game_state.gaming_pc_level * game_state.gaming_pc_interval_reduction * 100)}%"
            )
            line1_surface = font_nomal.render(line1_text, True, TEXT_SECONDARY)
            line1_rect = line1_surface.get_rect(center=(x_center, y_effect))
            screen.blit(line1_surface, line1_rect)

            # 2行目: 配信収益
            line2_text = f"配信収益+{format_japanese_unit(game_state.stock * game_state.gaming_pc_level * game_state.gaming_pc_income_per_game)}/秒"
            line2_surface = font_nomal.render(line2_text, True, TEXT_SECONDARY)
            line2_rect = line2_surface.get_rect(center=(x_center, y_effect + 20))
            screen.blit(line2_surface, line2_rect)
        elif i == 5:  # アーリーアクセスの場合
            # 1行目: 投資額と最大利益率
            line1_text = f"投資額 {format_japanese_unit(game_state.total_early_access_investment)} 最大利益率 {int(game_state.max_return_percent)}%"
            line1_surface = font_nomal.render(line1_text, True, TEXT_SECONDARY)
            line1_rect = line1_surface.get_rect(center=(x_center, y_effect))
            screen.blit(line1_surface, line1_rect)

            # 2行目: 投資効果
            investment_per_second_text = f"投資効果: {format_japanese_unit(game_state.early_access_investment_per_second)}/秒"
            investment_per_second_surface = font_nomal.render(
                investment_per_second_text, True, TEXT_SECONDARY
            )
            investment_per_second_rect = investment_per_second_surface.get_rect(
                center=(x_center, y_effect + 20)
            )
            screen.blit(investment_per_second_surface, investment_per_second_rect)
        else:  # その他の場合
            text_surface = font_nomal.render(text, True, TEXT_SECONDARY)
            text_rect = text_surface.get_rect(center=(x_center, y_effect))
            screen.blit(text_surface, text_rect)


# パーティクルシステムを初期化
particle_manager = None


def init_particle_manager():
    global particle_manager
    if particle_manager is None:
        particle_manager = ParticleSystem()


def draw_click_feedback(screen, game_state, buttons, yum_image, cold_sweat_image):
    """クリック時のフィードバック（画像、テキスト、パーティクル）を描画する関数"""
    animation_duration = 0.4
    clicked_button = buttons.get("clicked_button")
    clicked_upgrade = buttons.get("clicked_upgrade")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time")
    buy_button_rect = buttons.get("buy_button")  # main.pyから渡されるRect

    # パーティクルマネージャーを初期化
    init_particle_manager()

    # クリックされていない場合は何もしない
    if current_time - click_time >= animation_duration:
        # アニメーション終了後、パーティクルをクリア
        if particle_manager:
            particle_manager.particles = []
        return

    # フィードバック表示位置（メインボタンの中央下あたり）
    feedback_pos = (buy_button_rect.centerx, buy_button_rect.bottom + 50)

    # 購入ボタンがクリックされた場合
    if clicked_button == "buy":
        draw_buy_feedback(screen, game_state, feedback_pos, yum_image, buttons)

    # 労働ボタンがクリックされた場合
    elif clicked_button == "work":
        draw_work_feedback(screen, game_state, feedback_pos, cold_sweat_image)

    # アップグレードボタンがクリックされた場合
    elif clicked_upgrade is not None:
        draw_upgrade_feedback(screen, game_state, feedback_pos, clicked_upgrade)

    # リセットボタンがクリックされた場合
    elif clicked_button == "reset":
        draw_reset_feedback(screen, game_state)

    # パーティクルを更新・描画
    if particle_manager:
        particle_manager.update(current_time - click_time)
        particle_manager.draw(screen)


def draw_buy_feedback(screen, game_state, position, yum_image, buttons):
    """購入時のフィードバックを描画する関数"""
    # 画像を表示
    image_rect = yum_image.get_rect(midtop=position)
    screen.blit(yum_image, image_rect)

    # 購入成功メッセージを表示
    purchased_count = buttons.get("purchased_count", 1)  # デフォルトは1
    success_text = font_nomal.render(
        f"ゲームを{purchased_count}個購入したよ！", True, ACCENT_SUCCESS
    )
    text_rect = success_text.get_rect(
        midtop=(position[0], position[1] + yum_image.get_height() + 10)
    )
    screen.blit(success_text, text_rect)

    # パーティクル生成
    if particle_manager:
        particle_manager.create_success_particles(text_rect.centerx, text_rect.centery)


def draw_work_feedback(screen, game_state, position, cold_sweat_image):
    """労働時のフィードバックを描画する関数"""
    # 画像を表示
    image_rect = cold_sweat_image.get_rect(midtop=position)
    screen.blit(cold_sweat_image, image_rect)

    # 労働で得た金額を表示
    efficiency_bonus = 1.0
    if game_state.gaming_pc_level > 0:
        efficiency_bonus = 1.0 + (
            game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus
        )

    earned = int(game_state.work_unit_price * efficiency_bonus)
    earned_text = font_nomal.render(
        f"+{format_japanese_unit(earned)}", True, ACCENT_PRIMARY
    )
    text_rect = earned_text.get_rect(
        midtop=(position[0], position[1] + cold_sweat_image.get_height() + 10)
    )
    screen.blit(earned_text, text_rect)

    # 高額報酬時の追加メッセージ
    if earned >= 1000:
        bonus_text = font_small.render("がんばったね！", True, ACCENT_WARNING)
        bonus_rect = bonus_text.get_rect(midtop=(position[0], text_rect.bottom + 5))
        screen.blit(bonus_text, bonus_rect)

    # パーティクル生成
    if particle_manager:
        particle_manager.create_money_particles(
            text_rect.centerx, text_rect.centery, earned
        )


def draw_upgrade_feedback(screen, game_state, position, upgrade_index):
    """アップグレード購入時のフィードバックを描画する関数"""
    upgrade = game_state.upgrades[upgrade_index]

    # ゲーミングPCの場合は特別なメッセージ
    if upgrade_index == 4:
        if game_state.gaming_pc_level == 1:
            message = "ゲーミングPCを購入したよ！"
        else:
            message = (
                f"ゲーミングPCをLv.{game_state.gaming_pc_level}にアップグレードしたよ！"
            )
    else:
        message = f"{upgrade['name']}を購入したよ！"

    upgrade_text = font_nomal.render(message, True, TEXT_SECONDARY)
    upgrade_rect = upgrade_text.get_rect(midtop=(position[0], position[1] + 10))
    screen.blit(upgrade_text, upgrade_rect)

    # パーティクル生成
    if particle_manager:
        particle_manager.create_success_particles(
            upgrade_rect.centerx, upgrade_rect.centery
        )


def draw_texts(screen, game_state):
    """画面上のテキスト要素をすべて描画する関数"""
    draw_stats_cards(screen, game_state)


def draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image):
    """画面上のボタン要素をすべて描画する関数"""
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time", 0)

    # メインボタン（労働、購入）を描画
    work_button_rect, buy_button_rect = draw_main_buttons(
        screen, game_state, buttons, current_time, click_time
    )
    buttons["work_button"] = work_button_rect
    buttons["buy_button"] = buy_button_rect

    # アップグレードパネルとボタンを描画
    draw_upgrade_panel(screen, game_state, buttons, current_time, click_time)

    # クリック時のフィードバックを描画
    draw_click_feedback(screen, game_state, buttons, yum_image, cold_sweat_image)

    # リセットボタンの位置をアップグレードパネルの下に設定
    reset_button_rect = buttons.get("reset_button")
    if reset_button_rect is None:
        reset_button_rect = pygame.Rect(0, 0, 100, 40)
        buttons["reset_button"] = reset_button_rect

    # アップグレードパネルの位置とサイズからリセットボタンの位置を計算
    # リセットボタンの位置を画面右下に設定
    reset_button_rect.width = 100
    reset_button_rect.height = 40
    reset_button_rect.x = (
        screen.get_width() - reset_button_rect.width - 20
    )  # 右端から20px
    reset_button_rect.y = (
        screen.get_height() - reset_button_rect.height - 20
    )  # 下端から20px

    # リセットボタンを描画
    draw_reset_button(screen, buttons)


def draw_reset_button(screen, buttons):
    """リセットボタンを描画する関数"""
    reset_button_rect = buttons.get("reset_button")
    clicked_button = buttons.get("clicked_button")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time", 0)
    animation_duration = 0.4

    # マウスがボタン上にあるかチェック
    mouse_pos = pygame.mouse.get_pos()
    is_hover = reset_button_rect.collidepoint(mouse_pos)

    # ボタンの色を決定
    if clicked_button == "reset" and current_time - click_time < animation_duration:
        color = ACCENT_ERROR  # クリック時の色
    elif is_hover:
        color = (
            min(255, ACCENT_ERROR[0] + 20),
            max(0, ACCENT_ERROR[1] - 20),
            max(0, ACCENT_ERROR[2] - 20),
        )  # ホバー時の色を少し明るく
    else:
        color = ACCENT_ERROR  # 通常の色

    # ボタンを描画
    pygame.draw.rect(screen, color, reset_button_rect, border_radius=8)
    pygame.draw.rect(screen, GRAY_600, reset_button_rect, 2, border_radius=8)

    # テキストを描画
    reset_text = font_small.render("リセット", True, TEXT_INVERSE)
    text_rect = reset_text.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text, text_rect)


def draw_reset_feedback(screen, game_state):
    """リセット時のフィードバックを描画する関数"""
    # 画面中央に大きなメッセージを表示
    reset_text = font_large.render("ゲームをリセットしました！", True, ACCENT_ERROR)
    text_rect = reset_text.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(reset_text, text_rect)

    # サブメッセージを表示
    sub_text = font_nomal.render("新しい冒険の始まりだよ！", True, TEXT_SECONDARY)
    sub_rect = sub_text.get_rect(
        center=(screen.get_width() // 2, text_rect.bottom + 10)
    )
    screen.blit(sub_text, sub_rect)

    # 画面中央に大きな円形エフェクトを描画（グラスモーフィズム風）
    radius = 100
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2

    # 背景のブラー効果をシミュレート（簡易版）
    # pygame.gfxdraw.box(screen, (center_x - radius, center_y - radius, radius*2, radius*2), (255, 255, 255, 50))

    # 円を描画
    pygame.draw.circle(
        screen, (*BACKGROUND_SECONDARY, 150), (center_x, center_y), radius, 0
    )  # 半透明の背景
    pygame.draw.circle(
        screen, (*GRAY_300, 100), (center_x, center_y), radius, 2
    )  # 境界線
