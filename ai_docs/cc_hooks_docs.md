# Claude Code Hooks 参考文档

有关带示例的快速入门指南，请参见[Claude Code hooks 入门](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)。

## 配置

Claude Code钩子在您的[设置文件](https://docs.anthropic.com/en/docs/claude-code/settings)中配置：

- `~/.claude/settings.json` - 用户设置
- `.claude/settings.json` - 项目设置
- `.claude/settings.local.json` - 本地项目设置（不提交）
- 企业管理策略设置

### 结构

钩子按匹配器组织，每个匹配器可以有多个钩子：

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

- **matcher**: 匹配工具名称的模式，区分大小写（仅适用于`PreToolUse`和`PostToolUse`）
  - 简单字符串精确匹配：`Write`仅匹配Write工具
  - 支持正则表达式：`Edit|Write`或`Notebook.*`
  - 如果省略或为空字符串，钩子将为所有匹配事件运行
- **hooks**: 当模式匹配时要执行的命令数组
  - `type`: 目前仅支持`"command"`
  - `command`: 要执行的bash命令
  - `timeout`: （可选）命令运行时间限制（秒），超时后取消该特定命令。

对于像`UserPromptSubmit`、`Notification`、`Stop`和`SubagentStop`这样不使用匹配器的事件，您可以省略matcher字段：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

`"matcher": "*"`是无效的。请省略"matcher"或使用`"matcher": ""`。

## 钩子事件

### PreToolUse

在Claude创建工具参数后、处理工具调用前运行。

**常见匹配器：**
- `Task` - 代理任务
- `Bash` - Shell命令
- `Glob` - 文件模式匹配
- `Grep` - 内容搜索
- `Read` - 文件读取
- `Edit`, `MultiEdit` - 文件编辑
- `Write` - 文件写入
- `WebFetch`, `WebSearch` - Web操作

### PostToolUse

在工具成功完成后立即运行。

识别与PreToolUse相同的匹配器值。

### Notification

当Claude Code发送通知时运行。通知在以下情况下发送：

1. Claude需要您的权限来使用工具。例如："Claude需要您的权限来使用Bash"
2. 提示输入已空闲至少60秒。"Claude正在等待您的输入"

### UserPromptSubmit

当用户提交提示时运行，在Claude处理之前。这允许您根据提示/对话添加额外上下文、验证提示或阻止某些类型的提示。

### Stop

当主Claude Code代理完成响应时运行。如果停止是由于用户中断，则不运行。

### SubagentStop

当Claude Code子代理（Task工具调用）完成响应时运行。

### PreCompact

在Claude Code即将运行压缩操作之前运行。

**匹配器：**
- `manual` - 从`/compact`调用
- `auto` - 从自动压缩调用（由于上下文窗口已满）

## 钩子输入

钩子通过stdin接收包含会话信息和事件特定数据的JSON数据：

```typescript
{
  // 通用字段
  session_id: string
  transcript_path: string  // 对话JSON的路径
  cwd: string              // 调用钩子时的当前工作目录

  // 事件特定字段
  hook_event_name: string
  ...
}
```

### PreToolUse输入

`tool_input`的确切架构取决于工具。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "文件内容"
  }
}
```

### PostToolUse输入

`tool_input`和`tool_response`的确切架构取决于工具。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "文件内容"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Notification输入

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "任务成功完成"
}
```

