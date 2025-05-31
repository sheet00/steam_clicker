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
button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 20)
title_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 35)
large_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
small_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 16)  # アップグレード説明用
upgrade_font = pygame.font.Font(
    "C:/Windows/Fonts/meiryo.ttc", 18
)  # アップグレード名と価格用


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


def format_japanese_currency(number):
    """数値を日本円の単位（万、億、兆など）でフォーマットする関数"""
    if number < 10000:  # 1万未満
        return f"{number:,}円"

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
        if number >= value:
            formatted_number = number / value
            if formatted_number == int(formatted_number):
                return f"{int(formatted_number):,}{unit_name}円"
            else:
                return f"{formatted_number:.1f}{unit_name}円".replace(
                    f".0{unit_name}", unit_name
                )

    return f"{number:,}円"  # 念のためのフォールバック


def format_purchase_power(purchase_power):
    """購入力を適切にフォーマットする関数"""
    if purchase_power == int(purchase_power):
        return format_number(int(purchase_power))
    else:
        return f"{purchase_power:.1f}".replace(".0", "")


def draw_info_panel(screen, game_state):
    """情報パネルを描画する関数"""
    screen_width = screen.get_width()
    info_panel = pygame.Rect(40, 40, screen_width - 80, 180)
    pygame.draw.rect(screen, LIGHT_GRAY, info_panel, border_radius=15)
    pygame.draw.rect(screen, BLACK, info_panel, 3, border_radius=15)

    # 情報パネルの幅を計算
    panel_width = info_panel.width - 40

    # 基本情報の表示
    draw_basic_info(screen, game_state, info_panel)

    # 自動化情報の表示
    draw_automation_info(screen, game_state, info_panel)

    # 収益情報の表示
    draw_income_info(screen, game_state, info_panel)


def draw_basic_info(screen, game_state, info_panel):
    """基本的な情報（お金、積みゲー、賃金、購入力）を表示する関数"""
    # お金の表示
    money_text = f"総資産: {format_japanese_currency(game_state.money)}"
    money_surface = font.render(money_text, True, BLACK)
    screen.blit(money_surface, (60, 40))  # 左マージンを40から60に増やした

    # 積みゲーの表示
    stock_text = f"積みゲー: {format_number(game_state.stock)}個"
    stock_surface = font.render(stock_text, True, BLACK)
    stock_x = info_panel.right - stock_surface.get_width() - 40
    screen.blit(stock_surface, (stock_x, 40))

    # 賃金の表示（ボーナス込み）
    efficiency_bonus = 1.0
    if game_state.gaming_pc_level > 0:
        efficiency_bonus = 1.0 + (
            game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus
        )

    actual_wage = int(game_state.work_unit_price * efficiency_bonus)

    if game_state.gaming_pc_level > 0:
        text = f"賃金: {format_japanese_currency(actual_wage)} (ボーナス: +{int((efficiency_bonus-1)*100)}%)"
    else:
        text = f"賃金: {format_japanese_currency(game_state.work_unit_price)}"

    work_price_surface = button_font.render(text, True, BLACK)
    screen.blit(work_price_surface, (60, 90))  # 左マージンを40から60に増やした

    # 購入力の表示
    power_text = format_purchase_power(game_state.purchase_power)
    text = f"購入力: {power_text}個/回"
    purchase_power_surface = button_font.render(text, True, BLACK)
    purchase_x = info_panel.centerx - purchase_power_surface.get_width() // 2
    screen.blit(purchase_power_surface, (purchase_x, 90))


def draw_automation_info(screen, game_state, info_panel):
    """自動化関連の情報（自動クリック、自動購入）を表示する関数"""
    # 自動クリックの表示
    if game_state.auto_clicks > 0:
        text = f"自動クリック: {format_number(game_state.auto_clicks)}回/秒"
        auto_clicks_surface = button_font.render(text, True, (0, 100, 0))
        auto_x = info_panel.right - auto_clicks_surface.get_width() - 40
        screen.blit(auto_clicks_surface, (auto_x, 90))

    # 自動購入の表示
    if game_state.auto_purchases > 0:
        # ゲーミングPCのレベルに応じて自動購入間隔を短縮
        auto_purchase_interval = game_state.auto_purchase_interval
        if game_state.gaming_pc_level > 0:
            reduction_percent = (
                game_state.gaming_pc_level * game_state.gaming_pc_interval_reduction
            )
            auto_purchase_interval *= max(0.01, 1.0 - reduction_percent)

        text = f"自動購入: {format_number(game_state.auto_purchases)}回/{auto_purchase_interval:.2f}秒"
        auto_purchase_surface = button_font.render(text, True, (100, 0, 100))

        # 表示位置の決定
        auto_purchase_x = info_panel.right - auto_purchase_surface.get_width() - 40
        auto_purchase_y = 120 if game_state.auto_clicks > 0 else 90
        screen.blit(auto_purchase_surface, (auto_purchase_x, auto_purchase_y))


