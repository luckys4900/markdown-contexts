---
title: "claudecode-douga"
date: "2026-04-28T08:23:05.683Z"
source: "C:\Users\ライズコーポレーション\Desktop\context\exports\claudecode-douga.txt"
category: "tools"
---

了解しました。公式ドキュメントとGitHubの最新情報をもとに、**導入→運用→マネタイズ**の順で、実手順付きの完全ガイドを書きます。

---

# Claude Code × HeyGen Hyperframes 完全実践ガイド
## ──導入・運用・マネタイズの全手順

---

## PART 1｜導入編：環境構築から最初の動画出力まで

---

### ステップ0：前提確認（所要時間：5分）

まず、手元の環境を確認します。必要なものは3つだけです。

**必要なもの一覧**

| ツール | バージョン | 役割 |
|--------|-----------|------|
| Node.js | 22以上 | JavaScriptの実行基盤 |
| FFmpeg | 最新版 | 動画エンコード |
| Claude Code | 最新版 | AIエージェント本体 |

---

### ステップ1：Node.js・FFmpeg・Claude Codeのインストール

**Node.js（v22以上）**

```bash
# Mac（Homebrewを使う場合）
brew install node

# バージョン確認
node --version
# → v22.x.x 以上が出ればOK
```

```bash
# Windows（公式サイトからLTSをダウンロード）
# https://nodejs.org/ja/download
```

**FFmpeg**

```bash
# Mac
brew install ffmpeg

# Ubuntu / Debian系Linux
sudo apt install ffmpeg

# Windows（Chocolateyを使う場合）
choco install ffmpeg

# バージョン確認
ffmpeg -version
```

**Claude Code**

```bash
# npmでインストール
npm install -g @anthropic-ai/claude-code

# またはclaude.com/downloadからGUIインストーラを使う
```

---

### ステップ2：Hyperframesスキルをインストールする（2つの方法）

HyperFramesとGSAPのスキルをAIコーディングツールにインストールするには以下のコマンドを使います。

**方法A：Hyperframes CLI経由でインストール（推奨）**

Claude Code、Gemini CLI、Codex CLIすべてに一括インストールするには：

```bash
npx hyperframes skills
```

特定のツールだけに入れる場合は：

```bash
npx hyperframes skills --claude    # Claude Codeだけ
npx hyperframes skills --cursor    # Cursorだけ
npx hyperframes skills --claude --gemini  # 両方
```

**方法B：skills CLIで直接インストール**

```bash
npx skills add heygen-com/hyperframes
```

> ⚠️ **よくあるエラー対処**
> `git-lfs`関連のエラーが出た場合、v0.4.5以降のCLIであれば自動的に`GIT_CLONE_PROTECTION_ACTIVE=0`が設定されます。もし`npx skills add heygen-com/hyperframes`を直接使った場合は：
> ```bash
> GIT_CLONE_PROTECTION_ACTIVE=0 npx skills add heygen-com/hyperframes
> ```

---

### ステップ3：スキルが正しく入ったか確認する

Claude Codeを一度再起動してから、ターミナルで起動します。

```bash
claude
```

Claude Codeでは、スキルがスラッシュコマンドとして登録されます。
- `/hyperframes` → コンポジション（動画）の作成
- `/hyperframes-cli` → CLIコマンドのヘルプ
- `/gsap` → アニメーションの補助

これら3つが使えれば、セットアップ完了です。

---

### ステップ4：最初のプロジェクトを作る

エージェントモード（デフォルト）では`--example`フラグが必須です。

```bash
# エージェントモード（Claude Codeに全部任せる場合）
npx hyperframes init my-video --example blank

# 人間が対話しながら設定する場合
npx hyperframes init --human-friendly
```

既存の動画ファイルをベースにする場合：


```bash
npx hyperframes init my-video --example warm-grain --video ./intro.mp4
```
`--video`または`--audio`を指定すると、CLIが自動的にWhisperで音声を文字起こしして、字幕をコンポジションに組み込みます（`--skip-transcribe`で無効化可能）。

**プロジェクトフォルダに移動**

```bash
cd my-video
```

---

### ステップ5：ブラウザプレビューを立ち上げる


```bash
npx hyperframes preview
```
このコマンドでHyperframes Studioが立ち上がり、ブラウザでコンポジションが表示されます。`index.html`の編集を保存すると自動でリロードされます。ホットリロード対応なので、HTMLファイルを保存した瞬間にプレビューが更新されます。

ブラウザで `http://localhost:3002` が開けばOKです。

---

### ステップ6：Claude Codeに最初の動画を書かせる

プロジェクトフォルダをClaude Codeで開いた状態で、こう話しかけます：

```
/hyperframes を使って、10秒のプロダクト紹介動画を作ってほしい。
ダークな背景にタイトルが左からフェードインで入ってきて、
最後の2秒でキャッチコピーが下から出てくる。BGMは落ち着いた雰囲気で。
1920x1080、16:9。
```

> 💡 **必ず `/hyperframes` をコマンド先頭に入れること**
> スキルはHyperframes固有のルール（`class="clip"`の必須化、GSAPタイムラインの登録、`data-*`属性のセマンティクスなど）をエンコードしており、一般的なWebのドキュメントには含まれていません。スラッシュコマンドなしで頼むと、ルール違反のコードが生成されます。

---

### ステップ7：レンダリングしてMP4を出力する


```bash
# 通常レンダリング（高品質）
npx hyperframes render

# ドラフト品質（高速、確認用）
npx hyperframes render --quality draft

# 動画ファイルが重いコンポジションで安定して動かしたいとき
npx hyperframes render --workers 1
```

出力先は `./renders/output.mp4` です。

---

### ステップ8：問題が起きたらlintで原因特定


```bash
# 基本的なlint
npx hyperframes lint ./my-composition

# CI/ツール向けJSON出力
npx hyperframes lint ./my-composition --json

# 情報レベルの警告も含めて確認
npx hyperframes lint ./my-composition --verbose
```

エラーメッセージをそのままClaude Codeに貼ると、自動で修正してくれます。

---

## PART 2｜運用編：日常的な動画制作を自動化するまで

---

### 運用パターン①：テンプレートを1本作って量産する

最も基本的かつ強力なワークフローです。

**手順**

1. Claude Codeで「マスターテンプレ」を1本作る
2. `compositions/`フォルダ内のHTMLを複製する
3. テキストだけ差し替えてレンダリングする

**Claude Codeへの指示例（マスターテンプレ作成）**

```
/hyperframes を使って、SNS発信用のマスターテンプレを作ってほしい。

仕様：
- 9:16縦型（1080x1920）
- 冒頭2秒：背景が暗くフェードイン
- 2〜5秒：タイトル文字が下からバウンスして出てくる
- 5〜12秒：箇条書き3つが1秒おきにスライドイン
- 12〜15秒：CTAテキスト「詳細はプロフへ」がフェードアウト
- フォントはGoogle Fonts（Noto Sans JP）
- カラーは黒背景・白文字・アクセントカラーは#FF6B35

タイトル、箇条書き3つ、CTAの文言はプレースホルダーにして。
後でここだけ差し替えられるように。
```

**差し替え用スクリプト（bash）**

```bash
#!/bin/bash
# render_batch.sh
# 配列でタイトルと箇条書きを定義して一括生成

titles=("AI副業の始め方" "ChatGPT活用術" "動画量産の秘密")
bullet1=("まず口座を作る" "まずChatGPTに登録" "まずHyperframesを入れる")

for i in "${!titles[@]}"; do
    # HTMLテンプレをコピー
    cp compositions/template.html compositions/video_${i}.html
    
    # sedでプレースホルダーを置換
    sed -i '' "s/TITLE_PLACEHOLDER/${titles[$i]}/g" compositions/video_${i}.html
    sed -i '' "s/BULLET1_PLACEHOLDER/${bullet1[$i]}/g" compositions/video_${i}.html
    
    # レンダリング
    npx hyperframes render --composition video_${i} --output renders/video_${i}.mp4
    
    echo "完了: ${titles[$i]}"
done
```

これで、3本の動画を連続して出力できます。

---

### 運用パターン②：ビルトインブロックで演出を一瞬で追加する

50種類以上のすぐに使えるブロックとコンポーネントが用意されています。

```bash
npx hyperframes add flash-through-white  # シェーダートランジション
npx hyperframes add instagram-follow     # InstagramフォローSNSオーバーレイ
npx hyperframes add data-chart           # アニメーションチャート
```

**よく使うブロック早見表**

| コマンド | 用途 |
|---------|------|
| `npx hyperframes add instagram-follow` | Instagram風フォロー通知 |
| `npx hyperframes add youtube-lower-third` | YouTube下帯テロップ |
| `npx hyperframes add x-post-card` | X（旧Twitter）投稿カード |
| `npx hyperframes add spotify-now-playing` | Spotify Now Playing風 |
| `npx hyperframes add flash-through-white` | フラッシュトランジション |
| `npx hyperframes add glitch` | グリッチエフェクト |
| `npx hyperframes add data-chart` | アニメーションチャート |
| `npx hyperframes add grain-overlay` | 映画的フィルムグレイン |

**使い方の流れ**

```bash
# ブロックをプロジェクトに追加
npx hyperframes add instagram-follow

# 追加されたファイルを確認
ls compositions/
# → instagram-follow.html が追加されている

# Claude Codeに組み込みを依頼
# /hyperframes を使って、instagram-follow.htmlを
# メインのindex.htmlの8秒目に組み込んで。
# 表示は3秒間。フォロワー数は「12,345人がフォロー」にして。
```

---

### 運用パターン③：既存素材（動画・PDF・CSV）を渡して自動変換

**動画ファイルに字幕を自動付与**

```bash
npx hyperframes init caption-video --example warm-grain --video ./my_talk.mp4
# → Whisperが自動文字起こし → 字幕付きテンプレが生成される
```

**PDFをピッチ動画に変換（Claude Codeへの指示）**

```
このPDFを読んで、/hyperframes で45秒のピッチ動画にしてほしい。

構成：
- シーン1（0-8秒）：課題提起
- シーン2（8-22秒）：ソリューション3点
- シーン3（22-38秒）：実績数字のカウントアップ
- シーン4（38-45秒）：CTA

16:9、ダークモード、Noto Sans JP使用。
```

この「Warm start」形式は公式でも推奨されています。

**CSVからアニメーションチャートに変換**

```bash
# data-chartブロックを追加
npx hyperframes add data-chart
```

CSVファイルを用意して、Claude Codeに渡します：

```
このCSVを/hyperframesのdata-chartブロックに流し込んで、
月別売上のバーチャートレースアニメーションを作ってほしい。
30秒、16:9、色は青グラデで。
```

---

### 運用パターン④：Claude Design→Claude Codeの2段階ワークフロー

Claude Designは有効な初稿を出すことに向いており、ビジュアルアイデンティティ、レイアウト、ブランドに合ったコンテンツの判断が得意です。ただしモーションデザインツールではなく、構造的に有効なHyperframesプロジェクトを素早く作るための「ラピッドプロトタイピングツール」です。その後Claude Code（またはAIコーディングエージェント）が、アニメーションの磨き込み、タイミング調整、プレビューを見ながらの仕上げを担当します。

