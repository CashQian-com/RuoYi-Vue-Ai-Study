#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
会话停止钩子脚本 - Claude Code Hooks系统组件

该脚本在Claude代理会话结束时触发，主要用于清理工作和完成通知。
支持会话记录导出、TTS语音通知和LLM生成的个性化完成消息。

功能特性：
- 智能TTS服务选择（ElevenLabs > OpenAI > pyttsx3）
- LLM生成的个性化完成消息（OpenAI > Anthropic > 预设消息）
- 会话记录导出功能（.jsonl 转 JSON）
- 结构化日志记录和错误容错处理

命令参数：
    --chat    将会话记录复制到chat.json文件

输入数据格式：
    {
        "session_id": "session_123",
        "stop_hook_active": true,
        "transcript_path": "path/to/transcript.jsonl"
        # 其他会话结束相关信息...
    }
"""

import argparse
import json
import os
import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """
    返回友好的完成消息列表。
    
    这些消息用作后TTS语音通知的默认选项，
    当LLM服务不可用时会随机选择其中一条。
    
    Returns:
        list: 包含预设完成消息的列表
    """
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!"
    ]


def get_tts_script_path():
    """
    根据可用的API密钥确定使用哪个TTS脚本。
    优先级顺序：ElevenLabs > OpenAI > pyttsx3
    
    Returns:
        str or None: TTS脚本的绝对路径，如果没有可用脚本则返回None
    """
    # 获取当前脚本目录并构建utils/tts路径
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # 检查ElevenLabs API密钥（最高优先级）
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    # 检查OpenAI API密钥（第二优先级）
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # 回退到pyttsx3（不需要API密钥）
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def get_llm_completion_message():
    """
    使用可用的LLM服务生成完成消息。
    优先级顺序：OpenAI > Anthropic > 随机选择预设消息
    
    Returns:
        str: 生成的或默认的完成消息
    """
    # 获取当前脚本目录并构建utils/llm路径
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"
    
    # 首先尝试OpenAI（最高优先级）
    if os.getenv('OPENAI_API_KEY'):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(oai_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # 然后尝试Anthropic
    if os.getenv('ANTHROPIC_API_KEY'):
        anth_script = llm_dir / "anth.py"
        if anth_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(anth_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # 回退到随机预设消息
    messages = get_completion_messages()
    return random.choice(messages)

def announce_completion():
    """使用最佳可用TTS服务宣布完成。"""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # 没有可用的TTS脚本
        
        # 获取完成消息（LLM生成或默认消息）
        completion_message = get_llm_completion_message()
        
        # 使用完成消息调用TTS脚本
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ], 
        capture_output=True,  # 抑制输出
        timeout=10  # 10秒超时
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # 如果TTS遇到问题则静默失败
        pass
    except Exception:
        # 对于任何其他错误都静默失败
        pass


def main():
    try:
        # 解析命令行参数
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='将会话记录复制到chat.json')
        args = parser.parse_args()
        
        # 从标准输入读取JSON数据
        input_data = json.load(sys.stdin)

        # 提取必需字段
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # 确保日志目录存在
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "stop.json")

        # 读取现有日志数据或初始化空列表
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # 追加新数据
        log_data.append(input_data)
        
        # 格式化写回文件
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # 处理--chat开关
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # 读取.jsonl文件并转换为JSON数组
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # 跳过无效行
                    
                    # 写入到logs/chat.json
                    chat_file = os.path.join(log_dir, 'chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # 静默失败

        # 通过TTS宣布完成
        announce_completion()

        sys.exit(0)

    except json.JSONDecodeError:
        # 优雅地处理JSON解码错误
        sys.exit(0)
    except Exception:
        # 优雅地处理任何其他错误
        sys.exit(0)


if __name__ == "__main__":
    main()
