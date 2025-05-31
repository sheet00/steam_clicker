import pygame
import os

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 180)  # クリック時の色
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)  # クリック時の色
LIGHT_GRAY = (240, 240, 240)  # 背景パネル用
PURPLE = (150, 50, 200)
DARK_PURPLE = (100, 30, 150)

# フォント設定
pygame.init()
font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)
button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 20)  # サイズを元に戻す
title_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 35)
large_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
small_font = pygame.font.Font(
    "C:/Windows/Fonts/meiryo.ttc", 16
)  # アップグレード説明用に小さく
upgrade_font = pygame.font.Font(
    "C:/Windows/Fonts/meiryo.ttc", 18
)  # アップグレード名と価格用

# アップグレードアイコンの読み込み
upgrade_icons = []

# 各アイコンのファイル名を直接指定
icon_files = [
    "01_kabu_chart_woman.png",
    "02_shopping_omiyage_man.png",
    "03_ai_character01_smile.png",
    "04_shopping_cart.png",
    "05_computer_game_gaming_computer.png",
]

# アイコンを読み込む
current_dir = os.path.dirname(os.path.abspath(__file__))
for icon_file in icon_files:
    try:
        icon_path = os.path.join(current_dir, icon_file)
        icon_image = pygame.image.load(icon_path)
        # アイコンのサイズを調整（60x60ピクセル）
        icon_image = pygame.transform.scale(icon_image, (70, 70))
        upgrade_icons.append(icon_image)
    except Exception as e:
        print(f"アイコン読み込みエラー: {icon_file} - {e}")
        # 画像が読み込めない場合は空の画像を作成
        empty_surface = pygame.Surface((70, 70), pygame.SRCALPHA)
        empty_surface.fill((0, 0, 0, 0))  # 透明な画像
        upgrade_icons.append(empty_surface)


def format_number(number):
    """数値を3桁カンマ区切りでフォーマットする関数"""
    return f"{number:,}"


