# xbot

API を使わず、Web ページ取得 + ブラウザ自動操作で X に定時投稿するための雛形です。

## できること

- `config.yaml` で指定したテーマの情報を RSS / HTML から収集
- 収集結果を 1 本の投稿文に整形
- Playwright で X の投稿画面を開いて自動投稿
- macOS の `launchd` で **毎日 8:00 / 18:00** に実行

## 重要な注意

- これは **X API を使わないブラウザ自動化** です。
- X 側の画面変更、追加認証、Bot 判定で止まることがあります。
- サービス規約・運用リスクは必ず自分で確認してください。
- 最初は `.env` の `DRY_RUN=true` のまま試してください。

## ディレクトリ

```text
xbot/
├─ .env.example
├─ config.example.yaml
├─ requirements.txt
├─ README.md
├─ launchd/
│  └─ com.afrog.xbot.plist
├─ scripts/
│  ├─ install_launchd.sh
│  └─ run_once.sh
└─ src/
   ├─ collector.py
   ├─ compose.py
   ├─ main.py
   └─ post_x.py
```

## 使い方

### 1. 設定ファイル作成

```bash
cd 2026-03-21/xbot
cp .env.example .env
cp config.example.yaml config.yaml
```

`config.yaml` の `topic_name` と `sources` を、集めたいテーマに合わせて変更します。

例:

```yaml
topic_name: "写真"
sources:
  - type: rss
    name: "Google News"
    url: "https://news.google.com/rss/search?q=写真&hl=ja&gl=JP&ceid=JP:ja"
```

### 2. 初回ログイン

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python src/post_x.py --setup --headed
```

ブラウザが開いたら、X に手動ログインしてください。ログイン情報は `runtime/x_profile/` に保存されます。

### 3. 本文だけ確認

```bash
python src/main.py --dry-run
```

### 4. 実投稿

`.env` の `DRY_RUN=false` に変更してから実行:

```bash
python src/main.py --headed
```

### 5. 定時実行を登録

```bash
./scripts/install_launchd.sh
```

## 仕組み

1. `collector.py` が RSS / HTML から候補を収集
2. `compose.py` が投稿文を組み立て
3. `post_x.py` が Playwright で投稿画面を操作
4. `launchd` が 8:00 / 18:00 に `run_once.sh` を起動

## よくある詰まりどころ

- 投稿ボックスが見つからない
  - X 側 UI 変更、ログイン切れ、認証追加の可能性
- 急に止まる
  - Bot 判定や確認画面の可能性
- 文字数超過
  - `config.yaml` の `max_post_length` を減らす

## 実運用のおすすめ

- 最初の数日は `DRY_RUN=true` で本文だけ確認
- いきなり完全自動化せず、まずは半自動で精度を見る
- 1 テーマにつき 1 ボットに分ける
