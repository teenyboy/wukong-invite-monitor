---
name: wukong-invite-monitor
description: 钉钉悟空邀请码监控，自动截图 +OCR 识别，心跳推送通知。当前邀请码：灵山坠真经
version: 2.2.0
---

# 悟空邀请码监控 - 修复版

**当前状态：** ✅ 正常运行  
**当前邀请码：** 灵山坠真经  
**最后更新：** 2026-03-22

---

## 🚀 快速开始

```bash
cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts

# 1. 安装依赖（如已安装可跳过）
./install-dependencies.sh

# 2. 初始化状态
python3 monitor_fixed.py init

# 3. 测试检查
python3 monitor_fixed.py check

# 4. 查看状态
python3 monitor_fixed.py status
```

---

## 📋 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `check` | 执行一次检查 | `python3 monitor_fixed.py check` |
| `status` | 显示当前状态 | `python3 monitor_fixed.py status` |
| `set <内容>` | 手动设置邀请码 | `python3 monitor_fixed.py set "灵山坠真经"` |
| `init` | 重置状态 | `python3 monitor_fixed.py init` |
| `help` | 显示帮助 | `python3 monitor_fixed.py help` |

---

## 🔔 心跳推送通知

心跳检查已自动集成，每 5 分钟检查一次（官方时间段 9-18 点）：

```bash
# 手动测试心跳检查
python3 heartbeat-check.py
```

**特点：**
- ✅ 自动访问页面并点击"跳过动画"
- ✅ Playwright 截图 + OCR 识别
- ✅ MD5 hash 对比检测变化
- ✅ 只在官方时间段工作（9-12 点、14-18 点）
- ✅ 发现新内容才推送
- ✅ 避免重复通知

---

## 🛠️ 工作原理

```
每 5 分钟（9-18 点）
    ↓
heartbeat-check.py 触发
    ↓
monitor_fixed.py 执行
    ↓
1. Playwright 访问页面
2. 自动点击"跳过动画"
3. 等待主内容加载
4. 截图保存
5. OCR 识别文字
6. 提取邀请码
7. 对比 hash 检测变化
    ↓
有变化 → 写入通知文件 → 推送飞书
无变化 → 记录状态
```

---

## 📁 关键文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `monitor_fixed.py` | 主监控脚本 | 点击跳过 + OCR 识别 |
| `heartbeat-check.py` | 心跳检查 | 每 5 分钟自动检查 |
| `monitor_vision.py` | 视觉模型识别 | 备用方案 |
| `.wukong_state.json` | 状态文件 | 记录当前版本和 hash |
| `/tmp/wukong_invite.png` | 截图保存 | 每次检查的截图 |
| `/tmp/wukong-new-code-notify.txt` | 通知文件 | 推送内容 |

---

## 🔧 故障排查

### OCR 识别不准确
```bash
# 使用视觉模型识别（备用方案）
python3 monitor_vision.py check

# 或手动设置正确邀请码
python3 monitor_fixed.py set "灵山坠真经"
```

### 监控失效
```bash
# 查看状态
python3 monitor_fixed.py status

# 重置状态
python3 monitor_fixed.py init

# 重新测试
python3 monitor_fixed.py check
```

### 检查日志
```bash
# 查看监控日志
tail -f /tmp/wukong-monitor.log

# 查看心跳日志
tail -f /tmp/wukong-heartbeat.log
```

---

## 📖 完整文档

- [FINAL-REPORT.md](FINAL-REPORT.md) - 修复完成报告
- [FIX-REPORT.md](FIX-REPORT.md) - 问题分析和修复过程
- [README.md](README.md) - 完整使用指南（旧版）
- [HEARTBEAT.md](HEARTBEAT.md) - 心跳推送配置（旧版）

---

## 🎯 当前配置

### 检查频率
- **时间：** 每 5 分钟
- **时段：** 9-18 点（官方更新时间）
- **脚本：** `heartbeat-check.py` → `monitor_fixed.py`

### 通知方式
- **推送：** 飞书文本消息
- **触发：** 图片 hash 变化
- **防重：** 通过状态文件避免重复通知

### 识别方式
- **主要：** Tesseract OCR
- **备用：** 视觉模型（`monitor_vision.py`）
- **检测：** MD5 hash 对比（确保不漏检）

---

## ✅ 验证清单

- [x] Playwright 安装并可用
- [x] 自动访问悟空页面
- [x] 自动点击"跳过动画"
- [x] 截图保存正常
- [x] Hash 对比工作正常
- [x] 心跳检查集成
- [x] 通知文件更新
- [x] 当前邀请码正确（灵山坠真经）

---

*最后更新：2026-03-22 12:19*