def draw_texts(screen, game_state):
    """テキストを描画する関数"""
    # 上段：情報パネルの背景（画面幅いっぱいに広げる）
    screen_width = screen.get_width()
    info_panel = pygame.Rect(40, 40, screen_width - 80, 180)  # マージンを増やす
    pygame.draw.rect(screen, LIGHT_GRAY, info_panel, border_radius=15)
    pygame.draw.rect(screen, BLACK, info_panel, 3, border_radius=15)  # 枠線を太く

    # タイトル削除してスペース確保

    # 情報パネルを3つのセクションに分ける
    panel_width = info_panel.width - 40  # 左右のマージン20pxずつ

    # お金の表示（3桁カンマ区切り）- 専用の大きなエリアを確保
    money_text = f"お金: {format_number(game_state.money)}円"
    money_surface = font.render(money_text, True, BLACK)
    # お金表示用の背景を作成
    money_bg = pygame.Rect(40, 40, panel_width // 2, 40)  # 位置を上に移動
    # お金は左寄せで表示
    screen.blit(money_surface, (40, 40))  # 位置を上に移動

    # 積みゲーの表示（3桁カンマ区切り）- 右上
    stock_text = f"積みゲー: {format_number(game_state.stock)}個"
    stock_surface = font.render(stock_text, True, BLACK)
    stock_x = info_panel.right - stock_surface.get_width() - 40
    screen.blit(stock_surface, (stock_x, 40))  # 位置を上に移動

    # 賃金のテキスト（3桁カンマ区切り）- 左下
    # ゲーミングPCのボーナスを表示
    efficiency_bonus = 1.0
    if game_state.gaming_pc_level > 0:
        efficiency_bonus = 1.0 + (
            game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus
        )

    actual_wage = int(game_state.work_unit_price * efficiency_bonus)

    if game_state.gaming_pc_level > 0:
        text = f"賃金: {format_number(actual_wage)}円 (ボーナス: +{int((efficiency_bonus-1)*100)}%)"
    else:
        text = f"賃金: {format_number(game_state.work_unit_price)}円"

    work_price_surface = button_font.render(text, True, BLACK)
    screen.blit(work_price_surface, (40, 90))  # 位置を調整

    # 購入力のテキスト（3桁カンマ区切り）- 中央下
    text = f"購入力: {format_number(game_state.purchase_power)}個/回"
    purchase_power_surface = button_font.render(text, True, BLACK)
    purchase_x = info_panel.centerx - purchase_power_surface.get_width() // 2
    screen.blit(purchase_power_surface, (purchase_x, 90))  # 位置を調整

    # 自動クリックのテキスト（3桁カンマ区切り）- 右下
    if game_state.auto_clicks > 0:
        text = f"自動クリック: {format_number(game_state.auto_clicks)}回/秒"
        auto_clicks_surface = button_font.render(text, True, (0, 100, 0))
        auto_x = info_panel.right - auto_clicks_surface.get_width() - 40
        screen.blit(auto_clicks_surface, (auto_x, 90))  # 位置を調整

    # 自動購入のテキスト - 右下の自動クリックの下に表示
    if game_state.auto_purchases > 0:
        # ゲーミングPCのレベルに応じて自動購入間隔を短縮
        auto_purchase_interval = game_state.auto_purchase_interval
        if game_state.gaming_pc_level > 0:
            reduction_percent = (
                game_state.gaming_pc_level * game_state.gaming_pc_interval_reduction
            )
            auto_purchase_interval *= max(
                0.01, 1.0 - reduction_percent
            )  # 最低でも0.01秒は確保

        text = f"自動購入: {format_number(game_state.auto_purchases)}回/{auto_purchase_interval:.2f}秒"
        auto_purchase_surface = button_font.render(text, True, (100, 0, 100))
        if game_state.auto_clicks > 0:
            # 自動クリックがある場合はその下に表示
            auto_purchase_x = info_panel.right - auto_purchase_surface.get_width() - 40
            screen.blit(auto_purchase_surface, (auto_purchase_x, 120))  # 位置を調整
        else:
            # 自動クリックがない場合は同じ位置に表示
            auto_purchase_x = info_panel.right - auto_purchase_surface.get_width() - 40
            screen.blit(auto_purchase_surface, (auto_purchase_x, 90))  # 位置を調整

    # ゲーミングPCからの収入を表示（PCを持っている場合のみ）
    if game_state.gaming_pc_level > 0:
        income_per_sec = (
            game_state.stock
            * game_state.gaming_pc_level
            * game_state.gaming_pc_income_per_game
        )
        text = f"配信収益: {format_number(income_per_sec)}円/秒"
        pc_income_surface = button_font.render(text, True, (0, 0, 150))

        # 自動購入と自動クリックの両方がある場合は、さらに下に表示
        if game_state.auto_clicks > 0 and game_state.auto_purchases > 0:
            pc_income_x = info_panel.right - pc_income_surface.get_width() - 40
            screen.blit(pc_income_surface, (pc_income_x, 150))  # 位置を調整
        # 自動購入か自動クリックのどちらかがある場合
        elif game_state.auto_clicks > 0 or game_state.auto_purchases > 0:
            pc_income_x = info_panel.right - pc_income_surface.get_width() - 40
            screen.blit(pc_income_surface, (pc_income_x, 120))  # 位置を調整
        # どちらもない場合
        else:
            pc_income_x = info_panel.right - pc_income_surface.get_width() - 40
            screen.blit(pc_income_surface, (pc_income_x, 90))  # 位置を調整


def draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image):
    # クリックアニメーションの持続時間（秒）
    animation_duration = 0.4
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    clicked_button = buttons.get("clicked_button")
    clicked_upgrade = buttons.get("clicked_upgrade")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time")
    work_button = buttons.get("work_button")
    buy_button = buttons.get("buy_button")
    upgrade_buttons = buttons.get("upgrade_buttons", [])

    # 中段左：ボタンパネル
    button_panel = pygame.Rect(
        40, 260, screen_width // 2 - 60, screen_height - 300
    )  # マージンを増やす
    pygame.draw.rect(screen, (230, 240, 250), button_panel, border_radius=15)
    pygame.draw.rect(
        screen, (100, 120, 150), button_panel, 3, border_radius=15
    )  # 枠線を太く

    # ボタンの位置を中央に配置
    work_button.width = 300
    work_button.height = 120
    work_button.centerx = button_panel.centerx
    work_button.top = button_panel.top + 50  # 位置を上に調整

    buy_button.width = 300
    buy_button.height = 120
    buy_button.centerx = button_panel.centerx
    buy_button.top = work_button.bottom + 50  # 間隔を調整

    # 労働ボタンの色
    if clicked_button == "work" and current_time - click_time < animation_duration:
        work_color = DARK_BLUE
    else:
        work_color = BLUE

    # 購入ボタンの色
    if clicked_button == "buy" and current_time - click_time < animation_duration:
        buy_color = DARK_GREEN
    else:
        buy_color = GREEN

    # 角丸の矩形を描画する
    pygame.draw.rect(screen, work_color, work_button, border_radius=15)
    pygame.draw.rect(screen, buy_color, buy_button, border_radius=15)

    # ボタンテキストを描画
    work_text = large_font.render("労働", True, WHITE)
    buy_text = large_font.render("ゲーム購入", True, WHITE)

    work_text_rect = work_text.get_rect(center=work_button.center)
    buy_text_rect = buy_text.get_rect(center=buy_button.center)

    screen.blit(work_text, work_text_rect)
    screen.blit(buy_text, buy_text_rect)

    # ゲーム価格のテキスト（3桁カンマ区切り）
    game_price_surface = button_font.render(
        f"価格: {format_number(game_state.game_price)}円", True, BLACK
    )
    price_info_pos = (
        buy_button.centerx - game_price_surface.get_width() // 2,
        buy_button.bottom + 10,
    )
    screen.blit(game_price_surface, price_info_pos)

    # 中段右：アップグレードセクションの背景パネル
    upgrade_panel = pygame.Rect(
        screen_width // 2 + 40,
        260,
        screen_width // 2 - 80,
        screen_height - 300,  # マージンを増やす
    )
    pygame.draw.rect(
        screen, (245, 240, 250), upgrade_panel, border_radius=20
    )  # 薄い紫色の背景
    pygame.draw.rect(
        screen, (100, 50, 150), upgrade_panel, 3, border_radius=20
    )  # 枠線を太く

    # アップグレードボタンの位置を調整 - 固定マージンで配置
    margin_top = 40  # 上部マージン（調整用変数）
    button_spacing = 100  # ボタン間の固定間隔
    start_y = upgrade_panel.top + margin_top  # 開始位置

    # アップグレードボタンの描画
    for i, button in enumerate(upgrade_buttons):
        # ボタンの位置を設定
        button.width = 400  # 横幅を300pxから400pxに増やす
        button.height = 90  # 高さを少し小さく
        button.centerx = upgrade_panel.centerx
        button.top = start_y + i * (button.height + button_spacing)

        upgrade = game_state.upgrades[i]

        # ボタンとその説明をワンセットとして背景を描画
        set_rect = pygame.Rect(
            button.left - 30,  # 左側の余白を増やす
            button.top - 25,  # 上側の余白を増やす
            button.width + 60,  # 右側の余白を増やす
            button.height + 70,  # 説明文のスペースを増やす
        )

        # 背景と枠線を描画
        pygame.draw.rect(
            screen, (230, 225, 240), set_rect, border_radius=15
        )  # 薄い背景色
        pygame.draw.rect(
            screen, (130, 100, 170), set_rect, 3, border_radius=15
        )  # 枠線を太く

        # ボタンの色（クリック時は暗く）
        if clicked_upgrade == i and current_time - click_time < animation_duration:
            color = DARK_PURPLE
        else:
            color = PURPLE

        # お金が足りない場合は暗く表示
        if game_state.money < upgrade["cost"]:
            color = (color[0] // 2, color[1] // 2, color[2] // 2)

        # ボタンを描画
        pygame.draw.rect(screen, color, button, border_radius=15)

        # ボタンテキスト
        name_text = upgrade_font.render(upgrade["name"], True, WHITE)
        cost_text = upgrade_font.render(
            f"{format_number(upgrade['cost'])}円", True, WHITE
        )

        # ゲーミングPCの場合はレベルを表示、それ以外は所持数を表示
        if i == 4:  # ゲーミングPC
            if game_state.gaming_pc_level > 0:
                count_text = upgrade_font.render(
                    f"Lv.{game_state.gaming_pc_level}", True, WHITE
                )
            else:
                count_text = upgrade_font.render("未所持", True, WHITE)
        else:
            count_text = upgrade_font.render(f"所持: {upgrade['count']}", True, WHITE)

        # テキスト位置の基本設定
        text_offset = 0

        # アイコンを表示
        if i < len(upgrade_icons):
            icon = upgrade_icons[i]
            # アイコンの位置を設定（ボタンの左側）
            icon_x = button.left + 20
            icon_y = button.centery - icon.get_height() // 2
            screen.blit(icon, (icon_x, icon_y))

            # アイコンがある場合はテキストの位置を右にずらす
            text_offset = 30

        # テキスト位置を設定（アイコンがある場合は右にずらす）
        name_rect = name_text.get_rect(
            midtop=(button.centerx + text_offset, button.top + 10)
        )
        cost_rect = cost_text.get_rect(
            center=(button.centerx + text_offset, button.centery)
        )
        count_rect = count_text.get_rect(
            midbottom=(button.centerx + text_offset, button.bottom - 10)
        )

        # ボタンテキスト
        name_text = upgrade_font.render(upgrade["name"], True, WHITE)
        cost_text = upgrade_font.render(
            f"{format_number(upgrade['cost'])}円", True, WHITE
        )

        # ゲーミングPCの場合はレベルを表示、それ以外は所持数を表示
        if i == 4:  # ゲーミングPC
            if game_state.gaming_pc_level > 0:
                count_text = upgrade_font.render(
                    f"Lv.{game_state.gaming_pc_level}", True, WHITE
                )
            else:
                count_text = upgrade_font.render("未所持", True, WHITE)
        else:
            count_text = upgrade_font.render(f"所持: {upgrade['count']}", True, WHITE)

        # テキスト位置
        name_rect = name_text.get_rect(
            midtop=(button.centerx, button.top + 10)
        )  # 上部の余白を調整
        cost_rect = cost_text.get_rect(center=(button.centerx, button.centery))
        count_rect = count_text.get_rect(
            midbottom=(button.centerx, button.bottom - 10)
        )  # 下部の余白を調整

        # テキスト描画
        screen.blit(name_text, name_rect)
        screen.blit(cost_text, cost_rect)
        screen.blit(count_text, count_rect)

        # 説明テキスト
        desc_text = small_font.render(upgrade["description"], True, BLACK)
        # 説明テキストの位置をボタンの下部から30px下に配置（枠内に収まるように）
        desc_rect = desc_text.get_rect(center=(button.centerx, button.bottom + 30))
        screen.blit(desc_text, desc_rect)

    # クリックされたボタンに応じて画像を表示（固定位置：購入ボタンの下）
    fixed_img_pos = (buy_button.centerx, buy_button.bottom + 50)

    # 労働または購入ボタンがクリックされた場合のみ画像を表示
    # print(clicked_button)
    if clicked_button == "buy" and current_time - click_time < animation_duration:
        image_rect = yum_image.get_rect(midtop=fixed_img_pos)
        screen.blit(yum_image, image_rect)

        # 購入成功メッセージを表示
        success_text = button_font.render(
            f"{format_number(game_state.purchase_power)}個ゲットだよ！",
            True,
            (0, 150, 0),
        )
        text_rect = success_text.get_rect(
            midtop=(fixed_img_pos[0], fixed_img_pos[1] + yum_image.get_height() + 10)
        )
        screen.blit(success_text, text_rect)

    elif clicked_button == "work" and current_time - click_time < animation_duration:
        image_rect = cold_sweat_image.get_rect(midtop=fixed_img_pos)
        screen.blit(cold_sweat_image, image_rect)

        # 労働で得た金額を表示（ゲーミングPCのボーナスを含む）
        efficiency_bonus = 1.0
        if game_state.gaming_pc_level > 0:
            efficiency_bonus = 1.0 + (
                game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus
            )

        earned = int(game_state.work_unit_price * efficiency_bonus)

        earned_text = button_font.render(
            f"+{format_number(earned)}円", True, (0, 0, 150)
        )
        text_rect = earned_text.get_rect(
            midtop=(
                fixed_img_pos[0],
                fixed_img_pos[1] + cold_sweat_image.get_height() + 10,
            )
        )
        screen.blit(earned_text, text_rect)

        # 効果音を鳴らす代わりに視覚的なフィードバック
        if earned >= 1000:
            bonus_text = small_font.render("がんばったね！", True, (200, 0, 100))
            bonus_rect = bonus_text.get_rect(
                midtop=(fixed_img_pos[0], text_rect.bottom + 5)
            )
            screen.blit(bonus_text, bonus_rect)

    # アップグレードボタンがクリックされた場合は、購入成功メッセージを表示
    elif clicked_upgrade is not None and current_time - click_time < animation_duration:
        upgrade = game_state.upgrades[clicked_upgrade]

        # ゲーミングPCの場合は特別なメッセージ
        if clicked_upgrade == 4:
            if game_state.gaming_pc_level == 1:
                upgrade_text = button_font.render(
                    f"ゲーミングPCを購入したよ！", True, (150, 0, 150)
                )
            else:
                upgrade_text = button_font.render(
                    f"ゲーミングPCをLv.{game_state.gaming_pc_level}にアップグレードしたよ！",
                    True,
                    (150, 0, 150),
                )
        else:
            upgrade_text = button_font.render(
                f"{upgrade['name']}を購入したよ！", True, (150, 0, 150)
            )

        upgrade_rect = upgrade_text.get_rect(
            midtop=(fixed_img_pos[0], fixed_img_pos[1] + 10)
        )
        screen.blit(upgrade_text, upgrade_rect)
