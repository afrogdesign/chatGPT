# README autopost note

これは **検証用メモ** です。実運用を前提にせず、どこに自動投稿ロジックを差し込むかだけを示します。

## 差し込む場所

- **本文生成の出口**
  - `src/main.py`
  - ここで `compose.py` が作った最終テキストを受け取る
- **ブラウザ操作の担当**
  - `src/post_x.py`
  - ここに Playwright の処理を書く
- **定時実行の入口**
  - `scripts/run_once.sh`
  - ここで `python src/main.py` を起動する

## いちばん自然な流れ

1. `collector.py` で情報収集
2. `compose.py` で投稿文生成
3. `main.py` で完成文を受け取る
4. ここで `post_x.py` の関数を呼ぶ
5. `post_x.py` が X の投稿画面を開き、本文を入れる
6. 必要なら最後の送信まで行う

## 実際に手を入れるポイント

### A. `src/main.py`

ここで作られた `post_text` を、`post_x.py` に渡します。

```python
from post_x import open_compose, post_now

post_text = compose_post(str(CONFIG_PATH), items)

# 検証用: 投稿画面を開くだけ
open_compose(post_text, headed=True)

# 検証用: もし完全自動に挑戦するならこちら側を呼ぶ構成にする
# post_now(post_text, headed=False)
```

### B. `src/post_x.py`

このファイルに入れる役割は次の通りです。

- `setup_profile()`
  - 初回ログイン状態を `runtime/x_profile/` に保存
- `open_compose(text)`
  - 投稿画面を開いて本文を流し込む
- `post_now(text)`
  - 送信ボタンまで押す処理を書くならここ

つまり、**完全自動化したいなら `post_now()` をこのファイルに追加する** のがいちばん自然です。

## ざっくりした責務分離

- `collector.py`
  - 集めるだけ
- `compose.py`
  - 文章を作るだけ
- `post_x.py`
  - X の UI を触るだけ
- `main.py`
  - 全体の流れをつなぐだけ

## 検証時のおすすめ順

1. まず `main.py --dry-run` で本文だけ確認
2. 次に `open_compose()` で投稿画面に入るか確認
3. その後で `post_now()` を自作して試す
4. 最後に `launchd` に乗せる