def draw_income_info(screen, game_state, info_panel):
    """収益関連の情報（ゲーミングPC、アーリーアクセス）を表示する関数"""
    # ゲーミングPCからの収入表示
    if game_state.gaming_pc_level > 0:
        income_per_sec = (
            game_state.stock
            * game_state.gaming_pc_level
            * game_state.gaming_pc_income_per_game
        )
        text = f"配信収益: {format_japanese_currency(income_per_sec)}/秒"
        pc_income_surface = button_font.render(text, True, (0, 0, 150))

        # 表示位置の決定
        pc_income_x = info_panel.right - pc_income_surface.get_width() - 40

        if game_state.auto_clicks > 0 and game_state.auto_purchases > 0:
            pc_income_y = 150
        elif game_state.auto_clicks > 0 or game_state.auto_purchases > 0:
            pc_income_y = 120
        else:
            pc_income_y = 90

        screen.blit(pc_income_surface, (pc_income_x, pc_income_y))

    # アーリーアクセスからの収入表示
    if game_state.early_access_level > 0:
        # 基本の最大収益率
        max_return_percent = round(
            game_state.early_access_level * game_state.early_access_return_percent, 2
        )

        # ゲーム数によるボーナス（UI表示用に計算）
        game_bonus_percent = round((game_state.stock / 100) * 0.1, 2)
        total_max_percent = max_return_percent + game_bonus_percent

        # 最後の結果に基づいて色と表示内容を決定
        if game_state.last_early_access_result != 0:
            if game_state.last_early_access_is_negative:
                result_color = (200, 0, 0)  # 赤色（損失）
                result_text = f" 前回: -{format_japanese_currency(abs(game_state.last_early_access_result))} ({abs(game_state.last_early_access_actual_percent):.2f}%)"
            else:
                result_color = (0, 150, 0)  # 緑色（利益）
                result_text = f" 前回: +{format_japanese_currency(game_state.last_early_access_result)} ({game_state.last_early_access_actual_percent:.2f}%)"
        else:
            # 初回はまだ結果がない
            result_color = (100, 100, 100)
            result_text = " まだ収益が発生していません"

        # 基本の収益率表示
        expected_max = int(
            game_state.total_early_access_investment * (total_max_percent / 100)
        )

        # ゲームボーナスがある場合は表示に追加
        if game_bonus_percent > 0:
            bonus_text = f" +ゲームボーナス{game_bonus_percent:.2f}%"
            base_text = f"アーリーアクセス: 最大{format_japanese_currency(expected_max)}/{game_state.early_access_interval}秒 (0～{max_return_percent:.2f}%{bonus_text})"
        else:
            base_text = f"アーリーアクセス: 最大{format_japanese_currency(expected_max)}/{game_state.early_access_interval}秒 (0～{max_return_percent:.2f}%)"

        # 基本情報の表示
        early_access_surface = button_font.render(base_text, True, (150, 100, 0))

        # 結果テキストを表示（別の Surface に）
        result_surface = button_font.render(result_text, True, result_color)

        # 投資額も表示
        investment_text = f"総投資額: {format_japanese_currency(game_state.total_early_access_investment)}"
        investment_surface = button_font.render(investment_text, True, (150, 100, 0))

        # 表示位置
        early_access_x = 60
        early_access_y = 150

        # まず基本情報を表示
        screen.blit(early_access_surface, (early_access_x, early_access_y))

        # 結果テキストを基本情報の右側に表示
        result_x = early_access_x + early_access_surface.get_width()
        screen.blit(result_surface, (result_x, early_access_y))

        # 投資額は2行目に表示
        screen.blit(investment_surface, (early_access_x, early_access_y + 30))


