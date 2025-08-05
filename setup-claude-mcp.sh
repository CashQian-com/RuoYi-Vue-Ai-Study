#!/bin/bash

# 脚本：设置Claude Code MCP服务器

echo "开始配置Claude Code MCP服务器..."

# 添加Context7 MCP服务器
echo "添加Context7 MCP服务器..."
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# 添加Sequential Thinking服务器
echo "添加Sequential Thinking服务器..."
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# 添加Puppeteer服务器
echo "添加Puppeteer服务器..."
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer

# 添加Playwright服务器
echo "添加Playwright服务器..."
claude mcp add playwright npx @playwright/mcp@latest

# 添加Tmux服务器
echo "添加Tmux服务器..."
claude mcp add tmux npx mcp-tmux-server@latest

echo "所有MCP服务器配置完成！"
echo "运行 'claude mcp' 查看配置的服务器列表"