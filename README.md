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

## 测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```
