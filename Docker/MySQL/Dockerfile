FROM mysql:9.3.0

# Mysqlのローカル設定ファイルをコンテナにコピー
COPY /Docker/MySQL/my.cnf /etc/mysql/conf.d/my.cnf

# init.sqlをコンテナの/docker-entrypoint-initdb.dと共有
COPY /Docker/MySQL/init.sql /docker-entrypoint-initdb.d
