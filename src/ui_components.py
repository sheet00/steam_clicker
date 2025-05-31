import pygame

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
button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 20)
title_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 35)
large_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
small_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 18)


def format_number(number):
    """数値を3桁カンマ区切りでフォーマットする関数"""
    return f"{number:,}"


def draw_texts(screen, game_state):
    """テキストを描画する関数"""
    # 上段：情報パネルの背景（画面幅いっぱいに広げる）
    screen_width = screen.get_width()
    info_panel = pygame.Rect(20, 20, screen_width - 40, 150)
    pygame.draw.rect(screen, LIGHT_GRAY, info_panel, border_radius=15)
    pygame.draw.rect(screen, BLACK, info_panel, 2, border_radius=15)  # 枠線

    # タイトル
    title_surface = title_font.render("Steamクリッカー", True, BLACK)
    screen.blit(
        title_surface, (info_panel.centerx - title_surface.get_width() // 2, 30)
    )

    # 情報パネルを3つのセクションに分ける
    panel_width = info_panel.width - 40  # 左右のマージン20pxずつ
    
    # お金の表示（3桁カンマ区切り）- 専用の大きなエリアを確保
    money_text = f"お金: {format_number(game_state.money)}円"
    money_surface = font.render(money_text, True, BLACK)
    # お金表示用の背景を作成
    money_bg = pygame.Rect(40, 80, panel_width // 2, 40)
    # お金は左寄せで表示
    screen.blit(money_surface, (40, 80))
    
    # 積みゲーの表示（3桁カンマ区切り）- 右上
    stock_text = f"積みゲー: {format_number(game_state.stock)}個"
    stock_surface = font.render(stock_text, True, BLACK)
    stock_x = info_panel.right - stock_surface.get_width() - 40
    screen.blit(stock_surface, (stock_x, 80))
    
    # 賃金のテキスト（3桁カンマ区切り）- 左下
    text = f"賃金: {format_number(game_state.work_unit_price)}円"
    work_price_surface = button_font.render(text, True, BLACK)
    screen.blit(work_price_surface, (40, 130))

    # 購入力のテキスト（3桁カンマ区切り）- 中央下
    text = f"購入力: {format_number(game_state.purchase_power)}個/回"
    purchase_power_surface = button_font.render(text, True, BLACK)
    purchase_x = info_panel.centerx - purchase_power_surface.get_width() // 2
    screen.blit(purchase_power_surface, (purchase_x, 130))
    
    # 自動クリックのテキスト（3桁カンマ区切り）- 右下
    if game_state.auto_clicks > 0:
        text = f"自動クリック: {format_number(game_state.auto_clicks)}回/秒"
        auto_clicks_surface = button_font.render(text, True, (0, 100, 0))
        auto_x = info_panel.right - auto_clicks_surface.get_width() - 40
        screen.blit(auto_clicks_surface, (auto_x, 130))


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
    button_panel = pygame.Rect(20, 190, screen_width // 2 - 40, screen_height - 210)
    pygame.draw.rect(screen, (230, 240, 250), button_panel, border_radius=15)
    pygame.draw.rect(screen, (100, 120, 150), button_panel, 2, border_radius=15)  # 枠線

    # ボタンパネルのタイトル
    button_title = title_font.render("アクション", True, BLACK)
    screen.blit(
        button_title,
        (button_panel.centerx - button_title.get_width() // 2, button_panel.top + 20),
    )

    # ボタンの位置を中央に配置
    work_button.width = 300
    work_button.height = 120
    work_button.centerx = button_panel.centerx
    work_button.top = button_panel.top + 80

    buy_button.width = 300
    buy_button.height = 120
    buy_button.centerx = button_panel.centerx
    buy_button.top = work_button.bottom + 50

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
        screen_width // 2 + 20, 190, screen_width // 2 - 40, screen_height - 210
    )
    pygame.draw.rect(
        screen, (245, 240, 250), upgrade_panel, border_radius=20
    )  # 薄い紫色の背景
    pygame.draw.rect(screen, (100, 50, 150), upgrade_panel, 2, border_radius=20)  # 枠線

    # アップグレードセクションのタイトル
    upgrade_title = title_font.render("アップグレード", True, BLACK)
    screen.blit(
        upgrade_title,
        (
            upgrade_panel.centerx - upgrade_title.get_width() // 2,
            upgrade_panel.top + 20,
        ),
    )

    # アップグレードボタンの位置を調整
    button_spacing = 100  # ボタン間の間隔をさらに増やす（60から100に）
    total_buttons_height = (
        len(upgrade_buttons) * 150 + (len(upgrade_buttons) - 1) * button_spacing
    )
    start_y = upgrade_panel.top + 80

    # アップグレードボタンの描画
    for i, button in enumerate(upgrade_buttons):
        # ボタンの位置を設定
        button.width = 300
        button.height = 150
        button.centerx = upgrade_panel.centerx
        button.top = start_y + i * (button.height + button_spacing)

        upgrade = game_state.upgrades[i]

        # ボタンとその説明をワンセットとして背景を描画
        set_rect = pygame.Rect(
            button.left - 10,
            button.top - 10,
            button.width + 20,
            button.height + 50,  # 説明文のスペースも含める
        )
        pygame.draw.rect(
            screen, (230, 225, 240), set_rect, border_radius=10
        )  # 薄い背景色
        pygame.draw.rect(screen, (130, 100, 170), set_rect, 2, border_radius=10)  # 枠線

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
        name_text = button_font.render(upgrade["name"], True, WHITE)
        cost_text = button_font.render(f"{format_number(upgrade['cost'])}円", True, WHITE)
        count_text = button_font.render(f"所持: {upgrade['count']}", True, WHITE)

        # テキスト位置
        name_rect = name_text.get_rect(midtop=(button.centerx, button.top + 15))
        cost_rect = cost_text.get_rect(center=(button.centerx, button.centery))
        count_rect = count_text.get_rect(midbottom=(button.centerx, button.bottom - 15))

        # テキスト描画
        screen.blit(name_text, name_rect)
        screen.blit(cost_text, cost_rect)
        screen.blit(count_text, count_rect)

        # 説明テキスト
        desc_text = small_font.render(upgrade["description"], True, BLACK)
        desc_rect = desc_text.get_rect(midtop=(button.centerx, button.bottom + 15))
        screen.blit(desc_text, desc_rect)

    # クリックされたボタンに応じて画像を表示（固定位置：購入ボタンの下）
    fixed_img_pos = (buy_button.centerx, buy_button.bottom + 50)

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

        # 労働で得た金額を表示
        earned_text = button_font.render(
            f"+{format_number(game_state.work_unit_price)}円", True, (0, 0, 150)
        )
        text_rect = earned_text.get_rect(
            midtop=(
                fixed_img_pos[0],
                fixed_img_pos[1] + cold_sweat_image.get_height() + 10,
            )
        )
        screen.blit(earned_text, text_rect)
        
        # 効果音を鳴らす代わりに視覚的なフィードバック
        if game_state.work_unit_price >= 1000:
            bonus_text = small_font.render("がんばったね！", True, (200, 0, 100))
            bonus_rect = bonus_text.get_rect(midtop=(fixed_img_pos[0], text_rect.bottom + 5))
            screen.blit(bonus_text, bonus_rect)
