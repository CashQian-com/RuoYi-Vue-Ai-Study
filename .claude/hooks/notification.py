#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
通知钩子脚本 - Claude Code Hooks系统组件

该脚本处理Claude Code的通知事件，当代理需要用户输入时触发。
支持通过TTS（文本转语音）服务播放音频通知，并将通知数据记录到日志文件中。

功能特性：
- 智能TTS服务选择（ElevenLabs > OpenAI > pyttsx3）
- 可选的工程师姓名个性化通知
- 静默失败处理，确保钩子稳定性
- JSON格式的结构化日志记录

使用方法：
    python notification.py [--notify]
    
参数：
    --notify    启用TTS音频通知功能
"""

import argparse
import json
import os
import sys
import subprocess
import random
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


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


def announce_notification():
    """
    播放音频通知，告知用户代理需要输入。
    
    该函数会：
    1. 获取可用的TTS脚本路径
    2. 检查工程师姓名环境变量
    3. 以30%的概率在通知中包含个性化姓名
    4. 调用TTS脚本播放音频通知
    5. 静默处理所有异常，确保钩子稳定性
    """
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # 没有可用的TTS脚本
        
        # 获取工程师姓名（如果可用）
        engineer_name = os.getenv('ENGINEER_NAME', '').strip()
        
        # 创建通知消息，30%概率包含个性化姓名
        if engineer_name and random.random() < 0.3:
            notification_message = f"{engineer_name}, your agent needs your input"
        else:
            notification_message = "Your agent needs your input"
        
        # 调用TTS脚本播放通知消息
        subprocess.run([
            "uv", "run", tts_script, notification_message
        ], 
        capture_output=True,  # 抑制输出
        timeout=10  # 10秒超时
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # 如果TTS遇到问题，静默失败
        pass
    except Exception:
        # 对于任何其他错误，静默失败
        pass


def main():
    """
    通知钩子的主函数。
    
    处理流程：
    1. 解析命令行参数
    2. 从stdin读取JSON输入数据
    3. 创建日志目录并记录通知数据
    4. 根据--notify标志决定是否播放TTS通知
    5. 优雅处理所有异常情况
    """
    try:
        # 解析命令行参数
        parser = argparse.ArgumentParser()
        parser.add_argument('--notify', action='store_true', help='启用TTS通知功能')
        args = parser.parse_args()
        
        # 从stdin读取JSON输入数据
        input_data = json.loads(sys.stdin.read())
        
        # 确保日志目录存在
        import os
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'notification.json')
        
        # 读取现有的日志数据或初始化空列表
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # 追加新数据
        log_data.append(input_data)
        
        # 格式化写回文件
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # 仅在设置了--notify标志时通过TTS播放通知
        # 跳过通用的"Claude is waiting for your input"消息的TTS播放
        if args.notify and input_data.get('message') != 'Claude is waiting for your input':
            announce_notification()
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # 优雅处理JSON解码错误
        sys.exit(0)
    except Exception:
        # 处理任何其他错误
        sys.exit(0)

if __name__ == '__main__':
    main()