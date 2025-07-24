# YouTube Short Video Analysis Tool

YouTube Data APIを使用して、特定のキーワードでショート動画を検索し、人気のコメントを収集するツールです。

## 機能

- **キーワード検索**: "参政党", "選挙", "政治" のキーワードでYouTubeショート動画を検索
- **再生回数フィルタリング**: 100万回以上の再生回数の動画のみを対象
- **コメント収集**: 1000いいね以上の人気コメントを収集
- **CSV出力**: 動画URL、コメント内容、いいね数などをCSV形式で出力

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. YouTube Data API キーの設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. YouTube Data API v3を有効化
3. APIキーを作成
4. `.env.example`を`.env`にコピーし、APIキーを設定:

```bash
cp .env.example .env
```

`.env`ファイルを編集:
```
YOUTUBE_API_KEY=your_actual_api_key_here
```

## 使用方法

```bash
python main.py
```

## 出力

分析結果は `youtube_analysis_results.csv` ファイルに保存されます。

### CSV カラム

- `video_url`: 動画のURL
- `video_title`: 動画のタイトル
- `video_views`: 動画の再生回数
- `comment_text`: コメントの内容
- `comment_likes`: コメントのいいね数
- `comment_author`: コメント投稿者
- `comment_published`: コメント投稿日時

## 注意事項

- YouTube Data APIには1日あたりのクォータ制限があります
- レート制限を避けるため、リクエスト間に適切な間隔を設けています
- APIキーは適切に管理し、公開リポジトリにコミットしないでください

## ファイル構成

- `main.py`: メイン実行スクリプト
- `youtube_client.py`: YouTube Data API クライアント
- `video_analyzer.py`: 動画分析ロジック
- `requirements.txt`: 依存パッケージ一覧
- `.env.example`: 環境変数の例