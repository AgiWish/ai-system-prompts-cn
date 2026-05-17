# WEB / APP 原型工作指南

本仓库通过 `.skills` 下的技能文档，规范 **WEB 端** 与 **APP 端** 静态原型的创建流程。技能名称与 **`.skills` 子目录名** 一致；正文入口为各目录下的 **`SKILL.md`**（如 **`prd-writer`**、**`prototype-list`** 等）。**`prototype-list`** 用于在选用 generator 之前，把想法或需求稿整理为 **功能清单 + 完整页面结构**（Markdown 写入 **`doc/`**，详见该技能）。**`prd-writer`** 用于把已有方向的想法写成或迭代 **PRD**（Markdown 写入 **`docs/`**，详见该技能）。

## 预置视觉规范（`.style`）

**`.style/`** 目录预置多套 **可直接调用的视觉规范**（`*-style.md`：色板、字体、圆角、层次、组件气质与克制原则等），并配有浏览器预览（`*-preview.html`，便于选型对照）。

在使用 **`vibepm-web-generator`**（WEB 端）或 **`vibepm-app-generator`**（移动端壳内原型）产出页面时：

1. **用户已指定风格** → 先读取对应的 `*-style.md`，再在 `web/` 或 `app/` 中通过 `global.css` / 页面级 CSS 变量与样式规则 **落实该文档中的 tokens 与约束**，避免「规范写一套、实现写另一套」。
2. **用户未指定** → **先询问是否需要由助手根据场景推荐**；若用户需要，再根据场景从下表推荐一套，或列出选项请用户确认后再生成。
3. **需对齐某外部站点** → 使用 **`vibepm-style-extractor`** 从 URL/截图等提取；预置 `.style` 与提取结果可并存，提取产物也可后续沉淀为新的 `*-style.md`。

| 视觉规范（主文件） | 预览 |
|-------------------|------|
| `.style/亮色科技蓝-style.md` | `.style/亮色科技蓝-preview.html` |
| `.style/亮色现代极简-style.md` | `.style/亮色现代极简-preview.html` |
| `.style/亮色电光蓝-style.md` | `.style/亮色电光蓝-preview.html` |
| `.style/暗色低饱和黑灰-style.md` | `.style/暗色低饱和黑灰-preview.html` |
| `.style/暗色紫色科技感-style.md` | `.style/暗色紫色科技感-preview.html` |

## 技能与触发关键词

**规则：用户消息中任一触发词命中，即视为必须走对应技能（见下节「执行规则」）。**

> **端别判断**：原「创建页面 / 实现功能 / 开发模块」类需求，默认需区分交付物——**WEB 静态页** 用 `vibepm-web-generator`（产出在 `web/`），**带手机或小程序外框的 APP 原型** 用 `vibepm-app-generator`（产出在 `app/`）。用户未说明且语境不明时，**先询问再选技能**。

| 技能 | 触发关键词（任一匹配即触发） | 说明 |
|------|---------------------------|------|
| `prd-writer` | 需求文档、PRD、产品需求、功能文档、写需求、整理需求、补充需求、审查需求、改进需求文档、从零写 PRD、我想做个产品、我想做个功能、我想做个 App、做个工具、AI 写的需求有没有问题 | 读取 `.skills/prd-writer/SKILL.md` → 第零步判断是否适合本技能；**三视角诊断** 与 **模式 A/B/C**（从零两版交付、评估改进、增量融合）；产出 Markdown 存 **`docs/`**；**不写实现级代码细节**，与 generator 分工 |
| `prototype-list` | 功能清单、页面结构、信息结构、原型范围、MVP、分期、整理需求稿、站点地图、IA、基于 PRD 整理、feature checklist | 读取 `.skills/prototype-list/SKILL.md` → 将想法或需求稿提炼为 **功能 + 信息结构**，Markdown 存 **`doc/`**；**第 2 章** 须为 **完整页面结构列表**（按屏分段、每屏五项要点；**禁止**用宽表罗列入口/结构/功能/备注/文件名）；默认简短访谈，弱化技术实现 |
| `vibepm-web-generator` | 创建页面、生成页面、添加页面、新建页面、实现WEB页面、开发WEB模块、企业官网、落地页、营销页、多页静态站、用WEB技能、/vibepm-web-generator | 读取该技能 → 按 `web/` 目录与 HTML/CSS/JS 分离、资源本地化等规范交付 |
| `vibepm-app-generator` | APP原型、手机页面、小程序原型、iOS壳、微信壳、设备框、带壳页面、移动端原型、用APP技能、/vibepm-app-generator | 读取该技能 → 选模板 → 内容落在 `app-shell`；运行时资源闭环在 `app/` |
| `vibepm-style-extractor` | 模仿网站风格、参考站、提取风格、设计tokens、风格逆向、样式提取、从URL/截图提取、/vibepm-style-extractor | 输出 tokens 与可复用提示词，供后续 `vibepm-web-generator` / `vibepm-app-generator` 对齐视觉 |

