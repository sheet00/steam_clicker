import pygame
import os
import sys
from pygame.locals import *
from ui_components import draw_texts, draw_buttons

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
# 日本語対応フォントを指定
font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)  # メイリオ
button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 24)  # ボタン用フォント

# 画像の読み込み
# スクリプトと同じディレクトリのパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
yum_path = os.path.join(current_dir, "yum.png")
cold_sweat_path = os.path.join(current_dir, "cold_sweat.png")
yum_image = pygame.image.load(yum_path)
cold_sweat_image = pygame.image.load(cold_sweat_path)


class GameState:
    def __init__(self):
        self.money = 0
        self.stock = 0
        self.work_unit_price = 100
        self.auto_work_unit_price = 0
        self.purchase_power = 1
        self.game_price = 100  # ゲームの価格を定数として保持

    def click_work(self):
        self.money += self.work_unit_price

    def buy_game(self):
        if self.money >= self.game_price:
            self.money -= self.game_price
            self.stock += self.purchase_power


def main():

    # 画面設定
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Steamクリッカー")

    # ボタンの設定
    work_button = pygame.Rect(300, 200, 200, 80)
    buy_button = pygame.Rect(300, 300, 200, 80)

    clock = pygame.time.Clock()
    game_state = GameState()

    # デフォルトカーソルと手のカーソルを設定
    default_cursor = pygame.SYSTEM_CURSOR_ARROW
    hand_cursor = pygame.SYSTEM_CURSOR_HAND

    clicked_button = None
    click_time = 0

    while True:
        current_time = pygame.time.get_ticks() / 1000  # 秒単位の現在時刻
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                # クリックイベントの処理
                mouse_pos = pygame.mouse.get_pos()

                # 労働ボタンがクリックされた場合
                if work_button.collidepoint(mouse_pos):
                    game_state.click_work()
                    clicked_button = "work"
                    click_time = current_time

                # 購入ボタンがクリックされた場合
                if buy_button.collidepoint(mouse_pos):
                    game_state.buy_game()
                    clicked_button = "buy"
                    click_time = current_time

        # マウスカーソルの位置を取得
        mouse_pos = pygame.mouse.get_pos()

        # カーソル状態のキャッシュを追加して、不要なカーソル変更を防止
        if work_button.collidepoint(mouse_pos) or buy_button.collidepoint(mouse_pos):
            if pygame.mouse.get_cursor() != hand_cursor:
                pygame.mouse.set_cursor(hand_cursor)  # 手のカーソルに変更
        else:
            if pygame.mouse.get_cursor() != default_cursor:
                pygame.mouse.set_cursor(default_cursor)  # デフォルトカーソルに戻す

        # 画面の描画
        screen.fill(WHITE)

        # ボタン情報を辞書にまとめて引数を整理
        buttons = {
            "work_button": work_button,
            "buy_button": buy_button,
            "clicked_button": clicked_button,
            "click_time": click_time,
            "current_time": current_time,
        }

        # 修正: フォントと画像を引数として渡す
        draw_texts(screen, game_state, font, button_font)
        draw_buttons(screen, game_state, buttons, button_font, yum_image, cold_sweat_image)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
