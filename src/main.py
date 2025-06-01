import random
import pygame
import os
import sys
from pygame.locals import *
from ui_components import (
    draw_texts,
    draw_buttons,
    init_particle_manager,
    BACKGROUND_PRIMARY,
    draw_upgrade_status_panel,
)
from game_state import GameState

# 画面設定
WINDOW_WIDTH = 1480  # 画面幅を調整
WINDOW_HEIGHT = 1000  # 画面高さを調整

# 色の定義 (ui_components.pyで定義されているため削除)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

pygame.init()

# 画像の読み込み
# スクリプトと同じディレクトリのパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
yum_path = os.path.join(current_dir, "yum.png")
cold_sweat_path = os.path.join(current_dir, "cold_sweat.png")
yum_image = pygame.image.load(yum_path)
cold_sweat_image = pygame.image.load(cold_sweat_path)


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Steamクリッカー")

    # パーティクルマネージャーを初期化
    init_particle_manager()

    # メインボタンの設定
    # 画面中央の左半分に配置
    main_panel_width = WINDOW_WIDTH // 2 - 80
    main_panel_height = WINDOW_HEIGHT - 300
    main_panel_x = WINDOW_WIDTH // 2 - main_panel_width // 2
    main_panel_y = 260

    work_button_width = 300
    work_button_height = 120
    work_button = pygame.Rect(
        main_panel_x + (main_panel_width - work_button_width) // 2,
        main_panel_y + 50,
        work_button_width,
        work_button_height,
    )

    buy_button_width = 300
    buy_button_height = 120
    buy_button = pygame.Rect(
        main_panel_x + (main_panel_width - buy_button_width) // 2,
        work_button.bottom + 50,
        buy_button_width,
        buy_button_height,
    )

    # リセットボタンの設定 - 右上に小さく配置
    reset_button = pygame.Rect(WINDOW_WIDTH - 120, 40, 80, 30)

    # アップグレードボタンの設定 - 右側に2列で並べる
    upgrade_buttons = []
    game_state = GameState()
    upgrade_panel_width = WINDOW_WIDTH // 2 - 80
    card_width = (upgrade_panel_width - 60) // 2  # 2列表示
    card_height = 150
    margin_top = 30
    margin_left = 30
    card_spacing_x = 20
    card_spacing_y = 20
    upgrade_panel_x = WINDOW_WIDTH // 2 + 40
    upgrade_panel_y = 260

    for i in range(len(game_state.upgrades)):  # アップグレード数に応じて動的に生成
        row = i // 2
        col = i % 2
        x = upgrade_panel_x + margin_left + col * (card_width + card_spacing_x)
        y = upgrade_panel_y + margin_top + row * (card_height + card_spacing_y)
        upgrade_buttons.append(pygame.Rect(x, y, card_width, card_height))

    clock = pygame.time.Clock()
    game_state = GameState()
    game_state.last_auto_update = pygame.time.get_ticks() / 1000  # 初期化
    game_state.last_auto_purchase = pygame.time.get_ticks() / 1000  # 購入自動化の初期化
    game_state.last_pc_income_time = (
        pygame.time.get_ticks() / 1000
    )  # PCからの収入の初期化
    game_state.last_early_access_return = (
        pygame.time.get_ticks() / 1000
    )  # アーリーアクセスの初期化
    game_state.last_game_price_update_time = (
        pygame.time.get_ticks() / 1000
    )  # ゲーム価格変動の初期化

    # デフォルトカーソルと手のカーソルを設定
    default_cursor = pygame.SYSTEM_CURSOR_ARROW
    hand_cursor = pygame.SYSTEM_CURSOR_HAND

    # 変数の初期化
    clicked_button = None
    click_time = 0
    clicked_upgrade = None
    purchased_count = 0  # 購入数を追跡する変数を追加

    # リセットボタンの色はui_components.pyで定義

    # ボタン辞書を初期化
    buttons = {
        "work_button": work_button,
        "buy_button": buy_button,
        "reset_button": reset_button,
        "upgrade_buttons": upgrade_buttons,
        "clicked_button": None,
        "click_time": 0,
        "current_time": 0,
        "clicked_upgrade": None,
        "purchased_count": 0,
    }

    while True:
        current_time = pygame.time.get_ticks() / 1000  # 秒単位の現在時刻
        buttons["current_time"] = current_time

        # 自動クリックの更新
        game_state.update_auto_income(current_time)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                # クリックイベントの処理
                mouse_pos = pygame.mouse.get_pos()

                # 労働ボタンがクリックされた場合
                if buttons["work_button"].collidepoint(mouse_pos):
                    earned = game_state.click_work()
                    buttons["clicked_button"] = "work"
                    buttons["click_time"] = current_time

                # 購入ボタンがクリックされた場合
                if buttons["buy_button"].collidepoint(mouse_pos):
                    purchased_count = game_state.buy_game()
                    if purchased_count > 0:
                        buttons["clicked_button"] = "buy"
                        buttons["click_time"] = current_time
                        buttons["purchased_count"] = purchased_count

                # アップグレードボタンがクリックされた場合
                for i, button in enumerate(buttons["upgrade_buttons"]):
                    if button.collidepoint(mouse_pos):
                        buttons["clicked_button"] = "upgrade"
                        buttons["clicked_upgrade"] = i
                        buttons["click_time"] = current_time

                        # アップグレード購入を試みる
                        success = game_state.buy_upgrade(i)

                # リセットボタンがクリックされた場合
                if buttons["reset_button"].collidepoint(mouse_pos):
                    # .envファイルを再読み込みしてゲームステータスをリセット
                    buttons["clicked_button"] = "reset"
                    buttons["click_time"] = current_time
                    game_state = (
                        GameState()
                    )  # これで.envファイルから最新の設定を読み込む
                    game_state.last_auto_update = current_time
                    game_state.last_auto_purchase = current_time
                    game_state.last_pc_income_time = current_time
                    game_state.last_early_access_return = current_time
                    clicked_button = "reset"
                    clicked_upgrade = None  # クリックされたアップグレードをリセット
                    click_time = current_time

        # マウスカーソルの位置を取得
        mouse_pos = pygame.mouse.get_pos()

        # カーソル状態のキャッシュを追加して、不要なカーソル変更を防止
        if (
            work_button.collidepoint(mouse_pos)
            or buy_button.collidepoint(mouse_pos)
            or any(button.collidepoint(mouse_pos) for button in upgrade_buttons)
            or reset_button.collidepoint(mouse_pos)
        ):
            if pygame.mouse.get_cursor() != hand_cursor:
                pygame.mouse.set_cursor(hand_cursor)  # 手のカーソルに変更
        else:
            if pygame.mouse.get_cursor() != default_cursor:
                pygame.mouse.set_cursor(default_cursor)  # デフォルトカーソルに戻す

        # 画面の描画
        screen.fill(BACKGROUND_PRIMARY)

        # ボタン情報を辞書にまとめて引数を整理
        buttons = {
            "work_button": work_button,
            "buy_button": buy_button,
            "upgrade_buttons": upgrade_buttons,
            "reset_button": reset_button,
            "clicked_button": clicked_button,
            "clicked_upgrade": clicked_upgrade,
            "click_time": click_time,
            "current_time": current_time,
        }

        # 購入数情報を追加（購入ボタンがクリックされた場合のみ）
        if (
            clicked_button == "buy" and current_time - click_time < 0.4
        ):  # アニメーション中のみ
            buttons["purchased_count"] = purchased_count  # 購入数を記録

        # 画面の描画 (背景は既に描画済み)
        draw_texts(screen, game_state)  # draw_stats_cardsを呼び出す
        draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image)
        draw_upgrade_status_panel(
            screen, game_state
        )  # アップグレード情報表示パネルを追加

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
