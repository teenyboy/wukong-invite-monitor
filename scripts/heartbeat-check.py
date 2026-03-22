#!/usr/bin/env python3
"""
心跳检查脚本 - 检查悟空邀请码通知
使用 Playwright 截图监控，发现新内容时推送飞书通知
"""

import os
import sys
import json
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MONITOR_SCRIPT = os.path.join(SCRIPT_DIR, "monitor_fixed.py")
NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"
WATCHED_FILE = "/tmp/wukong-watched-state.json"

def load_watched():
    """加载已查看的通知"""
    try:
        with open(WATCHED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"last_notify": "", "last_check": None}

def save_watched(state):
    """保存状态"""
    with open(WATCHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def check_and_notify():
    """执行截图监控并推送通知"""
    # 检查是否在官方时间（9-12 点、14-18 点）
    hour = datetime.now().hour
    official_hours = [9, 10, 11, 12, 14, 15, 16, 17, 18]
    
    if hour not in official_hours:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 非官方时间，跳过检查")
        return {"status": "skipped", "reason": "not_official_time"}
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始检查悟空邀请码...")
    
    # 执行截图监控脚本
    try:
        result = subprocess.run(
            [sys.executable, MONITOR_SCRIPT, "check"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        print(output)
        
        # 分析输出判断是否有变化
        if "图片无变化" in output or "unchanged" in output:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 无变化")
            return {"status": "no_new"}
        
        if "发现新邀请码" in output or "changed" in output or "检测到图片变化" in output:
            # 有新变化！读取通知文件
            if os.path.exists(NOTIFY_FILE):
                with open(NOTIFY_FILE, 'r', encoding='utf-8') as f:
                    notify_content = f.read().strip()
                
                # 检查是否已通知过
                watched = load_watched()
                if notify_content == watched.get("last_notify", ""):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 已通知过，跳过")
                    return {"status": "no_new"}
                
                # 推送新通知
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = {
                    "msg_type": "text",
                    "content": {
                        "text": f"{notify_content}\n\n[自动监控] {timestamp}"
                    }
                }
                
                print("\n=== 推送消息 ===")
                print(json.dumps(message, ensure_ascii=False, indent=2))
                print("===============\n")
                
                # 更新状态
                watched["last_notify"] = notify_content
                watched["last_check"] = timestamp
                watched["notified_at"] = timestamp
                save_watched(watched)
                
                return {"status": "notified", "message": message}
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 检查完成")
        return {"status": "checked"}
        
    except subprocess.TimeoutExpired:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 检查超时")
        return {"status": "error", "reason": "timeout"}
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 检查失败：{e}")
        return {"status": "error", "reason": str(e)}

if __name__ == "__main__":
    result = check_and_notify()
    sys.exit(0 if result.get("status") in ["notified", "no_new", "skipped", "checked"] else 1)
