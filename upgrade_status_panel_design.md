# アップグレード情報表示パネル設計書（最終調整版）

## 変更点: ゲーミング → ゲーミング PC に表記統一

## 1. 表示内容（GameState プロパティ完全準拠）

| アイコン | アップグレード    | 表示形式                                   | 使用プロパティ                                                                       |
| -------- | ----------------- | ------------------------------------------ | ------------------------------------------------------------------------------------ |
| 💼       | 労働 DX 化        | `{count}回 * {percent}% = {total}%アップ`  | `upgrades[0]["count"]`, `work_unit_up_percent`                                       |
| 🛒       | 同時購入          | `{count}個/回`                             | `purchase_count`                                                                     |
| 🤖       | 労働自動化        | `毎秒{count}回クリック`                    | `auto_clicks`                                                                        |
| ⚡       | 購入自動化        | `{interval}秒毎に{count}回購入`            | `auto_purchases`, `auto_purchase_interval`                                           |
| 🎮       | **ゲーミング PC** | `効率+{efficiency}% 購入間隔-{reduction}%` | `gaming_pc_level`, `gaming_pc_efficiency_bonus`, `gaming_pc_interval_reduction`      |
| 🚀       | アーリーアクセス  | `投資額 {investment} 最大還元率 {return}%` | `total_early_access_investment`, `early_access_level`, `early_access_return_percent` |

## 2. 実装関数仕様（表記修正箇所）

```python
def draw_upgrade_status_panel(screen, game_state):
    # ...（中略）...

    # 1行目: 基本情報
    base_texts = [
        f"💼 労働DX化",
        f"🛒 同時購入",
        f"🤖 労働自動化",
        f"⚡ 購入自動化",
        f"🎮 ゲーミングPC",  # 修正: ゲーミング → ゲーミングPC
        f"🚀 アーリーアクセス"
    ]

    # 2行目: 具体的効果
    effect_texts = [
        # ...（他項目は変更なし）...

        # ゲーミングPC (修正: 表記を統一)
        f"効率+{int(game_state.gaming_pc_level * game_state.gaming_pc_efficiency_bonus * 100)}% "
        f"購入間隔-{int(game_state.gaming_pc_level * game_state.gaming_pc_interval_reduction * 100)}%",

        # ...（以下略）...
    ]
```

## 3. 表示イメージ更新

```
[新パネル1行目] ... 🎮ゲーミングPC ...
[新パネル2行目] ... 効率+5% 購入間隔-20% ...
```

## 4. 変更理由

- ゲーム内実装(`main.py`)では `gaming_pc_level` など「PC」を含む変数名を使用
- アップグレード名も「ゲーミング PC」と正式に表記
- ユーザーからの正確性要求に対応
