#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    ElevenLabs Turbo v2.5 TTS脚本 - Claude Code Hooks系统组件
    
    使用ElevenLabs的Turbo v2.5模型提供快速、高质量的文本转语音服务。
    接受可选的文本提示作为命令行参数。
    
    使用方法:
    - ./elevenlabs_tts.py                       # 使用默认文本
    - ./elevenlabs_tts.py "您的自定义文本"    # 使用提供的文本
    
    功能特性:
    - 快速生成（为实时使用优化）
    - 高质量语音合成
    - 稳定的生产模型
    - 高音量使用的成本效益
    
    环境变量:
        ELEVENLABS_API_KEY  # ElevenLabs API密钥（必需）
    """
    
    # 加载环境变量
    load_dotenv()
    
    # 从环境中获取API密钥
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ 错误: 在环境变量中未找到ELEVENLABS_API_KEY")
        print("请将您的ElevenLabs API密钥添加到.env文件中:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)
    
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play
        
        # 初始化客户端
        elevenlabs = ElevenLabs(api_key=api_key)
        
        print("🎙️  ElevenLabs Turbo v2.5 TTS")
        print("=" * 40)
        
        # 从命令行参数获取文本或使用默认值
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # 将所有参数连接为文本
        else:
            text = "The first move is what sets everything in motion."
        
        print(f"🎯 文本: {text}")
        print("🔊 生成并播放中...")
        
        try:
            # 直接生成并播放音频
            audio = elevenlabs.text_to_speech.convert(
                text=text,
                voice_id="WejK3H1m7MI9CHnIjW9K",  # 指定的声音
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
            )
            
            play(audio)
            print("✅ 播放完成!")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        
    except ImportError:
        print("❌ 错误: elevenlabs包未安装")
        print("此脚本使用UV自动安装依赖项。")
        print("确保已安装UV: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()