---
allowed-tools: Bash, Read
description: 通过分析代码库结构和README为新的代理会话加载上下文
---

# 启动

此命令通过检查代码库结构和读取项目README为新的代理会话加载必要的上下文。

## 指令
- 运行 `git ls-files` 了解代码库结构和文件组织
- 读取README.md了解项目目的、设置说明和关键信息
- 基于收集的上下文提供项目的简洁概述
- 基于目前项目情况，主动为用户安排，开始AI工作流任务

## 上下文
- 代码库结构git可访问：!`git ls-files`
- 代码库结构全部：!`eza . --tree`
- 项目README：@README.md
- 文档：
    @project/requirements.md
    @project/PRD.md
    @project/Architecture.md
    @project/Design.md
    @project/Task.md