**2段階ワークフローの手順**

```
【Step A：Claude Designで設計】
claude-design-hyperframes.mdをClaudeのDesignチャットに添付して、
こう依頼する：

「企業向けSaaS紹介の60秒動画のコンポジションを作ってほしい。
スタイル：ミニマルコーポレート
カラー：ネイビー×ホワイト×オレンジアクセント
シーン数：6シーン（10秒ずつ）」

→ HTML初稿が出力される

【Step B：Claude Codeで磨き込み】
出力されたHTMLをプロジェクトに置いて、
Claude Codeで：
「プレビューを確認して、シーン4のカウントアップが
 遅すぎるので速くして。シーン6のトランジションも
 whip-panに変えて。」
```

---

### 運用パターン⑤：lint→プレビュー→レンダリングのQAループ

質の高い出力のためのチェックリスト：構造的に有効であること（`npx hyperframes lint`がゼロエラーで通ること）、動画タイプに対して適切なシーン数と尺であること。

**推奨QAフロー**

```bash
# 1. lintで構造チェック
npx hyperframes lint

# 2. プレビューで目視確認
npx hyperframes preview

# 3. ドラフト品質でスピードレンダリング（確認用）
npx hyperframes render --quality draft --output preview.mp4

# 4. OKなら本番レンダリング
npx hyperframes render --output final.mp4
```

---

### 運用パターン⑥：GithubActionsでCI/CD自動化

Hyperframesは決定論的レンダリングで、同じ入力からは常に同一の出力が得られます。自動パイプライン向けに設計されています。

```yaml
# .github/workflows/render-video.yml
name: 動画自動レンダリング

on:
  push:
    paths:
      - 'compositions/**'
      - 'assets/**'

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Node.js セットアップ
        uses: actions/setup-node@v4
        with:
          node-version: '22'
      
      - name: FFmpegインストール
        run: sudo apt-get install -y ffmpeg
      
      - name: レンダリング
        run: npx hyperframes render --output output.mp4
      
      - name: MP4をArtifactとして保存
        uses: actions/upload-artifact@v4
        with:
          name: rendered-video
          path: output.mp4
```

これで、`compositions/`フォルダのHTMLを更新してpushするだけで、GitHubが自動的にMP4を生成します。

---

## PART 3｜マネタイズ編：この技術で稼ぐ8つのルート

---

### マネタイズルート①：動画制作代行サービス

**やること**
- クラウドワークス・ランサーズ・ココナラに出品
- 「SNS動画制作（10秒〜30秒）」を1本5,000〜15,000円で受注

**コスト構造の変化**

| 項目 | 従来 | Hyperframes導入後 |
|------|------|--------------------|
| 制作時間 | 2〜8時間/本 | 15〜30分/本 |
| 外注コスト | 0円（自分でやる場合） | 0円 |
| 月産可能本数 | 10〜20本 | 50〜100本 |
| 月売上上限 | 10〜30万円 | 50〜150万円 |

**出品文のポイント**
- 「After Effects・DaVinci不使用のモダンなAI制作フロー」と書く
- ポートフォリオにHyperframesで作ったデモ動画を最低5本並べる
- ナレーション対応はElevenLabsを組み合わせる（別途オプション料金）

---

### マネタイズルート②：テンプレート販売

**やること**
- Gumroad・BASE・noteに「Hyperframesテンプレート」を販売
- テンプレートHTMLファイル1本あたり3,000〜9,800円

**売れやすいテンプレートの種類**

```
✅ TikTok/Reels用フックビデオ（9:16）
✅ セールスレターVSLイントロ（16:9）
✅ YouTube動画エンドカード（16:9）
✅ コーチ・コンサル向けウェビナーオープニング
✅ 業種別（飲食・美容・不動産・士業）のブランド動画
```

**販売時の付加価値**
- HTMLファイル本体
- Claude Codeへの指示プロンプト集（PDF）
- カスタマイズ動画マニュアル（15分程度）

---

### マネタイズルート③：発信者向け「動画込み」コンテンツ販売

**やること**
- noteで記事を書く際に、Hyperframesで作った動画を冒頭に埋め込む
- 「動画＋テキスト」のセット記事として有料化

**具体的な組み方**

```
無料記事（リード）
└── 冒頭5秒のティザー動画（Hyperframesで制作）
└── 記事本文の最初の1,000文字

有料記事（本体）
└── 45秒の解説動画（全体像をビジュアルで）
└── 完全な本文
└── テンプレートHTMLのダウンロードリンク
```

**価格設定の目安**
- 記事単体：500〜1,500円
- テンプレートセット：3,000〜9,800円
- 月額メンバーシップ（動画テンプレ毎月配布）：2,980〜4,980円/月

---

### マネタイズルート④：法人向け「動画コンテンツ運用支援」

**やること**
- 企業のSNSアカウント運用を月額契約で受ける
- 毎月20〜30本の動画コンテンツを納品

**提案できるサービス内容**

```
月額プラン例：
【ライト】月15本の動画制作  → 月額9.8万円
【スタンダード】月30本 + 投稿代行 → 月額19.8万円
【プレミアム】月50本 + A/Bテスト + 分析レポート → 月額39.8万円
```

**セールスポイント**
- 「動画素材を毎月50本」という提案は従来不可能だったが、Hyperframesで実現可能
- 同じテンプレで多言語展開できる（訪日インバウンド需要）
- CI/CDで自動化すれば、受注数を増やしても工数が増えない

---

### マネタイズルート⑤：YouTubeチャンネル収益化

**やること**
- Hyperframesで毎日ショート動画を量産してチャンネル登録者を増やす
- YouTube AdSense＋メンバーシップで収益化

**おすすめチャンネルコンセプト**

```
「AI×○○業界ニュース」チャンネル
→ 毎朝、業界ニュースのCSVをHyperframesに流して
  1分の解説動画を自動生成。毎日1本投稿。

「AI副業実録」チャンネル
→ 自分がHyperframesを使って稼いでいく過程を
  Hyperframesで作った動画で記録。メタ的に面白い。
```

Claude Codeへの指示例：「9:16のTikTokスタイルのフックビデオを、[トピック]について/hyperframesで作ってほしい。TTSナレーションに合わせてキャプションがバウンスするように」

---

### マネタイズルート⑥：LINE公式アカウント運用代行

**やること**
- 飲食店・美容院・治療院など中小事業者のLINE公式アカウント運用を代行
- 毎月の動画配信コンテンツをHyperframesで制作

**セールストーク**

```
「他の代行業者は静止画の画像を送るだけですが、
 私のプランでは毎月15秒の動画コンテンツを3本配信できます。
 動画付きのLINE配信は開封率が1.5〜2倍になるという
 データがあり、販促効果が段違いです。」
```

**価格設定例**
- 画像のみのLINE運用代行：月3〜5万円（業界相場）
- 動画3本込みのLINE運用代行：月8〜15万円（差別化）

---

### マネタイズルート⑦：セールスレターLPの動画VSL制作

**やること**
- コーチ・コンサル・情報販売者のセールスページにVSL（動画セールスレター）を制作
- 1本制作費10〜30万円で受注

**制作フロー**

```
① クライアントのセールスレター（テキスト）を受け取る
② Claude Codeに渡す：
   「このセールスレターを読んで、冒頭30秒の
    VSLオープニング動画を/hyperframesで作って。
    課題提起→共感→約束の流れで。ダークモード、
    力強いタイポグラフィ、サスペンス系BGM。」
③ 1時間でドラフト完成
④ Claude Codeで対話しながら調整（30分）
⑤ 納品
```

**差別化ポイント**
- 「A/Bテスト用に2パターン作れます」を標準で提供
- 修正対応3回まで含む（Claudeで10分の作業）
- 10日以内納品保証

---

### マネタイズルート⑧：「Hyperframes使い方」講座販売

**やること**
- この技術自体を教えるオンライン講座・コンサルを販売
- note・Udemy・自社スクールで展開

**講座構成例**

```
「AI動画量産マスター講座」（498,00円）

Module 1：環境構築とHyperframes基礎（2時間）
Module 2：Claude Codeとの実践ワークフロー（3時間）
Module 3：テンプレート設計と量産体制の構築（2時間）
Module 4：SNS別・用途別の動画設計（2時間）
Module 5：マネタイズ戦略と営業の実際（1時間）

特典：
- マスターテンプレHTMLファイル10本
- Claude Code指示プロンプト集50本
- Discordコミュニティ参加権
```

**ターゲット**
- 個人事業主・フリーランスで動画制作コストに悩む人
- 副業で動画制作を始めたい会社員
- 法人のSNS担当者

---

## PART 4｜よくあるミスと対処法（実践上の注意点）

---

### ミス①：Reactで書かせてしまう

HyperFramesのコンポジションはHTMLファイルとデータ属性で構成されています。ReactもプロプライエタリなDSLも不要です。

**悪い指示**：「Reactコンポーネントで動画を作って」
**良い指示**：「素のHTML・CSS・GSAPで動画を作って（Reactは使わないで）」

---

### ミス②：`class="clip"`を忘れる

スキルはHyperframes固有のルール（timed要素に必須の`class="clip"`、GSAPタイムラインの登録、`data-*`属性のセマンティクスなど）をエンコードしており、一般的なWebのドキュメントには含まれていません。

アニメーションさせたい要素には必ず `class="clip"` が必要です。忘れると要素がレンダリングされません。

---

### ミス③：スラッシュコマンドをつけない

Claude Codeへの指示は必ず `/hyperframes` で始める。これを省くとスキルがロードされず、ルール違反のコードが出力されます。

---

### ミス④：動画ファイル直接をアニメーションさせる

`<video>`要素を直接アニメーション（width/height/top/leftの変更）させてはいけません。`<div>`でラップして、ラッパーをアニメーションさせてください。

```html
<!-- ❌ NG -->
<video id="clip-1" class="clip" data-start="0" data-duration="5"
       src="intro.mp4" style="transform:translateX(-100px)">

<!-- ✅ OK -->
<div id="clip-1-wrapper" class="clip" data-start="0" data-duration="5">
  <video src="intro.mp4" muted playsinline></video>
</div>
```

---

### ミス⑤：GSAPをサブコンポジションで読み込まない

サブコンポジションのHTMLファイルには、それぞれ独自に `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>` が必要です。GSAPは親のコンポジションからは継承されません。

---

## まとめ：今週動くための最短チェックリスト

```
【今日】
□ Node.js 22以上 インストール
□ FFmpeg インストール
□ Claude Code インストール
□ npx hyperframes skills --claude 実行
□ Claude Codeを再起動して /hyperframes が使えることを確認

【明日】
□ npx hyperframes init my-first-video --example warm-grain
□ /hyperframes を使って自分のジャンルの動画を1本作る
□ npx hyperframes preview でブラウザ確認
□ npx hyperframes render でMP4出力

【今週中】
□ 作った動画をXかnoteに1本投稿する
□ 自分がどのマネタイズルートで使うか決める
□ そのルートに特化したテンプレを1本作る

【来月まで】
□ テンプレを10本ストックする
□ 量産スクリプト（bash or Python）を組む
□ 1件受注するか、1本のコンテンツ販売を始める
```

