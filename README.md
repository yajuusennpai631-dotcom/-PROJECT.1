# Railway BOT 基盤

## ローカル実行
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # トークンを記入
export $(grep -v '^#' .env | xargs)
python bot.py
```

## Railwayへのデプロイ
1. このフォルダをGitHubリポジトリにpush
2. Railwayで **New Project → Deploy from GitHub repo** を選択
3. サービスの **Variables** に `DISCORD_TOKEN` を追加
4. 自動でビルド・起動されます(`railway.json` の startCommand を使用)

※ HTTPサーバーを持たないワーカー型なので、ドメイン発行(Generate Domain)は不要です。

## 構成
- `bot.py` … エントリーポイント(`/ping` コマンド付き)
- `railway.json` … ビルド・起動・再起動ポリシー
- `requirements.txt` … 依存パッケージ
