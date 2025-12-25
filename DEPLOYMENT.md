# Cloud Deployment Guide / 云端部署指南

Since "Entropy God" is a Python application, it needs a backend server to run. The easiest and free way to deploy is using **Streamlit Community Cloud**.
由于“熵之神”是 Python 应用，必须有后台服务器运行。免费且最简单的方式是使用 **Streamlit Community Cloud**。

## Option 1: Streamlit Community Cloud (Recommended / 推荐)
Suitable for demos and MVPs. Completely Free.
适合演示和 MVP。完全免费。

### Prerequisites / 准备工作
1.  **GitHub Account**: You need a GitHub account.
2.  **App Code**: Your code must be uploaded to a GitHub repository.

### Steps / 步骤
1.  **Push to GitHub / 上传代码到 GitHub**:
    *   Create a new repository on [GitHub](https://github.com/new).
    *   Upload all files in this folder to the repository.
    *   **Crucial**: Ensure `requirements.txt` is in the root URL. I have already created this file for you.

2.  **Deploy / 部署**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Log in with GitHub.
    *   Click **"New app"**.
    *   Select your repository used above.
    *   **Main file path**: Enter `app.py`.
    *   Click **"Deploy!"**.

3.  **Wait / 等待**:
    *   Streamlit will install dependencies (from `requirements.txt`) and start the server.
    *   Once you see the app running, copy the URL (e.g., `https://entropy-god.streamlit.app`).

4.  **Update App / 更新 App**:
    *   **Android App**: Re-build your Android App (using Method 2 in `README_ANDROID.md`) and change the URL to this new Cloud URL.
    *   **PWA**: Users can just visit the new URL on their phone.

---

## Option 2: Traditional Cloud Server (Advanced)
**VPS (阿里云/腾讯云/AWS)** using Docker or direct Python.

If you have a server (Ubuntu/CentOS):

1.  **Upload Code**: Copy files to server.
2.  **Install Python 3.9+**.
3.  **Install Deps**: `pip install -r requirements.txt`.
4.  **Run**: 
    ```bash
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
    ```
5.  **Background Run (Keep alive)**:
    Use `nohup` or `tmux`:
    ```bash
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > log.txt 2>&1 &
    ```
