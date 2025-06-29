
# SafeEmail 项目说明

SafeEmail 是一个基于 Flask 构建的邮件过滤和展示系统，支持指定发件人与收件人邮箱地址，从 QQ 邮箱中获取最新的匹配邮件并展示内容。前端使用 HTML/CSS/JavaScript 构建，界面简洁直观。

## 📦 项目结构

```
.
├── main.py         # Flask 后端主程序
├── find.py         # 邮件拉取逻辑
├── config.info     # 安全发件人列表（每行一个邮箱地址）
├── templates/
│   └── index.html  # 前端页面
```

## 🚀 功能介绍

- ✅ 从 QQ 邮箱中抓取邮件
- ✅ 根据发件人与收件人精准匹配邮件
- ✅ 前端页面支持选择发件人 + 输入收件人邮箱
- ✅ 展示最新一封匹配邮件的标题、发件人、收件人、时间与正文内容
- ✅ 支持配置可信发件人白名单

## 🔧 使用说明

### 1. 准备配置文件

在根目录下创建 `config.info` 文件，添加允许查询的发件人邮箱，每行一个，例如：

```
no-reply@cursor.sh
another-safe@domain.com
```

### 2. 配置邮箱账号

编辑 `find.py` 文件，配置 QQ 邮箱账号信息：

```python
EMAIL = "你的QQ邮箱@qq.com"
PASSWORD = "你的授权码"
IMAP_SERVER = "imap.qq.com"
```

> ⚠️ 注意：QQ邮箱需开启 IMAP 协议，并使用授权码登录。

### 3. 启动服务

```bash
python main.py
```

浏览器访问：`http://localhost:9838`

### 4. 使用前端页面

- 选择发件人
- 输入收件人邮箱地址
- 点击“搜索”按钮
- 若匹配成功，将显示邮件内容

## 📄 接口说明

### `/get_safe_senders`

获取安全发件人列表（来自 `config.info`）

- 请求方式：GET
- 响应：JSON 数组

### `/ymail`

根据发件人和收件人邮箱查询邮件

- 请求方式：POST
- 请求参数（JSON）：
```json
{
  "sender": "发件人邮箱",
  "recipient": "收件人邮箱"
}
```
- 响应：邮件数据或错误提示

## 🛡️ 安全性

- 所有请求邮箱地址的发件人需在 `config.info` 白名单中
- 对邮件正文做了字符编码处理，避免乱码

## 📌 注意事项

- 每次查询仅返回最新一封匹配邮件
- 当前版本仅支持 QQ 邮箱（imap.qq.com）
- 若遇到邮箱登录失败，请检查授权码或网络
