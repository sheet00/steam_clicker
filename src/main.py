import pygame
import os
import sys
from pygame.locals import *
from ui_components import draw_texts, draw_buttons

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
# OSに応じてフォントを設定
try:
    # Windowsの場合
    font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 36)
    button_font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 24)
except:
    # Windowsでない場合はデフォルトフォントを使用
    font = pygame.font.SysFont(None, 36)
    button_font = pygame.font.SysFont(None, 24)

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

        # アップグレードアイテムのリスト
        self.upgrades = [
            {
                "name": "効率化ツール",
                "cost": 500,
                "effect": 50,  # 労働単価アップ量
                "count": 0,
                "description": "労働単価+50円",
            },
            {
                "name": "バルクゲーム購入",
                "cost": 1000,
                "effect": 1,  # 購入力アップ量
                "count": 0,
                "description": "一度に購入するゲーム数+1",
            },
            {
                "name": "自動労働ツール",
                "cost": 2000,
                "effect": 10,  # 自動労働の秒間獲得額
                "count": 0,
                "description": "毎秒10円を自動獲得",
            },
        ]

        # 自動労働の秒間獲得額
        self.auto_income = 0
        # 最後の自動収入更新時間
        self.last_auto_update = 0

    def click_work(self):
        self.money += self.work_unit_price

    def buy_game(self):
        if self.money >= self.game_price:
            self.money -= self.game_price
            self.stock += self.purchase_power

    def buy_upgrade(self, index):
        upgrade = self.upgrades[index]
        if self.money >= upgrade["cost"]:
            self.money -= upgrade["cost"]
            upgrade["count"] += 1

            # アップグレードの効果を適用
            if index == 0:  # 効率化ツール
                self.work_unit_price += upgrade["effect"]
            elif index == 1:  # バルクゲーム購入
                self.purchase_power += upgrade["effect"]
            elif index == 2:  # 自動労働ツール
                self.auto_income += upgrade["effect"]

            # 価格上昇（購入するたびに1.5倍に）
            upgrade["cost"] = int(upgrade["cost"] * 1.5)

    def update_auto_income(self, current_time):
        # 前回の更新から経過した時間（秒）
        elapsed = current_time - self.last_auto_update
        if elapsed >= 1.0:  # 1秒以上経過していたら
            self.money += self.auto_income
            self.last_auto_update = current_time


def main():

    # 画面設定
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 1000
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Steamクリッカー")

    # ボタンの設定
    work_button = pygame.Rect(300, 200, 200, 80)
    buy_button = pygame.Rect(300, 300, 200, 80)

    # アップグレードボタンの設定
    upgrade_buttons = []
    for i in range(3):  # 3つのアップグレード
        upgrade_buttons.append(pygame.Rect(550, 150 + i * 100, 220, 80))

    clock = pygame.time.Clock()
    game_state = GameState()
    game_state.last_auto_update = pygame.time.get_ticks() / 1000  # 初期化

    # デフォルトカーソルと手のカーソルを設定
    default_cursor = pygame.SYSTEM_CURSOR_ARROW
    hand_cursor = pygame.SYSTEM_CURSOR_HAND

    clicked_button = None
    click_time = 0
    clicked_upgrade = None

    while True:
        current_time = pygame.time.get_ticks() / 1000  # 秒単位の現在時刻

        # 自動収入の更新
        game_state.update_auto_income(current_time)

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

                # アップグレードボタンがクリックされた場合
                for i, button in enumerate(upgrade_buttons):
                    if button.collidepoint(mouse_pos):
                        game_state.buy_upgrade(i)
                        clicked_upgrade = i
                        click_time = current_time

        # マウスカーソルの位置を取得
        mouse_pos = pygame.mouse.get_pos()

        # カーソル状態のキャッシュを追加して、不要なカーソル変更を防止
        if (
            work_button.collidepoint(mouse_pos)
            or buy_button.collidepoint(mouse_pos)
            or any(button.collidepoint(mouse_pos) for button in upgrade_buttons)
        ):
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
            "upgrade_buttons": upgrade_buttons,
            "clicked_button": clicked_button,
            "clicked_upgrade": clicked_upgrade,
            "click_time": click_time,
            "current_time": current_time,
        }

        # 修正: フォントと画像を引数として渡す
        draw_texts(screen, game_state, font, button_font)
        draw_buttons(
            screen, game_state, buttons, button_font, yum_image, cold_sweat_image
        )

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
