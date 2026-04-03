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

def bar(pct, n=16):
    f = int(n * pct / 100)
    return "█" * f + "░" * (n - f)

def fmt_reset(ms):
    left = max(0, (ms - int(time.time() * 1000)) / 60000)
    if left >= 1440:
        return time.strftime("%m/%d %H:%M", time.localtime(ms / 1000))
    h, m = int(left // 60), int(left % 60)
    return f"{h}h{m}m后"

TOOL_NAMES = {
    "search-prime": "搜索",
    "web-reader": "网页读取",
    "zread": "深度阅读",
}

def format_report(data):
    if not data.get("success"):
        return f"❌ {data.get('error', '查询失败')}"
    d = data["data"]
    level = d.get("level", "?").upper()
    limits = d.get("limits", [])
    lines = [f"📋 智谱AI Coding Plan · {level}", ""]
    for lim in sorted(limits, key=lambda x: 0 if x["type"] == "TOKENS_LIMIT" else 1):
        t = lim["type"]
        if t == "TOKENS_LIMIT":
            pct = lim.get("percentage", 0)
            unit = lim.get("unit", 5)
            number = lim.get("number", 1)
            nxt = lim.get("nextResetTime")
            lines.append(f"🔢 Token [{bar(pct)}] 已用{pct}%")
            detail = f"{unit}×{number}h滑动窗口"
            if nxt:
                detail += f" · {fmt_reset(nxt)}"
            lines.append(f"   {detail}")
            lines.append("")
        elif t == "TIME_LIMIT":
            pct = lim.get("percentage", 0)
            rem = lim.get("remaining", "?")
            cur = lim.get("currentValue", 0)
            total = lim.get("usage", "?")
            nxt = lim.get("nextResetTime")
            lines.append(f"⏱ 工具调用 {cur}/{total}次 [{bar(pct)}] 剩余{rem}%")
            detail = "每月重置"
            if nxt:
                detail += f" · {fmt_reset(nxt)}"
            lines.append(f"   {detail}")
            details = lim.get("usageDetails", [])
            if details:
                parts = [f"{TOOL_NAMES.get(dd['modelCode'], dd['modelCode'])}:{dd['usage']}" for dd in details]
                lines.append(f"   {' · '.join(parts)}")
            lines.append("")
    return "\n".join(lines).strip()

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else None
    data = query(key)
    print(format_report(data))
