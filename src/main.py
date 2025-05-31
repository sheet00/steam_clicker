import pygame
import os
import sys
from pygame.locals import *
from ui_components import draw_texts, draw_buttons

# 画面設定
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000  # 画面の高さを調整

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

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
        self.game_price = 100

        # 各アップグレードの効果量を変数として定義
        self.work_unit_up_percent = 10  # 賃金%アップ
        self.purchase_power_up_percent = 10  # 購入力%アップ
        self.auto_click_amount = 1  # 自動クリック回数（1秒あたり）
        self.auto_purchase_amount = 1  # 自動購入回数（3秒あたり）

        # 各アップグレードの初期コストをselfプロパティとして定義
        self.efficiency_tool_cost = 500
        self.bulk_purchase_cost = 1000
        self.auto_work_tool_cost = 500
        self.auto_purchase_tool_cost = 500

        # 値上がり率
        self.cost_upgrade_per = 1.1

        # 自動購入の設定
        self.auto_purchases = 0
        self.last_auto_purchase = 0
        self.auto_purchase_interval = 3.0  # 自動購入の間隔（秒）

        # ゲーミングPCの設定
        self.gaming_pc_level = 0  # 初期レベルは0（未所持）
        self.gaming_pc_base_cost = 100  # 初期購入コスト
        self.gaming_pc_upgrade_cost_multiplier = 1.5  # アップグレード時の価格上昇率
        self.gaming_pc_income_per_game = 1  # 積みゲー1個あたりの毎秒収入（円）
        self.gaming_pc_efficiency_bonus = 0.05  # レベルごとの労働効率ボーナス（5%）
        self.last_pc_income_time = 0  # 最後にPCからの収入を得た時間
        self.pc_income_interval = 1.0  # PCからの収入を得る間隔（秒）

        # アップグレードアイテムのリスト
        self.upgrades = [
            {
                "name": "効率化ツール",
                "cost": self.efficiency_tool_cost,
                "effect": self.work_unit_up_percent,  # 賃金アップ率（%）
                "count": 0,
                "description": f"賃金+{self.work_unit_up_percent}%アップ",
            },
            {
                "name": "バルクゲーム購入",
                "cost": self.bulk_purchase_cost,
                "effect": self.purchase_power_up_percent,  # 購入力アップ率（%）
                "count": 0,
                "description": f"購入力+{self.purchase_power_up_percent}%アップ",
            },
            {
                "name": "自動労働ツール",
                "cost": self.auto_work_tool_cost,
                "effect": self.auto_click_amount,  # 1秒あたりの自動クリック回数
                "count": 0,
                "description": f"毎秒{self.auto_click_amount}回、自動的に労働ボタンをクリック",
            },
            {
                "name": "自動購入ツール",
                "cost": self.auto_purchase_tool_cost,
                "effect": self.auto_purchase_amount,  # 3秒あたりの自動購入回数
                "count": 0,
                "description": f"{self.auto_purchase_interval}秒ごとに{self.auto_purchase_amount}回、自動的にゲームを購入",
            },
            {
                "name": "ゲーミングPC",
                "cost": self.gaming_pc_base_cost,
                "effect": self.gaming_pc_level,  # 現在のPCレベル
                "count": 0,
                "description": f"積みゲーをプレイして配信！ レベルアップで収益UP",
            },
        ]

        # 自動クリック回数（1秒あたり）
        self.auto_clicks = 0
        # 最後の自動クリック更新時間
        self.last_auto_update = 0

    def click_work(self):
        # ゲーミングPCのレベルに応じた労働効率ボーナスを計算
        efficiency_bonus = 1.0
        if self.gaming_pc_level > 0:
            efficiency_bonus = 1.0 + (
                self.gaming_pc_level * self.gaming_pc_efficiency_bonus
            )

        earned = int(self.work_unit_price * efficiency_bonus)
        self.money += earned
        return earned  # 増加した金額を返す

    def buy_game(self):
        if self.money >= self.game_price:
            self.money -= self.game_price
            self.stock += self.purchase_power
            return True  # 購入成功
        return False  # 購入失敗

    def buy_upgrade(self, index):
        upgrade = self.upgrades[index]
        if self.money >= upgrade["cost"]:
            self.money -= upgrade["cost"]
            upgrade["count"] += 1

            # アップグレードの効果を適用
            if index == 0:  # 効率化ツール
                # 現在の賃金に対して指定パーセント分アップ
                increase_amount = int(self.work_unit_price * (upgrade["effect"] / 100))
                self.work_unit_price += increase_amount
            elif index == 1:  # バルクゲーム購入
                self.purchase_power += upgrade["effect"]
            elif index == 2:  # 自動労働ツール
                self.auto_clicks += upgrade["effect"]
            elif index == 3:  # 自動購入ツール
                self.auto_purchases += upgrade["effect"]
            elif index == 4:  # ゲーミングPC
                if self.gaming_pc_level == 0:
                    # 初めてPCを購入した場合
                    self.gaming_pc_level = 1
                else:
                    # PCをアップグレードする場合
                    self.gaming_pc_level += 1

                # PCのレベルを更新
                upgrade["effect"] = self.gaming_pc_level

                # 次のアップグレード価格を計算
                upgrade["cost"] = int(
                    self.gaming_pc_base_cost
                    * (self.gaming_pc_upgrade_cost_multiplier**self.gaming_pc_level)
                )

                # 説明文を更新
                income_per_sec = self.gaming_pc_level * self.gaming_pc_income_per_game
                efficiency_bonus = int(
                    self.gaming_pc_level * self.gaming_pc_efficiency_bonus * 100
                )

                # レベルに応じた特別ボーナスの説明を追加
                special_bonus = ""
                if self.gaming_pc_level >= 10:
                    special_bonus = "、自動購入間隔-10%"

                upgrade["description"] = (
                    f"Lv.{self.gaming_pc_level}: 積みゲー×{income_per_sec}円/秒、労働効率+{efficiency_bonus}%{special_bonus}"
                )

                return True  # 購入成功

            # ゲーミングPC以外のアップグレードは通常の価格上昇
            if index != 4:
                upgrade["cost"] = int(upgrade["cost"] * self.cost_upgrade_per)

            return True  # 購入成功
        return False  # 購入失敗

    def update_auto_income(self, current_time):
        # 前回の更新から経過した時間（秒）
        elapsed = current_time - self.last_auto_update
        if elapsed >= 1.0:  # 1秒以上経過していたら
            # 自動クリック回数分だけ労働ボタンをクリックした効果を得る
            for _ in range(self.auto_clicks):
                self.click_work()
            self.last_auto_update = current_time

        # 自動購入の処理
        elapsed_purchase = current_time - self.last_auto_purchase

        # ゲーミングPCのレベルが10以上なら自動購入間隔を短縮
        auto_purchase_interval = self.auto_purchase_interval
        if self.gaming_pc_level >= 10:
            auto_purchase_interval *= 0.9  # 10%短縮

        if elapsed_purchase >= auto_purchase_interval:  # 設定した間隔以上経過していたら
            # 自動購入回数分だけゲームを購入
            for _ in range(self.auto_purchases):
                self.buy_game()  # 購入できない場合は何も起きない
            self.last_auto_purchase = current_time

        # ゲーミングPCからの収入処理
        if self.gaming_pc_level > 0:
            elapsed_pc_income = current_time - self.last_pc_income_time
            if elapsed_pc_income >= self.pc_income_interval:  # 1秒ごとに収入
                # 積みゲー数 × PCレベル × 収入係数で1秒あたりの収入を計算
                income_per_sec = self.stock * self.gaming_pc_level * self.gaming_pc_income_per_game
                self.money += int(income_per_sec)
                self.last_pc_income_time = current_time