Hyperframesは単なる新しいツールではなく、新しいカテゴリです。動画制作をGitで管理でき、エージェントが読めて、開発者に親しみやすいHTMLの世界に移行することで、HeyGenはこれまで見たことのない規模での自動化・プログラマティックな動画制作への扉を開いています。

HyperframesはApache 2.0ライセンスの完全なオープンソースです。商用利用も、どのような規模でも、レンダリングごとの課金なし、シート数制限なし、会社規模の制限なしで自由に使えます。

参入コストはゼロ。あとは「やるかやらないか」だけです。


情報が揃いました。では、**「Claude Code vs Cursor、どちらで実装するのが最適解か」**を、用途・スキルレベル・運用フェーズ別に完全整理します。

---

# Hyperframes実装：最適開発環境の完全判断ガイド
## ──Claude Code vs Cursor vs 組み合わせ、実運用ベースの結論

---

## 結論から言う：答えは「両方を役割分担させる」が最適解

先に結論だけ書きます。

```
【設計フェーズ】  Claude Design（claude.ai/design）
     ↓
【実装・修正フェーズ】  Claude Code（メイン）
     ↓
【ファイル直接編集・確認】  Cursor or VS Code（サブ）
     ↓
【量産・自動化フェーズ】  Claude Code + bash/GitHub Actions
```

実際、多くの開発者がこの両方を使い分けています。CursorをメインIDEとして使いながら（速いタブ補完、インライン編集）、長いエージェントタスクにはClaude Codeをターミナルまたは拡張機能から呼び出す、というパターンです。この2つは競合ではなく、違う仕事を担当しています。

なぜこの構成になるのか、ツールの特性から順番に解説します。

---

## SECTION 1｜各ツールの本質的な差を理解する

### Claude Code：Hyperframesとの相性が「最高」な理由

Claude Code、Cursor、Gemini CLI、Codexといった主要なAIコーディング環境でHyperframesが動く。Claude Codeでは、スキルがスラッシュコマンドとして登録される——`/hyperframes`でコンポジション作成、`/hyperframes-cli`でCLIコマンド、`/gsap`でアニメーション補助ができる。

Claude Codeは現時点で最も完成度の高いエージェントランタイムです。`CLAUDE.md`というプロジェクト固有の指示ファイルを読み込み、それがセッションをまたいで永続します。

**Hyperframes特有の理由でClaude Codeが優位な点：**

コンポジションの作成（リポジトリの開発ではなく）は、`npx skills add heygen-com/hyperframes`でインストールされたスキルによってガイドされる。コンポジション作成時は`/hyperframes`、`/hyperframes-cli`、`/hyperframes-registry`、`/gsap`を呼び出すこと。

つまり、**スラッシュコマンドがClaude Code上で最もネイティブに動く**のが最大の理由です。

---

### Cursorの強みと弱み

CursorはAI-first IDE——VS Codeのフォークで、タブ補完、Composer、Agentモードがエディタに組み込まれています。

Cursorでは、同じスキルがCursorプラグインとしてパッケージされており、Cursor Marketplaceからインストールするか、リポジトリをクローンしてSettings → Plugins → Load unpackedでサイドロードできます。

**Cursorが有利な場面：**

Cursorはセットアップ速度、Docker/Renderへのデプロイ、コード品質で優位。Claude Codeは素早いプロトタイプと生産的なターミナルUXに最適。

Cursorはプロジェクト全体のコンテキストとエディタ内自動化の組み合わせで、複雑なコラボレーション開発ワークフローに最適です。

**Cursorが不利な場面（Hyperframes文脈）：**

- スラッシュコマンドが`/hyperframes`としてネイティブに動かない
- ターミナルとエディタのコンテキストが分離している
- lintやrenderのコマンドをAgentに連続実行させるのがやや面倒

---

### 各ツールのHyperframes相性マトリクス

| 観点 | Claude Code | Cursor | Gemini CLI |
|------|------------|--------|-----------|
| スキル統合 | ◎ネイティブ | ○プラグイン経由 | ○インストール可 |
| `/hyperframes`スラッシュ | ◎即使える | △要設定 | ○使える |
| ターミナル連携 | ◎CLI一体 | △別ウィンドウ | ◎CLI一体 |
| ファイル編集のUI | △テキストのみ | ◎視覚的diff | △テキストのみ |
| 量産・自動化 | ◎hooks/scripts | △ | ○ |
| 無料で始められる | △（有料必須） | ○（無料tier有） | ◎（無料tier有） |
| マルチモデル | ✗Claudeのみ | ◎複数モデル対応 | △Geminiのみ |

---

## SECTION 2｜フェーズ別の最適ツール選択

### フェーズ1：設計（Claude Design）

Claude Designは、HyperFrames動画の有効な初稿——ブランドアイデンティティ、シーンコンテンツ、レイアウト、アニメーション、トランジション——を作成します。その後、ZIPをダウンロードして、任意のAIコーディングエージェント（Claude Code、Cursor、Codexなど）でlintとライブプレビューを使いながらリファインします。

**Claude Designの使い方**

```
1. claude.ai/design を開く

2. claude-design-hyperframes.md をダウンロードして
   チャットにドラッグ&ドロップ

3. こう伝える：
「企業向けSaaS紹介の30秒動画を作ってほしい。
 ブランドカラーは #1A1A2E と #E94560。
 フォントはNoto Sans JP。ミニマルで落ち着いたトーン。
 シーン数は4つ、各7-8秒」

4. ZIPでダウンロード → プロジェクトフォルダに展開
```

Claude Designが生成するのは有効な初稿——最終レンダーではありません。その強みはビジュアルアイデンティティ、レイアウト、ブランドに合ったコンテンツ判断です。モーションデザインツールではなく、構造的に有効なHyperFramesプロジェクトを素早く作るための「ラピッドプロトタイピングツール」です。Claude Code（または任意のAIコーディングエージェント）がアニメーションの磨き込み、タイミング調整、pacing、lintとプレビューを使った制作QAを担当します。

---

### フェーズ2：実装・修正（Claude Code）

ここがメインの作業場所です。

**Claude Codeの起動方法**

```bash
# プロジェクトフォルダに移動
cd my-video

# Claude Codeを起動（ターミナルで）
claude

# または、VS Code/JetBrains拡張機能から起動
# （同じエージェントがGUI上で動く）
```

Claude CodeはAnthropicのエージェントツール。ターミナルでの長時間マルチステップ実行用CLIとして始まり、現在はVS CodeとJetBrains拡張機能としても提供されており、hooks、skills、サブエージェントがファーストクラスのプリミティブとして搭載されています。

**実装の会話例：フルフロー**

```
# Step1：初稿確認
/hyperframes Claude Designで作ったHTML初稿を確認して、
構造的な問題があれば直してから、
npx hyperframes lint を実行して。

# Step2：動きの調整
/hyperframes シーン2のタイトルアニメーションが
遅すぎる。0.8秒のイーズアウトを0.4秒の
expo.outに変えて。

# Step3：パーツ追加
/hyperframes シーン3の終わりに
youtube-lower-third ブロックを追加して。
名前は「田中太郎」、肩書きは「AIプロデューサー」。

# Step4：レンダリング
npx hyperframes render --output final.mp4
```

---

### フェーズ3：ファイル確認・細部調整（Cursor または VS Code）

HTMLの中身を**目で見ながら直したい**ときはCursorが便利です。

**Cursorの使い方（Hyperframes文脈）**

```bash
# プロジェクトをCursorで開く
cursor .
```

Cursorはファイルを視覚的に確認しながら、Claude Codeが書いたHTMLの細部を人間が微調整するのに向いています。

**Cursorが活きる具体的な場面：**

- `data-start`や`data-duration`の数値を、タイムラインを見ながら微調整する
- 複数ファイルの`compositions/`フォルダを並べて差分を比較する
- Claude Codeが書いたコードに変なインデントがあったら、フォーマッターで整える
- CSSのカラー変数を一括置換する

---

### フェーズ4：量産・自動化（Claude Code + bash/GitHub Actions）

CLIはスクリプトとエージェントで駆動されるよう設計されており、fail-fastエラーとプレーンテキスト出力を提供します。

量産フェーズになったら、Claude Codeを「指示を出す人」ではなく「自律で動くシステム」として使います。

**Claude Codeのhooks機能で自動化**

```bash
# CLAUDE.md（プロジェクトルートに置く）
cat > CLAUDE.md << 'EOF'
# このプロジェクトのルール

## 動画制作の標準仕様
- アスペクト比：9:16（縦型SNS向け）
- 解像度：1080x1920
- フレームレート：30fps
- フォント：Noto Sans JP（Google Fonts）
- カラーパレット：#0D0D0D（背景）、#FFFFFF（メイン）、#FF6B35（アクセント）
- BGM：assets/bgm_default.mp3（音量0.3）

## 禁止事項
- Reactコンポーネントは使わない
- class="clip"の付け忘れ禁止
- window.__timelinesへの登録を必ず行う

## レンダリング前のチェック
- 必ずnpx hyperframes lintを実行
- エラー0件を確認してからrenderする
EOF
```

これをプロジェクトに置くと、**Claude Codeが毎回このルールを読んで動く**ので、指示のたびに「縦型で」「このカラーで」と言う必要がなくなります。

---

## SECTION 3｜実運用のための具体的な3つの構成

### 構成A：個人発信者向け（最小コスト・最速スタート）

**対象：**毎日Xやnoteで発信している個人、副業始めたい人

**ツール構成：**

```
Claude Code Pro（月$20） ← メインエージェント
+ VS Code（無料）        ← ファイル確認用
+ Cursor Free tier      ← オプション（試してみたい場合）
```

**日常ワークフロー：**

```bash
# 朝：その日の発信テーマを決める

# ターミナルを開く
cd ~/videos/sns-posts
claude

# Claude Codeに話しかける
/hyperframes 今日のXポスト用に9:16の縦動画を作って。
テーマは「ChatGPTで月10万円稼ぐ3ステップ」。
キャプションが下からポンと出てきて、
12秒の動画。いつものテンプレ（warm-grain）ベースで。

# 確認してレンダリング
npx hyperframes preview  # ブラウザで確認
npx hyperframes render --output today_post.mp4
```

**コスト感：**
- Claude Code Pro：月$20（約3,000円）
- 1日1本出しても月30本、1本あたり100円の制作コスト
- 外注なら1本5〜10万円だったものが、100円

---

### 構成B：コンテンツ制作者・代行業向け（量産重視）

**対象：**動画代行受注、テンプレ販売、法人のSNS運用代行

**ツール構成：**

```
Claude Code Max（月$100 or $200） ← エージェントメイン
+ Cursor Pro（月$20）             ← ファイル編集・確認
+ GitHub Actions（無料枠内）      ← 自動レンダリング
```

