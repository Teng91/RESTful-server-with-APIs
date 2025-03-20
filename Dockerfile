# 使用官方 Python 基礎映像檔
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製專案檔案到容器中
COPY . /app

# 安裝必要的系統套件和 Python 套件
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 預設的埠
EXPOSE 5000

# 啟動 Flask 應用程式
CMD ["python", "app.py"]