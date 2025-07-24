# GitHub Actions での使用方法

## セットアップ

1. **YouTube API キーをSecretsに追加**
   - GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」
   - 「New repository secret」をクリック
   - Name: `YOUTUBE_API_KEY`
   - Secret: あなたのYouTube Data API キー

## 実行方法

1. GitHubリポジトリの「Actions」タブに移動
2. 「YouTube Analysis」ワークフローを選択
3. 「Run workflow」をクリック
4. パラメータを入力：
   - **Keywords**: 検索キーワード（スペース区切り）
     - 例: `神谷 参政党 政治`
   - **Output filename**: 出力CSVファイル名  
     - 例: `results.csv`
5. 「Run workflow」をクリックして実行

## 結果の取得

実行完了後、「Artifacts」セクションから結果のCSVファイルをダウンロードできます。

## 注意事項

- YouTube Data APIの1日あたりのクォータ制限にご注意ください
- 実行には数分かかる場合があります
- CSVファイルは30日間保存されます