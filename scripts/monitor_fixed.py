#!/usr/bin/env python3
"""
Wukong Invitation Code Monitor - Fixed Version
正确点击跳过动画并识别邀请码
"""

import json
import sys
import os
import hashlib
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from ocr_local import ocr_image, check_tesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

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

def screenshot_with_playwright():
    """使用 Playwright 截图，正确跳过动画"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                viewport={'width': 375, 'height': 812}
            )
            page = context.new_page()
            
            # 访问页面
            log("访问悟空页面...")
            page.goto("https://www.dingtalk.com/wukong", wait_until='networkidle', timeout=30000)
            
            # 等待动画加载
            log("等待页面加载...")
            page.wait_for_timeout(3000)
            
            # 查找并点击"跳过"按钮
            log("查找跳过按钮...")
            skip_clicked = False
            try:
                # 尝试多种选择器
                skip_selectors = [
                    'text=跳过',
                    'text=跳过动画',
                    'button:has-text("跳过")',
                    '.skip-button',
                    '[class*="skip"]'
                ]
                
                for selector in skip_selectors:
                    try:
                        skip_button = page.query_selector(selector)
                        if skip_button and skip_button.is_visible():
                            log(f"点击跳过按钮：{selector}")
                            skip_button.click()
                            skip_clicked = True
                            page.wait_for_timeout(2000)
                            break
                    except:
                        continue
                
                if not skip_clicked:
                    log("未找到跳过按钮，继续等待...")
                    page.wait_for_timeout(3000)
                    
            except Exception as e:
                log(f"点击跳过失败：{e}")
                page.wait_for_timeout(3000)
            
            # 等待主内容加载
            log("等待主内容加载...")
            page.wait_for_timeout(3000)
            
            # 截图 - 完整页面
            log("截图...")
            screenshot_path = OUTPUT_IMAGE
            page.screenshot(path=screenshot_path, full_page=True)
            
            browser.close()
            
            # 计算 hash
            with open(screenshot_path, 'rb') as f:
                img_hash = hashlib.md5(f.read()).hexdigest()
            
            log(f"截图成功：{screenshot_path}")
            return True, img_hash
            
    except ImportError:
        log("❌ Playwright 未安装")
        return False, None
    except Exception as e:
        log(f"❌ 截图失败：{e}")
        return False, None

def extract_invite_code(ocr_text):
    """从 OCR 结果中提取邀请码"""
    if not ocr_text:
        return None
    
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    
    # 优先查找包含"邀请码"的行
    for line in lines:
        if '邀请码' in line:
            # 提取冒号后的内容
            if ':' in line:
                code = line.split(':', 1)[1].strip()
                if 2 <= len(code) <= 10:
                    return code
            # 或者行本身就是邀请码
            if 2 <= len(line) <= 10:
                return line
    
    # 查找 3-8 个字符的中文短语（邀请码格式）
    for line in lines:
        # 只保留中文字符
        chinese_only = ''.join(c for c in line if '\u4e00' <= c <= '\u9fff')
        if 3 <= len(chinese_only) <= 8:
            return chinese_only
    
    # 返回第一行非空内容
    if lines:
        return lines[0][:20]
    
    return None

def write_notify(text, img_hash):
    """写入通知文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""🎉 **悟空邀请码更新通知**
━━━━━━━━━━━━━━━━━━━━
📅 时间：{timestamp}
🔢 版本：{text}
💾 图片已保存到：{OUTPUT_IMAGE}
━━━━━━━━━━━━━━━━━━━━
"""
    
    with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"通知已写入：{NOTIFY_FILE}")

def check_once():
    log("=" * 50)
    log("开始检查悟空邀请码（修复版）...")
    log("=" * 50)
    
    state = load_state()
    last_hash = state.get("last_hash")
    last_text = state.get("last_text", "未知")
    
    # 1. 截图
    success, img_hash = screenshot_with_playwright()
    
    if not success:
        log("❌ 无法截图")
        return {"status": "error", "reason": "无法截图"}
    
    # 2. OCR 识别
    log("执行 OCR 识别...")
    ocr_text = None
    invite_code = None
    
    if OCR_AVAILABLE and check_tesseract():
        ocr_result = ocr_image(OUTPUT_IMAGE)
        if ocr_result.get("success"):
            ocr_text = ocr_result.get("text", "")
            log(f"OCR 原始结果:\n{ocr_text[:200]}...")
            
            # 提取邀请码
            invite_code = extract_invite_code(ocr_text)
            if invite_code:
                log(f"✅ 提取到邀请码：{invite_code}")
            else:
                log("⚠️ 未提取到有效邀请码")
        else:
            log(f"OCR 失败：{ocr_result.get('text', 'unknown')}")
    else:
        log("OCR 不可用")
    
    # 3. 检查变化
    if last_hash == img_hash:
        log(f"✅ 图片无变化 (当前：{last_text})")
        return {"status": "unchanged", "text": last_text, "hash": img_hash}
    
    # 4. 图片变化了
    log(f"⚡ 检测到图片变化！")
    log(f"   之前 hash: {last_hash[:8] if last_hash else 'None'}")
    log(f"   现在 hash: {img_hash[:8]}")
    
    # 使用提取的邀请码或默认文本
    current_text = invite_code if invite_code else f"[图片更新] {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # 5. 写入通知
    write_notify(current_text, img_hash)
    
    # 6. 保存状态
    state["last_hash"] = img_hash
    state["last_text"] = current_text
    state["total_changes"] = state.get("total_changes", 0) + 1
    save_state(state)
    
    log(f"✅ 检查完成")
    
    return {
        "status": "changed",
        "old_text": last_text,
        "new_text": current_text,
        "hash": img_hash,
        "image": OUTPUT_IMAGE,
        "ocr_text": ocr_text
    }

def show_status():
    """显示当前状态"""
    state = load_state()
    log("=" * 50)
    log("悟空邀请码监控状态（修复版）")
    log("=" * 50)
    log(f"最后检查：{state.get('last_check', '从未')}")
    log(f"最后版本：{state.get('last_text', '未知')}")
    log(f"总变化次数：{state.get('total_changes', 0)}")
    log(f"图片保存：{OUTPUT_IMAGE}")
    log(f"OCR 状态：{'✅ 可用' if OCR_AVAILABLE and check_tesseract() else '❌ 不可用'}")
    
    if os.path.exists(OUTPUT_IMAGE):
        size = os.path.getsize(OUTPUT_IMAGE)
        log(f"图片大小：{size / 1024:.1f} KB")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "check":
            check_once()
        elif cmd == "status":
            show_status()
        elif cmd == "init":
            state = load_state()
            state["last_hash"] = None
            state["last_text"] = None
            save_state(state)
            log("状态已重置")
        elif cmd == "set":
            if len(sys.argv) > 2:
                text = " ".join(sys.argv[2:])
                state = load_state()
                state["last_text"] = text
                save_state(state)
                log(f"已设置：{text}")
            else:
                print("用法：python3 monitor_fixed.py set <版本内容>")
        elif cmd == "help":
            print("用法：python3 monitor_fixed.py [check|status|set|init|help]")
        else:
            log(f"未知命令：{cmd}")
    else:
        check_once()
