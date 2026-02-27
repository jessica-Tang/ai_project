# AI 广告生成工具（原型）

这是基于三页流程的可运行原型，实现了 3 个模块并补充了 Agent/Skill 编排：

1. 模块 A：根据产品链接生成页面二推荐草案（`ProjectPlanningAgent`）
2. 模块 B：根据页面二输入生成页面三账户结构（`AccountStructuringAgent`）
3. 模块 C：按需生成 AI 素材候选（`CreativeGenerationAgent`）

## Agent / Skill 设计（对应你的流程）

- Page1 输入 URL -> `ProjectPlanningAgent`
  - 典型 skills：`channel-recommendation`、`compliance-check`
- Page2 用户修改并确认 -> `AccountStructuringAgent`
  - 典型 skills：`budget-allocation`、`compliance-check`
- Page2 可选点击生成素材 -> `CreativeGenerationAgent`
- Page3 点击创建 -> 交由工程代码调用媒体 API（不走 agent）

## 运行方式

```bash
python -m ad_tool.cli plan https://shop.example.com/shoe-ultra-1 --channel meta --budget 600
python -m ad_tool.cli creative "轻薄跑鞋" --channel meta --sizes 1080x1080,1080x1920 --count 3
python -m ad_tool.cli structure --channel meta --budget 600 --targeting 兴趣受众,类似受众 --creative-count 2
```

## 一键联调（推荐）

```bash
python -m ad_tool.cli flow https://shop.example.com/shoe-ultra-1 --channel meta --budget 600 --use-ai-creatives --ai-creative-count 3
```

输出里会包含：
- `planning_agent`（含 `skill_trace`）
- `creative_agent`（如果启用）
- `structuring_agent`（含 `skill_trace`）


## 可视化本地预览（页面方式）

启动本地预览服务：

```bash
python -m ad_tool.web_preview --host 0.0.0.0 --port 8000
```

浏览器打开：`http://127.0.0.1:8000`

你可以在单页面里完整试用：
1. Page1 输入 URL 并生成推荐（Project Planning Agent）
2. Page2 修改参数，选择手动素材或点击 AI 生成素材（Creative Generation Agent）
3. 生成 Page3 账户结构（Account Structuring Agent）
4. 点击“提交创建(模拟)”验证页面3后续已交给工程媒体 API 链路

## 本地脚本（自动生成文件）

```bash
bash scripts/run_local_flow.sh "https://shop.example.com/shoe-ultra-1" ./artifacts
```

将输出：
- `artifacts/plan.json`
- `artifacts/creative.json`
- `artifacts/flow.json`


## 打包成 ZIP（便于拷贝到本地运行）

```bash
bash scripts/package_zip.sh
```

默认输出：`dist/ai_ad_tool_preview.zip`。

可自定义输出目录和文件名：

```bash
bash scripts/package_zip.sh ./dist my_ad_tool.zip
```

## 测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```


### 常见问题：127.0.0.1 拒绝连接

1. 确认服务已启动：
```bash
python -m ad_tool.web_preview --host 0.0.0.0 --port 8000
```
2. 本机访问：`http://127.0.0.1:8000`；如果是容器/远程开发环境，请用对应转发地址（例如 `http://localhost:8000`）。
3. 检查端口是否在监听：
```bash
ss -ltnp | rg 8000
```
4. 如果 8000 被占用，换端口：
```bash
python -m ad_tool.web_preview --host 0.0.0.0 --port 8080
```
5. 用 curl 快速自检：
```bash
curl -s http://127.0.0.1:8000 | head -n 3
```
