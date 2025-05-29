import pygame
import sys
from pygame.locals import *


class GameState:
    def __init__(self):
        self.money = 0
        self.games = 0
        self.click_power = 1
        self.auto_click_power = 0
        self.purchase_power = 1

    def click_work(self):
        self.money += self.click_power

    def buy_game(self):
        if self.money >= 100:  # 仮の価格
            self.money -= 100
            self.games += self.purchase_power


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

    # 日本語対応フォントを指定
    font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)  # メイリオ

    clock = pygame.time.Clock()
    game_state = GameState()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                # クリックイベントの処理
                mouse_pos = pygame.mouse.get_pos()
                # ボタンの位置判定とアクション実行

        # 画面の描画
        screen.fill(WHITE)

        # UIの描画
        money_text = font.render(f"お金: {game_state.money}円", True, BLACK)
        games_text = font.render(f"積みゲー: {game_state.games}個", True, BLACK)
        screen.blit(money_text, (10, 10))
        screen.blit(games_text, (10, 50))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
