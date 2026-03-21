# chatGPT repository

このリポジトリは、**ChatGPT とファイルをやり取りするための書庫**です。

## 基本ルール

- ChatGPT からファイルをアップする時は、**その日の日付のフォルダー**を使います。
- 日付フォルダー名は、原則として **`YYYY-MM-DD` 形式**にします。
- ファイル名は、**内容がひと目でわかる、できるだけ明快な名前**にします。
- あいまいな名前や、あとから見て判別しにくい名前は避けます。

## 通常ファイルの置き方

通常の単体ファイルは、日付フォルダーの直下に置きます。

例:

```text
2026-03-21/recording_setup_diagram.html
2026-03-21/interview_notes.md
2026-03-21/reference_images.zip
```

## システムやプロジェクト一式を置く場合

システムを作る場合や、複数ファイルから成るプロジェクトを置く場合は、
**日付フォルダーの下にシステム用のフォルダーを作成し、その中に一式を入れます。**

例:

```text
2026-03-21/my-system/
2026-03-21/my-system/README.md
2026-03-21/my-system/src/
2026-03-21/my-system/docs/
2026-03-21/my-system/config/
```

## 命名の考え方

- 何のファイルか分かる名前にする
- できるだけ短く、意味が通る名前にする
- 必要に応じて用途を含める
- 同じ日に複数案がある場合は、末尾に用途や版を付ける
- 可能な限り、**英数字ベースのファイル名**にする

例:

```text
podcast_setup_v1.html
podcast_setup_v2.html
client_brief.md
image_assets.zip
```

## HTML を GitHub に作る時の運用

ユーザーが、たとえば次のような依頼をした場合は、
**HTML生成・GitHubアップロード・GitHub Pages プレビューURL提示までを一連の処理**として扱います。

- 「いまの説明をわかりやすくHTMLでGithubで作ってください」
- 「これをHTML化してGitHubに置いてください」
- 「説明をHTMLにしてプレビューURLも出してください」

### 標準フロー

1. 内容をHTML化する
2. `afrogdesign/chatGPT` にアップする
3. その日の日付フォルダー `YYYY-MM-DD/` を使う
4. ファイル名は内容が分かりやすい英数字ベースにする
5. システム一式の場合は、日付フォルダーの下にプロジェクト用フォルダーを作る
6. アップ後に GitHub Pages のプレビューURLを生成する
7. 最後に、**コマンドボックスでそのままコピーできる形式**でURLを表示する

### 出力形式

```text
GitHub Pages preview:
https://afrogdesign.github.io/chatGPT/YYYY-MM-DD/your_file_name.html
```

### GitHub Pages URL の考え方

GitHub上の `blob` URL はコード閲覧用です。
完成画面として見る時は、`github.io` のURLを使います。

例:

```text
https://github.com/afrogdesign/chatGPT/blob/main/2026-03-21/recording_setup_diagram.html
↓
https://afrogdesign.github.io/chatGPT/2026-03-21/recording_setup_diagram.html
```

## このリポジトリの目的

- ChatGPT とのファイル受け渡しを整理する
- 日付単位で履歴を追いやすくする
- 単体ファイルとシステム一式を混在させず、見通しを良くする
- HTMLファイルを GitHub Pages で見やすく公開できるようにする

---

運用に迷った場合は、まず **日付フォルダーを作る** ことを基本としてください。