**プロジェクト管理の構造：**

```
~/video-production/
├── clients/
│   ├── client-A/          ← クライアントAのプロジェクト
│   │   ├── CLAUDE.md      ← ブランドガイドライン
│   │   ├── compositions/
│   │   └── assets/
│   └── client-B/
├── templates/             ← 自分のマスターテンプレ集
│   ├── sns-hook-16-9/
│   ├── vsl-opener/
│   └── youtube-outro/
└── scripts/
    ├── batch_render.sh    ← 一括レンダリング
    └── deploy.sh          ← SNSへの自動アップロード
```

**クライアントごとのCLAUDE.mdを使った自動品質管理：**

```bash
# clients/client-A/CLAUDE.md の例
cat > clients/client-A/CLAUDE.md << 'EOF'
# クライアントA：○○株式会社 動画ガイドライン

## ブランド仕様
- 会社名：○○株式会社
- ロゴファイル：assets/logo.svg
- カラー：プライマリ #2563EB、セカンダリ #F59E0B
- フォント：Noto Sans JP Bold（見出し）、Regular（本文）
- トーン：プロフェッショナル、信頼感、テック系

## 動画仕様
- 横型（16:9）：1920x1080、YouTube・LP向け
- 縦型（9:16）：1080x1920、TikTok・Reels向け

## 禁止事項
- 競合他社名の記載
- 価格の明示（事前確認必要）
- カジュアルすぎる表現

## 毎回やること
1. npx hyperframes lint でエラー0件確認
2. preview で全シーン目視確認
3. render --quality draft で10秒テスト
4. 問題なければ本番render
EOF
```

これで「クライアントAのフォルダでClaude Codeを開く」だけで、ブランドガイドラインが自動で適用されます。

---

### 構成C：エンジニア・自動化重視（完全CI/CD）

**対象：**エンジニア、SaaSに組み込みたい人、大量の動画を自動生成したい人

**ツール構成：**

```
Claude Code API（従量課金）  ← バックグラウンドエージェント
+ GitHub Actions             ← CI/CD自動化
+ Docker                     ← 再現性のあるレンダリング環境
+ Cursor（開発時のみ）       ← コード確認・デバッグ
```

**完全自動化パイプラインの例（noteの記事→動画→X投稿）：**

```bash
#!/bin/bash
# auto_pipeline.sh

# Step1: noteのRSSから最新記事を取得
ARTICLE=$(curl -s "https://note.com/username/rss" | \
  python3 -c "import sys, feedparser; d = feedparser.parse(sys.stdin.read()); print(d.entries[0].title + '\n' + d.entries[0].summary)")

# Step2: Claude Code（非対話モード）でHyperframes動画を生成
echo "$ARTICLE" | claude --non-interactive \
  "この記事のタイトルと概要を読んで、
   /hyperframes で9:16の15秒縦動画を作って。
   compositions/daily.html に出力して。
   lint確認後、render --output renders/daily.mp4 まで実行して。"

# Step3: 生成されたMP4をXにアップロード
python3 scripts/post_to_x.py renders/daily.mp4

echo "完了: $(date)"
```

**GitHub Actionsで毎朝自動実行：**

```yaml
# .github/workflows/daily-video.yml
name: 毎朝動画自動生成

on:
  schedule:
    - cron: '0 0 * * *'  # 毎朝9時（JST）

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Node.js 22 セットアップ
        uses: actions/setup-node@v4
        with:
          node-version: '22'
      
      - name: FFmpeg インストール
        run: sudo apt-get install -y ffmpeg
      
      - name: Hyperframes スキルインストール
        run: npx skills add heygen-com/hyperframes
      
      - name: Claude Code で動画生成
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --non-interactive \
            "/hyperframes で今日のデイリー動画を生成して。
             templates/daily.html をベースに、
             日付を今日の日付に更新してrenderまで。"
      
      - name: MP4をArtifactに保存
        uses: actions/upload-artifact@v4
        with:
          name: daily-video-${{ github.run_id }}
          path: renders/*.mp4
```

---

## SECTION 4｜よくある判断ミスと正しい選択

### 「Cursorだけでやればいいじゃないか」という判断について

AIエージェント（Claude CodeやCursorなど）はPremiereProのような複雑なGUIベースのビデオエディタを操作することができません。しかし、HTMLとJavaScriptを書くことは得意です。

CursorはGUIが見やすく、使い慣れた人が多い。でも：

- **Hyperframesのスラッシュコマンドがネイティブに動かない**（Cursorプラグインで動くが、セットアップが必要）
- **renderやlintをエージェントが自律実行しにくい**（GUIのAgentモードとCLIの連携が弱い）
- **CLAUDE.mdのような永続コンテキストが効きにくい**

ターミナルで生活しているか、スクリプトを自動化しているなら、Claude Codeは欠かせません。

---

### 「Claude Code一本でいいじゃないか」という判断について

Claude Codeはhooks、skills、サブエージェント、スラッシュコマンドで繰り返し可能なエージェントワークフローをファーストクラスとして扱います。CLIはターミナル、CI、またはVS Code/JetBrainsの公式拡張機能の中で動く——同じエージェントがどこでも動きます。

Claude Code一本でもほぼできますが：

- **HTMLの細部をGUIで確認しながら直したい**場合はCursorが速い
- **複数ファイルのdiffを視覚的に見たい**場合はCursorが見やすい
- **タブ補完でHTMLを手動補完したい**場合はCursorが快適

---

## SECTION 5｜実装の現実的な落とし穴

### 落とし穴①：プレビューとレンダリング結果が違う

プレビューのグリッチは両ツールに存在します。Claude Designのブラウザプレビューはスタッターが発生することがあり、Hyperframesのプレビューもスクラブ時にGSAPタイムラインとオーディオの同期が外れることがあります。最終レンダリング結果は常に正確です。プレビューのバグは本物で、壊れていないものを直し始めてしまいます。プレビューで変に見えたら、プロンプトを書き直す前にまず10秒のテストクリップをレンダリングしてください。

**対処法：**

```bash
# プレビューで怪しいと思ったら
npx hyperframes render --quality draft --output test_10s.mp4
# → 実際のMP4を確認してから判断する
```

---

### 落とし穴②：音声付き動画の字幕タイミングが合わない

両ツールが同じ壁にぶつかるのは、オーディオを解釈しようとしたときです。ツールはあなたのナレーションを「聞く」ことができません。どこで言葉が終わるかを知りません。テキストで与えられた情報しか知らないのです。そのため、トランスクリプト（文字起こし）がこのワークフロー全体で最も重要な素材です——プロンプトよりも、デザインシステムよりも、使っているモデルよりも重要です。

**対処法：**

```bash
# 動画をWhisperで文字起こし（タイムスタンプ付き）
npx hyperframes init my-video --video ./narration.mp4
# → 自動で文字起こし＋タイムスタンプ付きのテンプレが生成される

# その後Claude Codeに渡す：
# /hyperframes このトランスクリプトのタイムスタンプに合わせて
# 字幕アニメーションを作って
```

---

### 落とし穴③：Claude Codeの使用量上限に当たる

Pro tier（月$20）だと多くの開発者が週10〜20の意味のあるコーディングセッションしか得られない。ヘビーユーザーは週の半ばに上限に当たると報告しています。Max tier（月$100）は助けになりますが、5倍の価格に比例した容量は得られません。

**対処法：**

| 状況 | 解決策 |
|------|--------|
| たまに動画を作る個人 | Claude Code Pro（月$20）で十分 |
| 毎日量産する発信者 | Claude Code Max（月$100）を検討 |
| 完全自動化パイプライン | Anthropic APIの従量課金（使った分だけ） |
| コスト最優先 | Gemini CLI（無料）でHyperframesスキルを使う |

Gemini CLI（Google）は無料です。1分あたり60リクエスト、1日1,000リクエスト、100万トークンのコンテキストウィンドウ。本当に太っ腹な無料tier。

---

## まとめ：あなたの状況別・最短ルート

```
【Hyperframesを試すだけ】
→ Gemini CLI（無料）でスキル追加してまず1本作る

【個人発信者・副業スタート】
→ Claude Code Pro（$20/月）一本でOK
   CLAUDE.mdにブランドガイドライン書いて、
   毎日ターミナル1つで動画を出していく

【動画代行・テンプレ販売で稼ぐ】
→ Claude Code Pro + Cursor Pro
   Claude Codeでエージェント実行、
   CursorでHTML細部を確認・調整

【完全自動化・法人受注】
→ Claude Code Max + GitHub Actions
   CI/CDで動画を自動生成する仕組みを組む
   CLAUDE.mdでクライアントごとのブランドを管理

【設計から丁寧に作りたい】
→ Claude Design → Claude Code → Cursor
   3段階で役割を分けて、
   初稿・実装・確認の流れを固める
```

Claude Code Design Systemでビジュアル言語を決め、HyperFramesでコンポジションとアニメーション、Auphonicでプログラマティックなオーディオクリーンアップ、そしてClaude Code自体がコンダクター（指揮者）——オーケストラではなく指揮者として機能します。その区別は見た目以上に重要であり、1つのプロンプトで動画を完成させようとするのをやめた瞬間に出力品質が跳ね上がります。

**最初の1手は決まっています。ターミナルを開いて、これだけ打ってください：**

```bash
npm install -g @anthropic-ai/claude-code
npx skills add heygen-com/hyperframes
npx hyperframes init first-video --example warm-grain
cd first-video
claude
```

あとは、Claude Codeに話しかけるだけです。


情報が揃いました。現時点（2026年4月）の最新データをもとに、完全に実用ベースで答えます。

---

# Claude Code ProプランでHyperframes実装は完結するか？
## ──トークン切れの現実・マルチエージェント構成・モデル選択の完全判断ガイド

---

## 結論：先に全部言う

```
【Proプランで完結するか】
→ 用途による。1日1〜3本の動画制作なら完結する。
  量産（1日10本以上）はトークン切れを起こす。

【トークン切れは起きるか】
→ 起きる。特にOpusを使うと3プロンプトで
  5時間枠の11%を消費したという報告がある。

【マルチエージェントは有効か】
→ 有効。ただしProプランでは逆効果になるケースがある。
  3エージェント同時起動すると単独セッションの7倍消費する。

【モデルは弱すぎるか】
→ Sonnet 4.6で十分。Opusは設計フェーズのみ使う。
  「OpusでPlan → SonnetでExecute」が最適解。
```

---

## SECTION 1｜Proプランの実態：数字で理解する

### 5時間ローリングウィンドウとは何か

Claude Codeは5時間のローリングウィンドウで動作しており、最初のメッセージを送った時点からカウントが始まります。

ターミナルで`claude`を実行した瞬間に5時間の計測が始まり、そのウィンドウ内のすべてのメッセージとトークン消費がプランのプールから引き落とされます。リセットは5時間経過後に次のメッセージを送ったときにのみ発生します。

**Proプランのトークン上限（具体的な数字）**

Proプランのユーザーは5時間ウィンドウあたり約44,000トークンにアクセスできます。これはコードベースの複雑さや具体的なタスクに応じて、おおよそ10〜40プロンプトに相当します。

