#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "python-dotenv",
# ]
# ///

"""
OpenAI API集成工具 - Claude Code Hooks系统组件

该脚本提供OpenAI API的集成功能，支持基本的LLM提示和完成消息生成。
使用最新的GPT模型提供高效的AI生成服务。

功能特性：
- 优先使用gpt-4.1-nano模型（最快速）
- 支持工程师姓名个性化的完成消息
- 自动清理和格式化响应内容
- 健壮的错误处理和失败备用
- 命令行界面支持

使用方法：
    python oai.py "your prompt here"     # 基本LLM提示
    python oai.py --completion           # 生成完成消息

环境变量：
    OPENAI_API_KEY      # OpenAI API密钥（必需）
    ENGINEER_NAME       # 工程师姓名（可选，用于个性化消息）
"""

import os
import sys
from dotenv import load_dotenv


def prompt_llm(prompt_text):
    """
    使用最快模型的基本OpenAI LLM提示方法。

    Args:
        prompt_text (str): 要发送给模型的提示内容

    Returns:
        str: 模型的响应文本，如果出错则返回None
        
    功能特性：
    - 使用gpt-4.1-nano模型（最快速）
    - 设置100 tokens限制，适合简短响应
    - 温度厂0.7，平衡创意性和一致性
    - 自动处理API密钥和异常
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # 最快的OpenAI模型
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=100,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None


def generate_completion_message():
    """
    使用OpenAI LLM生成完成消息。

    Returns:
        str: 自然语言的完成消息，如果出错则返回None
        
    功能特性：
    - 支持工程师姓名个性化（通过ENGINEER_NAME环境变量）
    - 30%概率包含个性化姓名
    - 自动清理响应格式（删除引号和多余格式）
    - 生成简洁、积极的完成提示
    """
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()

    if engineer_name:
        name_instruction = f"有时（大约30%的机率）以自然的方式包含工程师的姓名'{engineer_name}'。"
        examples = f"""样式示例: 
- 标准型: "Work complete!", "All done!", "Task finished!", "Ready for your next move!"
- 个性化型: "{engineer_name}, all set!", "Ready for you, {engineer_name}!", "Complete, {engineer_name}!", "{engineer_name}, we're done!" """
    else:
        name_instruction = ""
        examples = """样式示例: "Work complete!", "All done!", "Task finished!", "Ready for your next move!" """

    prompt = f"""为AI编程助手完成任务时生成一条简短、友好的完成消息。

要求：
- 保持10个单词以内
- 积极向上，面向未来
- 使用自然、对话式的语言
- 专注于完成/准备状态
- 不要包含引号、格式或解释
- 仅返回完成消息文本
{name_instruction}

{examples}

生成一条完成消息："""

    response = prompt_llm(prompt)

    # 清理响应 - 删除引号和多余格式
    if response:
        response = response.strip().strip('"').strip("'").strip()
        # 如果有多行，只取第一行
        response = response.split("\n")[0].strip()

    return response


def main():
    """
    命令行界面，用于测试和独立使用。
    
    支持的命令：
    - oai.py "prompt text"      # 直接LLM提示
    - oai.py --completion       # 生成完成消息
    - oai.py                    # 显示使用说明
    
    退出行为：
    - 成功：输出生成的内容
    - 失败：输出错误信息
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--completion":
            message = generate_completion_message()
            if message:
                print(message)
            else:
                print("生成完成消息时出错")
        else:
            prompt_text = " ".join(sys.argv[1:])
            response = prompt_llm(prompt_text)
            if response:
                print(response)
            else:
                print("调用OpenAI API时出错")
    else:
        print("使用方法: ./oai.py '您的提示内容' 或 ./oai.py --completion")


if __name__ == "__main__":
    main()
