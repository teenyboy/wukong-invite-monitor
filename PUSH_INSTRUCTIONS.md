# GitHub 推送指南

## 🎯 快速推送

### 方式 1：GitHub CLI（最简单）

```bash
# 1. 登录 GitHub（如果还没登录）
gh auth login

# 2. 推送代码
cd ~/.openclaw/workspace/skills/wukong-invite-monitor
git push -u origin main
```

**完成！** 🎉

---

### 方式 2：使用 Personal Access Token

**步骤：**

1. **创建 Token**
   - 访问：https://github.com/settings/tokens/new
   - 选择 scopes: `repo`, `workflow`
   - 点击 "Generate token"
   - 复制生成的 token（如 `ghp_xxxxxxxxxxxx`）

2. **推送代码**
   ```bash
   cd ~/.openclaw/workspace/skills/wukong-invite-monitor
   
   # 使用 token 推送（替换 YOUR_TOKEN）
   git remote set-url origin https://ghp_xxxxxxxxxxxx@github.com/teenyboy/wukong-invite-monitor.git
   git push -u origin main
   ```

---

### 方式 3：使用 SSH

**步骤：**

1. **生成 SSH 密钥（如果还没有）**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **添加 SSH 密钥到 GitHub**
   - 复制公钥：`cat ~/.ssh/id_ed25519.pub`
   - 访问：https://github.com/settings/keys
   - 点击 "New SSH key"
   - 粘贴公钥内容

3. **推送代码**
   ```bash
   cd ~/.openclaw/workspace/skills/wukong-invite-monitor
   git remote set-url origin git@github.com:teenyboy/wukong-invite-monitor.git
   git push -u origin main
   ```

---

## ✅ 推送后验证

### 1. 检查仓库

访问：https://github.com/teenyboy/wukong-invite-monitor

确认：
- ✅ 所有文件已上传
- ✅ README 正确显示
- ✅ 提交历史完整

### 2. 设置仓库信息

在 GitHub 仓库页面：
- **描述**: `钉钉悟空邀请码自动监控工具，零 token 消耗，支持本地 OCR 识别和心跳推送通知`
- **网站**: https://clawhub.ai/teenyboy/wukong-invite-monitor
- **Topics**: `openclaw` `skill` `wukong` `monitor` `ocr` `dingtalk` `zero-token`

### 3. 创建 Release

**使用 GitHub CLI:**
```bash
gh release create v2.1.0 \
  --title "v2.1.0 - 心跳推送通知" \
  --notes "新增心跳推送通知功能，只在官方更新时间段检查，避免重复通知"
```

**或手动创建:**
1. 访问：https://github.com/teenyboy/wukong-invite-monitor/releases/new
2. Tag version: `v2.1.0`
3. Release title: `v2.1.0 - 心跳推送通知`
4. 填写描述
5. 点击 "Publish release"

---

## 🔧 故障排查

### 问题 1：认证失败

**错误信息:**
```
fatal: could not read Username for 'https://github.com'
```

**解决:**
- 使用 GitHub CLI: `gh auth login`
- 或使用 Personal Access Token

### 问题 2：SSH 密钥问题

**错误信息:**
```
Host key verification failed
```

**解决:**
```bash
# 重新生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加到 GitHub
# https://github.com/settings/keys
```

### 问题 3：权限不足

**错误信息:**
```
remote: Permission denied (publickey)
```

**解决:**
- 确认 SSH 密钥已添加到 GitHub
- 或使用 Personal Access Token

---

## 📊 完整推送流程

```bash
# 1. 登录 GitHub CLI（首次需要）
gh auth login

# 2. 进入仓库目录
cd ~/.openclaw/workspace/skills/wukong-invite-monitor

# 3. 推送代码
git push -u origin main

# 4. 创建 Release
gh release create v2.1.0 \
  --title "v2.1.0 - 心跳推送通知" \
  --notes "新增心跳推送通知功能"

# 5. 打开仓库页面
gh repo view --web
```

---

## 🎉 完成检查清单

- [ ] 代码已推送到 GitHub
- [ ] 所有文件可见
- [ ] README 正确显示
- [ ] 设置仓库描述
- [ ] 添加 Topics
- [ ] 创建 v2.1.0 Release
- [ ] 更新 ClawHub 关联

---

**选择一种方式开始推送吧！** 🚀
