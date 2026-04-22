{functions}
{
  "description": "为 Web 服务器启动一个浏览器预览。这样用户就可以像平常一样与 Web 服务器交互，并向 Cascade 提供控制台日志以及其他来自该 Web 服务器的信息。注意，这个工具调用不会自动为用户打开浏览器预览，用户必须点击提供的某个按钮，才能在浏览器中打开它。",
  "name": "browser_preview",
  "parameters": {
    "properties": {
      "Name": {
        "description": "目标 Web 服务器的简短名称，3-5 个词，使用标题大小写，例如 'Personal Website'。直接输出普通字符串，不要使用 markdown，也不要加 'Title:' 之类的前缀。",
        "type": "string"
      },
      "Url": {
        "description": "需要提供浏览器预览的目标 Web 服务器 URL。它应包含协议（如 http:// 或 https://）、域名（如 localhost 或 127.0.0.1）以及端口（如 :8080），但不能包含路径。",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用 windsurf_deployment_id 检查某个 Web 应用部署的状态，并判断应用构建是否成功、是否已被认领。除非用户要求，否则不要运行它。它只能在 deploy_web_app 工具调用之后使用。",
  "name": "check_deploy_status",
  "parameters": {
    "properties": {
      "WindsurfDeploymentId": {
        "description": "我们要检查状态的 Windsurf 部署 ID。注意这不是 project_id。",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "从代码库中查找与搜索查询最相关的代码片段。当搜索查询更精确并且与代码的功能或用途相关时，这个工具效果最好。如果问题过于宽泛，比如询问某个大型组件或系统的整体“框架”或“实现”，结果会很差。它只会展示排名靠前条目的完整代码内容，而且这些内容也可能被截断。其他条目则只会展示 docstring 和签名。你可以使用相同的 path 和 node name 调用 view_code_item 来查看任何条目的完整代码内容。注意，如果你尝试在超过 500 个文件上搜索，搜索结果质量会明显下降。只有在确有必要时，才对大量文件执行搜索。",
  "name": "codebase_search",
  "parameters": {
    "properties": {
      "Query": {
        "description": "搜索查询",
        "type": "string"
      },
      "TargetDirectories": {
        "description": "要搜索的目录绝对路径列表",
        "items": {
          "type": "string"
        },
        "type": "array"
      }
    },
    "type": "object"
  }
}

{
  "description": "通过 ID 获取先前执行过的终端命令状态。返回当前状态（running、done）、按输出优先级返回的输出行，以及任何错误信息。不要尝试检查除后台命令 ID 以外的其他 ID。",
  "name": "command_status",
  "parameters": {
    "properties": {
      "CommandId": {
        "description": "要查询状态的命令 ID",
        "type": "string"
      },
      "OutputCharacterCount": {
        "description": "要查看的字符数。尽量设小，以避免占用过多内存。",
        "type": "integer"
      },
      "OutputPriority": {
        "description": "命令输出的显示优先级。必须是以下之一：'top'（显示最早的行）、'bottom'（显示最新的行）或 'split'（优先显示最早和最新的行，跳过中间内容）。",
        "enum": ["top", "bottom", "split"],
        "type": "string"
      },
      "WaitDurationSeconds": {
        "description": "在获取状态前等待命令完成的秒数。如果命令在此时间内完成，该工具会提前返回。若只想立即获取状态，设为 0。若只想等待完成，可设为 60。",
        "type": "integer"
      }
    },
    "type": "object"
  }
}

{
  "description": "将与用户及其任务相关的重要上下文保存到记忆数据库中。\n适合保存的上下文示例：\n- 用户偏好\n- 用户明确要求记住的内容，或希望你调整行为的说明\n- 重要代码片段\n- 技术栈\n- 项目结构\n- 重大里程碑或功能\n- 新的设计模式和架构决策\n- 以及其他你认为值得记住的信息。\n在创建新记忆之前，先检查数据库中是否已有语义相近的记忆。如果找到，就更新它，而不是创建重复项。\n必要时也可以用该工具删除错误记忆。",
  "name": "create_memory",
  "parameters": {
    "properties": {
      "Action": {
        "description": "对记忆执行的操作类型。必须是 'create'、'update' 或 'delete' 之一。",
        "enum": ["create", "update", "delete"],
        "type": "string"
      },
      "Content": {
        "description": "新建或更新记忆时的内容。删除已有记忆时留空。",
        "type": "string"
      },
      "CorpusNames": {
        "description": "与该记忆关联的工作区 CorpusNames。每个元素都必须与系统提示中提供的某个 CorpusName 完整且精确匹配，包括所有符号。仅在创建新记忆时使用。",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "Id": {
        "description": "要更新或删除的现有记忆 ID。创建新记忆时留空。",
        "type": "string"
      },
      "Tags": {
        "description": "与记忆关联的标签，用于过滤或检索。仅在创建新记忆时使用。使用 snake_case。",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "Title": {
        "description": "新建或更新记忆时使用的描述性标题。创建或更新时必填；删除时留空。",
        "type": "string"
      },
      "UserTriggered": {
        "description": "如果这是用户明确要求你创建 / 修改的记忆，则设为 true。",
        "type": "boolean"
      }
    },
    "type": "object"
  }
}

{
  "description": "将 JavaScript Web 应用部署到类似 Netlify 这样的部署提供商。站点不需要预先构建，只需要源文件即可。部署前务必先运行 read_deployment_config 工具，并确保所有缺失文件都已创建。如果部署的是已有站点，使用 project_id 标识该站点；如果部署的是新站点，则将 project_id 留空。",
  "name": "deploy_web_app",
  "parameters": {
    "properties": {
      "Framework": {
        "description": "Web 应用使用的框架。",
        "enum": ["eleventy", "angular", "astro", "create-react-app", "gatsby", "gridsome", "grunt", "hexo", "hugo", "hydrogen", "jekyll", "middleman", "mkdocs", "nextjs", "nuxtjs", "remix", "sveltekit", "svelte"],
        "type": "string"
      },
      "ProjectId": {
        "description": "如果该应用已存在于部署配置文件中，则填写该 Web 应用的 project ID。若是新站点，或用户想重命名站点，则留空。如果是重新部署，请在部署配置中找到项目 ID，并原样使用。",
        "type": "string"
      },
      "ProjectPath": {
        "description": "Web 应用项目的绝对路径。",
        "type": "string"
      },
      "Subdomain": {
        "description": "URL 中使用的子域名或项目名。如果是使用 project_id 部署已有站点，则留空。对于新站点，子域名应当唯一且与项目相关。",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用 fd 在指定目录中搜索文件和子目录。\n搜索默认采用智能大小写，并忽略 gitignore 文件。\nPattern 和 Excludes 都使用 glob 格式。如果你是按扩展名搜索，就不需要同时指定 Pattern 和 Extensions。\n为避免输出过多，结果最多返回 50 条。请用各类参数缩小范围。\n结果会包含类型、大小、修改时间以及相对路径。",
  "name": "find_by_name",
  "parameters": {
    "properties": {
      "Excludes": {
        "description": "可选，用于排除匹配给定 glob 的文件 / 目录",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "Extensions": {
        "description": "可选，限制包含的文件扩展名（不带前导点）。匹配路径必须至少命中一个扩展名。",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "FullPath": {
        "description": "可选，是否要求完整绝对路径匹配 glob 模式；默认只要求文件名匹配。启用该标志时请谨慎设置 glob，例如启用后 `*.py` 不会匹配 `/foo/bar.py`，但 `**/*.py` 会匹配。",
        "type": "boolean"
      },
      "MaxDepth": {
        "description": "可选，搜索的最大深度",
        "type": "integer"
      },
      "Pattern": {
        "description": "可选，要搜索的模式，支持 glob 格式",
        "type": "string"
      },
      "SearchDirectory": {
        "description": "执行搜索的目录",
        "type": "string"
      },
      "Type": {
        "description": "可选，类型过滤，取值为 file、directory、any",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用 ripgrep 在文件或目录中查找精确模式匹配。\n结果以 JSON 格式返回，每条匹配会包含：\n- Filename\n- LineNumber\n- LineContent：匹配所在行内容\n总结果最多 50 条。可以通过 Includes 过滤文件类型或具体路径来细化范围。",
  "name": "grep_search",
  "parameters": {
    "properties": {
      "CaseInsensitive": {
        "description": "若为 true，则执行不区分大小写的搜索。",
        "type": "boolean"
      },
      "Includes": {
        "description": "要搜索的文件或目录。支持文件模式（如 '*.txt'）或具体路径（如 'path/to/file.txt' 或 'path/to/dir'）。如果是在单个文件中 grep，可以留空。",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "MatchPerLine": {
        "description": "若为 true，则返回每一行匹配内容，包括行号与片段（等价于 'git grep -nI'）。若为 false，则仅返回包含该查询的文件名（等价于 'git grep -l'）。",
        "type": "boolean"
      },
      "Query": {
        "description": "要在文件中搜索的词或模式。",
        "type": "string"
      },
      "SearchPath": {
        "description": "要搜索的路径，可以是目录或文件。该参数必填。",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "列出某个目录的内容。目录路径必须是存在的绝对路径。输出中每个子项都会包含：相对该目录的路径、是目录还是文件、如果是文件则显示字节大小、如果是目录则显示递归子项数量。",
  "name": "list_dir",
  "parameters": {
    "properties": {
      "DirectoryPath": {
        "description": "要列出内容的目录路径，必须是一个存在的绝对目录路径",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "读取某个 Web 应用的部署配置，并判断应用是否已准备好部署。仅应在 deploy_web_app 之前使用。",
  "name": "read_deployment_config",
  "parameters": {
    "properties": {
      "ProjectPath": {
        "description": "Web 应用项目的绝对路径。",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "从 URL 读取内容。URL 必须是一个 HTTP 或 HTTPS 地址，并且指向可通过浏览器访问的有效互联网资源。",
  "name": "read_url_content",
  "parameters": {
    "properties": {
      "Url": {
        "description": "要读取内容的 URL",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用此工具编辑现有文件。请务必遵循以下规则：\n1. 不要对同一个文件并行调用多次此工具。\n2. 如果要编辑同一文件中多个不相邻的代码行，请只调用一次此工具，并将每次编辑作为独立的 ReplacementChunk。\n3. 对于每个 ReplacementChunk，需指定 TargetContent 和 ReplacementContent。TargetContent 中应填写要编辑的精确代码行，这些行必须与现有文件中的文本完全一致。ReplacementContent 中填写替换后的内容，它必须是对 TargetContent 的完整可直接替换版本，并包含所有需要修改的地方。\n4. 如果在同一文件中进行多处编辑，应提供多个独立的 ReplacementChunk。不要试图用整个新文件去替换整个旧文件，这样开销非常大。\n5. 不能编辑以下扩展名的文件： [.ipynb]\n你应在其他参数之前先指定以下参数：[TargetFile]",
  "name": "replace_file_content",
  "parameters": {
    "properties": {
      "CodeMarkdownLanguage": {
        "description": "代码块使用的 Markdown 语言，例如 'python' 或 'javascript'",
        "type": "string"
      },
      "Instruction": {
        "description": "对你正在对文件做的修改的描述。",
        "type": "string"
      },
      "ReplacementChunks": {
        "description": "要替换的块列表。若编辑位置不相邻，最好尽量提供多个块。这里必须是 JSON 数组，不能是字符串。",
        "items": {
          "additionalProperties": false,
          "properties": {
            "AllowMultiple": {
              "description": "若为 true，则如果找到多个 'targetContent'，会全部替换为 'replacementContent'。否则如果找到多个匹配，会返回错误。",
              "type": "boolean"
            },
            "ReplacementContent": {
              "description": "用于替换目标内容的文本。",
              "type": "string"
            },
            "TargetContent": {
              "description": "要被替换的精确字符串。它必须与要替换的现有字符序列完全一致，包括空白字符。务必小心保留前导空格，否则将完全无法工作。如果 AllowMultiple 不是 true，那么该字符串必须在文件中唯一，否则会报错。",
              "type": "string"
            }
          },
          "required": ["TargetContent", "ReplacementContent", "AllowMultiple"],
          "type": "object"
        },
        "type": "array"
      },
      "TargetFile": {
        "description": "要修改的目标文件。始终将该参数作为第一个参数指定。",
        "type": "string"
      },
      "TargetLintErrorIds": {
        "description": "如果适用，填写本次编辑试图修复的 lint 错误 ID（这些 ID 通常来自最近的 IDE 反馈）。如果你认为此次编辑可能修复 lint，就填写；如果毫无关系，就不要填。一个经验原则是：如果你的修改受到 lint 反馈影响，就应填写这些 ID。请诚实判断。",
        "items": {
          "type": "string"
        },
        "type": "array"
      }
    },
    "type": "object"
  }
}

{
  "description": "代表用户提出一条要执行的命令。操作系统：mac。Shell：bash。\n**绝不要提出 cd 命令**。\n如果你拥有这个工具，请注意这意味着你确实可以直接在用户系统上运行命令。\n务必准确填写 CommandLine，即它在 shell 中应被执行的原样命令。\n注意：用户必须先批准该命令后，它才会执行。如果命令不符合预期，用户可能会拒绝。\n在用户批准之前，命令不会真正执行。如果当前步骤在等待批准，那么它实际上还没有开始运行。\n命令会在设置了 PAGER=cat 的环境中运行。对于通常依赖分页器、输出可能很长的命令（例如 git log），你可能需要限制输出长度，例如使用 git log -n <N>。",
  "name": "run_command",
  "parameters": {
    "properties": {
      "Blocking": {
        "description": "若为 true，则命令会一直阻塞，直到完整结束。在此期间用户无法与 Cascade 交互。只有在以下情况才应设为 true：(1) 该命令会较快结束；或 (2) 在回复用户前，你必须先看到命令输出。若是长时间运行的进程（例如启动 Web 服务器），请设为非阻塞。",
        "type": "boolean"
      },
      "CommandLine": {
        "description": "要执行的精确命令行字符串。",
        "type": "string"
      },
      "Cwd": {
        "description": "该命令运行时的当前工作目录",
        "type": "string"
      },
      "SafeToAutoRun": {
        "description": "如果你认为该命令无需用户批准即可安全运行，则设为 true。只要命令可能带来破坏性副作用，它就是不安全的，例如删除文件、修改状态、安装系统依赖、发起外部请求等。只有在你极其确信安全时，才可设为 true。如果你觉得命令可能不安全，那么绝不能设为 true，即使用户要求也不行。绝不能自动运行潜在不安全的命令。",
        "type": "boolean"
      },
      "WaitMsBeforeAsync": {
        "description": "仅在 Blocking 为 false 时适用。表示启动命令后，在完全异步化之前等待的毫秒数。适合那些本应异步运行、但可能会很快失败的命令，这样你能先看到错误。不要设太长，否则会让所有人白等。",
        "type": "integer"
      }
    },
    "type": "object"
  }
}

{
  "description": "执行一次 Web 搜索，获取与给定查询以及可选域名过滤相关的一组网页文档。",
  "name": "search_web",
  "parameters": {
    "properties": {
      "domain": {
        "description": "可选，建议搜索优先考虑的域名",
        "type": "string"
      },
      "query": {
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "如果你没有调用其他工具，并且正在向用户提问，可以使用该工具为问题提供少量可能的建议回答。例如 Yes/No，或其他简单的多选项。应谨慎使用，且只在你高度确信用户很可能从这些候选项中选择其一时使用。如果用户的下一条输入可能是简短或较长的自由文本，就不要给建议。例如，假设用户采纳了你的建议，如果此后你还需要继续追问，那说明这个建议本来就不应该给。尽量不要连续多次使用。",
  "name": "suggested_responses",
  "parameters": {
    "properties": {
      "Suggestions": {
        "description": "建议列表。每项最多几个词，不要超过 3 个选项。",
        "items": {
          "type": "string"
        },
        "type": "array"
      }
    },
    "type": "object"
  }
}

{
  "description": "查看代码项节点的内容，例如文件中的类或函数。你必须使用完整限定的代码项名称，例如 grep_search 工具返回的名称。比如某个类叫 `Foo`，而你想查看该类中的函数定义 `bar`，就应使用 `Foo.bar` 作为 NodeName。如果某个符号的内容已经由 codebase_search 展示过，就不要再请求查看它。如果文件中找不到该符号，工具会返回空字符串。",
  "name": "view_code_item",
  "parameters": {
    "properties": {
      "File": {
        "description": "节点所在文件的绝对路径，例如 /path/to/file",
        "type": "string"
      },
      "NodePath": {
        "description": "节点在文件中的路径，例如 package.class.FunctionName",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "查看文件内容。文件行号以 0 为起始索引，工具会返回从 StartLine 到 EndLine（含）之间的内容，以及这些范围外代码的摘要。注意，一次最多只能查看 200 行。\n\n在使用该工具收集信息时，你有责任确保自己获得了完整上下文。具体来说，每次调用都应：\n1) 判断目前看到的文件内容是否足以继续任务。\n2) 若当前内容不足，而你怀疑所需信息在未展示行中，必须主动再次调用以查看那些行。\n3) 如果拿不准，就继续调用一次获取更多信息。记住，不完整的文件视图可能遗漏关键依赖、导入或功能。",
  "name": "view_file",
  "parameters": {
    "properties": {
      "AbsolutePath": {
        "description": "要查看的文件路径，必须是绝对路径。",
        "type": "string"
      },
      "EndLine": {
        "description": "查看的结束行（包含）。不能超过 StartLine 后 200 行。",
        "type": "integer"
      },
      "IncludeSummaryOfOtherLines": {
        "description": "若为 true，除了精确返回 StartLine 到 EndLine 的内容，还会附带整个文件其余部分的压缩摘要。",
        "type": "boolean"
      },
      "StartLine": {
        "description": "查看的起始行",
        "type": "integer"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用 URL 和块位置查看某个网页文档内容的特定片段。在此之前，必须已经先用 read_url_content 读取过该 URL。",
  "name": "view_web_document_content_chunk",
  "parameters": {
    "properties": {
      "position": {
        "description": "要查看的片段位置",
        "type": "integer"
      },
      "url": {
        "description": "该片段所属的 URL",
        "type": "string"
      }
    },
    "type": "object"
  }
}

{
  "description": "使用此工具创建新文件。若父目录不存在，也会一并创建。\n\t\t遵循以下说明：\n\t\t1. 绝不要用此工具修改或覆盖现有文件。调用前务必先确认 TargetFile 不存在。\n\t\t2. 你必须将 TargetFile 作为第一个参数指定。请在任何代码内容之前先完整填写 TargetFile。\n你应在其他参数之前优先指定以下参数：[TargetFile]",
  "name": "write_to_file",
  "parameters": {
    "properties": {
      "CodeContent": {
        "description": "要写入文件的代码内容。",
        "type": "string"
      },
      "EmptyFile": {
        "description": "若要创建空文件，则设为 true。",
        "type": "boolean"
      },
      "TargetFile": {
        "description": "要创建并写入代码的目标文件。",
        "type": "string"
      }
    },
    "type": "object"
  }
}
{/functions}
