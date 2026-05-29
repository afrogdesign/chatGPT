# 他社制作会社経由デプロイ用ZIP作成指示

更新日: 2026-05-29 JST

## 目的

北川鉄工所リクルート簡易CMSを、本番ドメイン `kiw.co.jp/recruit/` 以下へ反映するため、他社制作会社へ渡す納品ZIPを作成する。

今回はAFROGから本番FTPへ直接アップロードしない。北川鉄工所様経由で、サーバー管理会社・制作会社へZIPを渡し、`/recruit/` 以下へ展開・上書きしてもらう。

## CODEXの最重要ルール

- 本番FTPアップロードはしない。
- Apps Script deploy はしない。
- クライアントへメール送信しない。
- 秘密情報をZIPへ入れない。
- GitHub repo内にも秘密情報を書かない。
- `.git/`、`.DS_Store`、作業ログ、ローカル設定ファイルはZIPに入れない。
- ZIP作成前に `git status --short --branch` を確認する。

## 納品ZIPの基本方針

ZIPは、制作会社が `kiw.co.jp/recruit/` 以下へそのままアップロードしやすい構造にする。

推奨ZIP名:

```text
kiw_recruit_deploy_20260529.zip
```

ZIP内の推奨ルート:

```text
recruit/
```

制作会社への説明では、ZIP内の `recruit/` 配下を、本番サーバーの `kiw.co.jp/recruit/` 配下へ反映してもらう。

## ZIPに含める対象

現時点でGit管理されている `site_data/recruit/` を基準にする。

最低限含める対象:

```text
site_data/recruit/recruitment/new.html
site_data/recruit/highschool.html
site_data/recruit/number.html
site_data/recruit/work_support.html
site_data/recruit/preview/recruitment/new.html
site_data/recruit/preview/highschool.html
site_data/recruit/preview/number.html
site_data/recruit/preview/work_support.html
site_data/recruit/manage/index.html
site_data/recruit/manage/new.html
site_data/recruit/manage/highschool.html
site_data/recruit/manage/number.html
site_data/recruit/manage/work_support.html
site_data/recruit/assets/js/recruit-cms.js
site_data/recruit/assets/js/recruit-cms-config.js
site_data/recruit/assets/js/recruit-manage.js
site_data/recruit/assets/css/recruit-manage.css
site_data/recruit/assets/api/publish-json.php
site_data/recruit/assets/data/recruit-cms-fallback.json
site_data/recruit/assets/data/published/new.json
site_data/recruit/assets/data/published/highschool.json
site_data/recruit/assets/data/published/number.json
site_data/recruit/assets/data/published/work_support.json
```

ただし、既存デザインCSS・画像・共通JSが `site_data/recruit/inc/` などに存在し、今回の本番反映先にまだ存在しない可能性がある場合は、必ず人間確認を挟むこと。

## ZIPに入れないもの

```text
.git/
.github/
.vscode/
.DS_Store
node_modules/
apps_script/
docs/
build/
スプレッドシート/
設計書/
*.md
```

ただし、制作会社向け説明用にZIP直下へ `README_DEPLOY.txt` を入れるのは可。

## ZIP内に同梱する README_DEPLOY.txt

ZIPには、制作会社向けの短い説明ファイルを同梱すること。

ファイル名:

```text
README_DEPLOY.txt
```

内容案:

```text
北川鉄工所 採用サイト更新ファイル一式

このZIPは、kiw.co.jp/recruit/ 以下へ反映するための更新ファイルです。

作業前に、既存の /recruit/ ディレクトリをバックアップしてください。

反映先:
kiw.co.jp/recruit/

作業内容:
ZIP内の recruit/ 配下を、本番サーバーの /recruit/ 配下へ上書きしてください。

主な更新内容:
- 採用関連4ページのHTML
- プレビュー画面
- 管理画面
- CMS用 JavaScript / CSS
- 公開JSON
- 公開保存用API

注意:
- /recruit/ 以外のディレクトリは更新しないでください。
- 既存ファイルのバックアップ後に反映してください。
- FTP転送時は、テキストファイルの文字コードが変わらないようにしてください。
- PHPが実行できる状態で assets/api/publish-json.php が配置されている必要があります。

反映後の確認URL:
https://www.kiw.co.jp/recruit/recruitment/new.html
https://www.kiw.co.jp/recruit/highschool.html
https://www.kiw.co.jp/recruit/number.html
https://www.kiw.co.jp/recruit/work_support.html
https://www.kiw.co.jp/recruit/manage/index.html

以上です。
```

## CODEX作業手順

1. `main` を最新化する。
2. `git status --short --branch` を確認する。
3. 必要であれば、未反映PRや作業ブランチがないか確認する。
4. `site_data/recruit/` を元に、一時ディレクトリを作る。
5. 一時ディレクトリ内に `recruit/` を作り、対象ファイルを配置する。
6. ZIP直下に `README_DEPLOY.txt` を入れる。
7. ZIPを作成する。
8. ZIPの中身一覧を出力し、不要ファイルが入っていないか確認する。
9. `docs/handoffs/` に作業結果ログを残す。
10. ZIPファイル名、作成日時、含有ファイル数、確認結果を報告する。

