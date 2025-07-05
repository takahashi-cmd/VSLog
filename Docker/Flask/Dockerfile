FROM python:3.13.5

# pycファイルおよび__pycache__の生成は行わない
ENV PYTHONDONTWRITEBYTECODE=1
# Pythonの出力をバッファリングしないように設定（ログが見やすくなる）
ENV PYTHONUNBUFFERED=1

# コンテナ内のワーキングディレクトリを指定
WORKDIR /app

# ローカルのrequirements.txtをワーキングディレクトリにコピー
# 依存関係ファイルのみ先にコピー（キャッシュ効率化のため）
COPY requirements.txt .

# pipをアップデートして、Pythonのパッケージをインストール
# ローカルの保存用ディレクトリ（キャッシュ）の影響を排除して、常に最新のパッケージをインストールしたいため、--no-cache-dirを採用
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

# ソースコードをホストにコピー
COPY . /app

# Flaskのアプリケーションを実行
CMD [ "python", "__init__.py" ]