Pro利用者はウィンドウあたり平均10〜40プロンプトであるのに対し、Max 20×利用者はモデルの選択やコードサイズによって200〜800プロンプトを使えます。

**週次上限も別途存在する**

2025年8月28日から週次クォータが導入され、ProとMaxプランのヘビーユーザーに適用されています。すべてのClaude.aiプランはClaudeアプリとClaude Code間で共通の使用バケットを共有します。

**claude.aiとClaude Codeは同じバケットを共有する**

claude.ai、Claude Code、Claude Desktopの使用量はすべて単一の共有プールに対してカウントされます。ターミナル使用のための別バケットは存在しません。

つまり、**昼間にclaude.aiでチャットして夜にClaude Codeで動画を作ると、両方が同じ44,000トークンを食い合う**ということです。

---

### 実際にトークンはどれくらい消費されるか

**Hyperframes文脈での実際の消費量目安**

| 作業内容 | 消費プロンプト数（目安） | Proでの残り |
|---------|-----------------|-----------|
| `init`でプロジェクト作成 | 1〜2 | 38〜39/40 |
| 初稿HTML生成（15秒動画） | 3〜5 | 33〜37/40 |
| アニメーション調整（往復3回） | 3〜6 | 27〜34/40 |
| lintエラー修正 | 1〜3 | 24〜33/40 |
| ブロック追加（instagram-follow等） | 2〜3 | 21〜31/40 |
| **合計（1本の動画完成まで）** | **10〜19** | **残り21〜30** |

→ **1本の動画なら1セッション（5時間枠）内で余裕で完結する**
→ **3〜4本作ると枠の限界に近づく**
→ **Opusを使うと2〜3倍速くトークンが減る**

---

### Opusを使うと何が起きるか（実例）

あるデベロッパーは「$20分が1日で消えた。Plan modeでフロントエンドのアーキテクチャをリファクタリングするために使ったが、週次クレジットの11%を使い切った」と報告しています。

Opus 4.5（現在は4.7）はSonnet 4.5に比べてトークンあたりのコストが約1.7倍高く、AnthropicもOpusには週次時間上限をより厳しく設定しています。複雑なマルチファイルのエージェントワークフローでOpusを使っている場合、予想よりもはるかに早く上限に到達します。

**結論：Hyperframes実装でOpusをデフォルトにするのは禁止**

---

## SECTION 2｜プラン別・用途別の正直な判断

### プラン比較表（2026年4月現在）

2026年4月時点で、Claude Codeの料金はProが月$20、Max 5xが月$100、Max 20xが月$200です。

| プラン | 月額 | 5時間あたりトークン | 週次制限 | Hyperframes用途 |
|-------|-----|---------------|---------|----------------|
| Pro | $20 | ~44,000 | あり | 1日1〜3本まで |
| Max 5x | $100 | ~88,000 | あり | 1日5〜10本程度 |
| Max 20x | $200 | ~220,000 | あり | 1日20本以上の量産 |
| API従量課金 | 使った分 | 上限なし | なし | CI/CD自動化向け |

Max 5xはProの使用量の約5倍、つまり5時間ウィンドウあたり約88,000トークンです。

Max 20xはProの約20倍のアローワンス（5時間ウィンドウあたりおよそ220,000トークン）で、継続的に数時間のセッションを大規模コードベースで実行する開発者のために設計されています。

---

### あなたの状況別・ズバリの答え

**ケース1：個人発信者（Xに毎日1本投稿したい）**

```
→ Pro（$20/月）で完結する

理由：
- 1本あたり10〜19プロンプト消費
- Proの1セッション（5時間）= 10〜40プロンプト
- 1日1本なら余裕、2本でも5時間枠を
  うまく使えば収まる

注意点：
- Opusを使わない（Sonnet固定）
- claude.aiのチャットと共有なので
  日中にclaude.aiを多用しない
```

**ケース2：動画代行受注・テンプレート量産（1日5〜10本）**

```
→ Max 5x（$100/月）推奨

理由：
- 1日10本 × 15プロンプト = 150プロンプト/日
- Proの5時間枠（最大40プロンプト）では
  3〜4枠待ちが毎日発生する
- Max 5xなら1セッションで
  複数本をまとめて処理できる
```

**ケース3：CI/CDで自動量産（GitHub Actions等）**

```
→ API従量課金が最適

理由：
- サブスクリプションは「人間が使う」契約
- コードやCIがClaudeを呼ぶ場合は
  APIの方が正しい契約形態
- Sonnet 4.6なら$3/Mトークン（入力）
  1本の動画生成で数円〜十数円のコスト
```

Proは使用量制限付きのインタラクティブな人間の使用向けです。APIはプロジェクトが所有する従量課金の使用向けです。人間がターミナルでClaude Codeを使ってコーディングしているなら、Proが通常低摩擦の出発点です。コード、CI、またはアプリがClaudeを呼び出しているなら、API課金が正しい契約形態です。

---

### トークン切れが起きたときの対処法

Extra usage（超過使用）により、使用量上限に達した後でも標準APIレートの従量課金価格でシームレスにClaudeを使い続けることができます。上限に達してブロックされる代わりに、消費ベースの価格体系に切り替えて作業を中断せず継続できます。

Extra usageはPro、Max 5x、Max 20xを含むすべての有料Claudeプランで利用可能です。

**実用的な設定方法：**

```
Settings → Usage → Extra usage を有効化
→ 月の上限金額（例：$10）を設定
→ 上限に達したら自動的にAPI従量課金で継続
→ 月末に上限を超えたらストップ
```

これが「Proプランで使いつつ、繁忙期だけ超過分をAPIで賄う」という最もコスパの高い運用です。

バースト型のヘビーユーザーであれば、Pro＋Extra usageが最もスマートな設定になります。ほとんどの週はProで収まるが、リリース週、障害対応週、移行週などが強烈な週に押し込まれるというパターンです。

---

## SECTION 3｜マルチエージェント構成：Proで有効か、逆効果か

### マルチエージェント（サブエージェント）とは何か

サブエージェントは特定のタイプのタスクを処理する専門化されたAIアシスタントです。サイドタスクが検索結果、ログ、または二度と参照しないファイル内容でメイン会話を溢れさせてしまうときに使用します。サブエージェントはそれ自身のコンテキストでその作業を行い、サマリーだけを返します。

各サブエージェントはカスタムシステムプロンプト、特定のツールアクセス、独立した権限を持つ独自のコンテキストウィンドウで動作します。Claudeがサブエージェントの説明に合致するタスクに遭遇すると、そのサブエージェントに委譲し、サブエージェントが独立して作業して結果を返します。

### Proプランでマルチエージェントを使うと何が起きるか

**問題：コンテキストが増える = トークンが増える**

エージェントチームは複数のClaude Codeインスタンスを起動し、それぞれが独自のコンテキストウィンドウを持ちます。3エージェントチームは、各チームメンバーが独自のコンテキストウィンドウを維持し、別々のClaudeインスタンスとして動作するため、標準的な単独エージェントセッションの約7倍のトークンを消費します。

→ **Proの44,000トークン枠で3エージェントを立ち上げると、実質13,000トークン/エージェントしか使えない**

**ただし、メリットもある**

単一のAIエージェントに複雑なマルチステージのタスクを実行させると、コンテキストウィンドウを使い果たして重要な詳細を失い始めます。サブエージェントを使うことで、各スペシャリストに専用のコンテキストウィンドウが与えられ、各ステップの品質が保たれます。例えば、プロダクトマネージャーエージェントは20万トークンのコンテキスト全体をユーザーニーズとビジネスロジックだけに集中できます。シニアソフトウェアエンジニアエージェントは最終チケットを受け取り、最初のプロダクト議論のニュアンスを覚えておく必要なく、実装だけに集中できます。

### Hyperframesでのサブエージェント活用判断

**Proプランでのマルチエージェント：非推奨**

理由：44,000トークンを複数エージェントで分割すると、1エージェントあたりの能力が著しく低下し、結果として総作業量が減る。

**Max 5x以上でのマルチエージェント：推奨**

88,000〜220,000トークン枠があれば、役割分担による効率化が意味を持つ。

---

### 実用的なサブエージェント構成（Max 5x以上向け）

**Hyperframes専用の3エージェント構成**

```
.claude/agents/
├── hyperframes-designer.md   ← 設計・構成エージェント
├── hyperframes-coder.md      ← HTML/CSS/GSAP実装エージェント  
└── hyperframes-qa.md         ← lint・品質チェックエージェント
```

**hyperframes-designer.md（設計エージェント）**

```markdown
---
name: hyperframes-designer
description: 動画の構成、シーン設計、コンテンツ計画を担当する。
             HTMLは書かない。設計書とシーン仕様のみ出力する。
tools: Read
model: sonnet
---

あなたはHyperframes動画の設計スペシャリストです。
HTML実装は行いません。

担当範囲：
- ユーザーの要望を聞き、シーン構成を決定する
- 各シーンの開始時間・継続時間・コンテンツを仕様化する
- アニメーションの方向性と雰囲気を決定する
- 使用するビルトインブロックを選定する

出力形式：
必ず以下の形式でシーン仕様を出力する
- シーン数と各シーンの時間配分
- 各シーンに表示するコンテンツ（テキスト・画像・動画）
- アニメーション方向性（GSAPのeasing・duration指定含む）
- 使用するビルトインブロック（必要な場合）
- カラーパレットとフォント指定
```

**hyperframes-coder.md（実装エージェント）**

```markdown
---
name: hyperframes-coder
description: hyperframes-designerの仕様書を受け取り、
             HTMLを実装するエージェント。
tools: Read, Write, Edit, Bash
model: sonnet
---

あなたはHyperframes HTML実装スペシャリストです。

絶対ルール：
1. class="clip" を必ずすべての時間指定要素につける
2. window.__timelines に必ずGSAPタイムラインを登録する
3. GSAPはCDN（gsap@3.14.2）からのみ読み込む
4. Reactは絶対に使わない
5. 実装後は必ずnpx hyperframes lint を実行する

実装の流れ：
1. 設計書のシーン仕様を読む
2. index.htmlとcompositions/配下にHTMLを書く
3. GSAPアニメーションを実装する
4. npx hyperframes lint でエラー0を確認する
5. エラーがあれば自己修正する
```

**hyperframes-qa.md（QAエージェント）**

```markdown
---
name: hyperframes-qa
description: レンダリング前の最終品質チェックを担当する。
             lint・構造確認・ドラフトレンダリングまで行う。
tools: Read, Bash
model: haiku
---

あなたはHyperframesのQAスペシャリストです。

チェック項目（必須）：
1. npx hyperframes lint → エラー0件確認
2. data-start / data-duration の論理的整合性確認
3. class="clip"の付け忘れチェック
4. window.__timelinesへの登録漏れチェック
5. npx hyperframes render --quality draft でテスト出力

出力：
- 問題なし → 「QA完了。本番レンダリング可能です」
- 問題あり → 具体的な問題箇所と修正指示を出力
```

