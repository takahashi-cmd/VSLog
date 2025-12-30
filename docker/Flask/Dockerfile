FROM python:3.13.5

# Pythonの出力をバッファリングしないように設定（ログが見やすくなる）
ENV PYTHONUNBUFFERED=1

# コンテナ内のワーキングディレクトリを指定
WORKDIR /app

# matplotlibの日本語対応のフォントパッケージを先にインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-ipaexfont \
    && rm -rf /var/lib/apt/lists/*

# カレントディレクトリのrequirements.txtをワーキングディレクトリ直下にコピー
# 依存関係ファイルのみ先にコピー（キャッシュ効率化のため）
COPY requirements.txt .

# pipをアップデートして、Pythonのパッケージをインストール
# ローカルの保存用ディレクトリ（キャッシュ）の影響を排除して、常に最新のパッケージをインストールしたいため、--no-cache-dirを採用
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Flaskコンテナの起動時コマンド
ENTRYPOINT ["/bin/sh", "-c", "flask db upgrade && flask run --host=0.0.0.0 --debug"]
