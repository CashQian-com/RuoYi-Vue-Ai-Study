#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "openai[voice_helpers]",
#     "python-dotenv",
# ]
# ///

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv


async def main():
    """
    OpenAI TTS脚本 - Claude Code Hooks系统组件

    使用OpenAI最新的TTS模型提供高质量的文本转语音服务。
    接受可选的文本提示作为命令行参数。

    使用方法:
    - ./openai_tts.py                       # 使用默认文本
    - ./openai_tts.py "您的自定义文本"    # 使用提供的文本

    功能特性:
    - OpenAI gpt-4o-mini-tts模型（最新）
    - Nova声音（吸引人且温暖）
    - 支持指令的流式音频
    - 通过LocalAudioPlayer实现实时音频播放
    
    环境变量:
        OPENAI_API_KEY  # OpenAI API密钥（必需）
    """

    # 加载环境变量
    load_dotenv()

    # 从环境中获取API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误: 在环境变量中未找到OPENAI_API_KEY")
        print("请将您的OpenAI API密钥添加到.env文件中:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        from openai import AsyncOpenAI
        from openai.helpers import LocalAudioPlayer

        # 初始化OpenAI客户端
        openai = AsyncOpenAI(api_key=api_key)

        print("🎙️  OpenAI TTS")
        print("=" * 20)

        # 从命令行参数获取文本或使用默认值
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # 将所有参数连接为文本
        else:
            text = "Today is a wonderful day to build something people love!"

        print(f"🎯 文本: {text}")
        print("🔊 生成并流式传输中...")

        try:
            # 使用OpenAI TTS生成并流式传输音频
            async with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="nova",
                input=text,
                instructions="以快乐、积极但专业的语调说话。",
                response_format="mp3",
            ) as response:
                await LocalAudioPlayer().play(response)

            print("✅ 播放完成!")

        except Exception as e:
            print(f"❌ 错误: {e}")

    except ImportError as e:
        print("❌ 错误: 所需包未安装")
        print("此脚本使用UV自动安装依赖项。")
        print("确保已安装UV: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
