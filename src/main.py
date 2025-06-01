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
    draw_upgrade_status_panel,  # 追加
)
from config_loader import load_env_file
import pygame.gfxdraw  # グラスモーフィズム効果のために追加

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


class GameState:
    def __init__(self):
        # .envファイルから設定を読み込む
        current_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(current_dir, ".env")
        config = load_env_file(env_path)

        # 各アップグレードの初期コストをselfプロパティとして定義
        self.efficiency_tool_cost = config.get("EFFICIENCY_TOOL_COST", 200)
        self.bulk_purchase_cost = config.get("BULK_PURCHASE_COST", 200)
        self.auto_work_tool_cost = config.get("AUTO_WORK_TOOL_COST", 200)
        self.auto_purchase_tool_cost = config.get("AUTO_PURCHASE_TOOL_COST", 200)
        self.early_access_cost = config.get("EARLY_ACCESS_COST", 300)

        # 基本設定
        self.money = config.get("INITIAL_MONEY", 0)
        self.stock = config.get("INITIAL_STOCK", 0)
        self.work_unit_price = config.get("WORK_UNIT_PRICE", 100)
        self.auto_work_unit_price = 0
        self.purchase_count = config.get("PURCHASE_COUNT", 1)
        self.game_price = config.get("GAME_PRICE", 100.0)

        # 各アップグレードの効果量を変数として定義
        # 労働DX 賃金%アップ
        self.work_unit_up_percent = config.get("WORK_UNIT_UP_PERCENT", 1000)

        # 同時購入数%アップ
        self.purchase_power_up_percent = config.get("PURCHASE_POWER_UP_PERCENT", 200)

        # 労働自動化ツール 自動クリック%アップ
        self.auto_click_up_percent = config.get("AUTO_CLICK_UP_PERCENT", 100)
        self.auto_clicks = 0  # 自動クリック回数（1秒あたり）
        self.last_auto_update = 0  # 最後の自動クリック更新時間

        # 購入自動化ツール 購入自動化%アップ
        self.auto_purchase_up_percent = config.get("AUTO_PURCHASE_UP_PERCENT", 100)
        self.auto_purchases = 0  # 購入自動化回数（3秒あたり）
        self.last_auto_purchase = 0
        self.auto_purchase_interval = config.get(
            "AUTO_PURCHASE_INTERVAL", 3.0
        )  # 購入自動化の間隔（秒）

        # ゲーミングPCの設定
        self.gaming_pc_level = 0  # 初期レベルは0（未所持）
        self.gaming_pc_base_cost = config.get(
            "GAMING_PC_BASE_COST", 100
        )  # 初期購入コスト
        self.gaming_pc_income_per_game = config.get(
            "GAMING_PC_INCOME_PER_GAME", 100
        )  # 積みゲー1個あたりの毎秒収入（円）
        self.gaming_pc_efficiency_bonus = config.get(
            "GAMING_PC_EFFICIENCY_BONUS", 0.05
        )  # レベルごとの労働効率ボーナス
        self.gaming_pc_interval_reduction = config.get(
            "GAMING_PC_INTERVAL_REDUCTION", 0.2
        )  # レベルごとの購入自動化間隔短縮率
        self.last_pc_income_time = 0  # 最後にPCからの収入を得た時間
        self.pc_income_interval = 1.0  # PCからの収入を得る間隔（秒）

        # アーリーアクセス関連の設定
        self.early_access_level = 0  # アーリーアクセスのレベル
        self.early_access_return_percent = config.get(
            "EARLY_ACCESS_RETURN_PERCENT", 100
        )  # 基本の資産増加率（%）
        self.early_access_interval = config.get(
            "EARLY_ACCESS_INTERVAL", 1.0
        )  # 収益が発生する間隔（秒）
        self.last_early_access_return = 0  # 最後に収益が発生した時間
        self.total_early_access_investment = 0  # アーリーアクセスへの総投資額
        self.last_early_access_result = 0  # 最後のアーリーアクセス収益結果
        self.last_early_access_is_negative = False  # 最後の結果がマイナスだったか
        self.last_early_access_actual_percent = 0.0  # 最後に適用された実際の収益率
        self.last_early_access_game_bonus = 0.0  # ゲーム数によるボーナス収益率
        self.early_access_investment_per_second = 0  # 毎秒の投資効果

        # 値上がり率
        self.upgrade_cost_multiplier = config.get(
            "UPGRADE_COST_MULTIPLIER", 1.2
        )  # アップグレードの値上がり率
        self.game_cost_multiplier = config.get(
            "GAME_COST_MULTIPLIER", 1.0
        )  # ゲーム価格の値上がり率
        self.last_game_price_update_time = 0  # ゲーム価格の最終更新時間

        # アップグレードアイテムのリスト
        self.upgrades = [
            {
                "name": "労働のDX化",
                "cost": self.efficiency_tool_cost,
                "effect": self.work_unit_up_percent,  # 賃金アップ率（%）
                "count": 0,
                "description": f"賃金が{self.work_unit_up_percent}%アップ",
            },
            {
                "name": "同時購入数アップ",
                "cost": self.bulk_purchase_cost,
                "effect": self.purchase_power_up_percent,  # 購入数アップ率（%）
                "count": 0,
                "description": f"購入数が{self.purchase_power_up_percent}%アップ",
            },
            {
                "name": "労働自動化ツール",
                "cost": self.auto_work_tool_cost,
                "effect": self.auto_click_up_percent,  # 自動クリック%アップ
                "count": 0,
                "description": f"毎秒の自動クリック回数+{self.auto_click_up_percent}%アップ",
            },
            {
                "name": "購入自動化ツール",
                "cost": self.auto_purchase_tool_cost,
                "effect": self.auto_purchase_up_percent,  # 購入自動化%アップ
                "count": 0,
                "description": f"{self.auto_purchase_interval:.1f}秒ごとの自動購入回数+{self.auto_purchase_up_percent}%アップ",
            },
            {
                "name": "ゲーミングPC",
                "cost": self.gaming_pc_base_cost,
                "effect": self.gaming_pc_level,  # 現在のPCレベル
                "count": 0,
                "description": "積みゲーをプレイして配信！ レベルアップで収益UP",
            },
            {
                "name": "アーリーアクセス",
                "cost": self.early_access_cost,
                "effect": self.early_access_return_percent,  # 基本の資産増加率（%）
                "count": 0,
                "description": f"開発中のゲームに投資！投資額が変動して還元されます",
            },
        ]

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
        # 購入数分の合計金額を計算
        game_price_int = int(self.game_price)
        max_purchase = round(self.purchase_count)  # 購入数（最大購入可能数）

        # お金が足りない場合は、買える分だけ買う
        if self.money < game_price_int * max_purchase:
            # 買える最大数を計算（少なくとも1個は買えるようにする）
            affordable_count = max(1, self.money // game_price_int)
            # 購入数と買える数の小さい方を選択
            actual_purchase = min(affordable_count, max_purchase)
        else:
            # お金が十分ある場合は購入数分すべて買う
            actual_purchase = max_purchase

        # 実際の支払い金額を計算
        total_cost = game_price_int * actual_purchase

        if self.money >= total_cost and actual_purchase > 0:
            self.money -= total_cost  # 合計金額を支払い
            self.stock += actual_purchase  # 実際に購入した数を加算

            return actual_purchase  # 実際に購入した数を返す
        return 0  # 購入失敗（お金が1個分もない場合）

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
            elif index == 1:  # 同時購入数アップ
                # 現在の購入数に対して指定パーセント分アップ
                increase_amount = self.purchase_count * (upgrade["effect"] / 100)
                self.purchase_count += increase_amount
            elif index == 2:  # 労働自動化ツール
                # 現在の自動クリック数に対して指定パーセンテージ分アップ
                if self.auto_clicks == 0:  # 初期値が0の場合、1からスタート
                    self.auto_clicks = 1
                else:
                    increase_amount = self.auto_clicks * (upgrade["effect"] / 100)
                    self.auto_clicks += increase_amount
                # 説明文を更新
                upgrade["description"] = (
                    f"毎秒{int(self.auto_clicks)}回、自動的に労働ボタンをクリック"
                )
            elif index == 3:  # 購入自動化ツール
                # 現在の自動購入数に対して指定パーセンテージ分アップ
                if self.auto_purchases == 0:  # 初期値が0の場合、1からスタート
                    self.auto_purchases = 1
                else:
                    increase_amount = self.auto_purchases * (upgrade["effect"] / 100)
                    self.auto_purchases += increase_amount
                # 説明文を更新
                upgrade["description"] = (
                    f"{self.auto_purchase_interval:.1f}秒ごとに{int(self.auto_purchases)}回、自動的にゲームを購入"
                )
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
                    * (self.upgrade_cost_multiplier**self.gaming_pc_level)
                )

                # 説明文を更新
                income_per_sec = self.gaming_pc_level * self.gaming_pc_income_per_game
                efficiency_bonus = int(
                    self.gaming_pc_level * self.gaming_pc_efficiency_bonus * 100
                )

                # レベルに応じた特別ボーナスの説明を追加
                reduction_percent = int(
                    self.gaming_pc_level * self.gaming_pc_interval_reduction * 100
                )

                upgrade["description"] = (
                    f"Lv.{self.gaming_pc_level}: 積みゲー×{income_per_sec}円/秒、労働効率+{efficiency_bonus}%、購入自動化間隔-{reduction_percent}%"
                )
            elif index == 5:  # アーリーアクセス
                # アーリーアクセスのレベルを上げる
                self.early_access_level += 1

                # 投資額を記録
                self.total_early_access_investment += upgrade["cost"]

                # 収益率を更新（レベルごとに基本収益率が加算される）- 小数点2桁で丸める
                max_return_percent = round(
                    self.early_access_level * self.early_access_return_percent, 2
                )

                # 保有ゲーム数によるボーナスの説明を追加
                game_bonus_text = "（ゲーム数に応じてボーナス追加！上限なし）"

                # 価格上昇
                upgrade["cost"] = int(upgrade["cost"] * self.upgrade_cost_multiplier)
                upgrade["description"] = (
                    f"開発中のゲームに投資！投資額の0～{max_return_percent:.2f}%+ゲーム数ボーナスが還元 (Lv.{self.early_access_level})"
                )

                return True  # 購入成功

            # ゲーミングPCとアーリーアクセス以外のアップグレードは通常の価格上昇
            if index != 4 and index != 5:
                upgrade["cost"] = int(upgrade["cost"] * self.upgrade_cost_multiplier)

            return True  # 購入成功
        return False  # 購入失敗

    def update_auto_income(self, current_time):
        # 前回の更新から経過した時間（秒）
        elapsed = current_time - self.last_auto_update
        if elapsed >= 1.0:  # 1秒以上経過していたら
            # 自動クリック回数分だけ労働ボタンをクリックした効果を得る
            for _ in range(round(self.auto_clicks)):
                self.click_work()
            self.last_auto_update = current_time

        # 購入自動化の処理
        elapsed_purchase = current_time - self.last_auto_purchase

        # ゲーミングPCのレベルに応じて購入自動化間隔を短縮
        # レベル1ごとにself.gaming_pc_interval_reduction%短縮（上限なし）
        auto_purchase_interval = self.auto_purchase_interval
        if self.gaming_pc_level > 0:
            reduction_percent = self.gaming_pc_level * self.gaming_pc_interval_reduction
            auto_purchase_interval *= max(
                0.01, 1.0 - reduction_percent
            )  # 最低でも0.01秒は確保

        if elapsed_purchase >= auto_purchase_interval:  # 設定した間隔以上経過していたら
            # 購入自動化回数分だけゲームを購入
            for _ in range(round(self.auto_purchases)):
                self.buy_game()  # 購入できない場合は何も起きない
            self.last_auto_purchase = current_time

        # ゲーミングPCからの収入処理
        if self.gaming_pc_level > 0:
            elapsed_pc_income = current_time - self.last_pc_income_time
            if elapsed_pc_income >= self.pc_income_interval:  # 1秒ごとに収入
                # 積みゲー数 × PCレベル × 収入係数で1秒あたりの収入を計算
                income_per_sec = (
                    self.stock * self.gaming_pc_level * self.gaming_pc_income_per_game
                )
                self.money += int(income_per_sec)
                self.last_pc_income_time = current_time

        # アーリーアクセスからの収入処理
        if self.early_access_level > 0:
            elapsed_early_access = current_time - self.last_early_access_return
            if (
                elapsed_early_access >= self.early_access_interval
            ):  # 設定した間隔ごとに収入
                # 投資額に対して収益率を適用 - 小数点2桁で丸める
                max_return_percent = round(
                    self.early_access_level * self.early_access_return_percent, 2
                )

                # 保有ゲーム数によるボーナス
                game_bonus_percent = round((self.stock / 100) * 0.1, 2)
                max_return_percent += game_bonus_percent

                # 0%から最大収益率までのランダムな値を生成
                actual_return_percent = round(random.uniform(0, max_return_percent), 2)

                # 6:4の確率で増加または減少を決定
                is_negative = random.random() < 0.49  # 40%の確率で減少
                if is_negative:
                    actual_return_percent = -actual_return_percent  # マイナスにする

                # 収益額を計算
                return_amount = int(
                    self.total_early_access_investment * (actual_return_percent / 100)
                )

                # 収益を加算（マイナスの場合は減算）
                self.money += return_amount

                # 最後の収益時間を更新
                self.last_early_access_return = current_time

                # 今回の結果を記録（UI表示用）
                self.last_early_access_result = return_amount
                self.last_early_access_is_negative = is_negative
                self.last_early_access_actual_percent = actual_return_percent
                self.last_early_access_game_bonus = game_bonus_percent
                self.early_access_investment_per_second = (
                    return_amount  # 毎秒の投資効果を更新
                )

        # ゲーム価格の変動処理 (1秒ごと)
        elapsed_game_price = current_time - self.last_game_price_update_time
        if elapsed_game_price >= 1.0:  # 1秒以上経過していたら
            if random.random() < 0.4:
                # 価格を下降させる
                self.game_price = self.game_price / self.game_cost_multiplier
            else:
                # 価格を上昇させる
                self.game_price = self.game_price * self.game_cost_multiplier
            self.last_game_price_update_time = current_time


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
