# AI System Prompts 中文翻译版

> 各大 AI 厂商系统提示词（System Prompt）中文翻译整理，基于 [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) 项目。

## 项目简介

AI 实验室通过庞大的隐藏提示词来塑造模型行为。本项目将这些提示词翻译为中文，帮助中文用户理解：

- AI 被指定了什么人格与功能
- 哪些话题被禁止或限制
- 内置了怎样的伦理与行为框架

**如果你在不了解 System Prompt 的情况下与 AI 对话，你交流的并非中立的智能，而是被精心塑造过的影子。**

## 本地阅读器

仓库内置了一个极简双栏阅读器：[index.html](./index.html)。它会按厂商目录自动展示英文原文与 `中文/` 译文，适合做中英对照阅读和翻译校对。

启动方式：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000/index.html
```

不要直接用 `file://` 打开页面。现代浏览器通常会阻止页面读取本地文档，导致右侧内容显示 `Failed to fetch`。

阅读器功能：

- 双栏对照：中文和英文并排查看，支持均分、中宽、英宽三种布局
- 联动滚动：在任意一侧滚动，另一侧会按阅读进度同步移动
- 专注模式：可隐藏左侧目录和顶部工具条，把空间让给正文
- 快捷切换：`C` 切换目录，`T` 切换顶部工具条
- 自动清理：中文侧渲染时会隐藏翻译元信息头，让中英正文起点更接近

## 已收录厂商

| 厂商 | 目录 | 翻译状态 |
|------|------|----------|
| Anthropic (Claude) | [ANTHROPIC](./ANTHROPIC) | 进行中 |
| OpenAI (ChatGPT) | [OPENAI](./OPENAI) | 进行中 |
| Google (Gemini) | [GOOGLE](./GOOGLE) | 进行中 |
| xAI (Grok) | [XAI](./XAI) | 待翻译 |
| Perplexity | [PERPLEXITY](./PERPLEXITY) | 待翻译 |
| Cursor | [CURSOR](./CURSOR) | 待翻译 |
| Windsurf | [WINDSURF](./WINDSURF) | 待翻译 |
| Devin | [DEVIN](./DEVIN) | 待翻译 |
| Manus | [MANUS](./MANUS) | 待翻译 |
| Replit | [REPLIT](./REPLIT) | 进行中 |
| Meta | [META](./META) | 进行中 |
| Mistral | [MISTRAL](./MISTRAL) | 进行中 |
| Moonshot (Kimi) | [MOONSHOT](./MOONSHOT) | 进行中 |
| MiniMax | [MINIMAX](./MINIMAX) | 进行中 |
| Cline | [CLINE](./CLINE) | 待翻译 |
| Bolt | [BOLT](./BOLT) | 待翻译 |
| Lovable | [LOVABLE](./LOVABLE) | 待翻译 |
| Vercel V0 | [VERCEL V0](./VERCEL%20V0) | 待翻译 |
| Dia | [DIA](./DIA) | 进行中 |
| Cluely | [CLUELY](./CLUELY) | 进行中 |
| Brave Leo | [BRAVE](./BRAVE) | 进行中 |
| Hume | [HUME](./HUME) | 进行中 |
| 其他 | ... | 持续更新 |

## 目录结构

每个厂商目录下包含：
- 英文原文件 — 原始英文 System Prompt
- `中文/` — 中文翻译版本
- `说明.md` — 提取时间、版本、背景说明（部分目录适用）

当前仓库中有一部分目录尚未整理成 `原文/中文/说明` 三段式结构。现阶段采用的兼容策略是：

- 保留现有英文原文件不动
- 在同目录新增 `中文/同名文件`
- 中文文件头部标明原文路径、翻译日期和翻译方式

## 批量翻译脚本

仓库新增了批量翻译脚本：

```bash
python3 tools/translate_prompts.py
```

常用参数：

- `--paths ANTHROPIC OPENAI`：只翻译指定目录
- `--limit 5`：只处理前 5 个文件
- `--engine auto|google|mymemory`：选择翻译引擎或自动回退

脚本行为：

- 保留代码块、链接、路径、标签等结构
- 在每个厂商目录下生成 `中文/` 子目录
- 输出文件头部自动记录原文来源与翻译日期

## 如何贡献

1. Fork 本仓库
2. 在对应厂商目录下添加 `中文/` 翻译文件
3. 提交 PR，注明翻译的模型名称/版本及翻译方式

## 原始项目

本项目翻译内容来源于 [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S)，感谢 [@elder_plinius](https://x.com/elder_plinius) 的持续整理工作。

## License

[AGPL-3.0](./LICENSE) — 与原项目 [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) 保持一致。
