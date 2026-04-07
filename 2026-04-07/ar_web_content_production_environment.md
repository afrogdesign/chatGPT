---
title: "AR Web Content Production Environment 2026"
date: "2026-04-07"
tags:
  - AR
  - WebAR
  - 開発環境
  - 制作環境
  - 3D
---

> [!abstract]
> 2026年4月時点で、**「簡単なARをWebで作る」** なら最有力は **`<model-viewer>` を中心にした 3D表示＋AR起動型** です。
> 画像認識・顔AR・空間演出まで必要なら **ZapWorks**、エンジニア主導で自由度を取り切るなら **8th Wall + three.js / PlayCanvas** が有力です。
> なお、**Adobe Aero は提供終了済み** のため、新規案件の基盤としては外すのが安全です。

## 📋 目次

- [[#🎯 前提整理]]
- [[#🧭 2026年時点の現実的な選択肢]]
- [[#🛠 必要な制作環境]]
- [[#🏗 おすすめ構成 3案]]
- [[#🔄 制作フローの実務設計]]
- [[#⚠️ 注意点]]
- [[#🔗 参考リンク]]
- [[#✅ 結論]]

---

## 🎯 前提整理

「簡単なAR」といっても、実務ではだいたい次の3種類に分かれます。

| 種類 | 内容 | 難易度 | 向く用途 |
|---|---|---:|---|
| 3D配置型 | 商品やキャラクターを床や机の上に置く | 低 | 商品紹介、展示、販促LP |
| 画像認識型 | ポスター・パッケージ・カードを認識してAR表示 | 中 | 印刷連動、イベント、店頭施策 |
| 顔 / 空間演出型 | フィルター、フェイスエフェクト、空間演出 | 中〜高 | SNS拡散、キャンペーン、体験型施策 |

> [!info]
> ここでの提案は **「アプリを新規開発せず、まずは公開まで持っていく」** ことを重視しています。
> そのため、最初の判断軸は **Webで完結させるか / ネイティブARまで踏み込むか** です。

---

## 🧭 2026年時点の現実的な選択肢

まず前提として、**Adobe Aero は 2025年11月で提供終了** しています。
そのため、過去には入り口として有力でしたが、**いま新規案件の基盤にするのは非推奨** です。

また、ブラウザの **WebXR** は依然として互換性確認が必要で、**「素のWebXRだけで全部やる」構成はまだ事故りやすい** です。

そのため、簡単なAR案件では次の整理が現実的です。

| 方式 | いまの評価 | 理由 |
|---|---|---|
| `<model-viewer>` + Quick Look / Scene Viewer | **最有力** | iPhone は Quick Look、Android は Scene Viewer に逃がせるため実務で安定しやすい |
| ZapWorks / Mattercraft | **有力** | ブラウザベースの制作環境があり、画像・顔・ワールド追跡のWebARを比較的短く立ち上げやすい |
| 8th Wall オープンソース | **技術寄りに有力** | 自由度は高いが、制作会社側の実装力が要る |
| Unity AR Foundation | **Web用途では過剰になりやすい** | マルチプラットフォームARアプリには強いが、Webコンテンツとしては重い |

---

## 🛠 必要な制作環境

ARコンテンツ制作で最低限そろえるべき環境は、実務上は次の通りです。

| 区分 | 必要なもの | 役割 |
|---|---|---|
| 3D制作 | **Blender** | モデル作成・調整・アニメーション・glTF出力 |
| Web表示 | **`<model-viewer>`** または **ZapWorks / 8th Wall / three.js系** | Webページ上で3D表示し、AR起動へつなぐ中核 |
| iPhone / iPad 対応 | **USDZ** + **AR Quick Look** | Apple側でのAR表示 |
| Android 対応 | **GLB / glTF** + **Scene Viewer** | Android側でのAR表示 |
| 軽量化 | **glTF Transform** | glTF 2.0 の最適化や一括処理 |
| 公開環境 | **HTTPSホスティング** | WebXRやAR起動の前提条件 |
| テスト端末 | **iPhone 1台 + Android 1台** | Quick Look と Scene Viewer の挙動差分確認 |

> [!tip]
> Web案件なら、**3D制作ツール** と **AR再生方式** を分けて考えると整理しやすいです。
> つまり、**作るのは Blender**、**見せるのは `<model-viewer>` / ZapWorks / 8th Wall** です。

---

## 🏗 おすすめ構成 3案

### 1. 最短で公開したいなら

| 項目 | 提案 |
|---|---|
| 構成 | **Blender → GLB / USDZ → `<model-viewer>` → 既存サイト公開** |
| 向く案件 | 商品AR、立体物の配置、展示用、簡易プロモーション |
| 長所 | 実装が軽く、既存LPやCMSに載せやすい |
| 短所 | 画像認識・顔AR・複雑な演出には弱い |

この構成が強い理由は、`<model-viewer>` が **WebXR / Scene Viewer / Quick Look** を扱え、Androidは Scene Viewer、iOSは Quick Look に寄せられるからです。
**「簡単なARをWebに載せる」** という意味では、いま最も事故が少ない選択です。

---

### 2. 印刷物連動や顔ARをやりたいなら

| 項目 | 提案 |
|---|---|
| 構成 | **Mattercraft / ZapWorks + Universal AR SDK** |
| 向く案件 | ポスター認識、パッケージAR、フェイスフィルター、販促キャンペーン |
| 長所 | ブラウザベースの制作環境があり、画像・顔・ワールド追跡まで揃う |
| 短所 | 商用になると月額コストが乗る |

ZapWorks は **ブラウザベースの3D制作環境 Mattercraft** を持ち、Universal AR SDK では **image / face / world tracking** を提供しています。
小〜中規模の販促案件では、**開発工数を圧縮しやすい商用WebAR基盤** です。

---

### 3. エンジニア主導で自由度を最大化したいなら

| 項目 | 提案 |
|---|---|
| 構成 | **8th Wall Engine + three.js / PlayCanvas / Babylon.js** |
| 向く案件 | 演出多め、独自UI、ゲーム寄り、細かいカスタム制御 |
| 長所 | 自由度が高く、World / Image / Face 系を深く作れる |
| 短所 | 自己ホスト前提で、制作会社側の技術力が必要 |

8th Wall は現在、**ツールとエンジン自体は無料のオープンソース利用へ移行** しています。
つまり、**安くなったが“簡単になった”わけではない** という理解が正確です。

> [!warning]
> 8th Wall は以前より導入障壁は下がりましたが、
> **「いまから誰でも簡単」ではなく「自己責任で組めるチームなら強い」** 側に寄っています。

---

## 🔄 制作フローの実務設計

実際の進め方は、次の流れがもっとも素直です。

| Step | 作業 | 実務ポイント |
|---|---|---|
| 1 | 3Dモデル作成 | Blenderでモデリング・材質調整・必要ならアニメーション作成 |
| 2 | Web用書き出し | Android / Web側は GLB / glTF を基本にする |
| 3 | Apple用書き出し | iPhone / iPad向けには USDZ を用意する |
| 4 | 軽量化 | glTF Transform で最適化・一括処理・修正を行う |
| 5 | ページ実装 | まずは `<model-viewer>` で載せる。画像認識が要るなら ZapWorks へ |
| 6 | 公開 | HTTPS 必須。WebXRを使うなら埋め込み条件も確認 |
| 7 | 実機検証 | iPhone と Android の両方で AR 起動導線を確認する |

---

## ⚠️ 注意点

> [!warning]
> **WebXRのみ依存** はまだ危険です。
> 本番案件では、**Quick Look / Scene Viewer の逃げ道を持つ構成** が安全です。

> [!warning]
> **iPhoneとAndroidで必要ファイルが違う** 点を最初から設計に入れるべきです。
> Apple側は **USDZ + Quick Look**、Android側は **glTF / GLB + Scene Viewer** が基本です。

> [!tip]
> Android Scene Viewer では、**モデル軽量化** がかなり重要です。
> 三角形数やファイルサイズを抑えないと、表示品質より先に体験が破綻します。

> [!note]
> もし案件が **位置情報AR / 店舗回遊 / 現地固定配置** に進むなら、Webよりも **Unity AR Foundation + ARCore Geospatial Creator** のようなネイティブ寄り構成のほうが筋が良いです。

---

## 🔗 参考リンク

- Adobe Aero End of Support FAQ  
  https://helpx.adobe.com/aero/aero-end-of-support-faq.html

- model-viewer AR examples  
  https://modelviewer.dev/examples/augmentedreality/

- Apple AR Quick Look  
  https://developer.apple.com/augmented-reality/quick-look/

- Google Scene Viewer  
  https://developers.google.com/ar/develop/scene-viewer?hl=ja

- MDN WebXR Device API  
  https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API

- Blender glTF 2.0 exporter  
  https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html

- glTF Transform  
  https://gltf-transform.dev/

- ZapWorks Mattercraft  
  https://zap.works/mattercraft/

- 8th Wall  
  https://www.8thwall.com/

- Unity AR Foundation  
  https://docs.unity3d.com/6000.6/Documentation/Manual/com.unity.xr.arfoundation.html

---

## ✅ 結論

| やりたいこと | 最適解 | 制作負荷 | ひと言評価 |
|---|---|---:|---|
| まず1本、簡単なARをWeb公開したい | **`<model-viewer>` + GLB / USDZ** | 低 | いちばん現実的。最初の1本はこれで良い |
| パッケージ認識・顔AR・販促演出をしたい | **ZapWorks / Mattercraft** | 中 | 制作会社案件として回しやすい |
| 将来的に独自演出やゲーム性を強くしたい | **8th Wall + three.js / PlayCanvas** | 高 | 強いが、技術体制が前提 |
| アプリ前提で本格ARに行きたい | **Unity AR Foundation** | 高 | Web案件の枠を超えるなら候補 |

> [!abstract]
> プロデューサー視点での最終提案はこれです。
> **最初の案件は `<model-viewer>` で始める。**
> **画像認識や顔ARが必要になったら ZapWorks。**
> **独自性を最大化したくなったら 8th Wall / three.js 系へ進む。**
