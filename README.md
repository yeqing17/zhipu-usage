# 智谱AI Coding Plan 用量查询

OpenClaw Skill，通过智谱AI官方API实时查询 Coding Plan 的配额使用情况。

## 功能

- 查询 Token 滑动窗口消耗限额
- 查询 MCP 工具调用次数（搜索、网页读取、深度阅读）
- 显示套餐等级、已用百分比、重置倒计时
- 支持智谱AI和Z.ai两个平台

## 效果示例

```
📋 智谱AI Coding Plan · LITE

🔢 Token [██░░░░░░░░░░░░░░] 已用13%
   3×5h滑动窗口 · 0h58m后

⏱ 工具调用 3/100次 [░░░░░░░░░░░░░░░░] 剩余97%
   每月重置 · 04/22 22:34
   搜索:1 · 网页读取:2 · 深度阅读:0
```

## 安装

### 方式一：下载 .skill 文件

从 [Releases](https://github.com/yeqing17/zhipu-usage/releases) 下载最新的 `zhipu-usage.skill` 文件，然后：

```bash
openclaw skills install zhipu-usage.skill
```

### 方式二：手动安装

```bash
git clone https://github.com/yeqing17/zhipu-usage.git
cp -r zhipu-usage ~/.openclaw/skills/zhipu-usage
```

## 使用

安装后在 OpenClaw 中使用以下触发词查询用量：

- "查下智谱用量"
- "zhipu 配额"
- "z.ai 剩余额度"
- "Token 限额"

## 配置

需要智谱AI的 API Key。支持两种方式：

1. **环境变量**：`export ZHIPU_API_KEY=your_key`
2. **OpenClaw 认证配置**：自动从 `~/.openclaw/agents/main/agent/auth-profiles.json` 中读取 `zai:default.key`

## API 说明

**端点：**
- 智谱：`https://open.bigmodel.cn/api/monitor/usage/quota/limit`
- Z.ai：`https://api.z.ai/api/monitor/usage/quota/limit`

**返回字段：**
| 字段 | 说明 |
|------|------|
| `TOKENS_LIMIT` | Token 消耗滑动窗口限额 |
| `TIME_LIMIT` | MCP 工具调用次数（搜索、网页读取等）|
| `level` | 套餐等级（lite / pro）|
| `nextResetTime` | 下次重置时间（毫秒时间戳）|
| `percentage` | 已用百分比 |

## License

MIT
