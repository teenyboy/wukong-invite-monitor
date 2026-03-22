# GitHub 发布指南

## 📦 准备工作

### 方式 1：使用 GitHub CLI（推荐）

```bash
# 1. 登录 GitHub
gh auth login

# 2. 创建仓库并推送
cd ~/.openclaw/workspace/skills/wukong-invite-monitor
gh repo create wukong-invite-monitor --public --source=. --remote=origin --push
```

### 方式 2：使用 Git 命令

```bash
# 1. 在 GitHub 上创建新仓库
# 访问：https://github.com/new
# 仓库名：wukong-invite-monitor
# 可见性：Public
# 不要初始化 README（我们已经有代码了）

# 2. 添加远程仓库并推送
cd ~/.openclaw/workspace/skills/wukong-invite-monitor
git remote add origin https://github.com/teenyboy/wukong-invite-monitor.git
git branch -M main
git push -u origin main
```

### 方式 3：使用 Git + SSH

```bash
# 1. 配置 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 添加 SSH 密钥到 GitHub
# 访问：https://github.com/settings/keys
# 复制 ~/.ssh/id_ed25519.pub 的内容

# 3. 推送代码
cd ~/.openclaw/workspace/skills/wukong-invite-monitor
git remote add origin git@github.com:teenyboy/wukong-invite-monitor.git
git branch -M main
git push -u origin main
```

---

## 📁 已准备的文件

所有文件已准备就绪，位于：
```
~/.openclaw/workspace/skills/wukong-invite-monitor/
```

包含：
- ✅ 完整源代码
- ✅ README.md（GitHub 版本）
- ✅ LICENSE（MIT）
- ✅ .gitignore
- ✅ 完整文档

---

## 🎯 推送后步骤

### 1. 设置仓库信息

在 GitHub 仓库页面：
- 添加描述：`钉钉悟空邀请码自动监控工具，零 token 消耗，支持本地 OCR 识别和心跳推送通知`
- 添加 Topics: `openclaw`, `skill`, `wukong`, `monitor`, `ocr`, `dingtalk`
- 设置网站：ClawHub 页面链接

### 2. 创建 Release

```bash
# 使用 GitHub CLI
gh release create v2.1.0 --title "v2.1.0 - 心跳推送通知" --notes "新增心跳推送通知功能，只在官方更新时间段检查"
```

或手动创建：
- 访问：https://github.com/teenyboy/wukong-invite-monitor/releases
- 点击 "Create a new release"
- Tag version: `v2.1.0`
- Release title: `v2.1.0 - 心跳推送通知`

### 3. 更新 ClawHub

ClawHub 已发布 v2.1.0，等待安全审核通过后会自动同步。

---

## 📊 GitHub 仓库结构

```
teenyboy/wukong-invite-monitor
├── 📄 README.md              # 主文档（GitHub 版本）
├── 📄 SKILL.md               # Skill 主文档
├── 📄 QUICKSTART.md          # 快速开始
├── 📄 HEARTBEAT.md           # 心跳配置指南
├── 📄 LOCAL-OCR.md           # OCR 配置详解
├── 📄 LICENSE                # MIT 许可证
├── 📄 _meta.json             # 元数据
├── 📁 scripts/               # 脚本目录
│   ├── monitor_lite.py
│   ├── ocr_local.py
│   ├── heartbeat-check.py
│   ├── check-new-code.py
│   ├── notify-watcher.py
│   ├── install-dependencies.sh
│   └── setup-cron.sh
└── 📁 .github/               # GitHub 配置
    └── README_GITHUB.md      # GitHub README 源文件
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/teenyboy/wukong-invite-monitor
- **ClawHub 页面**: https://clawhub.ai/teenyboy/wukong-invite-monitor
- **Issues**: https://github.com/teenyboy/wukong-invite-monitor/issues
- **Releases**: https://github.com/teenyboy/wukong-invite-monitor/releases

---

## 💡 提示

### 批量推送命令

```bash
# 一键推送（如果已配置 GitHub CLI）
cd ~/.openclaw/workspace/skills/wukong-invite-monitor
gh repo create wukong-invite-monitor --public --source=. --remote=origin --push
```

### 后续更新

```bash
# 修改代码后
git add .
git commit -m "feat: 更新说明"
git push
```

### 查看状态

```bash
git status
git log --oneline
```

---

## ✅ 检查清单

推送前确认：
- [ ] 所有代码文件已提交
- [ ] 文档完整（README, LICENSE, .gitignore）
- [ ] 无敏感信息（密码、密钥、个人路径）
- [ ] .gitignore 已配置
- [ ] 使用 MIT 许可证

推送后确认：
- [ ] GitHub 仓库创建成功
- [ ] 所有文件可见
- [ ] README 正确显示
- [ ] 许可证正确
- [ ] 设置仓库描述和 Topics
- [ ] 创建 v2.1.0 Release

---

**准备就绪！选择一种方式推送到 GitHub 即可。** 🚀
