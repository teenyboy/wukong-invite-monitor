#!/usr/bin/env python3
"""
Wukong Invitation Code Monitor - Manual Check Version
当自动检测失败时，支持手动输入邀请码
"""

import json
import sys
import os
import hashlib
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, ".wukong_state.json")
OUTPUT_IMAGE = "/tmp/wukong_invite.png"
NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"last_hash": None, "last_check": None, "last_text": None, "total_changes": 0}

def save_state(state):
    state["last_check"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def write_notify(text):
    """写入通知文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""🎉 **悟空邀请码更新通知**
━━━━━━━━━━━━━━━━━━━━
📅 时间：{timestamp}
🔢 版本：{text}
💾 图片：请访问 https://www.dingtalk.com/wukong 查看
━━━━━━━━━━━━━━━━━━━━
💡 提示：自动监控已失效，请手动检查页面
"""
    
    with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"通知已写入：{NOTIFY_FILE}")

def manual_check():
    """手动检查模式"""
    log("=" * 50)
    log("悟空邀请码监控 - 手动检查模式")
    log("=" * 50)
    
    state = load_state()
    last_text = state.get("last_text", "未知")
    
    print(f"\n当前记录版本：{last_text}")
    print(f"请访问：https://www.dingtalk.com/wukong")
    print(f"输入你看到的邀请码内容（直接回车跳过）：")
    
    user_input = input("> ").strip()
    
    if not user_input:
        log("跳过本次检查")
        return {"status": "skipped"}
    
    # 检查变化
    if user_input == last_text:
        log(f"✅ 版本无变化：{user_input}")
        return {"status": "unchanged", "text": user_input}
    
    # 发现变化！
    log(f"⚡ 发现新邀请码！")
    log(f"   之前：{last_text}")
    log(f"   现在：{user_input}")
    
    # 写入通知
    write_notify(user_input)
    
    # 保存状态
    state["last_text"] = user_input
    state["total_changes"] = state.get("total_changes", 0) + 1
    save_state(state)
    
    log(f"✅ 已记录并通知")
    
    return {"status": "changed", "new_text": user_input}

def set_manual(text):
    """手动设置当前版本"""
    state = load_state()
    old_text = state.get("last_text", "未知")
    
    state["last_text"] = text
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    log(f"✅ 已设置当前版本：{text}")
    log(f"   之前：{old_text}")
    log(f"   现在：{text}")
    
    write_notify(text)

def show_status():
    """显示当前状态"""
    state = load_state()
    log("=" * 50)
    log("悟空邀请码监控状态")
    log("=" * 50)
    log(f"最后检查：{state.get('last_check', '从未')}")
    log(f"最后版本：{state.get('last_text', '未知')}")
    log(f"总变化次数：{state.get('total_changes', 0)}")
    log(f"\n访问页面：https://www.dingtalk.com/wukong")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "check":
            manual_check()
        elif cmd == "status":
            show_status()
        elif cmd == "set":
            if len(sys.argv) > 2:
                text = " ".join(sys.argv[2:])
                set_manual(text)
            else:
                print("用法：python3 monitor_manual.py set <版本内容>")
        elif cmd == "init":
            state = load_state()
            state["last_hash"] = None
            state["last_text"] = None
            save_state(state)
            log("状态已重置")
        elif cmd == "help":
            print("用法：python3 monitor_manual.py [check|status|set|init|help]")
            print("  check  - 手动检查一次")
            print("  status - 显示状态")
            print("  set <text> - 手动设置版本")
            print("  init   - 重置状态")
            print("  help   - 显示帮助")
        else:
            log(f"未知命令：{cmd}")
    else:
        manual_check()
