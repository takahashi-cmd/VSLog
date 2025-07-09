#!/bin/bash

# パスの設定
export PYTHONPATH=/code

# 初回のみ：migrationsディレクトリがなければ初期化
if [ ! -d "migrations" ]; then
    flask db init
fi

# 常時：マイグレーションファイル作成＋適用
flask db migrate -m "auto migration"

# MySQL が起動するまでリトライしながらマイグレーション適用
until flask db upgrade; do
  echo "Waiting for MySQL to be ready..."
  sleep 2
done

# Flaskアプリ起動
exec flask run --host=0.0.0.0 --debug


