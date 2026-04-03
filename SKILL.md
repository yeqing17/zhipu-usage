---
name: zhipu-usage
description: 智谱AI / Z.ai Coding Plan 用量查询。当用户询问智谱、zhipu、z.ai 的配额、用量、剩余额度、Token限额时触发。
---

# 智谱AI Coding Plan 用量查询

通过官方 API 实时查询 Coding Plan 配额使用情况。

## 使用方法

运行查询脚本：

```bash
ZHIPU_API_KEY=<key> python3 scripts/query_usage.py
```

API Key 通常存储在 OpenClaw 认证配置中（`~/.openclaw/agents/main/agent/auth-profiles.json` → `zai:default.key`），也可通过 `ZHIPU_API_KEY` 环境变量传入。

## API 端点

- 智谱: `https://open.bigmodel.cn/api/monitor/usage/quota/limit`
- Z.ai: `https://api.z.ai/api/monitor/usage/quota/limit`

请求头: `Authorization: Bearer <api_key>`

## 返回数据说明

- `TIME_LIMIT`: 时段调用次数限制（如 5 小时时段）
- `TOKENS_LIMIT`: Token 消耗限额（如 3×5 小时滑动窗口）
- `level`: 套餐等级（lite / pro）
- `nextResetTime`: 下次重置时间戳（毫秒）
