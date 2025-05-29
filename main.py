import pygame
import sys
from pygame.locals import *


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


def draw_buttons(screen, work_button, buy_button, BLUE, DARK_BLUE, GREEN, DARK_GREEN, 
                work_button_clicked, buy_button_clicked, work_click_counter, buy_click_counter):
    """ボタンを描画する関数"""
    
    # ボタンのクリックアニメーション処理
    if work_button_clicked:
        work_click_counter -= 1
        if work_click_counter <= 0:
            work_button_clicked = False

    if buy_button_clicked:
        buy_click_counter -= 1
        if buy_click_counter <= 0:
            buy_button_clicked = False

    # 労働ボタンの描画
    work_btn_color = DARK_BLUE if work_button_clicked else BLUE
    work_btn_rect = work_button.copy()
    if work_button_clicked:
        shrink = 4
        work_btn_rect.inflate_ip(-shrink, -shrink)
        work_btn_rect.move_ip(shrink // 2, shrink // 2)
    pygame.draw.rect(screen, work_btn_color, work_btn_rect, border_radius=10)
    
    # 購入ボタンの描画
    buy_btn_color = DARK_GREEN if buy_button_clicked else GREEN
    buy_btn_rect = buy_button.copy()
    if buy_button_clicked:
        shrink = 4
        buy_btn_rect.inflate_ip(-shrink, -shrink)
        buy_btn_rect.move_ip(shrink // 2, shrink // 2)
    pygame.draw.rect(screen, buy_btn_color, buy_btn_rect, border_radius=10)

    # テキスト情報の位置を設定
    work_info_pos = (work_button.x, work_button.y + work_button.height + 5)
    price_info_pos = (buy_button.x, buy_button.y + buy_button.height + 5)
    
    return work_click_counter, buy_click_counter, work_btn_rect, buy_btn_rect, work_info_pos, price_info_pos


def draw_texts(screen, font, button_font, game_state, BLACK, WHITE, work_btn_rect, buy_btn_rect, work_info_pos, price_info_pos):
    """テキストを描画する関数"""
    # お金の表示
    money_surface = font.render(f"お金: {game_state.money}円", True, BLACK)
    screen.blit(money_surface, (10, 10))
    
    # 積みゲーの表示
    stock_surface = font.render(f"積みゲー: {game_state.stock}個", True, BLACK)
    screen.blit(stock_surface, (10, 50))
    
    # 労働ボタンのテキスト
    work_surface = button_font.render("労働", True, WHITE)
    work_rect = work_surface.get_rect(center=work_btn_rect.center)
    screen.blit(work_surface, work_rect)
    
    # 労働単価のテキスト
    work_price_surface = button_font.render(f"{game_state.work_unit_price}円", True, BLACK)
    screen.blit(work_price_surface, work_info_pos)
    
    # 購入ボタンのテキスト
    buy_surface = button_font.render("購入", True, WHITE)
    buy_rect = buy_surface.get_rect(center=buy_btn_rect.center)
    screen.blit(buy_surface, buy_rect)
    
    # ゲーム価格のテキスト
    game_price_surface = button_font.render(f"{game_state.game_price}円", True, BLACK)
    screen.blit(game_price_surface, price_info_pos)


def main():
    pygame.init()

    # 画面設定
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Steamクリッカー")

    # 色の定義
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 180)  # クリック時の色
    GREEN = (0, 200, 0)
    DARK_GREEN = (0, 150, 0)  # クリック時の色

    # 日本語対応フォントを指定
    font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)  # メイリオ
    button_font = pygame.font.Font(
        "C:/Windows/Fonts/meiryo.ttc", 24
    )  # ボタン用フォント

    # ボタンの設定
    work_button = pygame.Rect(300, 200, 200, 80)
    buy_button = pygame.Rect(300, 300, 200, 80)

    # クリックアニメーション用の変数
    work_button_clicked = False
    buy_button_clicked = False
    click_animation_frames = 10
    work_click_counter = 0
    buy_click_counter = 0
    
    # 描画関数で使用する変数を初期化
    work_btn_rect = None
    buy_btn_rect = None
    work_info_pos = None
    price_info_pos = None

    clock = pygame.time.Clock()
    game_state = GameState()

    # デフォルトカーソルと手のカーソルを設定
    default_cursor = pygame.SYSTEM_CURSOR_ARROW
    hand_cursor = pygame.SYSTEM_CURSOR_HAND

    while True:
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
                    work_button_clicked = True
                    work_click_counter = click_animation_frames

                # 購入ボタンがクリックされた場合
                if buy_button.collidepoint(mouse_pos):
                    game_state.buy_game()
                    buy_button_clicked = True
                    buy_click_counter = click_animation_frames

        # マウスカーソルの位置を取得
        mouse_pos = pygame.mouse.get_pos()

        # ボタンの上にカーソルがあるかチェック
        if work_button.collidepoint(mouse_pos) or buy_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)  # 手のカーソルに変更
        else:
            pygame.mouse.set_cursor(default_cursor)  # デフォルトカーソルに戻す

        # 画面の描画
        screen.fill(WHITE)
        
        # ボタンとテキストの描画
        work_click_counter, buy_click_counter, work_btn_rect, buy_btn_rect, work_info_pos, price_info_pos = draw_buttons(
            screen, work_button, buy_button, BLUE, DARK_BLUE, GREEN, DARK_GREEN, 
            work_button_clicked, buy_button_clicked, work_click_counter, buy_click_counter
        )
        
        draw_texts(
            screen, font, button_font, game_state, BLACK, WHITE, work_btn_rect, buy_btn_rect,
            work_info_pos, price_info_pos
        )

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
