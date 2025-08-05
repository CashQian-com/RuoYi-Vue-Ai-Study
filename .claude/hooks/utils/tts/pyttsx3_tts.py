#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

import sys
import random

def main():
    """
    pyttsx3 TTS脚本 - Claude Code Hooks系统组件
    
    使用pyttsx3进行离线文本转语音合成。
    接受可选的文本提示作为命令行参数。
    
    使用方法:
    - ./pyttsx3_tts.py                      # 使用默认文本
    - ./pyttsx3_tts.py "您的自定义文本"   # 使用提供的文本
    
    功能特性:
    - 离线TTS（不需要API密钥）
    - 跨平台兼容性
    - 可配置的声音设置
    - 即时音频播放
    
    配置:
    - 语速: 180 单词/分钟
    - 音量: 0.8 (0.0-1.0)
    """
    
    try:
        import pyttsx3
        
        # 初始化TTS引擎
        engine = pyttsx3.init()
        
        # 配置引擎设置
        engine.setProperty('rate', 180)    # 语音速度（单词/分钟）
        engine.setProperty('volume', 0.8)  # 音量（0.0到1.0）
        
        print("🎙️  pyttsx3 TTS")
        print("=" * 15)
        
        # 从命令行参数获取文本或使用默认值
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # 将所有参数连接为文本
        else:
            # 默认完成消息
            completion_messages = [
            "Work complete!",
            "All done!",
            "Task finished!",
            "Job complete!",
            "Ready for next task!"
            ]
            text = random.choice(completion_messages)
        
        print(f"🎯 文本: {text}")
        print("🔊 正在说话...")
        
        # 说出文本
        engine.say(text)
        engine.runAndWait()
        
        print("✅ 播放完成!")
        
    except ImportError:
        print("❌ 错误: pyttsx3包未安装")
        print("此脚本使用UV自动安装依赖项。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()