# 長いコマンドを省略して打てるようにするための設定
# PHONYはMakefileで独自コマンドを設定するための宣言
.PHONY: up down build logs sh migrate mm csu db

up:        ## 起動
	docker compose up -d
down:      ## 停止
	docker compose down
build:     ## ビルド
	docker compose up --build
logs:      ## Flaskのログ確認
	docker compose logs -f app
sh:        ## Flaskコンテナのシェルに入る
	docker compose exec -it app /bin/bash
migrate:   ## マイグレーション実行
	docker compose exec app flask db migrate
db:		   ## MySQLコンテナに入る
	docker compose exec -it db mysql -u testuser -p