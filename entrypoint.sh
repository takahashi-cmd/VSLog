#!/bin/bash

# migrations初期化
flask db init

# 初回：マイグレーションファイル作成＋適用
flask db migrate -m "Initial migration"

# 差分があればマイグレーションをアップデート
flask db upgrade

# Flaskアプリ起動
exec flask run --host=0.0.0.0 --debug