**本仓库 `.skills` 中未包含的技能**（下表勿当作本包内置能力；若需可自行扩展目录）：`page-generator`、`annotation`、`pm-test-cases`、`pm-operation-manual`。其中「做页面 / 做功能」由上表 **`vibepm-web-generator` / `vibepm-app-generator`** 覆盖；**产品需求结构化与 PRD** 由 **`prd-writer`**（及可选 **`prototype-list`**）覆盖。

## 执行规则

**检查清单（每次收到用户请求时建议执行）：**

1. **触发检测**：扫描用户消息是否命中上表「触发关键词」列（含同义口语变体）。
2. **强制调用**：若命中，须先通过 **`Skill` 工具** 加载对应技能名称（与上表第一列一致），**不得**在未加载技能的情况下直接大段写代码、生成文档或改文件。
3. **禁止跳步**：不允许跳过技能直接实现、直接杜撰需求结构或自行「简化」技能规定的输出格式。
4. **工作流遵守**：加载技能后，须阅读并执行该目录下的 **`SKILL.md`**（如 **`prd-writer`**、**`prototype-list`**），严格按文档内步骤与门禁（如 **`prd-writer`** 的第零步、三视角诊断与分阶段交付）执行。
5. **完整性检查**：不省略步骤、不擅自合并技能规定的多阶段输出；若技能要求任务清单，须按清单逐项更新状态。

**示例判断：**

✅ 正确：
```
用户："做一个 SaaS 落地页，要有价格和 FAQ"
→ 命中「落地页」等 → Skill: vibepm-web-generator
→ 阅读 .skills/vibepm-web-generator/SKILL.md → 按 web/ 与 html/css/js 分离规范交付
```

✅ 正确：
```
用户："帮我从零写一份健身 App 的 PRD，想法是记录训练与饮食"
→ 命中「PRD」「App」→ Skill: prd-writer
→ 阅读 .skills/prd-writer/SKILL.md → 第零步与三视角诊断 → 按模式 A 分两版写入 docs/*.md；不写实现代码
```

✅ 正确：
```
用户："把这个 PRD 整理成功能清单和全站页面结构，再定 MVP"
→ 命中「功能清单」「页面结构」「MVP」→ Skill: prototype-list
→ 阅读 .skills/prototype-list/SKILL.md → 写入 doc/*.md；第 2 章为完整页面结构列表（按屏 + 五项要点），再接 generator 落原型
```

❌ 错误：
```
用户："实现用户管理 WEB 页面"
→ 未选技能直接改 web/*.html ← 错误！应先 Skill: vibepm-web-generator（需求边界不清时可先简短澄清或接 prd-writer / prototype-list）
```

❌ 错误：
```
用户："帮我写 PRD"
→ 跳过第零步与三视角诊断，直接输出一版长文档 ← 错误！应先 Skill: prd-writer，并执行 .skills/prd-writer/SKILL.md 中的阶段与门禁
```

## 推荐工作流

1. **有基本产品/功能方向，要写或迭代 PRD** → `prd-writer`（产出 `docs/YYYY-MM-DD-<主题>PRD.md` 等；无方向时技能内第零步会引导用户先想清楚再进入）
2. **要先对齐功能与页面/屏结构、分期与 MVP 边界**（再画原型或对照 PRD）→ `prototype-list`（产出 `doc/YYYY-MM-DD-<主题>.md`；可与 **`prd-writer`** 前后衔接）
3. **WEB 静态原型** → 选定 **`.style` 中某 `*-style.md`**（或 `vibepm-style-extractor`）→ `vibepm-web-generator`
4. **APP 壳内原型** → 同上选定视觉规范 → `vibepm-app-generator`

## 通用原则

### 克制

只做被明确要求的事；未提到的样式、动效、额外组件不要自行追加。若认为有必要扩展，先征得同意再动手。

### 注释与可维护性

以当前所用技能中的约定为准（例如 `web/`、`app/` 下的文件组织、样式作用域、禁止 CDN 等）。在技能未单独规定处：对非显而易见的逻辑保留简短注释，便于后续把原型迁入工程化项目时对照。
