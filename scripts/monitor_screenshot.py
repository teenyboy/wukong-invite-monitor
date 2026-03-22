#!/usr/bin/env python3
"""
Wukong Invitation Code Monitor - Screenshot Version
使用 Playwright 截图并 OCR 识别
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
    """使用 Playwright 截图"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                viewport={'width': 375, 'height': 812}
            )
            page = context.new_page()
            
            # 访问页面
            log("访问悟空页面...")
            page.goto("https://www.dingtalk.com/wukong", wait_until='networkidle', timeout=30000)
            
            # 等待页面加载
            page.wait_for_timeout(5000)
            
            # 尝试点击"跳过动画"按钮（如果存在）
            try:
                skip_button = page.query_selector('text=跳过')
                if skip_button:
                    log("点击跳过动画...")
                    skip_button.click()
                    page.wait_for_timeout(2000)
            except:
                pass
            
            # 再次等待内容加载
            page.wait_for_timeout(3000)
            
            # 截图 - 截取首屏 600px（邀请码通常在顶部）
            log("截图...")
            screenshot_path = OUTPUT_IMAGE
            page.screenshot(path=screenshot_path, clip={'x': 0, 'y': 0, 'width': 375, 'height': 600})
            
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

def screenshot_with_selenium():
    """使用 Selenium 截图（备用）"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=375,812')
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.dingtalk.com/wukong")
        driver.implicitly_wait(10)
        
        screenshot_path = OUTPUT_IMAGE
        driver.save_screenshot(screenshot_path)
        driver.quit()
        
        with open(screenshot_path, 'rb') as f:
            img_hash = hashlib.md5(f.read()).hexdigest()
        
        log(f"截图成功：{screenshot_path}")
        return True, img_hash
        
    except Exception as e:
        log(f"❌ Selenium 失败：{e}")
        return False, None

def write_notify(text):
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
    log("开始检查悟空邀请码（截图版）...")
    log("=" * 50)
    
    state = load_state()
    last_hash = state.get("last_hash")
    last_text = state.get("last_text", "未知")
    
    # 1. 截图
    success, img_hash = screenshot_with_playwright()
    
    if not success:
        # 尝试 Selenium
        log("尝试 Selenium...")
        success, img_hash = screenshot_with_selenium()
    
    if not success:
        log("❌ 无法截图，请安装 Playwright 或 Selenium")
        log("安装命令：pip3 install playwright && playwright install chromium")
        return {"status": "error", "reason": "无法截图"}
    
    # 2. OCR 识别
    log("执行 OCR 识别...")
    if OCR_AVAILABLE and check_tesseract():
        ocr_result = ocr_image(OUTPUT_IMAGE)
        if ocr_result.get("success"):
            current_text = ocr_result.get("text", "").strip()
            # 清理 OCR 结果，提取关键信息
            # 只保留 2-10 个字符的中文短语（邀请码通常是这样的格式）
            lines = [line.strip() for line in current_text.split('\n') if line.strip()]
            # 过滤出可能的邀请码（短中文短语）
            short_lines = [line for line in lines if 2 <= len(line) <= 10 and any('\u4e00' <= c <= '\u9fff' for c in line)]
            if short_lines:
                current_text = short_lines[0]  # 取第一个匹配的
            else:
                current_text = lines[0] if lines else current_text[:20]
            log(f"OCR 识别结果：{current_text}")
        else:
            current_text = f"[OCR 失败] {datetime.now().strftime('%Y-%m-%d')}"
            log(f"OCR 失败：{ocr_result.get('text', 'unknown')}")
    else:
        current_text = f"[图片] hash={img_hash[:8]}"
        log("OCR 不可用，使用图片 hash")
    
    # 3. 检查变化
    if last_hash == img_hash:
        log(f"✅ 图片无变化 (当前：{last_text})")
        return {"status": "unchanged", "text": last_text, "hash": img_hash}
    
    # 4. 发现变化！
    log(f"⚡ 发现新邀请码！")
    log(f"   之前：{last_text}")
    log(f"   现在：{current_text}")
    
    # 5. 写入通知
    write_notify(current_text)
    
    # 6. 保存状态
    state["last_hash"] = img_hash
    state["last_text"] = current_text
    state["total_changes"] = state.get("total_changes", 0) + 1
    save_state(state)
    
    log(f"✅ 检查完成，已通知")
    
    return {
        "status": "changed",
        "old_text": last_text,
        "new_text": current_text,
        "hash": img_hash,
        "image": OUTPUT_IMAGE
    }

def show_status():
    """显示当前状态"""
    state = load_state()
    log("=" * 50)
    log("悟空邀请码监控状态（截图版）")
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
        elif cmd == "help":
            print("用法：python3 monitor_screenshot.py [check|status|init|help]")
        else:
            log(f"未知命令：{cmd}")
    else:
        check_once()