### UserPromptSubmit输入

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "写一个计算数字阶乘的函数"
}
```

### Stop和SubagentStop输入

当Claude Code由于停止钩子而已经继续时，`stop_hook_active`为true。检查此值或处理记录以防止Claude Code无限运行。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

### PreCompact输入

对于`manual`，`custom_instructions`来自用户传递给`/compact`的内容。对于`auto`，`custom_instructions`为空。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

## 钩子输出

钩子有两种方式将输出返回给Claude Code。输出传达是否阻止以及应向Claude和用户显示的任何反馈。

### 简单：退出代码

钩子通过退出代码、stdout和stderr传达状态：

- **退出代码0**：成功。在记录模式（CTRL-R）中`stdout`显示给用户。
- **退出代码2**：阻止错误。`stderr`自动反馈给Claude处理。请参见下面的每个钩子事件行为。
- **其他退出代码**：非阻止错误。`stderr`显示给用户，执行继续。

提醒：如果退出代码为0，Claude Code不会看到stdout。

#### 退出代码2行为

| 钩子事件           | 行为                                         |
| ------------------ | -------------------------------------------- |
| `PreToolUse`       | 阻止工具调用，向Claude显示stderr             |
| `PostToolUse`      | 向Claude显示stderr（工具已运行）             |
| `Notification`     | 不适用，仅向用户显示stderr                   |
| `UserPromptSubmit` | 阻止提示处理，擦除提示，仅向用户显示stderr   |
| `Stop`             | 阻止停止，向Claude显示stderr                 |
| `SubagentStop`     | 阻止停止，向Claude子代理显示stderr           |
| `PreCompact`       | 不适用，仅向用户显示stderr                   |

### 高级：JSON输出

钩子可以在`stdout`中返回结构化JSON以进行更复杂的控制：

#### 通用JSON字段

所有钩子类型都可以包含这些可选字段：

```json
{
  "continue": true, // Claude是否应在钩子执行后继续（默认：true）
  "stopReason": "string" // continue为false时显示的消息
  "suppressOutput": true, // 隐藏记录模式中的stdout（默认：false）
}
```

如果`continue`为false，Claude在钩子运行后停止处理。

- 对于`PreToolUse`，这与`"decision": "block"`不同，后者仅阻止特定工具调用并向Claude提供自动反馈。
- 对于`PostToolUse`，这与`"decision": "block"`不同，后者向Claude提供自动反馈。
- 对于`UserPromptSubmit`，这阻止提示被处理。
- 对于`Stop`和`SubagentStop`，这优先于任何`"decision": "block"`输出。
- 在所有情况下，`"continue" = false`优先于任何`"decision": "block"`输出。

`stopReason`伴随`continue`提供显示给用户的原因，不显示给Claude。

#### `PreToolUse`决策控制

`PreToolUse`钩子可以控制工具调用是否继续。

- "approve"绕过权限系统。`reason`显示给用户但不显示给Claude。
- "block"阻止工具调用执行。`reason`显示给Claude。
- `undefined`导致现有权限流程。忽略`reason`。

```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "决策解释"
}
```

#### `PostToolUse`决策控制

`PostToolUse`钩子可以控制工具调用是否继续。

- "block"自动用`reason`提示Claude。
- `undefined`不做任何事。忽略`reason`。

```json
{
  "decision": "block" | undefined,
  "reason": "决策解释"
}
```

#### `UserPromptSubmit`决策控制

`UserPromptSubmit`钩子可以控制用户提示是否被处理。

- `"block"`阻止提示被处理。提交的提示从上下文中擦除。`"reason"`显示给用户但不添加到上下文。
- `undefined`允许提示正常进行。忽略`"reason"`。

```json
{
  "decision": "block" | undefined,
  "reason": "决策解释"
}
```

#### `Stop`/`SubagentStop`决策控制

`Stop`和`SubagentStop`钩子可以控制Claude是否必须继续。

- "block"阻止Claude停止。您必须填充`reason`以便Claude知道如何继续。
- `undefined`允许Claude停止。忽略`reason`。

```json
{
  "decision": "block" | undefined,
  "reason": "当Claude被阻止停止时必须提供"
}
```

#### JSON输出示例：Bash命令编辑

```python
#!/usr/bin/env python3
import json
import re
import sys

# 将验证规则定义为（正则表达式模式，消息）元组列表
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "使用 'rg' (ripgrep) 而不是 'grep' 以获得更好的性能和功能",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "使用 'rg --files | rg pattern' 或 'rg --files -g pattern' 而不是 'find -name' 以获得更好的性能",
    ),
]

def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"错误：无效的JSON输入：{e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

# 验证命令
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # 退出代码2阻止工具调用并向Claude显示stderr
    sys.exit(2)
```

#### UserPromptSubmit示例：添加上下文和验证

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

# 从stdin加载输入
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"错误：无效的JSON输入：{e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# 检查敏感模式
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token|密码|密钥|令牌)\s*[:=]", "提示包含潜在机密"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # 使用JSON输出以特定原因阻止
        output = {
            "decision": "block",
            "reason": f"安全策略违规：{message}。请在不包含敏感信息的情况下重新表述您的请求。"
        }
        print(json.dumps(output))
        sys.exit(0)

# 向上下文添加当前时间
context = f"当前时间：{datetime.datetime.now()}"
print(context)

# 允许提示继续进行，带有额外上下文
sys.exit(0)
```