**サブエージェントルーティングをCLAUDE.mdに設定**

```markdown
# CLAUDE.md（プロジェクトルート）

## サブエージェント使用ルール

### 並列実行（条件が揃った場合のみ）
- 複数の独立したシーンを同時に作成する場合
- 互いのファイルに依存関係がない場合

### 順次実行（通常のフロー）
Designer → Coder → QA

### 直接実行（サブエージェント不要）
- 小さな修正（テキスト変更、数値調整）
- 単一プロパティの変更
- renderコマンドの実行のみ

### モデル割り当て
- 設計段階（複雑な判断）: Opus
- 実装段階（コード生成）: Sonnet
- チェック・lint: Haiku
```

---

## SECTION 4｜モデル選択の完全判断基準

### 各モデルの特性をHyperframes文脈で整理

Sonnetはデフォルトで、大多数のコーディング作業に適しています。高速、有能、コスト効率が良い。Opusはクロスカットリファクタリング、難しいデバッグ、アーキテクチャ判断など難しい問題の深い推論に向いています。クォータをより多く消費するため、必要なときだけ切り替える。Haikuは最速で最もコストが低く、クイックな検索、シンプルな編集、大量スクリプト実行に適しています。

**Hyperframes作業とモデルのマッピング**

| 作業内容 | 推奨モデル | 理由 |
|---------|----------|------|
| 動画全体の構成設計 | Opus | 複雑な判断が必要 |
| HTMLコード生成 | Sonnet | 大量学習データで十分 |
| GSAPアニメーション実装 | Sonnet | パターンが豊富で安定 |
| lintエラー修正 | Sonnet | 機械的な作業 |
| テキスト置換・微調整 | Haiku | 軽量タスクで十分 |
| CI/CD自動生成 | Haiku/Sonnet | コスト最優先 |

### 「OpusでPlan、SonnetでExecute」パターン

プランを作るのに数百トークンしかかかりません。OpusでPlan、SonnetでExecuteを推奨します。Opusの最も価値の高い使い方は、深い推論が実際に効果を発揮するプラン自体を書くことです。一度良いプランができたら、実行はほとんど機械的なものであり、Sonnetははるかに低いコストでそれを処理します。このパターンは`/model opusplan`として組み込まれており、計画中はOpusを使い、実行にはSonnetを使います。

**実際の使い方：**

```bash
# Claude Codeを起動
claude

# まずOpusで設計（数百トークンで完了）
/model opus
「この商品紹介LP用の45秒動画の構成を設計して。
シーン数、各シーンの役割、アニメーション方針を決めて。
HTMLは書かなくていい。設計書だけ出して。」

# 設計書が出たらSonnetに切り替えて実装
/model sonnet
「/hyperframes 今の設計書をもとにHTMLを実装して。
lint確認まで全部やって。」

# QAはHaikuで十分
/model haiku
「npx hyperframes lint を実行して、エラーがあれば直して。」
```

セッションの途中でモデルを変更しても会話は失われません。つまり、OpusがPlanを書いた内容をSonnetはそのまま見た状態で実装に入れます。

### サブエージェントのモデルを個別に制御する

`CLAUDE_CODE_SUBAGENT_MODEL`環境変数でサブエージェントが使用するモデルを制御できます。メインセッションをOpusで複雑な推論のために動かしながら、サブエージェントにフォーカスされたタスクをSonnetで処理させる一般的なパターンがあります。これによりコストが大幅に削減されます。

```bash
# サブエージェントをSonnetに固定
export CLAUDE_CODE_SUBAGENT_MODEL="claude-sonnet-4-6-20260205"

# その後Claude Codeを起動
claude
# → メインはOpus、サブエージェントはSonnetで動く
```

---

## SECTION 5｜コンテキスト管理：セッションを長持ちさせる技術

### /compactと/clearの使い分け

新しいターンごとに以前のすべてのメッセージが再送信されるため、3つの無関係な問題をさまよったセッションは、新しいメッセージごとに3つすべての費用を支払います。実践：ログインリダイレクトのデバッグを終えてデータベースマイグレーションを書きたい場合は、まず`/clear`を実行してください。次のプロンプトが新しいターミナルで完全に意味をなすなら、送信前にクリアしてください。CLAUDE.mdとプロジェクトファイルはそのまま残り、チャット履歴だけが消えます。

注意：`/clear`は元に戻せません。履歴からまだ必要なものがある場合は、先にコピーするか、すべてを消すのではなくサマリーを保持する`/compact`を実行してください。

**実用的な使い分けルール：**

```
/compact → 使う場面：
  - 1本の動画を作り続けているが会話が長くなった
  - 文脈は保持したいが無駄なログを圧縮したい
  - 「続きから」作業したい

/clear → 使う場面：
  - 1本の動画が完成して次の動画に移る
  - 完全に別のプロジェクトを始める
  - トークン節約を最優先したい
```

### CLAUDE.mdの長さを管理する

ルールは「2ストライクで記録する」。同じことを2度訂正しなければならなくなった場合にのみメモを追加する（初回の問題は大抵一回限り）。ファイルは200行程度に収める。新しいことを追加する必要があって余裕がない場合は、古いものを削除する。

更新するタイミング：同じことをClaude に2度訂正した直後のセッション。数週間ごとにファイル全体を読み、もはや真実でないか目的を思い出せないものを削除する。古いメモは欠けているメモよりも悪い、なぜならClaudeを積極的に誤誘導するからです。

---

## SECTION 6｜状況別の最終推奨構成まとめ

### 構成A：Proプラン一本（最小コスト）

```
月額：$20
用途：1日1〜3本の動画制作
上限緩和：Extra usageをオン（月$10上限で設定）

トークン節約の設定：
1. CLAUDE.mdは200行以内に収める
2. Sonnetをデフォルトに設定
   /model sonnet を最初に実行
3. 1本完成したら /clear
4. Opusは設計フェーズのみ（1回/日）

推奨ワークフロー：
1. /model opus → 構成設計（数百トークン）
2. /model sonnet → /hyperframes HTML実装
3. /model haiku → lint確認
4. 本番render
5. /clear → 次の動画へ
```

### 構成B：Max 5xプラン（量産・代行業向け）

```
月額：$100
用途：1日5〜10本の量産、動画代行受注

サブエージェント構成（使って良い）：
- hyperframes-designer（Sonnet）
- hyperframes-coder（Sonnet）
- hyperframes-qa（Haiku）

環境変数設定：
export CLAUDE_CODE_SUBAGENT_MODEL="claude-sonnet-4-6"

バッチ処理：
- 同じテンプレの差し替えは
  サブエージェントで並列処理
- 独立したシーン → 並列
- 依存関係あり → 順次
```

並列実行の条件（ALL必須）：3つ以上の独立したタスクまたはドメイン、タスク間で共有状態がない、重複のない明確なファイル境界がある。

### 構成C：API従量課金（CI/CD自動化向け）

```
月額：使った分だけ
対象：GitHub Actionsでの自動生成
    note記事→動画の自動パイプライン
    
コスト試算（Sonnet 4.6）：
- 入力：$3/Mトークン
- 出力：$15/Mトークン
- 1本あたり約10,000トークン消費と仮定
  → 1本 = 約0.15円（入力） + 約2円（出力）
  → 1日100本生成しても月6,000円程度

設定：
export ANTHROPIC_API_KEY="sk-ant-..."
claude --non-interactive \
  "/hyperframes [指示]"
```

APIキーユーザーは使用上限がありませんが、費用が気になる場合は`/cost`コマンドとコンソールのダッシュボードで確認できます。予想外に高い数値はほぼ常に、クリアされることなく続いた非常に長いセッションに起因しています。

---

## まとめ：判断フロー一覧

```
Q1: 1日に動画を何本作るか？
├── 1〜3本 → Pro（$20）
├── 4〜10本 → Max 5x（$100）
└── 10本以上 or CI/CD → API従量課金 or Max 20x（$200）

Q2: Opusを使うか？
├── 設計フェーズのみ → OK（コスト管理できる）
└── デフォルトで使う → NG（3プロンプトで枠の11%消費）

Q3: マルチエージェントを使うか？
├── Proプラン → 非推奨（7倍トークン消費で逆効果）
├── Max 5x → 条件付きで推奨（並列条件を満たす場合のみ）
└── Max 20x → 積極的に推奨

Q4: トークン切れが頻繁に起きる場合は？
├── まずExtra usageをオン（月$10上限）
├── 次にモデルをSonnetに統一
├── CLAUDE.mdを200行以内に整理
└── それでも足りなければMax 5xにアップグレード
```

Proから始めてください。1ヶ月間使用量を追跡して、頻繁に上限に達する場合はMaxにアップグレードしてください。達していなければ、年間$960の節約です。これがこの決定へのスマートなアプローチです。


まず最新情報を調べます。情報が揃いました。現時点の最新データで完全に答えます。

---

# OpenCode × GLM-5.1 / GLM-5-Turbo でHyperframes導線は作れるか？
## ──実現可能性・コスト・モデル性能・設定手順の完全判断ガイド

---

## 結論：先に全部言う

```
【OpenCodeでHyperframesは動かせるか】
→ 動かせる。OpenCodeは75以上のプロバイダーに対応しており、
  GLM系モデルをOpenRouter経由またはZ.ai直接APIで接続できる。

【GLM-5.1 / GLM-5-Turboのモデルは弱すぎるか】
→ 弱くない。GLM-5.1はSWE-Bench Proでトップクラスの
  コーディング性能を持ち、Hyperframesの用途では
  十分以上の性能がある。

【Claude Code Proのトークン問題を回避できるか】
→ できる。OpenCodeはサブスクリプション上限がなく、
  使った分だけAPIコストを払う従量課金モデルなので
  5時間ウィンドウ制限が存在しない。

【コストはどうか】
→ Claude Code Pro（$20/月固定）より大幅に安くなる
  可能性が高い。1本の動画生成あたり数円以下のコスト。

【ただし重要な注意点がある】
→ HyperframesのスキルはClaude Code向けに
  最適化されている。OpenCodeでは代替手段が必要。
```

---

## SECTION 1｜OpenCodeとは何か：Claude Codeとの本質的な差

### OpenCodeの現状

OpenCodeはSSTチーム（Serverless Stack）によって作られたオープンソースのプロバイダー非依存のコーディングエージェントです。Goで書かれ、Bubble Teaによるリッチなターミナルインターフェースを持ち、Ollamaによる完全ローカルモデルを含む75以上のLLMプロバイダーをサポートしており、開発者はどのモデルでコーディングワークフローを動かすかを完全にコントロールできます。

OpenCodeは2026年4月時点で147,000のGitHubスターと650万人の月間開発者を達成しており、Claude Codeのスター増加速度の4.5倍のペースで成長しています。

OpenCode CLIはClaude Code、Gemini CLIといった他のエージェントCLIと並ぶ存在ですが、**根本的に異なるアプローチ**を取っています。単一のプロバイダーに縛られる代わりに、OpenAI、Anthropic Claude、Google Gemini、ローカルLLMをOllama経由で含む75以上のプロバイダーをサポートしており、開発者はモデルをオンデマンドで切り替え、出力を比較し、ベンダーロックインを回避できます。

