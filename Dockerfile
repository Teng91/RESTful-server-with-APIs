# 使用官方的 Python 基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄的內容到容器中的 /app 目錄
COPY . /app

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 預設的埠
EXPOSE 5000

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 執行 Flask 應用程式
CMD ["flask", "run"]