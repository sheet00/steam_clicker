import pygame

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 180)  # クリック時の色
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)  # クリック時の色

# フォントの初期化はmain.pyで行い、ここでは引数として受け取る

def draw_texts(screen, game_state, font, button_font):
    """テキストを描画する関数"""
    # 画面左上
    # お金の表示
    money_surface = font.render(f"お金: {game_state.money}円", True, BLACK)
    screen.blit(money_surface, (10, 10))

    # 積みゲーの表示
    stock_surface = font.render(f"積みゲー: {game_state.stock}個", True, BLACK)
    screen.blit(stock_surface, (10, 50))

    # 労働単価のテキスト（背景付きで見やすく表示）
    text = f"労働時給: {game_state.work_unit_price}円"
    work_price_surface = button_font.render(text, True, BLACK)
    # テキストの背景用の矩形を作成（少し余白をつける）
    bg_rect = work_price_surface.get_rect(topleft=(10, 120))
    bg_rect.inflate_ip(10, 6)  # 横に10px、縦に6px余白を追加
    # 薄いグレーの背景を描画
    pygame.draw.rect(screen, (220, 220, 220), bg_rect)
    # テキストを描画
    screen.blit(work_price_surface, (15, 123))  # 背景の内側に少しずらして描画
    
    # 購入力のテキスト
    text = f"購入力: {game_state.purchase_power}個/回"
    purchase_power_surface = button_font.render(text, True, BLACK)
    bg_rect = purchase_power_surface.get_rect(topleft=(10, 160))
    bg_rect.inflate_ip(10, 6)
    pygame.draw.rect(screen, (220, 220, 220), bg_rect)
    screen.blit(purchase_power_surface, (15, 163))
    
    # 自動収入のテキスト
    if game_state.auto_income > 0:
        text = f"自動収入: {game_state.auto_income}円/秒"
        auto_income_surface = button_font.render(text, True, BLACK)
        bg_rect = auto_income_surface.get_rect(topleft=(10, 200))
        bg_rect.inflate_ip(10, 6)
        pygame.draw.rect(screen, (220, 220, 220), bg_rect)
        screen.blit(auto_income_surface, (15, 203))


def draw_buttons(screen, game_state, buttons, button_font, yum_image, cold_sweat_image):
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
    pygame.draw.rect(screen, work_color, work_button, border_radius=10)
    pygame.draw.rect(screen, buy_color, buy_button, border_radius=10)

    # ボタンテキストを描画
    work_text = button_font.render("労働", True, WHITE)
    buy_text = button_font.render("ゲーム購入", True, WHITE)

    work_text_rect = work_text.get_rect(center=work_button.center)
    buy_text_rect = buy_text.get_rect(center=buy_button.center)

    screen.blit(work_text, work_text_rect)
    screen.blit(buy_text, buy_text_rect)
    
    # アップグレードボタンの描画
    PURPLE = (150, 50, 200)
    DARK_PURPLE = (100, 30, 150)
    
    for i, button in enumerate(upgrade_buttons):
        upgrade = game_state.upgrades[i]
        
        # ボタンの色（クリック時は暗く）
        if clicked_upgrade == i and current_time - click_time < animation_duration:
            color = DARK_PURPLE
        else:
            color = PURPLE
            
        # お金が足りない場合は暗く表示
        if game_state.money < upgrade["cost"]:
            color = (color[0]//2, color[1]//2, color[2]//2)
            
        # ボタンを描画
        pygame.draw.rect(screen, color, button, border_radius=10)
        
        # ボタンテキスト
        name_text = button_font.render(upgrade["name"], True, WHITE)
        cost_text = button_font.render(f"{upgrade['cost']}円", True, WHITE)
        count_text = button_font.render(f"所持: {upgrade['count']}", True, WHITE)
        
        # テキスト位置
        name_rect = name_text.get_rect(midtop=(button.centerx, button.top + 5))
        cost_rect = cost_text.get_rect(center=(button.centerx, button.centery))
        count_rect = count_text.get_rect(midbottom=(button.centerx, button.bottom - 5))
        
        # テキスト描画
        screen.blit(name_text, name_rect)
        screen.blit(cost_text, cost_rect)
        screen.blit(count_text, count_rect)
        
        # 説明テキスト
        # OSに応じてフォントを設定
        try:
            # Windowsの場合
            small_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 16)
        except:
            # Windowsでない場合はデフォルトフォントを使用
            small_font = pygame.font.SysFont(None, 16)
            
        desc_text = small_font.render(upgrade["description"], True, BLACK)
        desc_rect = desc_text.get_rect(midtop=(button.centerx, button.bottom + 5))
        screen.blit(desc_text, desc_rect)

    # クリックされたボタンに応じて画像を中央に表示
    img_pos = (buy_button.centerx, buy_button.bottom + 10)
    if clicked_button == "buy" and current_time - click_time < animation_duration:
        image_rect = yum_image.get_rect(midtop=img_pos)
        screen.blit(yum_image, image_rect)

    elif clicked_button == "work" and current_time - click_time < animation_duration:
        image_rect = cold_sweat_image.get_rect(midtop=img_pos)
        screen.blit(cold_sweat_image, image_rect)

    # ゲーム価格のテキスト
    game_price_surface = button_font.render(f"{game_state.game_price}円", True, BLACK)
    price_info_pos = (
        buy_button.right + 10,
        buy_button.centery - game_price_surface.get_height() // 2,
    )
    screen.blit(game_price_surface, price_info_pos)
