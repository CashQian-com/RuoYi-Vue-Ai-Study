# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RuoYi-Vue-Ai-Study is an AI-assisted development project built on RuoYi-Vue framework (v3.8.5) with a sophisticated agent-based workflow system. It combines a traditional Java enterprise backend (Spring Boot + MyBatis-Plus) with a modern Vue 3 frontend (Element Plus + Vite) and custom tool libraries.

**Quick Context Loading**: Use the `/prime` command to load project context for new sessions.

## Technology Stack

**Backend**: Spring Boot 2.7.10, MyBatis-Plus 3.5.3, Spring Security + JWT, Redis 6.0+ + Caffeine, Forest 1.5.30 (declarative HTTP client)
**Frontend**: Vue 3.2.45, Element Plus 2.2.27, Pinia 2.0.22, Vite 3.2.3
**Tools**: java-spring-tools 1.0.0 (common, base-forest, validator, wechat, payment, message modules)

## Critical Module Architecture

**READ THIS FIRST** - The project uses a unique multi-module structure that differs from standard RuoYi:

```
lf-base              # Base module (shared base classes like LBaseEntity)
lf-modules           # Business module container - NEW!
├── cn.lf.modules.*  # Business domain modules (domain, mapper, service ONLY - NO Controller)
└── cn.ynlky.modules.* # Specific business submodules
lf-admin             # Backend management Controller module (ALL Controllers go here)
lf-open-api          # Open API module (frontend interfaces for mini-programs/H5)
ruoyi-*              # RuoYi framework modules (DO NOT MODIFY)
```

**Critical Rules**:
1. **Controllers** MUST be in `lf-admin` module (`cn.lf.base.controller`)
2. **Domain/Mapper/Service** MUST be in `lf-modules` business submodules (e.g., `cn.lf.modules.ai`)
3. **Package names MUST strictly match file paths**
4. Business submodules organized by domain: `cn.lf.modules.ai`, `cn.ynlky.modules.ydcx_user`

**Cross-Module References**:
```java
// Controller in lf-admin references lf-modules
import cn.lf.modules.ai.domain.AiModel;           // domain from lf-modules
import cn.lf.modules.ai.service.IAiModelService;  // service from lf-modules

// Service in lf-modules implements local interface, references lf-base
import cn.lf.modules.ai.domain.AiModel;           // same module domain
import cn.lf.base.domain.LBaseEntity;             // base class from lf-base
```

See `.ai-rules/module-package-structure.md` for detailed architecture documentation.

## Common Development Commands

**Backend**:
```bash
cd RuoYi-Vue
mvn clean install
mvn spring-boot:run -pl ruoyi-admin
```

**Frontend**:
```bash
cd RuoYi-Vue/ruoyi-ui
npm install
npm run dev
```

**Code Generation** (fastest development path):
1. Design database table
2. Import table in code generator (System Tools -> Code Generation)
3. Configure generation info and generate code
4. Deploy to appropriate modules following the architecture rules above
5. Configure menu permissions

**Access Points**:
- Frontend: http://localhost:8111
- Backend: http://localhost:8080
- Default credentials: admin/admin123
- Swagger/Knife4j: http://localhost:8080/doc.html

## DO NOT MODIFY These Modules

- `ruoyi-framework` - Framework core, security, AOP
- `ruoyi-common` - Common utilities, annotations
- `ruoyi-system` - System management (user, role, menu, etc.)
- `ruoyi-generator` - Code generator

## Extension Points

- **Controllers**: `lf-admin/src/main/java/cn/lf/base/controller/` (backend management)
- **Business Logic**: Create new submodules in `lf-modules/src/main/java/cn/lf/modules/[domain]/`
- **OpenAPI**: `lf-base-service/src/main/java/cn/lf/base_service/controller/open_api/` (mini-program/H5)
- **Frontend Pages**: `ruoyi-ui/src/views/`
- **Tool Libraries**: `java-spring-tools/` for shared utilities

## Agent System

This project includes 19 specialized AI agents for different development tasks. Key agents:

**Core Development**:
- `product-requirements-analyst` - Requirements analysis and PRD creation
- `architecture-designer` - System architecture design
- `project-manager` - Task planning and management

