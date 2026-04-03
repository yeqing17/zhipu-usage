#!/usr/bin/env python3
"""智谱AI / Z.ai Coding Plan 用量查询脚本"""
import json, sys, urllib.request, os, time

API_KEY = os.environ.get("ZHIPU_API_KEY", "")
BASE_URL = "https://open.bigmodel.cn/api/monitor/usage/quota/limit"

def query(api_key=None):
    key = api_key or API_KEY
    if not key:
        return {"success": False, "error": "缺少API Key"}
    req = urllib.request.Request(BASE_URL)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"success": False, "error": str(e)}

def fmt_countdown(next_ms):
    left = max(0, (next_ms - int(time.time() * 1000)) / 60000)
    if left >= 1440:
        return time.strftime("%m/%d", time.localtime(next_ms / 1000))
    h, m = int(left // 60), int(left % 60)
    return f"{h}h{m}m"

def format_report(data):
    if not data.get("success"):
        return f"❌ {data.get('error', '查询失败')}"
    d = data["data"]
    level = d.get("level", "?")
    limits = d.get("limits", [])
    lines = []
    token_reset = ""
    time_reset = ""
    token_pct = 0
    time_pct = 0
    for lim in limits:
        if lim["type"] == "TOKENS_LIMIT":
            token_pct = lim.get("percentage", 0)
            nxt = lim.get("nextResetTime")
            if nxt:
                token_reset = fmt_countdown(nxt)
        elif lim["type"] == "TIME_LIMIT":
            time_pct = lim.get("percentage", 0)
            nxt = lim.get("nextResetTime")
            if nxt:
                time_reset = fmt_countdown(nxt)
    lines.append(f"📋 {level.upper()} | Token {token_pct}% | 工具 {time_pct}%")
    if token_reset:
        lines.append(f"⏰ Token重置: {token_reset} | 工具重置: {time_reset}")
    return "\n".join(lines)

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else None
    data = query(key)
    print(format_report(data))