def main():

    # 画面設定
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 1000
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Steamクリッカー")

    # メインボタンの設定 - 中央に大きく配置
    work_button = pygame.Rect(0, 0, 300, 120)  # 位置は後で調整
    buy_button = pygame.Rect(0, 0, 300, 120)  # 位置は後で調整

    # アップグレードボタンの設定 - 右側に縦に並べる
    upgrade_buttons = []
    for i in range(5):  # 5つのアップグレード（ゲーミングPC追加）
        upgrade_buttons.append(pygame.Rect(0, 0, 300, 150))  # 位置は後で調整

    clock = pygame.time.Clock()
    game_state = GameState()
    game_state.last_auto_update = pygame.time.get_ticks() / 1000  # 初期化
    game_state.last_auto_purchase = pygame.time.get_ticks() / 1000  # 自動購入の初期化
    game_state.last_pc_income_time = (
        pygame.time.get_ticks() / 1000
    )  # PCからの収入の初期化

    # デフォルトカーソルと手のカーソルを設定
    default_cursor = pygame.SYSTEM_CURSOR_ARROW
    hand_cursor = pygame.SYSTEM_CURSOR_HAND

    clicked_button = None
    click_time = 0
    clicked_upgrade = None

    while True:
        current_time = pygame.time.get_ticks() / 1000  # 秒単位の現在時刻

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
                if work_button.collidepoint(mouse_pos):
                    earned = game_state.click_work()
                    clicked_button = "work"
                    click_time = current_time

                # 購入ボタンがクリックされた場合
                if buy_button.collidepoint(mouse_pos):
                    success = game_state.buy_game()
                    if success:
                        clicked_button = "buy"
                        click_time = current_time

                # アップグレードボタンがクリックされた場合
                for i, button in enumerate(upgrade_buttons):
                    if button.collidepoint(mouse_pos):
                        clicked_button = "upgrade"

                        # アップグレード購入を試みる
                        success = game_state.buy_upgrade(i)
                        if success:  # 購入に成功した場合のみ
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

        # 画面の描画
        screen.fill(WHITE)
        draw_texts(screen, game_state)
        draw_buttons(screen, game_state, buttons, yum_image, cold_sweat_image)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
