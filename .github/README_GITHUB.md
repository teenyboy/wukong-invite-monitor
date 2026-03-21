# 悟空邀请码监控 (Wukong Invite Monitor)

[![ClawHub](https://img.shields.io/badge/ClawHub-v2.1.0-blue)](https://clawhub.ai/teenyboy/wukong-invite-monitor)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Zero Token](https://img.shields.io/badge/token-0-orange)](https://docs.openclaw.ai)

钉钉悟空邀请码自动监控工具，**零 token 消耗**，支持本地 OCR 识别和心跳推送通知。

## ✨ 特性

- 🚀 **零 token 消耗** - 纯代码运行，不依赖大模型 API
- 🔍 **本地 OCR** - 集成 Tesseract OCR，完全离线识别
- 🔔 **心跳推送** - 发现新邀请码自动推送通知
- ⚡ **精准监控** - 只在官方更新时间段检查（9-12 点、14-18 点）
- 📦 **自动安装** - 一键安装脚本，自动检测并安装依赖
- 🎯 **优雅降级** - 无 OCR 时仍可下载图片供人工查看

## 📦 快速开始

### 通过 ClawHub 安装（推荐）

```bash
# 安装技能
clawhub install wukong-invite-monitor

# 进入目录
cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts

# 安装依赖
./install-dependencies.sh

# 初始化
python3 monitor_lite.py init

# 测试
python3 monitor_lite.py check
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/teenyboy/wukong-invite-monitor.git \
  ~/.openclaw/workspace/skills/wukong-invite-monitor

# 进入目录
cd scripts

# 安装依赖
./install-dependencies.sh

# 初始化
python3 monitor_lite.py init
```

## 🎯 使用方法

### 基本命令

```bash
# 初始化（首次使用）
python3 monitor_lite.py init

# 检查一次
python3 monitor_lite.py check

# 查看状态
python3 monitor_lite.py status

# 扫描版本
python3 monitor_lite.py scan
```

### 设置定时监控

```bash
# 每 5 分钟检查
./setup-cron.sh 5

# 查看日志
tail -f /tmp/wukong-monitor.log
```

### 心跳推送通知

```bash
# 添加心跳检查任务
*/5 * * * * python3 heartbeat-check.py >> /tmp/wukong-heartbeat.log 2>&1
```

## 📊 输出示例

```
🎉 发现新邀请码！
━━━━━━━━━━━━━━━━━━━━━━━
📅 时间：2026-03-21 16:20:05
🔢 版本：v18 → v19
📝 内容：大圣闹瑶池
🔍 OCR: Tesseract (tesseract 4.1.1)
📦 大小：77.0 KB
💡 本地 OCR 识别，零 token 消耗！
```

## 💡 资源消耗

| 项目 | 消耗 |
|------|------|
| **Token** | **0**（完全本地） |
| **CPU** | < 1% |
| **内存** | < 10MB |
| **网络** | ~1KB/次 |
| **每天总消耗** | < 2000 tokens（按 1-2 次更新） |

## 📁 项目结构

```
wukong-invite-monitor/
├── scripts/
│   ├── monitor_lite.py         # 主监控脚本
│   ├── ocr_local.py            # 本地 OCR 模块
│   ├── heartbeat-check.py      # 心跳检查脚本
│   ├── check-new-code.py       # 日志检查脚本
│   ├── notify-watcher.py       # 通知监控脚本
│   ├── install-dependencies.sh # 依赖安装脚本
│   └── setup-cron.sh           # Cron 设置脚本
├── README.md                   # 使用指南
├── SKILL.md                    # Skill 主文档
├── QUICKSTART.md               # 快速开始
├── HEARTBEAT.md                # 心跳配置指南
├── LOCAL-OCR.md                # OCR 配置详解
└── LICENSE                     # MIT 许可证
```

## 🔧 依赖说明

### 自动安装

```bash
./install-dependencies.sh
```

### 手动安装

**Alibaba Cloud Linux / CentOS / RHEL:**
```bash
sudo yum install -y tesseract tesseract-langpack-chi_sim
```

**Ubuntu / Debian:**
```bash
sudo apt install -y tesseract-ocr tesseract-ocr-chi-sim
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

## 📖 完整文档

- [README.md](README.md) - 完整使用指南
- [QUICKSTART.md](QUICKSTART.md) - 60 秒快速开始
- [HEARTBEAT.md](HEARTBEAT.md) - 心跳推送配置
- [LOCAL-OCR.md](LOCAL-OCR.md) - OCR 配置详解
- [SKILL.md](SKILL.md) - Skill 主文档

## ❓ 常见问题

### Q: 必须安装 Tesseract 吗？

**A:** 不是必须。不安装时：
- ✅ 版本检测正常
- ✅ 图片下载正常
- ⚠️ OCR 降级为简单分析

### Q: 如何停止监控？

```bash
crontab -e  # 删除包含 wukong 的行
```

### Q: 心跳推送如何工作？

**A:** 心跳检查脚本会：
1. 每 5 分钟检查通知文件
2. 只在官方更新时间段工作（9-12 点、14-18 点）
3. 发现新内容时推送通知
4. 自动避免重复通知

## 🔒 安全说明

- ✅ 只访问公开 URL（钉钉官网）
- ✅ 本地文件操作（无外部上传）
- ✅ 无凭证存储
- ✅ 无第三方 API 调用
- ✅ 无隐私信息收集

## 📝 更新日志

### v2.1.0 (2026-03-21)
- ✅ 新增心跳推送通知功能
- ✅ 新增日志监控功能
- ✅ 只在官方更新时间段检查
- ✅ 自动避免重复通知
- ✅ 更新文档

### v2.0.0 (2026-03-21)
- ✅ 完全重写，零 token 消耗
- ✅ 本地 OCR 集成
- ✅ 自动依赖安装

### v1.0.0
- ✅ 初始版本

## 🎯 官方更新时间

钉钉悟空邀请码官方更新时间：
- **上午**: 9:00-12:00（每个整点后 5 分钟内）
- **下午**: 14:00-18:00（每个整点后 5 分钟内）
- **合计**: 每天 9 次更新

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [ClawHub 页面](https://clawhub.ai/teenyboy/wukong-invite-monitor)
- [钉钉悟空官网](https://www.dingtalk.com/wukong)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

**免责声明**: 本工具仅供学习交流使用，不保证邀请码的准确性或及时性。邀请码以钉钉官方发布为准。
