# UserPromptSubmit Hook 文档

UserPromptSubmit钩子是Claude Code中一个强大的生命周期事件，在用户提交提示时立即触发，在Claude处理之前。该钩子提供了根据自定义标准记录、验证、修改甚至阻止用户提示的能力。

## 概述

**钩子名称：** `UserPromptSubmit`  
**触发时机：** 用户向Claude Code提交提示时立即触发  
**可以阻止：** 是（退出代码2带stderr消息）  
**主要用例：** 提示记录、验证、安全过滤、上下文注入  

## JSON载荷结构

UserPromptSubmit钩子通过stdin接收以下JSON载荷：

```json
{
  "hook_event_type": "UserPromptSubmit",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "prompt": "用户提交的提示文本",
  "timestamp": "2024-01-20T15:30:45.123Z",
  "context": {
    "working_directory": "/path/to/project",
    "git_status": "clean",
    "platform": "darwin"
  }
}
```

### 载荷字段

- **hook_event_type**: 对于此钩子始终为"UserPromptSubmit"
- **session_id**: Claude Code会话的唯一标识符
- **prompt**: 用户提交的确切文本
- **timestamp**: 提示提交时的ISO 8601时间戳
- **context**: 环境的额外上下文信息

## 钩子功能

### 1. 记录和审计

最基本的用例是记录所有用户提示以供审计：

```python
# 将用户提示记录到会话目录
log_dir = ensure_session_log_dir(session_id)
log_file = log_dir / 'user_prompt_submit.json'

# 追加到现有日志
log_data.append(input_data)
with open(log_file, 'w') as f:
    json.dump(log_data, f, indent=2)
```

### 2. 提示验证和阻止

钩子可以验证提示并在违反政策时阻止它们：

```python
def validate_prompt(prompt):
    """验证用户提示是否违反安全或政策。"""
    blocked_patterns = [
        ('sudo rm -rf /', '检测到危险命令'),
        ('delete all', '过于宽泛的删除请求'),
        ('api_key', '潜在的机密暴露风险')
    ]
    
    prompt_lower = prompt.lower()
    
    for pattern, reason in blocked_patterns:
        if pattern.lower() in prompt_lower:
            return False, reason
    
    return True, None

# 在main()中：
is_valid, reason = validate_prompt(prompt)
if not is_valid:
    print(f"提示被阻止：{reason}", file=sys.stderr)
    sys.exit(2)  # 退出代码2阻止提示
```

### 3. 上下文注入

钩子可以打印附加的上下文，这些上下文会被添加到用户提示的前面：

```python
# 添加将包含在提示中的上下文信息
print(f"项目：{project_name}")
print(f"当前分支：{git_branch}")
print(f"时间：{datetime.now()}")
```

### 4. 提示修改

虽然钩子不能直接修改提示文本，但它可以提供额外的上下文，有效地改变Claude看到的内容：

```python
# 示例：添加编码标准提醒
if "写代码" in prompt.lower():
    print("提醒：遵循PEP 8样式指南并包含类型提示")
```

## 退出代码和流程控制

UserPromptSubmit钩子遵循标准的Claude Code钩子退出代码约定：

| 退出代码 | 行为 | 用例 |
|----------|------|------|
| 0 | 成功 | 提示正常处理，stdout内容作为上下文添加 |
| 2 | 阻止 | 提示被阻止，stderr消息显示给用户 |
| 其他 | 非阻止错误 | 错误显示给用户，提示仍被处理 |

## 高级JSON输出控制

除了简单的退出代码，UserPromptSubmit还可以返回结构化JSON：

```json
{
  "decision": "block" | "approve" | undefined,
  "reason": "决策解释",
  "context": "添加到提示前面的额外上下文",
  "suppressOutput": true | false
}
```

- **decision: "block"** - 阻止提示处理，向用户显示原因
- **decision: "approve"** - 明确允许提示（对白名单有用）
- **context** - 添加到用户提示前面的文本
- **suppressOutput** - 隐藏stdout不被添加到提示中

## 实现示例

### 示例1：基本记录

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
from pathlib import Path

# 读取输入
input_data = json.loads(sys.stdin.read())
session_id = input_data.get('session_id', 'unknown')
prompt = input_data.get('prompt', '')

# 记录到文件
log_dir = Path(f"logs/{session_id}")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / 'user_prompts.json'

# 追加提示
if log_file.exists():
    with open(log_file, 'r') as f:
        prompts = json.load(f)
else:
    prompts = []

prompts.append({
    'timestamp': input_data.get('timestamp'),
    'prompt': prompt
})

with open(log_file, 'w') as f:
    json.dump(prompts, f, indent=2)

