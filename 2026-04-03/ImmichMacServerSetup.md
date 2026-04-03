---
title: ImmichMacServerSetup
date: 2026-04-03
tags:
  - immich
  - mac-server
  - docker
  - iphone-photo-backup
  - obsidian
---

> [!abstract]
> iMac を Immich の受け皿として構築すれば、iPhone の写真を自動でバックアップする自前サーバーを作れます。
> 最短構成は **Docker Desktop + Immich 公式 Docker Compose** です。
> 実運用では、**写真本体は外付け APFS ストレージ**、**DB は内蔵 SSD 側** に分けるのが安全です。
> このノートでは、Mac で Immich を立てる手順を、迷いにくい順番でまとめています。

---

## 📋 目次

- [[#✅ 先に結論]]
- [[#🧱 おすすめ構成]]
- [[#🔍 事前確認]]
- [[#📦 Docker Desktop を入れる]]
- [[#📁 保存先を決める]]
- [[#⬇️ Immich の公式ファイルを取得する]]
- [[#✏️ .env を編集する]]
- [[#▶️ Immich を起動する]]
- [[#📱 iPhone から写真をバックアップする]]
- [[#💾 バックアップと更新]]
- [[#⚠️ Mac でハマりやすい点]]
- [[#🧩 既存の写真フォルダを後から読ませる方法]]
- [[#✅ 最後にやること一覧]]

---

## ✅ 先に結論

| 項目 | 推奨内容 |
|---|---|
| 構築方法 | Docker Desktop + 公式 Docker Compose |
| 写真・動画の保存先 | 外付け SSD / HDD（APFS 推奨） |
| データベース保存先 | 内蔵 SSD 側 |
| iPhone 連携 | Immich iOS アプリ |
| 最初の接続 | 家の LAN 内だけで確認 |
| 外部アクセス | 動作確認後に追加 |

Immich を Mac 上で受け皿として使うなら、最短かつ無難なのは **Docker Desktop で公式構成をそのまま動かす方法** です。

重要なのは、保存先を最初から分けることです。

- **写真本体** は大容量ストレージへ
- **DB** は安定したローカルディスクへ

これで、容量の拡張性と運用の安定性の両方を確保しやすくなります。

> [!tip]
> 「まず動かす」ことを優先するなら、最初は **LAN 内だけ** で組むのが安全です。
> 外部公開や独自ドメインは、動作確認後に追加した方が事故りにくいです。

---

## 🧱 おすすめ構成

### 構成イメージ

```text
iPhone
  ↓ Immichアプリで自動バックアップ
Mac Server (Docker Desktop)
  ├─ Immich Server
  ├─ PostgreSQL
  └─ Redis
       ↓
  写真保存先: /Volumes/PhotoVault/immich-media
  DB保存先:   ~/immich-server/postgres
```

### 構成の考え方

| 役割 | 保存先 | 理由 |
|---|---|---|
| 写真・動画の実体 | 外付けストレージ | 容量を増やしやすい |
| データベース | 内蔵 SSD | 安定性と速度を確保しやすい |
| 設定ファイル | ホームディレクトリ配下 | 管理しやすい |

> [!note]
> DB はファイルシステム依存の地雷を踏みやすいので、**とりあえず全部外付けに置く** より、
> **DBだけは内蔵SSD側** に寄せた方が安全です。

---

## 🔍 事前確認

まず確認するべきなのは次の3点です。

| 確認項目 | 目安 |
|---|---|
| macOS | Docker Desktop のサポート対象であること |
| CPU / RAM | 2コア以上 / メモリ6GB以上が目安 |
| 保存先ディスク | APFS 推奨 |

確認コマンドです。

```bash
sw_vers
uname -m
```

### ここで見るポイント

- `sw_vers` で macOS バージョンを確認
- `uname -m` で `arm64` か `x86_64` を確認

> [!info]
> Apple Silicon でも Intel Mac でも基本手順はほぼ同じです。
> ただし性能面では、重い動画処理は CPU に寄りやすいです。

---

## 📦 Docker Desktop を入れる

Mac Server 上で Immich を動かすには、まず Docker Desktop を入れます。

### インストール後の確認

```bash
docker --version
docker compose version
```

この2つが通れば、Immich を起動する前提が整っています。

> [!warning]
> `docker compose` が使えない状態では先へ進まない方がいいです。
> Immich は `docker-compose` ではなく、**`docker compose`** 前提です。

---

## 📁 保存先を決める

まず、Immich 用の作業ディレクトリと、写真保存先を決めます。

### 推奨例

| 用途 | パス例 |
|---|---|
| Immich 作業ディレクトリ | `~/immich-server` |
| 写真保存先 | `/Volumes/PhotoVault/immich-media` |

作成コマンドです。

```bash
mkdir -p ~/immich-server
mkdir -p /Volumes/PhotoVault/immich-media
```

### この分け方の意味

- `~/immich-server` に設定や compose を置く
- `/Volumes/PhotoVault/immich-media` に写真本体を置く
- DB はあとで `~/immich-server/postgres` に置く

> [!tip]
> 外付けディスク名は自分の環境に合わせて置き換えてください。
> `PhotoVault` は例です。

---

## ⬇️ Immich の公式ファイルを取得する

公式の `docker-compose.yml` と `.env` を取得します。

```bash
cd ~/immich-server

curl -L -o docker-compose.yml \
  https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml

curl -L -o .env \
  https://github.com/immich-app/immich/releases/latest/download/example.env
```

これで、Immich の基本構成ファイルが揃います。

---

## ✏️ `.env` を編集する

まず `.env` を開きます。

```bash
cd ~/immich-server
nano .env
```

### 最低限変更する項目

```dotenv
UPLOAD_LOCATION=/Volumes/PhotoVault/immich-media
DB_DATA_LOCATION=/Users/YOURNAME/immich-server/postgres
TZ=Asia/Tokyo
IMMICH_VERSION=v2
DB_PASSWORD=ImmichDbPass2026
```

### 各項目の意味

| 項目 | 意味 |
|---|---|
| `UPLOAD_LOCATION` | 写真・動画の保存先 |
| `DB_DATA_LOCATION` | PostgreSQL の保存先 |
| `TZ` | タイムゾーン |
| `IMMICH_VERSION` | 利用するバージョン系統 |
| `DB_PASSWORD` | DB の認証パスワード |

### 自分の環境に合わせて直す場所

- `YOURNAME` は自分の macOS ユーザー名に変更
- `PhotoVault` は実際の外付けディスク名に変更

### nano の保存方法

```text
Control + O → Enter → Control + X
```

> [!warning]
> `.env` を変更しただけでは反映されません。
> 変更後は再度 `docker compose up -d` を実行する必要があります。

---

## ▶️ Immich を起動する

起動コマンドです。

```bash
cd ~/immich-server
docker compose up -d
```

### 状態確認

```bash
docker compose ps
docker compose logs -f
```

### ブラウザで開くURL

```text
http://<MacのIPアドレス>:2283
```

LAN 内の IP を確認する例です。

```bash
ipconfig getifaddr en0
```

> [!info]
> 最初に登録したユーザーが管理者になります。
> まずはブラウザでログインできることを確認してください。

---

## 📱 iPhone から写真をバックアップする

サーバーが起動したら、iPhone 側で Immich アプリを設定します。

### 手順

1. Immich iOS アプリをインストールする
2. サーバー URL に `http://<MacのIPアドレス>:2283` を入れる
3. ログインする
4. バックアップしたいアルバムを選ぶ
5. **Enable Backup** を有効化する

### 最初のおすすめ

いきなり全写真で試すより、先に少数のアルバムで確認した方が安全です。

| テスト方法 | 理由 |
|---|---|
| 10枚くらいの小さいアルバムで試す | 動作確認しやすい |
| Wi-Fi接続時のみで試す | 失敗時の切り分けが楽 |
| 先に保存先フォルダを見る | 実際に入っているか確認できる |

> [!tip]
> まずは「少数で成功すること」を確認し、その後に全体へ広げると安心です。

---

## 💾 バックアップと更新

Immich は写真の受け皿として使えますが、**それ自体もバックアップ対象** です。

### バックアップで分けて考えるもの

| 対象 | 中身 | 対応 |
|---|---|---|
| DB | ユーザー情報・メタデータ | Immich側のDBバックアップ |
| 写真本体 | 画像・動画ファイル | 別途バックアップ必須 |

### 更新コマンド

```bash
cd ~/immich-server
docker compose pull && docker compose up -d
docker image prune
```

> [!warning]
> DBバックアップだけでは写真本体は守れません。
> `UPLOAD_LOCATION` 側のディレクトリを、別ディスクや別バックアップ先へ複製する運用が必要です。

---

## ⚠️ Mac でハマりやすい点

### 1. Docker の容量が膨らむ

Docker Desktop はイメージやコンテナを内部ディスクイメージにまとめて持つため、放置すると容量を食いやすいです。

### 2. 動画処理が重い

Mac Server 上の Immich は、動画の変換やサムネイル生成で CPU に寄りやすく、古い iMac では重く感じることがあります。

### 3. 外付けディスクの形式が不適切

特に DB 側は、雑なファイルシステム選択でトラブルになりやすいです。

### 4. 最初から外部公開しようとして詰まる

ローカル確認前に公開設定まで一気にやると、切り分けが難しくなります。

> [!danger]
> **「DBも写真も全部 exFAT 外付けに置く」**
> これは避けた方がいいです。
> 最低でも **DB は内蔵 SSD 側** に置く方が安全です。

---

## 🧩 既存の写真フォルダを後から読ませる方法

すでに Mac 側に大量の写真フォルダがある場合は、今後 iPhone から入る写真とは別に、既存アーカイブを読ませたいことがあります。

その場合は、考え方を次のように分けると整理しやすいです。

| 種類 | 入れ方 |
|---|---|
| 今後 iPhone から入る写真 | 通常のバックアップ先へ保存 |
| 過去に持っている大量アーカイブ | 外部ライブラリとして追加 |

これにより、

- 新規流入分
- 過去アーカイブ分

を混ぜずに扱いやすくなります。

> [!note]
> 最初から全部一気に混ぜるより、
> **新規バックアップ系統** と **既存アーカイブ系統** を分けて考えた方が運用しやすいです。

---

## ✅ 最後にやること一覧

| 手順 | やること |
|---|---|
| 1 | Docker Desktop をインストールする |
| 2 | `~/immich-server` を作る |
| 3 | 外付け保存先を作る |
| 4 | 公式 `docker-compose.yml` と `.env` を取得する |
| 5 | `.env` のパスとタイムゾーンを編集する |
| 6 | `docker compose up -d` で起動する |
| 7 | ブラウザで `:2283` にアクセスする |
| 8 | iPhone の Immich アプリでバックアップを有効化する |
| 9 | 写真保存先のバックアップ方針も作る |

> [!abstract]
> まずは **LAN 内で動かすこと**、次に **iPhone から写真が入ること**、最後に **写真本体のバックアップを別で持つこと**。
> この順番で進めると、Mac Server を Immich の受け皿として安定させやすいです。
