# CODEX CLI フル権限まわりまとめ

## 目次
- [[#結論]]
- [[#基本コマンド]]
- [[#設定の意味]]
- [[#おすすめ運用]]
- [[#恒久設定 config.toml]]
- [[#alias 例]]
- [[#注意点]]

## 結論

確認メッセージをできるだけ出さずに自動で進めたい場合は、まず以下を使う。

```bash
codex -a never --sandbox danger-full-access
```

これが実運用ではいちばん現実的。

超危険だが、承認と sandbox をまとめて強く外すモードもある。

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

別名:

```bash
codex --yolo
```

---

## 基本コマンド

### 1. 確認だけ消す

```bash
codex -a never
```

意味:
- 承認プロンプトを出さない
- ただし sandbox 制限は残る

### 2. かなりフルアクセス寄り

```bash
codex -a never --sandbox danger-full-access
```

意味:
- 承認プロンプトを出さない
- sandbox を強い制限なしに近い状態へ
- 実運用で使うならこのあたりが本命

### 3. 完全解除レベル

```bash
codex --dangerously-bypass-approvals-and-sandbox
```

または

```bash
codex --yolo
```

意味:
- 承認も sandbox もまとめて強く解除
- かなり危険
- 検証用VMや捨て環境向け

---

## 設定の意味

### `-a never`
- approval policy を `never` にする
- 確認ダイアログを出さない
- ただし「何ができるか」は sandbox 次第

### `--sandbox danger-full-access`
- 強い sandbox 制限を外す寄りの設定
- ローカルでかなり自由に動きやすくなる

### `--dangerously-bypass-approvals-and-sandbox`
- 承認と sandbox をまとめてバイパス
- 事故った時の被害が大きい

### `--full-auto` との違い
`--full-auto` は名前ほどフル権限ではない。

実態は概ね以下のショートカット。

- `workspace-write`
- `on-request`

つまり:
- 作業フォルダ内はやりやすい
- ただし外部や危険操作では確認が残る

---

## おすすめ運用

### 普段使い

```bash
codex -a never --sandbox danger-full-access
```

向いている場面:
- 自分の管理しているローカル作業
- 毎回確認がうるさいとき
- でも `--yolo` までは行きたくないとき

### 危険テスト環境専用

```bash
codex --yolo
```

向いている場面:
- 使い捨て環境
- VM
- 壊れてもよい検証環境

---

## 恒久設定 config.toml

毎回打ちたくないなら、ユーザー設定に書く。

保存場所:

```bash
~/.codex/config.toml
```

例:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

これで毎回オプションを打たずに済む。

---

## alias 例

`~/.zshrc` に入れる例。

```bash
alias codexall='codex -a never --sandbox danger-full-access'
alias codexyolo='codex --dangerously-bypass-approvals-and-sandbox'
```

反映:

```bash
source ~/.zshrc
```

以後は:

```bash
codexall
```

または

```bash
codexyolo
```

で起動できる。

---

## 注意点

- `-a never` だけでは sandbox 制限は残る
- `--full-auto` は完全フル権限ではない
- `--yolo` は本当に危険
- 組織ポリシーや `requirements.toml` で禁止されている場合がある
- 重要データがある本番Macで `--yolo` はあまりおすすめしない

---

## ひとことで

日常運用ならこれ。

```bash
codex -a never --sandbox danger-full-access
```

本当に全部外すのはこれ。

```bash
codex --yolo
```

ただし、後者は隔離環境前提。