### Claude CodeとOpenCodeの決定的な差

| 比較軸 | Claude Code | OpenCode |
|--------|------------|---------|
| モデル | Claudeのみ | 75以上のプロバイダー |
| 料金モデル | $20〜$200/月固定 + 上限あり | 使った分だけAPI従量課金 |
| トークン上限 | 5時間ウィンドウ制限あり | **制限なし** |
| Hyperframesスキル | `/hyperframes`でネイティブ対応 | カスタム設定が必要 |
| オープンソース | ✗ | ✓（MIT相当） |
| ローカル実行 | ✗ | ✓（Ollama経由） |
| スター数 | 非公開 | 147,000+ |

多くのAIコーディングツールは今日、IDEエクステンションか、モデルコストを月額費用に束ねたサブスクリプションラップ型プロダクトです。OpenCodeは異なるアプローチを取っています：ターミナルで動くオープンソースのコーディングエージェントで、あなたがすでに使っているモデルとプロバイダーに接続し、邪魔をしません。

---

## SECTION 2｜GLM-5.1 / GLM-5-Turboのモデル性能：Hyperframes用途での実力

### GLM-5.1（オープンソース・フラッグシップ）

GLM-5.1はZ.aiのフラッグシップオープンソースAIモデルで、2026年4月7日にリリースされ、エージェント型エンジニアリングと長期ソフトウェア開発タスクのために特別に構築されています。GLM-5ベースモデルへのポストトレーニングアップグレードで、同じ744億パラメーターのMixture-of-Expertsアーキテクチャを持ちながら、コーディング、ツール使用、自律実行能力が大幅に強化されています。

2026年4月7日、Z.aiはGLM-5.1をSWE-Bench Proで58.4スコアで投入し、GPT-5.4の57.7とClaude Opus 4.6の57.3を上回り、グローバルリーダーボードのトップに立ちました。MITライセンスです。

このモデルは最初のパスでコードを生成するだけでなく、反復するよう設計されています。人間の介入なしに最大8時間、完全な「計画・実行・テスト・修正・最適化」ループを自律的に管理できます。

**Hyperframes文脈での特に重要な点：**

このモデルはClaude Code、OpenCode、Kilo Code、Roo Code、Cline、Droidを含む幅広い開発者ツールとの互換性がすでに確認されています。これらのツールのいずれかをすでに使っているなら、GLM-5.1をワークフローに組み込むのはワンライン設定の変更です。

### GLM-5-Turbo（エージェント特化・高速）

Z.aiのGLM-5-Turboは、OpenClawスタイルのツール使用、長チェーン実行、永続的自動化といったエージェント駆動ワークフローを目的として設計された高速モデルで、より速いモデルとして位置づけられています。

GLM-5-Turboはツール呼び出し精度を大幅に強化し、外部ツールや各種スキルの呼び出しにおいてより安定した信頼性を確保しています。OpenClawシナリオのために深く最適化された基盤モデルで、ツール呼び出し、命令追従、タイミング・永続タスク、長チェーン実行といった主要な機能が強化されています。

GLM-5-Turboは約202,800トークンのコンテキストウィンドウと131,100トークンの最大出力を持ち、ツール呼び出しと構造化出力をサポートしています。毎秒48トークンのスループットと8.16秒の補完時間、0.67%という大幅に低いツールエラー率を実現しています。

### GLM-5.1 vs GLM-5-Turbo：Hyperframesでどちらを選ぶか

「TurboはスプリンターでGLM-5.1はマラソンランナー」という表現が的確です。両者は異なるユースケースに対応し、価格も異なります。

エージェントパイプラインが最も恩恵を受けます。パイプラインの多くのステップは完全なGLM-5.1の推論深度を必要としませんが、問題が難しくなったときには構造化された思考モードの恩恵を受けます。GLM-5-Turboは軽量な思考モードでルーティンステップを高速に処理し、より難しいステップをより深いモードにエスカレートでき、すべて同じモデルとAPIコールフォーマットで行えます。

**Hyperframes実装の推奨モデル割り当て：**

| Hyperframes作業 | 推奨 | 理由 |
|---------------|-----|------|
| 動画全体の構成設計 | GLM-5.1 | 長期推論・複雑判断が得意 |
| HTML/GSAP実装 | GLM-5-Turbo | 高速・ツール呼び出し安定 |
| lint修正・反復調整 | GLM-5-Turbo | 短チェーン・高スループット |
| CI/CD自動生成 | GLM-5-Turbo | 低コスト・高速処理 |

---

## SECTION 3｜コスト比較：Claude Code Proと何が違うか

### 料金の実数字

GLM-5.1は入力100万トークンあたり$1.40、出力$4.40の価格です。GLM-5-Turboは入力$1.20、出力$4.00です。

GLM-5.1はキャッシュ割引により繰り返し入力を100万トークンあたり$0.26に下げられます。北京時間14時〜18時のピーク時間帯は標準レートの3倍のクォータを消費します。

**Hyperframes動画1本あたりのコスト試算：**

```
【1本の動画生成の想定トークン消費】
- 入力トークン：約5,000〜8,000（指示 + CLAUDE.md + 既存ファイル）
- 出力トークン：約3,000〜5,000（HTML + GSAP + 修正）
- 往復3〜5回のやり取り

GLM-5-Turboでの1本あたりコスト：
- 入力：8,000 × $1.20 / 1,000,000 ≈ $0.0096（約1.4円）
- 出力：5,000 × $4.00 / 1,000,000 ≈ $0.02（約3円）
- 合計：約5円/本

月100本生成しても：約500円（$3〜4）
月1,000本生成しても：約5,000円（$33）
```

**Claude Code Proとの比較：**

```
Claude Code Pro：$20/月固定
・1日1〜3本なら収まる
・3本/日 × 30日 = 90本で上限に近づく
・超過分はExtra usageで追加課金

GLM-5-Turbo × OpenCode：使った分だけ
・1日100本でも月500円程度
・上限なし・5時間ウィンドウなし
・量産すればするほど単価が下がる
```

---

## SECTION 4｜OpenCodeの設定手順：GLM系モデルをHyperframesで動かすまで

### ステップ1：OpenCodeのインストール

```bash
# Mac（Homebrew推奨）
brew install anomalyco/tap/opencode

# または curl でインストール
curl -fsSL https://opencode.ai/install | bash

# npmでもOK
npm i -g opencode-ai@latest

# バージョン確認
opencode --version
```

### ステップ2：Z.ai APIキーまたはOpenRouterの取得

**方法A：Z.ai直接API（推奨・最低コスト）**

```
1. https://z.ai にアクセス
2. アカウント作成・ログイン
3. API Keys → Create API Key
4. キーをコピー（sk-zai-...）
```

**方法B：OpenRouter経由（簡単・複数モデル管理が楽）**

OpenRouterダッシュボードにアクセスし、「Create API Key」をクリックしてキーをコピーします。その後`/connect`コマンドを実行してOpenRouterを検索します。

```
1. https://openrouter.ai にアクセス
2. Sign up → Dashboard → Keys → Create Key
3. キーをコピー（sk-or-v1-...）
```

### ステップ3：OpenCodeにプロバイダーを設定する

OpenCodeは設定と認証情報を2つのファイルに分けています。設定は`~/.config/opencode/opencode.jsonc`でプロバイダー、モデル、動作を定義し、認証情報は`~/.local/share/opencode/auth.json`にAPIキーを保存します。

片方だけ更新してもう片方を忘れるのが最も多いセットアップミスです。

**opencode.jsonc を作成（Z.ai直接の場合）：**

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "provider": {
    "zai": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://open.bigmodel.cn/api/paas/v4"
      },
      "models": {
        "glm-5.1": {},
        "glm-5-turbo": {},
        "glm-5": {}
      }
    }
  },
  // デフォルトモデルの設定
  "model": "zai/glm-5-turbo",
  "autoshare": false
}
```

**opencode.jsonc を作成（OpenRouter経由の場合）：**

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "provider": {
    "openrouter": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://openrouter.ai/api/v1"
      },
      "models": {
        "z-ai/glm-5.1": {},
        "z-ai/glm-5-turbo": {},
        "z-ai/glm-5": {}
      }
    }
  },
  "model": "openrouter/z-ai/glm-5-turbo"
}
```

**auth.json にAPIキーを設定：**

```json
// ~/.local/share/opencode/auth.json
{
  "zai": {
    "type": "api",
    "key": "あなたのZ.ai APIキー"
  }
}
```

または OpenRouter の場合：

```json
{
  "openrouter": {
    "type": "api",
    "key": "あなたのOpenRouter APIキー"
  }
}
```

### ステップ4：接続確認

```bash
# OpenCodeを起動
opencode

# モデル一覧確認
/models

# z-ai/glm-5-turboが見えることを確認

# モデルを切り替える
/model openrouter/z-ai/glm-5-turbo

# または（Z.ai直接の場合）
/model zai/glm-5-turbo
```

---

## SECTION 5｜Hyperframesスキルの代替設定：OpenCodeでの実装方法

### 重要な問題：`/hyperframes`スラッシュコマンドはOpenCodeで動かない

Claude CodeのHyperframesスキルは`npx skills add heygen-com/hyperframes`でインストールするもので、Claude Code専用の仕組みです。OpenCodeにはこの`/hyperframes`スラッシュコマンドがそのままでは存在しません。

ただし、OpenCodeには同等の機能を実現できる仕組みがあります。

### 解決策：OpenCodeのカスタムコマンドでHyperframesを再現する

OpenCodeはユーザーが作成できるカスタムコマンドをサポートしており、AIアシスタントに事前定義されたプロンプトを素早く送ることができます。カスタムコマンドは3つの場所のいずれかにMarkdownファイルとして保存された事前定義プロンプトです。各`.md`ファイルがカスタムコマンドになります。ファイル名（拡張子なし）がコマンドIDになります。

**Hyperframesカスタムコマンドの作成手順：**

```bash
# コマンド保存ディレクトリを作成
mkdir -p ~/.config/opencode/commands
```

**hyperframes.md を作成：**

