# audio-search-app
- [環境構築のGitHubリポジトリ](https://github.com/Ituki-t/audio-search-env-meilisearch.git)

# 仕様書
## 概要
- このアプリケーションは、音声データをテキスト化し、検索キーワードから検索できるWebアプリケーション。
- ユーザーが音声ファイルをアップロードすると、自動で文字起こしされ、その内容が保存される。
## 背景
- 長時間の音声や動画において、特定の内容を探す際に手動で探す必要があり、目的の箇所を見つけるのに時間がかかるという課題があった。
- そこで、目的箇所のタイムスタンプを自動で取得できれば効率的に内容を確認できると考えた。
## 機能
- 音声ファイルのアップロード機能
- 音声の自動文字起こし機能
- 音声ファイルの一覧表示機能
- 音声からテキスト化された文章の編集機能
- 音声ファイル削除機能
- Elasticsearch、Meilisearchを用いたテキスト検索機能
- 検索結果から該当時間の表示、該当時間から再生機能
## 使用技術
- フロントエンド : Django Template
- バックエンド : Django
  - 管理機能が充実しており、開発速度を重視して採用
- 非同期処理 : Celery + Redis
  - 音声の文字起こし処理に時間がかかるため、ユーザー体験を損なわないようバックグラウンド処理として実装
- 検索エンジン : Elasticsearch, Meilisearch
  - データ量が増加した時の検索性能を考慮し採用
  - これら検索エンジンの性能の比較を行うため2つの検索エンジンを併用する
- 音声認識 : Whisper
  - 音声ファイルをテキスト化するための手段として採用
- 環境構築 : Docker
  - 複数のサービスを一括で管理するため、Docker Composeを用いて構築
## データ設計
Voice
- id
- title
- audio_file
- transcribe_status(未使用)

Segment
- id
- voice_id
- start_time
- end_time
- text
## 工夫した点
- 音声の文字起こしに時間がかかってしまいユーザー体験を損なってしまうため、Celeryを用いてバックグラウンド処理できるよう工夫した。
- また、Whisperの誤認識があり検索制度が下るという問題があったため、音声データを一定時間で区切り、各区間でのテキスト文を編集できる仕組みを実装した
## 今後の展望
音声・動画の情報共有や、会議などの議事録での活用を目指し、ユーザーごとのアクセス制御を実現するため、閲覧、編集などのユーザー権限を付与する機能の実装を行う。

# README
## Recreate meilisearch's index
```python
# shell
from voices.meili_service import recreate_index
recreate_index()
```

# git
- about push
```bash
git push -u meili meili
```

## 参照
- ChatGPT
- [https://docs.djangoproject.com/ja/6.0/topics/files/](https://docs.djangoproject.com/ja/6.0/topics/files/)(2026/02/12)
- [https://rinsaka.com/django4/comment/06-install_app.html](https://rinsaka.com/django4/comment/)(2026/02/12)
- [https://docs.djangoproject.com/ja/6.0/topics/http/file-uploads/](https://docs.djangoproject.com/ja/6.0/topics/http/file-uploads/)(2026/01/13)
- [https://docs.djangoproject.com/ja/6.0/ref/request-response/#fileresponse-objects](https://docs.djangoproject.com/ja/6.0/ref/request-response/#fileresponse-objects)(2026/01/13)
- [https://zenn.dev/shimakaze_soft/articles/bbd859803c63a6](https://zenn.dev/shimakaze_soft/articles/bbd859803c63a6)(2026/02/14)
- [https://qiita.com/NEKOYASAN/items/532f71fab273d4cd4cd3](https://qiita.com/NEKOYASAN/items/532f71fab273d4cd4cd3)(2026/02/24)
- [https://web-camp.io/magazine/archives/80578/](https://web-camp.io/magazine/archives/80578/)(2026/03/18)
- [https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/currentTime)(2026/04/12)