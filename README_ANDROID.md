# Android Installation Guide / 安卓安装指南

You have three options to run "Entropy God" as an Android App.
您有三种方式将“熵之神”作为安卓 App 运行。

Note: Since this is a Python app, the "brain" must run on a server (your laptop or cloud). The Android App is just a window (shell) looking at that server.
注意：因为这是 Python应用，核心逻辑必须运行在服务器（您的电脑或云端）上。安卓 App 只是一个查看服务器的窗口（壳）。

## Method 1: Progressive Web App (Recommended / 推荐)
**No coding required. / 无需编程。**
The easiest way. Works exactly like an App.
最简单的方法，体验和原生 App 几乎一致。

1.  Start the app on your computer/server (`streamlit run app.py`).
2.  Ensure your phone is on the same Wi-Fi network.
3.  Open Chrome on your Android phone.
4.  Navigate to your computer's IP address (e.g., `http://192.168.1.5:8501`).
5.  Tap the Chrome menu (three dots) -> **"Add to Home Screen"** (添加到主屏幕).
6.  The app will appear on your home screen with the logo and launch in fullscreen mode nicely.

---

## Method 2: HBuilderX (Uni-app) - RELIABLE
**Use the provided wrapper project.** / **使用已提供的 wrapper 项目。**

Since Wap2App cloud build is restricted, we use a standard `uni-app` wrapper. I have already generated the code for you in the `uniapp_wrapper` folder.
由于 Wap2App 云打包受限，我们使用标准的 `uni-app` 壳。我已经为您在 `uniapp_wrapper` 文件夹中生成了代码。

### Steps / 步骤
1.  **Configure URL / 配置连接地址**:
    *   Open `uniapp_wrapper/pages/index/index.vue` in a text editor (or HBuilderX).
    *   Find `url: 'http://YOUR_IP_ADDRESS:8501'`.
    *   **CRITICAL**: Change it to your computer's local IP (e.g., `http://192.168.1.5:8501`).
    *   注意：务必将 `url` 修改为您电脑的实际 IP 地址。

3.  **Open in HBuilderX / 在 HBuilderX 中打开**:
    *   **IMPORTANT**: Do NOT open the main "entropy_god_mvp" folder.
    *   **重要**: 请不要直接打开最外层的 "entropy_god_mvp" 文件夹，那样会提示缺少 manifest。
    *   File -> Open Directory (文件 -> 打开目录).
    *   **Select the `uniapp_wrapper` folder to open.** (请选中 `uniapp_wrapper` 这个子文件夹打开).
    *   You should see `manifest.json` in the root of the project view.

3.  **Cloud Build / 云打包**:
    *   Menu: Publish -> Native App-Cloud Packaging (发行 -> 原生App-云打包).
    *   Select "Use DCloud Certificate" (使用公共测试证书).
    *   Click "Pack" (打包).

4.  **Install**:
    *   Download the APK and install on your phone.

---

## Method 3: Native Android App (Advanced)
**Using Android Studio.** / **使用 Android Studio。**

If you need full control or offline capabilities (not possible here due to Python), use this.
如果您需要完全控制（需要 Android Studio）。

### Steps / 步骤
1.  Create a **New Project** -> **Empty Activity** (Java).
2.  Open `AndroidManifest.xml` (in `app/src/main`) and add permissions:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" /> 
<!-- Camera needed for 'Lens' feature -->
```

3.  Inside the `<application>` tag in `AndroidManifest.xml`, add `android:usesCleartextTraffic="true"` (if you are testing with local HTTP IP):

```xml
<application
    ...
    android:usesCleartextTraffic="true">
    ...
</application>
```

4.  Replace `MainActivity.java` content with the code below.
    *   **IMPORTANT**: Change `myUrl` to your deployed URL or local IP (e.g., `http://192.168.1.X:8501`).

```java
package com.example.entropygod; // Use your actual package name

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {

    private WebView myWebView;
    private String myUrl = "http://YOUR_SERVER_IP:8501"; // CHANGE THIS!

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        myWebView = new WebView(this);
        setContentView(myWebView);

        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setMediaPlaybackRequiresUserGesture(false);

        // Handle Camera Permissions for Streamlit
        myWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                request.grant(request.getResources());
            }
        });

        myWebView.setWebViewClient(new WebViewClient());
        
        // Check Runtime Permissions
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) 
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 1);
        }

        myWebView.loadUrl(myUrl);
    }
    
    @Override
    public void onBackPressed() {
        if (myWebView.canGoBack()) {
            myWebView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
```

5.  Build -> **Build Bundle(s) / APK(s)** -> **Build APK(s)**.
