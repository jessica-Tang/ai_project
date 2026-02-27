# AI 广告生成工具（原型）

这是基于三页流程的可运行原型，实现了 3 个模块：

1. 模块 A：根据产品链接生成页面二推荐草案
2. 模块 B：根据页面二输入生成页面三账户结构
3. 模块 C：按需生成 AI 素材候选

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

会返回一个合并 JSON：
- `plan`：模块 A 产物
- `creatives`：素材列表（可选 AI）
- `structure`：模块 B 产物

## 本地脚本（自动生成文件）

```bash
bash scripts/run_local_flow.sh "https://shop.example.com/shoe-ultra-1" ./artifacts
```

将输出：
- `artifacts/plan.json`
- `artifacts/creative.json`
- `artifacts/flow.json`

## 测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```
