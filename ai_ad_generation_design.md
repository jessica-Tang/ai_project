# AI 生成广告功能设计方案（含 Agent / Skill 编排）

## 1. 目标与边界

### 1.1 目标
围绕三页流程，设计一套“可控、可编辑、可落地”的 AI 广告生成功能，并补充 Agent / Skill 调用链路：
1. **页面一（产品链接输入）**：由 Project Planning Agent 生成推荐草案。
2. **页面二（信息编辑 + 素材区）**：用户可修改推荐；可选触发 Creative Generation Agent。
3. **页面三（账户结构预算预览）**：由 Account Structuring Agent 生成结构供预览。

### 1.2 边界
- 页面三点击“提交创建”后，**不需要 Agent 参与**；由工程代码调用媒体 API 完成创建。
- Agent 负责“建议、编排、校验”，不直接替代投放系统。

---

## 2. 端到端流程（你要求的形态）

```text
[User]
   ↓
Page1: 输入URL
   ↓
Project Planning Agent
   ↓
Page2 展示推荐
   ↓
用户修改 & 确认
   ↓
Account Structuring Agent
   ↓
Page3 展示结构
   ↓
用户点击创建
   ↓
工程调用媒体 API
```

可选分支：
```text
Page2 点击生成素材
   ↓
Creative Generation Agent
```

---

## 3. Agent 与 Skill 设计

### 3.1 Project Planning Agent（页面一后）
- 目标：从产品链接输出页面二推荐值。
- 输入：`product_url` + 渠道/预算提示。
- 输出：`page2_defaults`、`hidden_recommendations`。
- 默认 skills：
  - `channel-recommendation`：按渠道映射推荐账户等默认值。
  - `compliance-check`：补充风险提示（敏感词/极限词）。

### 3.2 Account Structuring Agent（页面二确认后）
- 目标：将页面二最终信息编排为 Campaign / Adset / Ad。
- 输入：渠道、预算、时间、定向、素材。
- 输出：结构化账户草案 + 校验信息。
- 默认 skills：
  - `budget-allocation`：多 adset 预算自动拆分。
  - `compliance-check`：结构输出附带合规提示。

### 3.3 Creative Generation Agent（页面二可选）
- 触发：用户点击“AI 生成素材”。
- 输出：素材候选 + 可编辑文案字段。
- 说明：该 agent 可独立调用，不阻塞手动上传素材流程。

---

## 4. 模块与 Agent 的对应

- 模块 A（链接 -> 推荐）= `ProjectPlanningAgent`
- 模块 B（页面二 -> 结构）= `AccountStructuringAgent`
- 模块 C（素材生成）= `CreativeGenerationAgent`

也就是说你的原 3 模块划分保持不变，只是补了 Agent/Skill 运行层。

---

## 5. MVP 验收补充（Agent/Skill）

1. `plan`/`flow` 响应中可看到 `planning_agent.skill_trace`。
2. `structure`/`flow` 响应中可看到 `structuring_agent.skill_trace`。
3. 用户不触发素材生成时，流程依旧可走通（手动素材）。
4. 页面三点击创建后不再进入任何 agent。