## 推奨コマンド例

```zsh
cd /Users/marupro/CODEX/kiw-recruit-cms

git checkout main
git pull --ff-only origin main
git status --short --branch

rm -rf dist/vendor_deploy
mkdir -p dist/vendor_deploy/recruit

rsync -av \
  --exclude='.DS_Store' \
  --exclude='.git' \
  --exclude='docs' \
  --exclude='build' \
  --exclude='apps_script' \
  site_data/recruit/ dist/vendor_deploy/recruit/

cat > dist/vendor_deploy/README_DEPLOY.txt <<'EOF'
北川鉄工所 採用サイト更新ファイル一式

このZIPは、kiw.co.jp/recruit/ 以下へ反映するための更新ファイルです。

作業前に、既存の /recruit/ ディレクトリをバックアップしてください。

反映先:
kiw.co.jp/recruit/

作業内容:
ZIP内の recruit/ 配下を、本番サーバーの /recruit/ 配下へ上書きしてください。

主な更新内容:
- 採用関連4ページのHTML
- プレビュー画面
- 管理画面
- CMS用 JavaScript / CSS
- 公開JSON
- 公開保存用API

注意:
- /recruit/ 以外のディレクトリは更新しないでください。
- 既存ファイルのバックアップ後に反映してください。
- FTP転送時は、テキストファイルの文字コードが変わらないようにしてください。
- PHPが実行できる状態で assets/api/publish-json.php が配置されている必要があります。

反映後の確認URL:
https://www.kiw.co.jp/recruit/recruitment/new.html
https://www.kiw.co.jp/recruit/highschool.html
https://www.kiw.co.jp/recruit/number.html
https://www.kiw.co.jp/recruit/work_support.html
https://www.kiw.co.jp/recruit/manage/index.html

以上です。
EOF

cd dist/vendor_deploy
zip -r ../kiw_recruit_deploy_20260529.zip . -x '*.DS_Store'
cd ../..

unzip -l dist/kiw_recruit_deploy_20260529.zip
```

## ZIP作成後の確認ポイント

ZIP内に以下があること。

```text
README_DEPLOY.txt
recruit/recruitment/new.html
recruit/highschool.html
recruit/number.html
recruit/work_support.html
recruit/preview/recruitment/new.html
recruit/preview/highschool.html
recruit/preview/number.html
recruit/preview/work_support.html
recruit/manage/index.html
recruit/manage/new.html
recruit/manage/highschool.html
recruit/manage/number.html
recruit/manage/work_support.html
recruit/assets/js/recruit-cms.js
recruit/assets/js/recruit-cms-config.js
recruit/assets/js/recruit-manage.js
recruit/assets/css/recruit-manage.css
recruit/assets/api/publish-json.php
recruit/assets/data/recruit-cms-fallback.json
recruit/assets/data/published/new.json
recruit/assets/data/published/highschool.json
recruit/assets/data/published/number.json
recruit/assets/data/published/work_support.json
```

ZIP内に以下がないこと。

```text
.git
.DS_Store
docs/
build/
apps_script/
スプレッドシート/
設計書/
```

## 制作会社へ依頼する内容

北川鉄工所様経由で、制作会社へ以下を依頼する。

- ZIP内の `recruit/` 配下を `kiw.co.jp/recruit/` 以下へ反映。
- 反映前に既存 `/recruit/` のバックアップを取得。
- `/recruit/` 以外は触らない。
- 反映後に4ページと管理画面の表示確認。

## 反映後に人間が確認するURL

```text
https://www.kiw.co.jp/recruit/recruitment/new.html
https://www.kiw.co.jp/recruit/highschool.html
https://www.kiw.co.jp/recruit/number.html
https://www.kiw.co.jp/recruit/work_support.html
https://www.kiw.co.jp/recruit/manage/index.html
```

確認内容:

- ページが404にならない。
- CSSと画像が崩れていない。
- `[br]` や `[em]` が文字として露出しない。
- `/` が通常文字として表示される。
- 管理画面が開く。
- 公開処理は、公開トークン設定後に別途確認する。

## CODEXへの最初の指示

```text
このrepoの docs/handoffs/2026-05-29_vendor_deploy_zip_instructions.md を読んでください。

目的は、kiw.co.jp/recruit/ 以下へ他社制作会社経由で反映してもらうための納品ZIPを作成することです。

本番FTPアップロードはしないでください。
Apps Script deploy はしないでください。
クライアントへメール送信しないでください。
秘密情報をZIPやrepoへ入れないでください。

main を最新化し、site_data/recruit/ を元に dist/kiw_recruit_deploy_20260529.zip を作成してください。
ZIP内は recruit/ をルートにし、制作会社向け README_DEPLOY.txt を同梱してください。

ZIP作成後、unzip -l で中身一覧を確認し、不要ファイルが入っていないことを報告してください。
```