## 与MCP工具配合使用

Claude Code钩子与[模型上下文协议（MCP）工具](https://docs.anthropic.com/en/docs/claude-code/mcp)无缝配合。当MCP服务器提供工具时，它们以特殊命名模式出现，您可以在钩子中匹配该模式。

### MCP工具命名

MCP工具遵循模式`mcp__<server>__<tool>`，例如：

- `mcp__memory__create_entities` - Memory服务器的创建实体工具
- `mcp__filesystem__read_file` - Filesystem服务器的读取文件工具
- `mcp__github__search_repositories` - GitHub服务器的搜索工具

### 为MCP工具配置钩子

您可以针对特定MCP工具或整个MCP服务器：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## 示例

有关包括代码格式化、通知和文件保护在内的实际示例，请参见入门指南中的[更多示例](https://docs.anthropic.com/en/docs/claude-code/hooks-guide#more-examples)。

## 安全注意事项

### 免责声明

**使用风险自负**：Claude Code钩子在您的系统上自动执行任意shell命令。通过使用钩子，您承认：

- 您对配置的命令完全负责
- 钩子可以修改、删除或访问您用户账户可以访问的任何文件
- 恶意或编写不当的钩子可能导致数据丢失或系统损坏
- Anthropic不提供保证，不承担因钩子使用而导致的任何损害的责任
- 您应该在生产使用之前在安全环境中彻底测试钩子

在将任何钩子命令添加到您的配置之前，请始终审查和理解它们。

### 安全最佳实践

以下是编写更安全钩子的一些关键实践：

1. **验证和清理输入** - 不要盲目信任输入数据
2. **始终引用shell变量** - 使用`"$VAR"`而不是`$VAR`
3. **阻止路径遍历** - 检查文件路径中的`..`
4. **使用绝对路径** - 为脚本指定完整路径
5. **跳过敏感文件** - 避免`.env`、`.git/`、密钥等

### 配置安全

对设置文件中钩子的直接编辑不会立即生效。Claude Code：

1. 在启动时捕获钩子快照
2. 在整个会话中使用此快照
3. 如果钩子被外部修改，则发出警告
4. 需要在`/hooks`菜单中审查更改才能应用

这防止恶意钩子修改影响您当前的会话。

## 钩子执行详情

- **超时**：默认60秒执行限制，每个命令可配置。
  - 单个命令的超时不会影响其他命令。
- **并行化**：所有匹配的钩子并行运行
- **环境**：在当前目录中运行，使用Claude Code的环境
- **输入**：通过stdin接收JSON
- **输出**：
  - PreToolUse/PostToolUse/Stop：进度显示在记录中（Ctrl-R）
  - Notification：仅记录到调试（`--debug`）

## 调试

### 基本故障排除

如果您的钩子不工作：

1. **检查配置** - 运行`/hooks`查看您的钩子是否已注册
2. **验证语法** - 确保您的JSON设置有效
3. **测试命令** - 首先手动运行钩子命令
4. **检查权限** - 确保脚本可执行
5. **查看日志** - 使用`claude --debug`查看钩子执行详情

常见问题：

- **引号未转义** - 在JSON字符串中使用`\"`
- **错误的匹配器** - 检查工具名称完全匹配（区分大小写）
- **命令未找到** - 为脚本使用完整路径

### 高级调试

对于复杂的钩子问题：

1. **检查钩子执行** - 使用`claude --debug`查看详细的钩子执行
2. **验证JSON架构** - 使用外部工具测试钩子输入/输出
3. **检查环境变量** - 验证Claude Code的环境是否正确
4. **测试边缘情况** - 尝试使用异常文件路径或输入的钩子
5. **监控系统资源** - 检查钩子执行期间的资源耗尽
6. **使用结构化日志** - 在您的钩子脚本中实现日志记录

### 调试输出示例

使用`claude --debug`查看钩子执行详情：

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

进度消息出现在记录模式（Ctrl-R）中显示：

- 正在运行哪个钩子
- 正在执行的命令
- 成功/失败状态
- 输出或错误消息