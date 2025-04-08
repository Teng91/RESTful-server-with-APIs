# RESTful Server with APIs
- 本專案是一個基於 Flask 的 RESTful API 伺服器，提供用戶管理功能，包括創建用戶、刪除用戶、批量添加用戶、獲取用戶列表以及計算用戶平均年齡等功能
- 專案包含單元測試、Swagger 文件生成以及 Docker 支援，方便開發者快速部署和測試
```
RESTful-server-with-APIs/ 
├── app.py # 主程式，包含 API 定義與邏輯 
├── unittest_app.py # 單元測試程式 
├── backend_users.csv # 用戶數據的 CSV 文件 
├── requirements.txt # Python 套件需求 
├── Dockerfile # Docker 映像檔定義 
├── docker-compose.yaml # Docker Compose 配置
```

---

## 關鍵技術與功能

### 1. **Flask 與 Flask-RESTful**
- 使用 Flask 作為 Web 框架，並透過 Flask-RESTful 提供 RESTful API 支援
- API 路由定義於 `app.py`，包括以下功能：
  - **創建用戶**：`POST /create_user`
  - **刪除用戶**：`DELETE /delete_user`
  - **獲取用戶列表**：`GET /get_users`
  - **批量添加用戶**：`POST /bulk_add_users`
  - **計算平均年齡**：`GET /average_age`

### 2. **Swagger 文件生成**
- 使用 `flasgger` 套件自動生成 API 文件。
- Swagger 文件可透過 [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs) 存取，提供互動式 API 測試

### 3. **數據處理**
- 使用 Pandas 處理批量用戶數據（CSV 文件）
- 用戶數據存儲於全域變數 `users`，結構如下：
  ```python
  users = [
      {"name": "Bulbasaur", "age": 14},
      {"name": "Charmander", "age": 22},
      ...
  ]```
### 4. **單元測試**
- 使用 Python 的內建 unittest 模組進行單元測試
- 測試檔案為 unittest_app.py，涵蓋以下測試案例：
  - 測試創建用戶時名稱為空的情況
  - 測試創建用戶時年齡超出範圍的情況
### 5. **Docker 支援**
- 提供 Dockerfile 和 docker-compose.yaml，方便部署應用程式
- 使用 Docker 可快速啟動應用程式，指令如下：```docker-compose up --build```

---

## 安裝與執行

### 1. **環境需求**
- Python 3.11 或以上版本
- pip 套件管理工具
- Docker（可選）
### 2. **安裝步驟**
- 本地執行
  1. 複製專案
  ```
  git clone https://github.com/Teng91/RESTful-server-with-APIs.git
  cd RESTful-server-with-APIs
  ```
  2. 安裝依賴庫
  ```pip install -r requirements.txt```
  3. 啟動伺服器
  ```python app.py```
  4. 開啟瀏覽器，訪問 ```http://127.0.0.1:5000/apidocs``` 查看 API 文件
- 使用Docker
  1. 建立並啟動容器
  ```docker-compose up --build```
  2. 開啟瀏覽器，訪問 ```http://127.0.0.1:5000/apidocs``` 查看 API 文件
