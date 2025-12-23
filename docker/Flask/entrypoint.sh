#!/bin/bash
# Flaskアプリ起動（migrateは手動で明示的に実施する）
# 再利用性や可読性を向上させるため、FlaskのDockerfileには実行コマンドをまとめずに、本ファイルにまとめる。
exec flask run --host=0.0.0.0 --debug