**RuoYi-Specific**:
- `ruoyi-code-generator` - Code generation expert
- `ruoyi-backend-interface-engineer` - API interfaces + Forest HTTP client
- `ruoyi-frontend-developer` - Vue frontend development
- `ruoyi-data-engineer` - Database design
- `ruoyi-tool-developer` - java-spring-tools development
- `ruoyi-integration-tester` - Integration testing

**General Development**:
- `backend-developer` - General backend development
- `frontend-developer` - General frontend development
- `fullstack-developer` - Full-stack development
- `test-engineer` - Testing

See `README.md` for complete agent descriptions and workflow.

## Standard Development Workflow

1. **Requirements**: Use `product-requirements-analyst` to create PRD.md
2. **Database**: Use `ruoyi-data-engineer` for table design
3. **Code Generation**: Use `ruoyi-code-generator` (fastest) or manual development
4. **Backend**: Use `ruoyi-backend-interface-engineer` for APIs
5. **Frontend**: Use `ruoyi-frontend-developer` for Vue pages
6. **Testing**: Use `ruoyi-integration-tester` for integration testing

## Key Configuration Files

- **Backend Config**: `RuoYi-Vue/ruoyi-admin/src/main/resources/application.yml`
- **Datasource**: `RuoYi-Vue/ruoyi-admin/src/main/resources/application-druid.yml`
- **Frontend Config**: `RuoYi-Vue/ruoyi-ui/.env.development`
- **Vite Config**: `RuoYi-Vue/ruoyi-ui/vite.config.js`

## Multi-Endpoint Support

The project supports multiple endpoints:

1. **Management Backend** (default): Port 8080, JWT token via `Authorization` header
2. **OpenAPI Frontend** (`/open-api/` prefix): Independent JWT via `OPEN-API-TOKEN` header for mini-programs/H5

## Special Integration Features

**Forest HTTP Client**: Declarative HTTP client for third-party API integration with automatic JSON conversion, custom interceptors, timeout/retry handling

**WeChat Integration** (lf-wechat): Mini-program APIs, common WeChat APIs, access token management

**Payment Integration** (java-spring-tools/payment): WeChat Pay (JSAPI, Native, H5, APP), Alipay (APP, web, WAP)

## Important Architecture Documents

- `.ai-rules/module-package-structure.md` - **CRITICAL**: Module organization and package structure rules
- `.ai-rules/coding-standards.md` - Java and Vue coding standards
- `.ai-rules/project-context.md` - Complete project overview
- `docs/AI-DEVELOPMENT-GUIDE.md` - AI development manual with agent usage
- `ai_docs/Subagents.md` - Subagent creation and usage

## Backend Development Standards

**Permission Annotation**:
```java
@PreAuthorize("@ss.hasPermi('system:user:list')")
@GetMapping("/list")
public TableDataInfo list(SysUser user) {
    startPage();
    List<SysUser> list = userService.selectUserList(user);
    return getDataTable(list);
}
```

**Permission Identifier Format**: `system:module:operation` (e.g., `system:user:list`, `system:user:add`)

**Operation Logging**:
```java
@Log(title = "用户管理", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@RequestBody SysUser user) { }
```

**Data Permissions**:
```java
@DataScope(tableAlias = "u", userAlias = "su")
public List<SysUser> selectUserList(SysUser user)
```

## Frontend Development Standards

**API Calls**:
```javascript
// api/system/user.js
import request from '@/utils/request'

export function listUser(query) {
  return request({
    url: '/system/user/list',
    method: 'get',
    params: query
  })
}
```

**Permission Directives**:
```html
<!-- Single permission -->
<el-button v-hasPermi="['system:user:add']">Add</el-button>

<!-- Multiple permissions (OR logic) -->
<el-button v-hasPermi="['system:user:edit', 'system:user:remove']">Edit</el-button>

<!-- Role permission -->
<el-button v-hasRole="['admin']">Admin Button</el-button>
```

## Database Initialization

SQL scripts are in `RuoYi-Vue/sql/`:
- `ry_20230223.sql` - RuoYi framework initialization
- `lf_service.sql` - Business tables
- `quartz.sql` - Scheduled task tables

## Environment Variables

Required environment variables (see `.env.sample`):
- Database credentials in `application-druid.yml`
- Redis connection in `application.yml`
- Optional: API keys for external services (WeChat, payment gateways)