def draw_main_buttons(screen, game_state, buttons, current_time, click_time):
    """メインボタン（労働、購入）を描画する関数"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    animation_duration = 0.4

    clicked_button = buttons.get("clicked_button")
    work_button = buttons.get("work_button")
    buy_button = buttons.get("buy_button")

    # ボタンパネルの描画
    button_panel = pygame.Rect(40, 260, screen_width // 2 - 60, screen_height - 300)
    pygame.draw.rect(screen, (230, 240, 250), button_panel, border_radius=15)
    pygame.draw.rect(screen, (100, 120, 150), button_panel, 3, border_radius=15)

    # ボタンの位置設定
    work_button.width = 300
    work_button.height = 120
    work_button.centerx = button_panel.centerx
    work_button.top = button_panel.top + 50

    buy_button.width = 300
    buy_button.height = 120
    buy_button.centerx = button_panel.centerx
    buy_button.top = work_button.bottom + 50

    # ボタンの色設定
    work_color = (
        DARK_BLUE
        if clicked_button == "work" and current_time - click_time < animation_duration
        else BLUE
    )
    buy_color = (
        DARK_GREEN
        if clicked_button == "buy" and current_time - click_time < animation_duration
        else GREEN
    )

    # ボタンの描画
    pygame.draw.rect(screen, work_color, work_button, border_radius=15)
    pygame.draw.rect(screen, buy_color, buy_button, border_radius=15)

    # ボタンテキストの描画
    work_text = large_font.render("労働", True, WHITE)
    buy_text = large_font.render("ゲーム購入", True, WHITE)

    work_text_rect = work_text.get_rect(center=work_button.center)
    buy_text_rect = buy_text.get_rect(center=buy_button.center)

    screen.blit(work_text, work_text_rect)
    screen.blit(buy_text, buy_text_rect)

    # ゲーム価格の表示
    game_price_surface = button_font.render(
        f"価格: {format_japanese_currency(int(game_state.game_price))}", True, BLACK
    )
    price_info_pos = (
        buy_button.centerx - game_price_surface.get_width() // 2,
        buy_button.bottom + 10,
    )
    screen.blit(game_price_surface, price_info_pos)


def draw_upgrade_panel(screen, game_state, buttons, current_time, click_time):
    """アップグレードパネルとボタンを描画する関数"""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    animation_duration = 0.4

    clicked_upgrade = buttons.get("clicked_upgrade")
    upgrade_buttons = buttons.get("upgrade_buttons", [])

    # アップグレードパネルの描画
    upgrade_panel = pygame.Rect(
        screen_width // 2 + 40,
        260,
        screen_width // 2 - 80,
        screen_height - 300,
    )
    pygame.draw.rect(screen, (245, 240, 250), upgrade_panel, border_radius=20)
    pygame.draw.rect(screen, (100, 50, 150), upgrade_panel, 3, border_radius=20)

    # アップグレードボタンの配置設定
    margin_top = 40
    button_spacing = 70
    start_y = upgrade_panel.top + margin_top

    # 各アップグレードボタンの描画
    for i, button in enumerate(upgrade_buttons):
        draw_single_upgrade_button(
            screen,
            game_state,
            button,
            i,
            upgrade_panel,
            start_y,
            button_spacing,
            clicked_upgrade,
            current_time,
            click_time,
        )


def draw_single_upgrade_button(
    screen,
    game_state,
    button,
    index,
    panel,
    start_y,
    spacing,
    clicked_upgrade,
    current_time,
    click_time,
):
    """単一のアップグレードボタンを描画する関数"""
    animation_duration = 0.4
    upgrade = game_state.upgrades[index]

    # ボタンの位置とサイズを設定
    button.width = 600
    button.height = 90
    button.centerx = panel.centerx
    button.top = start_y + index * (button.height + spacing)

    # ボタンセットの背景を描画
    set_rect = pygame.Rect(
        button.left - 30,
        button.top - 25,
        button.width + 60,
        button.height + 70,
    )
    pygame.draw.rect(screen, (230, 225, 240), set_rect, border_radius=15)
    pygame.draw.rect(screen, (130, 100, 170), set_rect, 3, border_radius=15)

    # ボタンの色を決定
    if clicked_upgrade == index and current_time - click_time < animation_duration:
        color = DARK_PURPLE
    else:
        color = PURPLE

    # お金が足りない場合は暗く表示
    if game_state.money < upgrade["cost"]:
        color = (color[0] // 2, color[1] // 2, color[2] // 2)

    # ボタンを描画
    pygame.draw.rect(screen, color, button, border_radius=15)

    # ボタンテキストを準備
    name_text = upgrade_font.render(upgrade["name"], True, WHITE)
    cost_text = upgrade_font.render(
        f"{format_japanese_currency(upgrade['cost'])}", True, WHITE
    )

    # 所持数/レベルテキストを準備
    if index == 4:  # ゲーミングPC
        if game_state.gaming_pc_level > 0:
            count_text = upgrade_font.render(
                f"Lv.{game_state.gaming_pc_level}", True, WHITE
            )
        else:
            count_text = upgrade_font.render("未所持", True, WHITE)
    else:
        count_text = upgrade_font.render(f"所持: {upgrade['count']}", True, WHITE)

    # アイコンを表示
    if index < len(upgrade_icons):
        icon = upgrade_icons[index]
        icon_x = button.left + 20
        icon_y = button.centery - icon.get_height() // 2
        screen.blit(icon, (icon_x, icon_y))

    # テキスト位置を設定
    name_rect = name_text.get_rect(midtop=(button.centerx, button.top + 10))
    cost_rect = cost_text.get_rect(center=(button.centerx, button.centery))
    count_rect = count_text.get_rect(midbottom=(button.centerx, button.bottom - 10))

    # テキストを描画
    screen.blit(name_text, name_rect)
    screen.blit(cost_text, cost_rect)
    screen.blit(count_text, count_rect)

    # 説明テキストを描画
    desc_text = small_font.render(upgrade["description"], True, BLACK)
    desc_rect = desc_text.get_rect(center=(button.centerx, button.bottom + 30))
    screen.blit(desc_text, desc_rect)


def draw_click_feedback(screen, game_state, buttons, yum_image, cold_sweat_image):
    """クリック時のフィードバック（画像、テキスト）を描画する関数"""
    animation_duration = 0.4
    clicked_button = buttons.get("clicked_button")
    clicked_upgrade = buttons.get("clicked_upgrade")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time")
    buy_button = buttons.get("buy_button")

    # クリックされていない場合は何もしない
    if current_time - click_time >= animation_duration:
        return

    # 画像表示位置
    fixed_img_pos = (buy_button.centerx, buy_button.bottom + 50)

    # 購入ボタンがクリックされた場合
    if clicked_button == "buy":
        draw_buy_feedback(screen, game_state, fixed_img_pos, yum_image)

    # 労働ボタンがクリックされた場合
    elif clicked_button == "work":
        draw_work_feedback(screen, game_state, fixed_img_pos, cold_sweat_image)

    # アップグレードボタンがクリックされた場合
    elif clicked_upgrade is not None:
        draw_upgrade_feedback(screen, game_state, fixed_img_pos, clicked_upgrade)


def draw_buy_feedback(screen, game_state, position, yum_image):
    """購入時のフィードバックを描画する関数"""
    # 画像を表示
    image_rect = yum_image.get_rect(midtop=position)
    screen.blit(yum_image, image_rect)

    # 購入成功メッセージを表示
    power_text = format_purchase_power(game_state.purchase_power)
    success_text = button_font.render(f"{power_text}個ゲットだよ！", True, (0, 150, 0))
    text_rect = success_text.get_rect(
        midtop=(position[0], position[1] + yum_image.get_height() + 10)
    )
    screen.blit(success_text, text_rect)


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
    earned_text = button_font.render(
        f"+{format_japanese_currency(earned)}", True, (0, 0, 150)
    )
    text_rect = earned_text.get_rect(
        midtop=(position[0], position[1] + cold_sweat_image.get_height() + 10)
    )
    screen.blit(earned_text, text_rect)

    # 高額報酬時の追加メッセージ
    if earned >= 1000:
        bonus_text = small_font.render("がんばったね！", True, (200, 0, 100))
        bonus_rect = bonus_text.get_rect(midtop=(position[0], text_rect.bottom + 5))
        screen.blit(bonus_text, bonus_rect)


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

    upgrade_text = button_font.render(message, True, (150, 0, 150))
    upgrade_rect = upgrade_text.get_rect(midtop=(position[0], position[1] + 10))
    screen.blit(upgrade_text, upgrade_rect)


def draw_texts(screen, game_state):
    """画面上のテキスト要素をすべて描画する関数"""
    draw_info_panel(screen, game_state)


def draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image):
    """画面上のボタン要素をすべて描画する関数"""
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time", 0)

    # メインボタン（労働、購入）を描画
    draw_main_buttons(screen, game_state, buttons, current_time, click_time)

    # アップグレードパネルとボタンを描画
    draw_upgrade_panel(screen, game_state, buttons, current_time, click_time)

    # クリック時のフィードバックを描画
    draw_click_feedback(screen, game_state, buttons, yum_image, cold_sweat_image)
