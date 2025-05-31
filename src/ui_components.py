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
button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 24)
title_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 48)
large_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 40)
small_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 18)


def draw_texts(screen, game_state):
    """テキストを描画する関数"""
    # 情報パネルの背景
    info_panel = pygame.Rect(20, 20, 400, 250)
    pygame.draw.rect(screen, LIGHT_GRAY, info_panel, border_radius=15)
    pygame.draw.rect(screen, BLACK, info_panel, 2, border_radius=15)  # 枠線

    # タイトル
    title_surface = title_font.render("Steamクリッカー", True, BLACK)
    screen.blit(
        title_surface, (info_panel.centerx - title_surface.get_width() // 2, 30)
    )

    # 画面左上
    # お金の表示
    money_surface = font.render(f"お金: {game_state.money}円", True, BLACK)
    screen.blit(money_surface, (40, 80))

    # 積みゲーの表示
    stock_surface = font.render(f"積みゲー: {game_state.stock}個", True, BLACK)
    screen.blit(stock_surface, (40, 130))

    # 労働単価のテキスト
    text = f"労働時給: {game_state.work_unit_price}円"
    work_price_surface = button_font.render(text, True, BLACK)
    screen.blit(work_price_surface, (40, 180))

    # 購入力のテキスト
    text = f"購入力: {game_state.purchase_power}個/回"
    purchase_power_surface = button_font.render(text, True, BLACK)
    screen.blit(purchase_power_surface, (40, 220))

    # 自動収入のテキスト
    if game_state.auto_income > 0:
        # 自動収入パネル
        auto_panel = pygame.Rect(20, 290, 400, 60)
        pygame.draw.rect(screen, (220, 255, 220), auto_panel, border_radius=10)
        pygame.draw.rect(screen, (0, 100, 0), auto_panel, 2, border_radius=10)  # 枠線

        text = f"自動収入: {game_state.auto_income}円/秒"
        auto_income_surface = button_font.render(text, True, (0, 100, 0))
        screen.blit(auto_income_surface, (40, 310))


def draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image):
    # クリックアニメーションの持続時間（秒）
    animation_duration = 0.4

    clicked_button = buttons.get("clicked_button")
    clicked_upgrade = buttons.get("clicked_upgrade")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time")
    work_button = buttons.get("work_button")
    buy_button = buttons.get("buy_button")
    upgrade_buttons = buttons.get("upgrade_buttons", [])

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

    # アップグレードセクションのタイトル
    upgrade_title = title_font.render("アップグレード", True, BLACK)
    screen.blit(upgrade_title, (upgrade_buttons[0].left, upgrade_buttons[0].top - 50))

    # アップグレードボタンの描画
    for i, button in enumerate(upgrade_buttons):
        upgrade = game_state.upgrades[i]

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
        cost_text = button_font.render(f"{upgrade['cost']}円", True, WHITE)
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
        desc_rect = desc_text.get_rect(midtop=(button.centerx, button.bottom + 5))
        screen.blit(desc_text, desc_rect)

    # クリックされたボタンに応じて画像を中央に表示
    img_pos = (buy_button.centerx, buy_button.bottom + 50)
    if clicked_button == "buy" and current_time - click_time < animation_duration:
        image_rect = yum_image.get_rect(midtop=img_pos)
        screen.blit(yum_image, image_rect)

    elif clicked_button == "work" and current_time - click_time < animation_duration:
        image_rect = cold_sweat_image.get_rect(midtop=img_pos)
        screen.blit(cold_sweat_image, image_rect)

    # ゲーム価格のテキスト
    game_price_surface = button_font.render(
        f"価格: {game_state.game_price}円", True, BLACK
    )
    price_info_pos = (
        buy_button.centerx - game_price_surface.get_width() // 2,
        buy_button.bottom + 10,
    )
    screen.blit(game_price_surface, price_info_pos)
