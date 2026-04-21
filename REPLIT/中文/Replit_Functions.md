# Replit_Functions（中文翻译）

> 原文：`../Replit_Functions.md`
> 来源路径：`REPLIT/Replit_Functions.md`
> 翻译方式：Codex 直译整理
> 翻译日期：2026-04-20

---

# 可用函数

```json
{"description": "重新启动（或启动）一个工作流。", "name": "restart_workflow", "parameters": {"properties": {"name": {"description": "工作流名称。", "type": "string"}}, "required": ["name"], "type": "object"}}
```

```json
{"description": "该工具会搜索并打开代码库中相关的文件。", "name": "search_filesystem", "parameters": {"properties": {"class_names": {"default": [], "description": "要在代码库中搜索的特定类名列表。区分大小写，仅支持精确匹配。可用来查找特定类定义及其使用位置。", "items": {"type": "string"}, "type": "array"}, "code": {"default": [], "description": "要在代码库中搜索的精确代码片段列表。适合查找特定实现或模式。每个片段应是完整代码片段，而不只是关键词。", "items": {"type": "string"}, "type": "array"}, "function_names": {"default": [], "description": "要搜索的特定函数或方法名列表。区分大小写，仅支持精确匹配。可用于定位函数定义及其调用。", "items": {"type": "string"}, "type": "array"}, "query_description": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": null, "description": "一个自然语言查询，用于语义相似度搜索。用普通英语描述你要找的内容，例如：'查找数据库连接中的错误处理' 或 '定位认证中间件实现'。"}}, "type": "object"}}
```

```json
{"description": "安装语言（如有需要），并安装或卸载一组库或项目依赖。应通过此工具来安装依赖，而不是手动执行 shell 命令或改文件。若将 `language_or_system=system`，则用于添加系统依赖，而不是使用 apt install。首次安装某种语言对应的依赖时，也会自动创建必要的项目文件（例如 package.json 等）。", "name": "install_dependencies"}
```

```json
{"description": "向用户请求项目所需的 secret API keys。如果缺少某个密钥，应尽早使用这个工具。这些 secrets 会被加入环境变量。该工具调用成本较高。", "name": "ask_secrets"}
```

```json
{"description": "检查环境中是否存在某个 secret。该工具用于验证 secret 是否存在，而不会暴露其实际值。", "name": "check_secrets"}
```

> 注：原文件是单行压缩的函数清单，这里保留原意并拆分为可读的中文块。更完整的参数细节仍建议对照原文查看。
