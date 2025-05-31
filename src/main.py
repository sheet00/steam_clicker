import pygame
import os
import sys
from pygame.locals import *

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 180)  # クリック時の色
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)  # クリック時の色


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


# GameStateクラスの重複を削除し、1つに統合しました
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


def draw_texts(screen, game_state):
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


def draw_buttons(screen, game_state, buttons):
    # クリックアニメーションの持続時間（秒）
    animation_duration = 0.4

    clicked_button = buttons.get("clicked_button")
    current_time = buttons.get("current_time")
    click_time = buttons.get("click_time")
    work_button = buttons.get("work_button")
    buy_button = buttons.get("buy_button")

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

        draw_texts(screen, game_state)
        draw_buttons(screen, game_state, buttons)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
