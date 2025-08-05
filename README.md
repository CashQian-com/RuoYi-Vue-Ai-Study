# AI Coding Setup - 自动化AI工作流

这是一个基于Claude Code的自动化AI开发工作流系统，通过专业化的AI代理团队实现从产品需求到项目部署的全流程自动化开发。

## 🤖 AI代理工作流


### 核心工作流程

原始的需求放在project/requirements.md

本系统通过9个专业化AI代理实现完整的软件开发生命周期管理：

```
产品需求 → 架构设计 → UI/UX设计 → 项目管理 → 开发实现 → 测试验证 → 部署运维
    ↓         ↓         ↓         ↓         ↓         ↓         ↓
 需求分析师 → 架构师 → UI设计师 → 项目经理 → 开发工程师 → 测试工程师 → 运维工程师
```

### 🏗️ 代理架构体系

#### 1. 需求与设计阶段
- **产品需求分析师** (product-requirements-analyst)
  - 负责业务需求分析和PRD文档创建
  - 将业务需求转化为结构化的产品需求文档
  - 生成：`PRD.md`

- **系统架构师** (architecture-designer)  
  - 进行技术架构设计和技术选型
  - 设计系统整体架构和模块划分
  - 生成：`Architecture.md`

- **UI/UX设计师** (ui-ux-designer)
  - 界面设计和用户体验优化
  - 创建全面的设计规范和组件库
  - 生成：`Design.md`

#### 2. 项目管理阶段
- **项目经理** (project-manager)
  - 统筹管理整个开发生命周期
  - 将需求分解为可执行的开发任务
  - 生成：`Task.md`

#### 3. 开发实现阶段
- **前端工程师** (frontend-developer)
  - 专注前端界面开发和用户交互
  - 精通React、Vue、Angular等主流框架
  - 执行Task.md中"前端"类型任务

- **后端工程师** (backend-developer)
  - API开发、数据库设计、业务逻辑实现
  - 支持Spring Boot、Django、Flask、FastAPI等框架
  - 执行Task.md中"后端"类型任务

- **全栈工程师** (fullstack-developer)
  - 处理需要前后端协调的复杂功能
  - 负责端到端的功能实现和集成
  - 执行跨领域的综合性开发任务

#### 4. 质量保证阶段
- **测试工程师** (test-engineer)
  - 单元测试、集成测试、端到端测试
  - 性能测试和安全测试
  - 执行Task.md中"测试"类型任务

#### 5. 部署运维阶段
- **运维工程师** (devops-engineer)
  - Docker容器化、Kubernetes编排
  - CI/CD流水线、云服务部署
  - 执行Task.md中"部署"和"运维"类型任务

### 📋 工作流标准文档

系统通过标准化文档实现代理间的协作：

1. **PRD.md** - 产品需求文档，定义功能需求和业务逻辑
2. **Architecture.md** - 技术架构文档，规划系统架构和技术栈
3. **Design.md** - UI/UX设计规范，界面和交互设计标准  
4. **Task.md** - 开发任务列表，具体的可执行任务清单

### 🚀 使用方式

#### 快速启动
使用 `/prime` 命令为新的代理会话加载项目上下文：
```bash
/prime
```

#### 标准开发流程
1. **需求分析**: 使用product-requirements-analyst创建PRD.md
2. **架构设计**: 使用architecture-designer设计技术架构
3. **界面设计**: 使用ui-ux-designer制定设计规范
4. **任务规划**: 使用project-manager分解开发任务
5. **功能开发**: 各专业代理按Task.md执行相应任务
6. **测试验证**: test-engineer执行各类测试任务
7. **部署上线**: devops-engineer处理部署和运维

