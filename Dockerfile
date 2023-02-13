
# ベースとなるイメージを指定
FROM python:3
# バッファにデータを保持しない設定(1でなくても任意の文字でいい)
ENV PYTHONUNBUFFERED 1
# コンテナの中にディレクトリを作成
RUN mkdir /code
# 作業ディレクトリを指定
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
