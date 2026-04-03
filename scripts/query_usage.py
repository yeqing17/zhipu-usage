#!/usr/bin/env python3
"""智谱AI / Z.ai Coding Plan 用量查询脚本"""
import json, sys, urllib.request, os, time

API_KEY = os.environ.get("ZHIPU_API_KEY", "")
BASE_URL = "https://open.bigmodel.cn/api/monitor/usage/quota/limit"

def query(api_key=None):
    key = api_key or API_KEY
    if not key:
        print(json.dumps({"error": "缺少 API Key，请设置 ZHIPU_API_KEY 环境变量或传入参数"}))
        sys.exit(1)
    req = urllib.request.Request(BASE_URL)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"success": False, "error": str(e)}

def make_bar(pct, length=16):
    filled = int(length * pct / 100)
    return "█" * filled + "░" * (length - filled)

def fmt_countdown(next_ms):
    left = max(0, (next_ms - int(time.time() * 1000)) / 60000)
    if left >= 1440:
        return time.strftime("%m-%d %H:%M", time.localtime(next_ms / 1000))
    h, m = int(left // 60), int(left % 60)
    return f"{h}h{m:02d}m后重置"

def format_report(data):
    if not data.get("success"):
        return f"❌ 查询失败: {data.get('error', '未知错误')}"
    d = data["data"]
    level = d.get("level", "unknown")
    limits = d.get("limits", [])
    lines = [f"📋 智谱AI Coding Plan · {level.upper()}", ""]
    for lim in limits:
        t = lim["type"]
        if t == "TIME_LIMIT":
            pct = lim.get("percentage", 0)
            rem = lim.get("remaining", "?")
            cur = lim.get("currentValue", 0)
            total = lim.get("usage", "?")
            unit = lim.get("unit", 5)
            nxt = lim.get("nextResetTime")
            lines.append(f"⏱ {unit}h时段 [{make_bar(pct)}] 剩余{rem}%")
            lines.append(f"   已用 {cur}/{total} 次")
            if nxt:
                lines.append(f"   重置: {fmt_countdown(nxt)}")
            details = lim.get("usageDetails", [])
            if details:
                parts = [f"{dd['modelCode']}:{dd['usage']}" for dd in details]
                lines.append(f"   {' · '.join(parts)}")
            lines.append("")
        elif t == "TOKENS_LIMIT":
            pct = lim.get("percentage", 0)
            unit = lim.get("unit", 5)
            number = lim.get("number", 1)
            nxt = lim.get("nextResetTime")
            lines.append(f"🔢 Token {unit}×{number}h限额 [{make_bar(pct)}] 已用{pct}%")
            if nxt:
                lines.append(f"   重置: {fmt_countdown(nxt)}")
            lines.append("")
    return "\n".join(lines).strip()

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else None
    data = query(key)
    print(format_report(data))