```bash
cat > ~/.config/opencode/commands/hyperframes.md << 'EOF'
# Hyperframes Video Composition Generator

あなたはHyperframes動画制作スペシャリストです。
以下のルールを厳守してください。

## 絶対ルール
1. **class="clip"を必ずすべての時間指定要素につける**
2. **window.__timelinesにGSAPタイムラインを必ず登録する**
3. **GSAPはCDN（gsap@3.14.2）からのみ読み込む**
4. **Reactは絶対に使わない（素のHTMLのみ）**
5. **実装後はnpx hyperframes lintを実行してエラー0を確認する**

## HTMLの基本構造

\`\`\`html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>
  <div id="root"
       data-composition-id="[COMPOSITION_ID]"
       data-start="0"
       data-width="[WIDTH]"
       data-height="[HEIGHT]">

    <!-- 各要素にclass="clip"とdata属性が必須 -->
    <div id="element-1"
         class="clip"
         data-start="0"
         data-duration="5"
         data-track-index="0">
      コンテンツ
    </div>

    <script>
      const tl = gsap.timeline({ paused: true });
      // アニメーションをここに書く
      tl.from("#element-1", { opacity: 0, duration: 1 }, 0);

      // 必ずwindow.__timelinesに登録する
      window.__timelines = window.__timelines || {};
      window.__timelines["[COMPOSITION_ID]"] = tl;
    </script>
  </div>
</body>
</html>
\`\`\`

## アスペクト比の標準値
- 横型（YouTube/LP）: 1920×1080
- 縦型（TikTok/Reels/Xポスト）: 1080×1920
- 正方形（インスタグラム）: 1080×1080

## 実装フロー
1. ユーザーの要望を確認する
2. HTMLファイルをcompositions/配下に作成する
3. GSAPアニメーションを実装する
4. `npx hyperframes lint` でエラー0を確認する
5. エラーがあれば自己修正する
6. `npx hyperframes preview` でプレビューURLを提供する

## ユーザーのリクエストを受けてください：
$PROMPT
EOF
```

**OpenCodeで使う方法：**

```bash
opencode

# カスタムコマンドで呼び出す
/user:hyperframes TikTok用の15秒縦動画を作って。
「AI副業で月10万円」というタイトルが下からバウンスして出てきて、
3つのポイントが順番にスライドインする内容で。
```

### マルチエージェント設定：OpenCodeのエージェント構成

エージェントは特定のタスクとワークフローのために設定できる専門化されたAIアシスタントです。カスタムプロンプト、モデル、ツールアクセスを持つフォーカスされたツールを作成できます。

OpenCodeには2種類のエージェントがあります。プライマリエージェントは直接対話するメインアシスタントで、Tabキーでサイクルするか設定した`switch_agent`キーバインドで切り替えられます。

**Hyperframes専用エージェント設定ファイル：**

```bash
# エージェント設定ディレクトリを作成
mkdir -p ~/.config/opencode/agents
```

**hyperframes-planner.md（設計エージェント）：**

```markdown
---
name: hyperframes-planner
description: Hyperframes動画の構成設計を担当。HTMLは書かない。
model: openrouter/z-ai/glm-5.1
temperature: 0.3
tools:
  - read
mode: primary
---

あなたはHyperframes動画の設計スペシャリストです。
HTMLの実装は行いません。設計書のみ出力します。

出力形式：
- 総尺（秒）
- シーン数と各シーンの時間配分（開始〜終了秒）
- 各シーンのコンテンツ（テキスト・画像・動画ファイル名）
- アニメーション方向性（GSAPのeasing・duration指定）
- カラーパレット（HEXコード指定）
- フォント（Google Fonts名）
- 使用するビルトインブロック（必要な場合）
```

**hyperframes-coder.md（実装エージェント）：**

```markdown
---
name: hyperframes-coder
description: 設計書を受け取りHTMLを実装するエージェント。
model: openrouter/z-ai/glm-5-turbo
temperature: 0
tools:
  - read
  - write
  - edit
  - bash
mode: primary
---

あなたはHyperframes HTML実装スペシャリストです。

絶対ルール：
1. class="clip" を必ずすべての時間指定要素につける
2. window.__timelines に必ずGSAPタイムラインを登録する
3. GSAPはCDN（gsap@3.14.2）からのみ読み込む
4. Reactは絶対に使わない
5. 実装後は必ずnpx hyperframes lint を実行する
6. lintエラーがあれば自動修正してから完了を報告する
```

**hyperframes-qa.md（QAエージェント）：**

```markdown
---
name: hyperframes-qa
description: lint確認とドラフトレンダリングを担当する。
model: openrouter/z-ai/glm-5-turbo
temperature: 0
tools:
  - bash
  - read
mode: subagent
---

チェックリスト（全項目必須）：
1. npx hyperframes lint → エラー0件確認
2. class="clip"の付け忘れチェック
3. window.__timelinesへの登録漏れチェック
4. npx hyperframes render --quality draft でテスト出力

問題なし → "QA完了。本番render可能です"
問題あり → 具体的な問題箇所と修正内容を出力
```

**エージェント切り替えの実際の操作：**

```bash
# OpenCodeを起動
opencode

# Tabキーでエージェントを切り替える
# planner → coder → qa の順に切り替え可能

# または@メンションで直接指定
@hyperframes-planner 45秒のSaaS紹介動画を設計して

# 設計書が出たら
@hyperframes-coder 上の設計書でHTMLを実装して

# 実装完了後
@hyperframes-qa チェックして
```

---

## SECTION 6｜OpenCode × GLM × Hyperframesの完全ワークフロー

### 実際の1本作成フロー（コマンド全量）

```bash
# ターミナル1：Hyperframesプロジェクト準備
cd ~/videos
npx hyperframes init my-glm-video --example warm-grain
cd my-glm-video

# ターミナル2：OpenCodeを起動（GLM-5-Turbo使用）
opencode

# OpenCode内での操作
/model openrouter/z-ai/glm-5-turbo

# カスタムコマンドで動画生成を指示
/user:hyperframes
9:16縦型15秒の動画を作って。
テーマ：「ChatGPTで副業を始める3ステップ」
スタイル：ダークモード、白文字、オレンジアクセント
アニメーション：各ステップが1秒おきに下からスライドイン
使用フォント：Noto Sans JP

# → compositions/video.html が生成される

# HTMLが生成されたらlint確認
# （QAエージェントに任せる場合）
@hyperframes-qa 確認して

# プレビュー（別ターミナルで）
npx hyperframes preview

# 調整が必要なら（GLM-5-Turboに直接話しかける）
タイトルをもう少し大きく。
ステップ3のアニメーションを遅くして。

# 完成したらレンダリング
# （OpenCodeから直接コマンドを実行させる）
npx hyperframes render --output my-video.mp4
```

### 量産バッチ処理（OpenCodeの非対話モード）

OpenCodeに直接プロンプトをコマンドライン引数として渡すことで非対話モードで実行できます。これはスクリプティング、自動化、フルTUIを起動せずに素早い回答が欲しい場合に便利です。

```bash
#!/bin/bash
# batch_generate.sh：GLM-5-Turboで動画を一括生成

themes=(
  "ChatGPTで月10万円稼ぐ方法"
  "AI副業を始める3ステップ"
  "Hyperframesで動画量産する方法"
)

for i in "${!themes[@]}"; do
    echo "生成中: ${themes[$i]}"
    
    # OpenCodeの非対話モードでHTMLを生成
    opencode -p "
    /user:hyperframes
    テーマ「${themes[$i]}」で9:16縦型15秒動画のHTMLを作って。
    compositions/video_${i}.html に保存して。
    lintエラー0を確認してから完了を報告して。
    " -q
    
    # レンダリング
    npx hyperframes render \
      --composition video_${i} \
      --output renders/video_${i}.mp4
    
    echo "完了: renders/video_${i}.mp4"
done
```

---

## SECTION 7｜OpenCode × GLM の実用上の注意点と限界

### 注意点①：Hyperframesスキルのネイティブ対応はない

Claude Codeの`/hyperframes`スラッシュコマンドはClaude Code専用の仕組みです。OpenCodeではカスタムコマンド（`~/.config/opencode/commands/hyperframes.md`）で同等の機能を作る必要があります。設定手順はSECTION 5に書いた通りです。

### 注意点②：GLM-5.1のピーク時間帯の課金倍増

北京時間14時〜18時（日本時間15時〜19時）のピーク時間帯は標準レートの3倍のクォータを消費します。

→ 日本の夕方〜夜に大量生成する場合はコストが跳ね上がります。**量産バッチは深夜〜早朝に実行する**のが節約になります。

### 注意点③：GLM-5-TurboはクローズドソースでZ.ai依存

Z.aiはGLM-5-Turboを導入しましたが、これはエージェントベースのワークフロー向けに設計された高速でわずかに安価なプロプライエタリ版で、オープンソース戦略からの注目すべき転換を示しています。フラッグシップのGLM-5とは異なり、GLM-5-TurboはクローズドソースでありZ.aiの商業的提供として位置づけられています。

→ **コスト最優先かつプライバシー重視なら、オープンソース版のGLM-5.1をローカルで動かす**という選択肢もあります。ただし必要GPUがH100×8枚以上なので個人には非現実的です。

### 注意点④：GLM-5.1のベンチマークは独立検証待ち

独立した検証はまだ待ちの状態です。価格とスペックは2026年4月2日時点のZ.ai公式ドキュメントで確認されています。すべてのベンチマーク数値はZ.aiの自己申告データです（特に断りがない限り）。独立した検証がなされるまでは暫定的なものとして扱ってください。

---

## SECTION 8｜結論：あなたの状況別・最適解の選択肢

```
【状況A：今すぐ始めたい、技術的にあまり詳しくない】
→ Claude Code Pro（$20/月）が最短

理由：
- /hyperframesがすぐ使える
- 設定ゼロ
- 1日1〜3本なら上限に引っかからない
- まず動くものを作ることが最優先

【状況B：毎日5〜10本量産したい、コストを最適化したい】
→ OpenCode × GLM-5-Turbo（従量課金）が最適

理由：
- 5時間ウィンドウ制限がない
- 月500〜2,000円でClaude Code Pro相当以上の量産が可能
- トークン切れの心配なし
- カスタムコマンドの設定さえ終われば同じ操作感

【状況C：長期的な自動化・CI/CD・プライバシー重視】
→ OpenCode × GLM-5.1（API従量課金）

理由：
- MITライセンス・オープンソースで透明性が高い
- SWE-Bench ProでClaude Opus 4.6とほぼ同等性能
- 長時間自律実行（最大8時間）に向いている
- 将来的にセルフホストも検討できる

【状況D：コストゼロで試したい】
→ OpenCode × Gemini CLI（無料枠）でまず試す

Gemini CLIは1分60リクエスト・1日1,000リクエスト・
100万トークンコンテキストが無料。
OpenCodeからOpenRouter経由でも
一部無料枠モデルが使える。
```

---

## まとめ：判断マトリクス

| 判断軸 | Claude Code | OpenCode × GLM |
|-------|------------|----------------|
| セットアップの速さ | ◎即日 | △1〜2時間（設定必要） |
| トークン上限 | ✗あり（5時間枠） | ◎なし |
| コスト（月30本） | $20固定 | 約$0.15 |
| コスト（月300本） | $20+超過課金 | 約$1.5 |
| Hyperframesネイティブ対応 | ◎`/hyperframes` | △カスタム設定で再現 |
| モデル性能（HTML生成） | ◎Claude Opus 4.7 | ◎GLM-5.1（同等クラス） |
| ローカル実行 | ✗不可 | ◎Ollama経由で可 |
| 量産・CI/CD適性 | △上限に引っかかる | ◎制限なし |

**一言でまとめると：今日から始めるならClaude Code Pro。量産・コスト最適化・自動化が目標ならOpenCode×GLM-5-Turboが最適解です。**