# websecurity

一个 Flask 动态网站，包含登录、注册、个人主页和留言功能。

## 本地运行

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
python app.py
```

打开 http://127.0.0.1:5000 。

## 发布到 GitHub + Render

1. 将本项目上传到 GitHub 仓库。
2. 在 Render 中选择 **New → Blueprint**，连接该仓库。
3. Render 会根据 `render.yaml` 自动安装依赖、初始化数据库并启动网站。
4. 部署完成后，Render 会提供一个任何人都能访问的 `onrender.com` 地址。

SQLite 数据库配置了持久磁盘，避免服务重启后用户和留言丢失。不要把 `users.db` 中的真实用户数据提交到公开仓库。
