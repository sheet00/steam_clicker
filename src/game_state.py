import os
import random
from config_loader import load_env_file


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
        self.work_unit_up_percent = config.get("WORK_UNIT_UP_PERCENT", 0.03)

        # 同時購入数%アップ
        self.purchase_power_up_percent = config.get("PURCHASE_POWER_UP_PERCENT", 0.03)

        # 労働自動化ツール 自動クリック%アップ
        self.auto_click_up_percent = config.get("AUTO_CLICK_UP_PERCENT", 0.03)
        self.auto_clicks = 0  # 自動クリック回数（1秒あたり）
        self.last_auto_update = 0  # 最後の自動クリック更新時間

        # 購入自動化ツール 購入自動化%アップ
        self.auto_purchase_up_percent = config.get("AUTO_PURCHASE_UP_PERCENT", 0.03)
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
            "GAMING_PC_EFFICIENCY_BONUS_PERCENT", 0.01
        )  # レベルごとの労働効率ボーナス
        self.gaming_pc_interval_reduction = config.get(
            "GAMING_PC_INTERVAL_REDUCTION_PERCENT", 0.02
        )  # レベルごとの購入自動化間隔短縮率
        self.last_pc_income_time = 0  # 最後にPCからの収入を得た時間
        self.pc_income_interval = 1.0  # PCからの収入を得る間隔（秒）

        # アーリーアクセス関連の設定
        self.early_access_level = 0  # アーリーアクセスのレベル
        self.early_access_return_percent = config.get(
            "EARLY_ACCESS_RETURN_PERCENT", 0.01
        )  # 基本の資産増加率（%）
        self.max_return_percent = 0.0  # 最大利益率の初期値を追加
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
                "description": f"労働をDX化して業務効率化！\n賃金が{self.work_unit_up_percent*100:.0f}%アップ",
            },
            {
                "name": "同時購入数アップ",
                "cost": self.bulk_purchase_cost,
                "effect": self.purchase_power_up_percent,  # 購入数アップ率（%）
                "count": 0,
                "description": f"一括大量購入で、無駄遣いも効率的に！\n購入数が{self.purchase_power_up_percent*100:.0f}%アップ",
            },
            {
                "name": "労働自動化ツール",
                "cost": self.auto_work_tool_cost,
                "effect": self.auto_click_up_percent,  # 自動クリック%アップ
                "count": 0,
                "description": f"全自動で働いてくれるロボット\n毎秒の自動クリック回数+{self.auto_click_up_percent*100:.0f}%アップ",
            },
            {
                "name": "購入自動化ツール",
                "cost": self.auto_purchase_tool_cost,
                "effect": self.auto_purchase_up_percent,  # 購入自動化%アップ
                "count": 0,
                "description": f"勝手にゲームを購入してくれるロボット\n{self.auto_purchase_interval:.1f}秒ごとの自動購入回数+{self.auto_purchase_up_percent*100:.0f}%アップ",
            },
            {
                "name": "ゲーミングPC",
                "cost": self.gaming_pc_base_cost,
                "effect": self.gaming_pc_level,  # 現在のPCレベル
                "count": 0,
                "description": f"ゲーミングPCで配信収益 賃金{self.gaming_pc_efficiency_bonus*100:.0f}%アップ\n購入自動化{self.gaming_pc_interval_reduction*100:.2f}%短縮 配信収益ゲーム数*PCレベル*{self.gaming_pc_income_per_game}円",
            },
            {
                "name": "アーリーアクセス",
                "cost": self.early_access_cost,
                "effect": self.early_access_return_percent,  # 基本の資産増加率（%）
                "count": 0,
                "description": f"未完成の夢に投資しよう\n {self.early_access_interval}秒毎、投資額の{self.early_access_return_percent*100:.2f}%収益",
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
                increase_amount = int(self.work_unit_price * upgrade["effect"])
                self.work_unit_price += increase_amount
            elif index == 1:  # 同時購入数アップ
                # 現在の購入数に対して指定パーセント分アップ
                increase_amount = self.purchase_count * upgrade["effect"]
                self.purchase_count += increase_amount
            elif index == 2:  # 労働自動化ツール
                # 現在の自動クリック数に対して指定パーセンテージ分アップ
                if self.auto_clicks == 0:  # 初期値が0の場合、1からスタート
                    self.auto_clicks = 1
                else:
                    increase_amount = self.auto_clicks * upgrade["effect"]
                    self.auto_clicks += increase_amount
            elif index == 3:  # 購入自動化ツール
                # 現在の自動購入数に対して指定パーセンテージ分アップ
                if self.auto_purchases == 0:  # 初期値が0の場合、1からスタート
                    self.auto_purchases = 1
                else:
                    increase_amount = self.auto_purchases * upgrade["effect"]
                    self.auto_purchases += increase_amount
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
            elif index == 5:  # アーリーアクセス
                # アーリーアクセスのレベルを上げる
                self.early_access_level += 1

                # 投資額を記録
                self.total_early_access_investment += upgrade["cost"]

                # 価格上昇
                upgrade["cost"] = int(upgrade["cost"] * self.upgrade_cost_multiplier)
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
            # click_work()のロジックを直接ここに展開し、moneyに直接加算
            efficiency_bonus = 1.0
            if self.gaming_pc_level > 0:
                efficiency_bonus = 1.0 + (
                    self.gaming_pc_level * self.gaming_pc_efficiency_bonus
                )
            earned_per_click = int(self.work_unit_price * efficiency_bonus)
            self.money += earned_per_click * round(self.auto_clicks)
            self.last_auto_update = current_time

        # 購入自動化の処理
        elapsed_purchase = current_time - self.last_auto_purchase

        # ゲーミングPCのレベルに応じて購入自動化間隔を短縮
        # レベル1ごとにself.gaming_pc_interval_reduction%短縮（上限なし）
        cal_purchase_interval = self.auto_purchase_interval
        if self.gaming_pc_level > 0:
            reduction_percent = self.gaming_pc_level * self.gaming_pc_interval_reduction
            cal_purchase_interval *= max(
                0.01, 1.0 - reduction_percent
            )  # 最低でも0.01秒は確保

        if elapsed_purchase >= cal_purchase_interval:  # 設定した間隔以上経過していたら
            # 購入自動化回数分だけゲームを購入
            # buy_game()のロジックを直接ここに展開し、stockとmoneyに直接加算
            game_price_int = int(self.game_price)
            max_purchase_per_auto = round(self.purchase_count)

            # 買える最大数を計算
            affordable_count = 0
            if game_price_int > 0:
                affordable_count = max(0, self.money // game_price_int)

            # 実際に購入する数を決定
            actual_purchase_this_interval = min(
                affordable_count, max_purchase_per_auto * round(self.auto_purchases)
            )

            if actual_purchase_this_interval > 0:
                total_cost_this_interval = (
                    game_price_int * actual_purchase_this_interval
                )
                self.money -= total_cost_this_interval
                self.stock += actual_purchase_this_interval
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
                self.max_return_percent = round(
                    self.early_access_level * self.early_access_return_percent,
                    2,
                )

                # 保有ゲーム数によるボーナス
                game_bonus_percent = round((self.stock / 100) * 0.1, 2)
                self.max_return_percent += game_bonus_percent

                # 0%から最大収益率までのランダムな値を生成
                actual_return_percent = round(
                    random.uniform(0, self.max_return_percent), 2
                )

                # 6:4の確率で増加または減少を決定
                is_negative = random.random() < 0.4  # 40%の確率で減少
                if is_negative:
                    actual_return_percent = -actual_return_percent  # マイナスにする

                # 収益額を計算
                return_amount = int(
                    self.total_early_access_investment * actual_return_percent
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
