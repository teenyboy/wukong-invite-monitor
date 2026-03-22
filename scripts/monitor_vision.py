#!/usr/bin/env python3
"""
Wukong Invitation Code Monitor - Vision API Version
使用视觉模型识别邀请码（需要 OpenClaw image 工具）
"""

import json
import sys
import os
import hashlib
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, ".wukong_state.json")
OUTPUT_IMAGE = "/tmp/wukong_invite.png"
NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"
WORKSPACE = "/home/admin/.openclaw/workspace"

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

def screenshot_and_get_invite():
    """截图并使用视觉模型识别邀请码"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
                viewport={'width': 375, 'height': 812}
            )
            page = context.new_page()
            
            log("访问悟空页面...")
            page.goto("https://www.dingtalk.com/wukong", wait_until='networkidle', timeout=30000)
            
            log("等待并点击跳过...")
            page.wait_for_timeout(3000)
            
            # 点击跳过
            try:
                skip_button = page.query_selector('text=跳过')
                if skip_button:
                    skip_button.click()
                    page.wait_for_timeout(2000)
            except:
                pass
            
            page.wait_for_timeout(3000)
            
            # 截图到 workspace
            screenshot_path = os.path.join(WORKSPACE, "wukong-current.png")
            page.screenshot(path=screenshot_path, full_page=True)
            log(f"截图成功：{screenshot_path}")
            
            browser.close()
            
            # 计算 hash
            with open(screenshot_path, 'rb') as f:
                img_hash = hashlib.md5(f.read()).hexdigest()
            
            return True, img_hash, screenshot_path
            
    except Exception as e:
        log(f"❌ 截图失败：{e}")
        return False, None, None

def recognize_with_vision(image_path):
    """使用 OpenClaw image 工具识别邀请码"""
    try:
        # 调用 OpenClaw image 工具
        cmd = [
            'openclaw', 'image', image_path,
            '--prompt', '这是钉钉悟空页面点击跳过后的截图。请找出"当前邀请码"的内容，通常是 5-6 个中文字，如"灵山坠真经"。只返回邀请码文字，不要其他内容。'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # 解析输出
            output = result.stdout.strip()
            # 提取邀请码（假设在输出中）
            if '邀请码' in output:
                # 简单提取
                for line in output.split('\n'):
                    if '邀请码' in line and ':' in line:
                        code = line.split(':', 1)[1].strip().strip('**').strip()
                        if 3 <= len(code) <= 10:
                            return code
            
            # 如果没有明确格式，返回第一个短句
            lines = [l.strip() for l in output.split('\n') if l.strip() and len(l.strip()) < 20]
            if lines:
                return lines[0].strip('**').strip()
        
        return None
        
    except Exception as e:
        log(f"视觉识别失败：{e}")
        return None

def write_notify(text):
    """写入通知文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""🎉 **悟空邀请码更新通知**
━━━━━━━━━━━━━━━━━━━━
📅 时间：{timestamp}
🔢 版本：{text}
💾 图片已保存到：{WORKSPACE}/wukong-current.png
━━━━━━━━━━━━━━━━━━━━
"""
    
    with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"通知已写入：{NOTIFY_FILE}")

def check_once():
    log("=" * 50)
    log("开始检查悟空邀请码（视觉版）...")
    log("=" * 50)
    
    state = load_state()
    last_hash = state.get("last_hash")
    last_text = state.get("last_text", "未知")
    
    # 1. 截图
    success, img_hash, screenshot_path = screenshot_and_get_invite()
    
    if not success or not screenshot_path:
        log("❌ 无法截图")
        return {"status": "error"}
    
    # 2. 检查 hash 变化
    if last_hash == img_hash:
        log(f"✅ 图片无变化 (当前：{last_text})")
        return {"status": "unchanged", "text": last_text}
    
    # 3. 图片变化了，使用视觉模型识别
    log("使用视觉模型识别邀请码...")
    invite_code = recognize_with_vision(screenshot_path)
    
    if invite_code:
        log(f"✅ 识别到邀请码：{invite_code}")
    else:
        log("⚠️ 视觉识别失败，使用时间戳")
        invite_code = f"[图片更新] {datetime.now().strftime('%Y-%m-%d')}"
    
    # 4. 写入通知
    write_notify(invite_code)
    
    # 5. 保存状态
    state["last_hash"] = img_hash
    state["last_text"] = invite_code
    state["total_changes"] = state.get("total_changes", 0) + 1
    save_state(state)
    
    log(f"✅ 检查完成")
    
    return {
        "status": "changed",
        "old_text": last_text,
        "new_text": invite_code,
        "hash": img_hash
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "check":
            check_once()
        elif cmd == "status":
            state = load_state()
            log(f"当前版本：{state.get('last_text', '未知')}")
            log(f"最后检查：{state.get('last_check', '从未')}")
        elif cmd == "set":
            if len(sys.argv) > 2:
                text = " ".join(sys.argv[2:])
                state = load_state()
                state["last_text"] = text
                save_state(state)
                log(f"已设置：{text}")
        elif cmd == "init":
            state = load_state()
            state["last_hash"] = None
            state["last_text"] = None
            save_state(state)
            log("状态已重置")
        else:
            print("用法：python3 monitor_vision.py [check|status|set|init]")
    else:
        check_once()
