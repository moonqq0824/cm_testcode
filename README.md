-----

### **回家後，如何快速還原專案環境：SOP 清單**

#### **第零步：基礎軟體安裝 (只需做一次)**

在你的新電腦上，確保已安裝以下核心軟體：

1.  **Git**: 前往 [Git 官網](https://git-scm.com/downloads)下載並安裝。
2.  **Python**: 前往 [Python 官網](https://www.python.org/downloads/)下載並安裝 (建議 3.10 或更新版本)。
3.  **Node.js**: 前往 [Node.js 官網](https://nodejs.org/)下載並安裝 **LTS (長期支援)** 版本。
4.  **VS Code**: 前往 [VS Code 官網](https://code.visualstudio.com/)下載並安裝。
5.  **VS Code 擴充功能**: 打開 VS Code，在擴充功能市集中安裝以下我們用過的工具：
      * `Python` (由 Microsoft 提供)
      * `Pylance` (由 Microsoft 提供)
      * `SQLite` (由 alexcvzz 提供)

#### **第一步：從 GitHub 下載你的專案**

1.  打開你的 GitHub 專案頁面 (`https://github.com/moonqq0824/cm_testcode`)。
2.  點擊綠色的 `<> Code` 按鈕，複製 **HTTPS** 的 URL。
3.  打開電腦的終端機 (Terminal)，`cd` 到你想要存放專案的資料夾 (例如 `Desktop`)，然後執行 `git clone` 指令：
    ```bash
    git clone https://github.com/moonqq0824/cm_testcode.git
    ```
4.  下載完成後，進入專案資料夾：
    ```bash
    cd cm_testcode
    ```
5.  **設定 Git 身分** (如果這台電腦是第一次使用 Git)：
    ```bash
    git config --global user.name "你的名字"
    git config --global user.email "你的Email"
    ```

#### **第二步：設定後端 (Backend) 環境**

1.  **進入後端資料夾**：
    ```bash
    cd backend
    ```
2.  **建立並啟用虛擬環境**：
    ```bash
    # 建立 venv
    python -m venv venv

    # 啟用 venv (Windows)
    .\venv\Scripts\activate
    # 啟用 venv (macOS/Linux)
    # source venv/bin/activate
    ```
3.  **安裝所有 Python 套件**：
      * 這一步會讀取 `requirements.txt` 檔案，自動安裝我們需要的所有東西 (`Flask`, `Flask-RESTx` 等)。
    <!-- end list -->
    ```bash
    pip install -r requirements.txt
    ```
4.  **設定 VS Code 解譯器**：
      * 在 VS Code 中，按下 `Ctrl+Shift+P`，執行 `Python: Select Interpreter`，然後選擇路徑中包含 `venv` 的那個 Python 解譯器。
5.  **建立資料庫**：
      * `app.db` 檔案因為被 `.gitignore` 忽略了，所以不會被下載，我們需要手動建立它。
    <!-- end list -->
    ```bash
    # 進入 Flask shell
    flask shell

    # 在 shell 環境中 (>>>)，執行建立指令
    >>> db.create_all()

    # 離開 shell
    >>> exit()
    ```
6.  **(可選) 啟動後端伺服器進行測試**：
    ```bash
    flask run
    ```
      * 你可以打開瀏覽器訪問 `http://127.0.0.1:5000/api/v1/samples`。

#### **第三步：設定前端 (Frontend) 環境**

1.  **打開一個新的終端機**，並同樣 `cd` 到專案根目錄 `cm_testcode`。
2.  **進入前端資料夾**：
    ```bash
    cd frontend
    ```
3.  **安裝所有 Node.js 套件**：
      * 這一步會讀取 `package.json` 檔案，自動安裝 `Vue` 和 `Vite` 等所有前端需要的工具。
    <!-- end list -->
    ```bash
    npm install
    ```
4.  **(可選) 啟動前端開發伺服器進行測試**：
    ```bash
    npm run dev
    ```
      * 你可以打開瀏覽器訪問它提供的網址 (例如 `http://localhost:5173`)。

-----