sys.exit(0)
```

### 示例2：安全验证

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
import re

# 要阻止的安全模式
DANGEROUS_PATTERNS = [
    (r'rm\s+-rf\s+/', '危险的系统删除命令'),
    (r'curl.*\|\s*sh', '不安全的远程脚本执行'),
    (r'eval\s*\(', '不安全的代码评估'),
    (r'export\s+.*KEY', '潜在的凭据暴露'),
]

input_data = json.loads(sys.stdin.read())
prompt = input_data.get('prompt', '')

# 检查危险模式
for pattern, reason in DANGEROUS_PATTERNS:
    if re.search(pattern, prompt, re.IGNORECASE):
        print(f"安全策略违规：{reason}", file=sys.stderr)
        sys.exit(2)  # 阻止提示

sys.exit(0)
```

### 示例3：上下文增强

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

input_data = json.loads(sys.stdin.read())
prompt = input_data.get('prompt', '')

# 为编码请求添加项目上下文
if any(keyword in prompt.lower() for keyword in ['代码', '实现', '函数', '类', 'code', 'implement', 'function', 'class']):
    project_name = os.getenv('PROJECT_NAME', '未知项目')
    coding_standards = os.getenv('CODING_STANDARDS', '遵循最佳实践')
    
    print(f"项目：{project_name}")
    print(f"标准：{coding_standards}")
    print(f"生成时间：{datetime.now().isoformat()}")
    print("---")  # 分隔符

sys.exit(0)
```

### 示例4：智能提示分析

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_prompt_intent(prompt):
    """使用LLM分析提示意图和风险。"""
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    analysis_prompt = f"""分析此用户提示的潜在风险或政策违规：
    
    提示："{prompt}"
    
    用包含以下内容的JSON响应：
    - risk_level: "low"、"medium"或"high"
    - concerns: 具体关注点列表
    - recommendation: "allow"、"block"或"warn"
    """
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": analysis_prompt}]
    )
    
    return json.loads(response.content[0].text)

input_data = json.loads(sys.stdin.read())
prompt = input_data.get('prompt', '')

# 分析提示
analysis = analyze_prompt_intent(prompt)

if analysis['recommendation'] == 'block':
    print(f"已阻止：{', '.join(analysis['concerns'])}", file=sys.stderr)
    sys.exit(2)
elif analysis['recommendation'] == 'warn':
    # 添加警告作为上下文
    print(f"⚠️  注意：{', '.join(analysis['concerns'])}")
    print("请确保您理解其含义。")
    print("---")

sys.exit(0)
```

## 配置选项

此代码库中的UserPromptSubmit钩子支持几个命令行标志：

- **--validate**: 启用针对安全模式的提示验证
- **--log-only**: 仅记录提示，不进行任何验证或阻止
- **--summarize**: 生成提示的AI摘要（与可观察性集成时）

`.claude/settings.json`中的示例配置：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/user_prompt_submit.py --log-only"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/send_event.py --source-app my-app --event-type UserPromptSubmit --summarize"
          }
        ]
      }
    ]
  }
}
```

## 最佳实践

1. **快速执行**：保持处理最小化，因为这在每个提示上都运行
2. **清晰消息**：阻止时，向用户提供清晰的原因
3. **失败开放**：错误时，使用退出代码0以避免阻止合法工作
4. **隐私**：注意记录敏感信息
5. **上下文相关性**：仅添加与提示相关的上下文

## 与其他钩子的集成

UserPromptSubmit通常与其他钩子协同工作：

- **PreToolUse**：UserPromptSubmit可以设置影响工具阻止的上下文
- **Stop**：可以验证提示中请求的任务是否已完成
- **Notification**：可以基于提示内容触发自定义通知

## 安全注意事项

1. **输入清理**：始终验证和清理提示内容
2. **日志轮转**：实施日志轮转以防止无界增长
3. **敏感数据**：考虑在日志中编辑敏感信息
4. **速率限制**：考虑对重复提示实施速率限制

## 故障排除

常见问题和解决方案：

1. **钩子未触发**：确保钩子在settings.json中正确配置
2. **阻止不工作**：验证您使用的是退出代码2和stderr
3. **上下文未添加**：确保您打印到stdout，而不是stderr
4. **JSON错误**：始终优雅地处理JSON解析错误

## 总结

UserPromptSubmit钩子为以下功能提供了强大的拦截点：
- 记录所有用户交互
- 执行安全策略
- 添加上下文信息
- 防止危险操作
- 分析提示模式

当与其他Claude Code钩子结合使用时，它形成了一个用于控制和监控AI助手行为的综合系统。