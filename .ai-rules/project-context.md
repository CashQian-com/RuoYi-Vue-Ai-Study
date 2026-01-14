# RuoYi-Vue-Ai-Study 项目上下文

## 项目概述

**项目名称**: RuoYi-Vue-Ai-Study
**项目类型**: 基于RuoYi-Vue框架的AI辅助开发项目
**基础框架**: RuoYi-Vue 3.8.5（若依框架定制版）
**开发模式**: AI Agent协同开发

## 技术栈

### 后端技术栈
- **框架**: Spring Boot 2.7.10
- **ORM**: MyBatis-Plus 3.5.3
- **数据库**: MySQL 5.7+
- **缓存**: Redis 6.0+ + Caffeine（本地缓存）
- **安全**: Spring Security + JWT
- **API文档**: Swagger 3.0 / Knife4j
- **任务调度**: Quartz
- **HTTP客户端**: Forest 1.5.30
- **工具库**: Hutool 5.8.22, Lombok 1.18.26
- **JSON**: Jackson 2.13.5
- **验证**: Hibernate Validator

### 前端技术栈
- **框架**: Vue 3.2.45
- **UI组件**: Element Plus 2.2.27
- **状态管理**: Pinia 2.0.22
- **路由**: Vue Router 4.1.4
- **HTTP客户端**: Axios 0.27.2
- **构建工具**: Vite 3.2.3
- **图表**: ECharts 5.4.0
- **富文本**: @vueup/vue-quill 1.1.0

### 工具库
- **项目**: java-spring-tools 1.0.0
- **模块**:
  - common: 通用工具和分布式锁
  - base-forest: Forest HTTP客户端封装
  - validator: 自定义验证器
  - wechat: 微信SDK封装
  - payment: 支付服务（微信+支付宝）
  - message: 消息服务（短信+推送+微信）

## 项目结构

### 后端项目结构

```
RuoYi-Vue/
├── ruoyi-admin/          # 管理端入口模块
│   └── src/main/
│       ├── java/com/ruoyi/
│       │   ├── RuoYiApplication.java    # 启动类
│       │   └── web/controller/          # 控制器
│       │       ├── common/              # 公共接口（验证码、文件上传）
│       │       ├── monitor/             # 系统监控
│       │       └── system/              # 系统管理
│       └── resources/
│           ├── application.yml          # 主配置
│           ├── application-druid.yml    # 数据源配置
│           └── mapper/                  # MyBatis映射
│
├── ruoyi-framework/      # 框架核心模块（不可改动）
│   └── src/main/java/com/ruoyi/framework/
│       ├── config/                   # 配置类
│       │   ├── SecurityConfig        # 安全配置
│       │   ├── MybatisConfig         # MyBatis配置
│       │   ├── RedisConfig           # Redis配置
│       │   └── DruidConfig           # Druid数据源配置
│       ├── security/                 # 安全相关
│       │   ├── filter/               # JWT过滤器
│       │   ├── handle/               # 认证处理
│       │   └── context/              # 认证上下文
│       └── aspectj/                  # AOP切面
│           ├── LogAspect             # 日志切面
│           ├── DataScopeAspect       # 数据权限切面
│           └── DataSourceAspect      # 数据源切面
│
├── ruoyi-common/         # 通用工具模块（不可改动）
│   └── src/main/java/com/ruoyi/common/
│       ├── annotation/              # 注解定义
│       │   ├── Log                   # 操作日志
│       │   ├── Excel                 # Excel导出
│       │   ├── DataScope             # 数据权限
│       │   ├── RateLimiter           # 限流
│       │   └── RepeatSubmit          # 防重复提交
│       ├── core/                    # 核心类
│       │   ├── domain/               # 基础实体
│       │   ├── page/                 # 分页
│       │   └── text/                 # 响应结果
│       ├── utils/                   # 工具类
│       │   ├── SecurityUtils         # 安全工具
│       │   ├── ServletUtils          # Servlet工具
│       │   ├── StringUtils           # 字符串工具
│       │   ├── DateUtils             # 日期工具
│       │   └── file/                 # 文件工具
│       ├── enums/                   # 枚举
│       └── exception/               # 异常类
│
├── ruoyi-system/         # 系统管理模块（不可改动）
│   └── src/main/java/com/ruoyi/system/
│       ├── domain/                  # 实体类
│       │   ├── SysUser               # 用户
│       │   ├── SysRole               # 角色
│       │   ├── SysMenu               # 菜单
│       │   ├── SysDept               # 部门
│       │   ├── SysDictData           # 字典数据
│       │   ├── SysDictType           # 字典类型
│       │   ├── SysConfig             # 参数配置
│       │   ├── SysNotice             # 通知公告
│       │   └── SysPost               # 岗位
│       ├── mapper/                  # MyBatis Mapper
│       ├── service/                 # 业务接口
│       └── service/impl/            # 业务实现
│
├── ruoyi-generator/      # 代码生成器
│   └── src/main/
│       ├── java/com/ruoyi/generator/
│       │   ├── controller/          # 代码生成控制器
│       │   ├── domain/               # 生成表实体
│       │   ├── service/              # 生成服务
│       │   └── util/                 # 生成工具
│       └── resources/vm/            # 代码模板
│           ├── java/                 # Java模板
│           ├── xml/                  # MyBatis模板
│           └── vue/                  # Vue模板
│
├── ruoyi-quartz/         # 定时任务模块
│   └── src/main/java/com/ruoyi/quartz/
│       ├── config/                  # Quartz配置
│       ├── controller/              # 定时任务接口
│       ├── domain/                  # 定时任务实体
│       ├── service/                 # 定时任务服务
│       ├── task/                    # 定时任务执行类
│       └── util/                    # Cron表达式工具
│
├── lf-wechat/            # 微信服务模块
│   └── src/main/java/cn/lf/wechat/
│       ├── annotation/              # AccessToken注解
│       ├── api/                     # 微信API接口
│       │   ├── MiniProgramInterface # 小程序接口
│       │   └── WechatCommonInterface# 通用接口
│       ├── service/                 # 微信服务
│       ├── config/                  # Forest配置
│       ├── domain/                  # 实体类
│       └── utils/                   # 加密工具
│
├── lf-base-service/      # 业务服务模块（OpenAPI前台）
│   └── src/main/java/cn/lf/base_service/
│       ├── controller/              # 控制器
│       │   └── open_api/            # OpenAPI前台接口
│       │       ├── MiniProgamUserController    # 小程序用户
│       │       ├── CarouselController         # 轮播图
│       │       ├── OpenApiAgreementController # 协议
│       │       └── OpenApiOssController       # OSS
│       ├── service/                 # 业务服务
│       ├── domain/                  # 实体类
│       └── mapper/                  # Mapper
│
└── lf-base/              # 基础服务模块
    └── src/main/java/cn/lf/base/
        ├── annotation/              # 注解
        │   ├── OpenApiRepeatSubmit  # OpenAPI防重提交
        │   └── QueryParamsJackson    # Jackson参数序列化
        ├── common/                  # 工具类
        │   ├── CacheUtil            # 缓存工具
        │   ├── JacksonUtil          # JSON工具
        │   ├── FileUploadUtil       # 文件上传
        │   └── OpenAPISecurityUtils # OpenAPI安全
        ├── domain/                  # 实体类
        │   ├── LBaseEntity          # 基础实体
        │   ├── User                 # 用户
        │   ├── Attach               # 附件
        │   └── SysCarousel          # 轮播图
        ├── security/                # 安全
        │   └── filter/
        │       └── OpenApiJwtAuthenticationTokenFilter
        └── config/                  # 配置
            ├── JacksonConfig       # Jackson配置
            └── JetcacheConfig      # 多级缓存配置
```

### 前端项目结构

```
ruoyi-ui/                 # Vue 3管理端
├── src/
│   ├── api/              # API接口
│   │   ├── monitor/      # 监控接口
│   │   ├── service/      # 业务接口
│   │   ├── system/       # 系统接口
│   │   ├── tool/         # 工具接口
│   │   └── wechat/       # 微信接口
│   ├── assets/           # 静态资源
│   │   ├── icons/        # SVG图标
│   │   ├── images/       # 图片
│   │   ├── logo/         # Logo
│   │   └── styles/       # 全局样式
│   ├── components/       # 公共组件
│   │   ├── DictTag/      # 字典标签
│   │   ├── Editor/       # 富文本编辑器
│   │   ├── FileUpload/   # 文件上传
│   │   ├── ImageUpload/  # 图片上传
│   │   ├── Pagination/   # 分页
│   │   ├── RightToolbar/ # 右侧工具栏
│   │   ├── SvgIcon/      # SVG图标
│   │   └── TreeSelect/   # 树选择
│   ├── directive/        # 自定义指令
│   │   ├── permission/
│   │   │   ├── hasPermi.js    # 权限指令
│   │   │   └── hasRole.js     # 角色指令
│   │   └── common/
│   │       └── copyText.js    # 复制文本
│   ├── layout/           # 布局组件
│   │   ├── components/   # 布局子组件
│   │   │   ├── Navbar/    # 导航栏
│   │   │   ├── Sidebar/   # 侧边栏
│   │   │   ├── TagsView/  # 标签页
│   │   │   └── Settings/  # 设置
│   │   └── index.vue      # 主布局
│   ├── plugins/          # 插件
│   │   ├── cache.js      # 缓存插件
│   │   ├── modal.js      # 模态框
│   │   ├── download.js   # 下载插件
│   │   └── tab.js        # 标签页插件
│   ├── router/           # 路由
│   │   └── index.js      # 路由配置
│   ├── store/            # 状态管理（Pinia）
│   │   ├── modules/
│   │   │   ├── app.js         # 应用设置
│   │   │   ├── permission.js  # 权限
│   │   │   ├── settings.js    # 系统设置
│   │   │   ├── tagsView.js    # 标签页
│   │   │   └── user.js        # 用户信息
│   │   └── index.js
│   ├── utils/            # 工具函数
│   │   ├── request.js    # 请求封装
│   │   ├── auth.js       # 认证
│   │   ├── permission.js # 权限
│   │   ├── dict.js       # 字典
│   │   ├── validate.js   # 验证
│   │   └── ruoyi.js      # 若依工具
│   ├── views/            # 页面视图
│   │   ├── login/        # 登录页
│   │   ├── index/        # 首页
│   │   ├── monitor/      # 系统监控
│   │   │   ├── operlog/  # 操作日志
│   │   │   ├── logininfor/# 登录日志
│   │   │   ├── online/   # 在线用户
│   │   │   ├── server/   # 服务器监控
│   │   │   └── cache/    # 缓存监控
│   │   ├── system/       # 系统管理
│   │   │   ├── user/     # 用户管理
│   │   │   ├── role/     # 角色管理
│   │   │   ├── menu/     # 菜单管理
│   │   │   ├── dept/     # 部门管理
│   │   │   ├── post/     # 岗位管理
│   │   │   ├── dict/     # 字典管理
│   │   │   ├── config/   # 参数设置
│   │   │   └── notice/   # 通知公告
│   │   ├── service/      # 业务管理
│   │   │   ├── user/     # 用户管理
│   │   │   ├── agreement/# 协议管理
│   │   │   ├── carousel/ # 轮播图管理
│   │   │   └── oss/      # OSS管理
│   │   ├── tool/         # 系统工具
│   │   │   └── gen/      # 代码生成
│   │   └── wechat/       # 微信管理
│   │       └── wechat_app_config/
│   ├── App.vue           # 根组件
│   ├── main.js           # 入口文件
│   └── permission.js     # 权限控制
├── vite/                 # Vite配置
│   └── plugins/
│       ├── auto-import.js     # 自动导入
│       ├── compression.js     # 压缩
│       ├── icon.js            # 图标
│       └── setup-extend.js    # setup扩展
├── vite.config.js        # Vite配置
├── package.json
└── .env.development       # 环境变量
```

## 数据库设计

### 核心表结构

**用户权限表**:
- `sys_user`: 用户表
- `sys_role`: 角色表
- `sys_menu`: 菜单表
- `sys_dept`: 部门表
- `sys_user_role`: 用户角色关联表
- `sys_role_menu`: 角色菜单关联表

**业务表** (lf_service.sql):
- `user`: 用户表（小程序用户）
- `wechat_app_config`: 微信应用配置
- `sys_carousel`: 轮播图
- `sys_agreement`: 协议
- `sys_oss`: OSS配置
- `attach`: 附件表

### 数据库脚本位置

```
sql/
├── ry_20230223.sql      # RuoYi初始化脚本
├── lf_service.sql       # 业务表脚本
└── quartz.sql           # 定时任务脚本
```

## 开发规范

### ⚠️ 模块包结构规范（重要）

**详见**: `.ai-rules/module-package-structure.md`

**核心架构**（基于实际项目ydcx-admin）:
```
项目结构
├── lf-base              # 基础模块（通用基础类）
├── lf-modules           # 业务模块容器（按业务领域划分子模块）
│   └── cn.lf.modules.*, cn.ynlky.modules.*
├── lf-admin             # 后台管理Controller模块
├── lf-open-api          # 开放API模块（前台接口）
└── ruoyi-*              # 若依框架模块
```

**关键规则**:
1. **Controller**: 必须放在 `lf-admin` 模块的 `cn.lf.base.controller` 包下
2. **Domain/Mapper/Service**: 必须放在 `lf-modules` 模块的业务子模块中（如 `cn.lf.modules.ai`）
3. **按业务领域划分子模块**: 如 `cn.lf.modules.ai`、`cn.ynlky.modules.ydcx_user`
4. **包名必须与文件路径严格匹配**

**跨模块引用规则**:
```java
// lf-admin/controller (引用 lf-modules)
import cn.lf.modules.ai.domain.AiModel;           // ✅ 引用lf-modules的domain
import cn.lf.modules.ai.service.IAiModelService;  // ✅ 引用lf-modules的service接口

// lf-modules/service/impl (实现 lf-modules)
import cn.lf.modules.ai.domain.AiModel;           // ✅ 同模块domain
import cn.lf.modules.ai.mapper.AiModelMapper;     // ✅ 同模块mapper
import cn.lf.base.domain.LBaseEntity;             // ✅ 引用lf-base的基础类

// lf-modules/mapper (引用 lf-modules + lf-base)
import cn.lf.modules.ai.domain.AiModel;           // ✅ 同模块domain
import cn.lf.base.domain.LBaseEntity;             // ✅ 引用lf-base的基础类
```

**❌ 常见错误**:
- 将Controller放在 `lf-modules` 模块（应该在lf-admin）
- 将Domain/Service放在 `lf-base` 模块（应该在lf-modules的业务子模块）
- 包名与文件路径不匹配

### 代码分层规范

**后端分层**:
1. **Controller层**: 接口控制层（在lf-admin模块）
   - 系统管理: `ruoyi-admin/web/controller/system/` (若依系统管理)
   - 业务管理: `lf-admin/src/main/java/cn/lf/base/controller/` (后台业务管理)
   - OpenAPI前台: `lf-open-api/src/main/java/cn/lf/open_api/controller/` (小程序/H5前台)

2. **Service层**: 业务逻辑层（在lf-modules模块）
   - 按业务子模块划分: `lf-modules/src/main/java/cn/lf/modules/[业务名]/service/`
   - 接口: `I[Entity]Service.java`
   - 实现: `impl/[Entity]ServiceImpl.java`

3. **Mapper层**: 数据访问层（在lf-modules模块）
   - 接口: `lf-modules/src/main/java/cn/lf/modules/[业务名]/mapper/[Entity]Mapper.java`
   - XML: `lf-modules/src/main/resources/mapper/[Entity]Mapper.xml`

4. **Entity层**: 实体类（在lf-modules模块）
   - 业务实体: `lf-modules/src/main/java/cn/lf/modules/[业务名]/domain/[Entity].java`
   - 基础实体继承: `LBaseEntity` (lf-base) 或 `BaseEntity` (ruoyi-common)

**示例：AI模型管理模块**
```
lf-modules/src/main/java/cn/lf/modules/ai/
├── domain/AiModel.java              # 实体类
├── mapper/AiModelMapper.java         # Mapper接口
├── service/IAiModelService.java      # Service接口
└── service/impl/AiModelServiceImpl.java  # Service实现

lf-admin/src/main/java/cn/lf/base/controller/
└── AiModelController.java            # Controller
```

### 接口开发规范

**Controller规范**:
```java
@RestController
@RequestMapping("/system/user")
public class SysUserController extends BaseController {

    @Autowired
    private ISysUserService userService;

    /**
     * 查询用户列表
     */
    @PreAuthorize("@ss.hasPermi('system:user:list')")
    @GetMapping("/list")
    public TableDataInfo list(SysUser user) {
        startPage();
        List<SysUser> list = userService.selectUserList(user);
        return getDataTable(list);
    }

    /**
     * 获取用户详细信息
     */
    @PreAuthorize("@ss.hasPermi('system:user:query')")
    @GetMapping(value = "/{userId}")
    public AjaxResult getInfo(@PathVariable("userId") Long userId) {
        return success(userService.selectUserById(userId));
    }
}
```

**权限标识规范**:
```
系统:模块:操作

示例：
- system:user:list        # 用户列表
- system:user:add         # 新增用户
- system:user:edit        # 修改用户
- system:user:remove      # 删除用户
```

### 前端开发规范

**API调用规范**:
```javascript
// api/system/user.js
import request from '@/utils/request'

// 查询用户列表
export function listUser(query) {
  return request({
    url: '/system/user/list',
    method: 'get',
    params: query
  })
}
```

**权限指令使用**:
```html
<!-- 单个权限 -->
<el-button v-hasPermi="['system:user:add']">新增</el-button>

<!-- 多个权限（满足其一即可） -->
<el-button v-hasPermi="['system:user:edit', 'system:user:remove']">
  操作
</el-button>

<!-- 角色权限 -->
<el-button v-hasRole="['admin']">管理员按钮</el-button>
```

## 关键路径

### 后端关键路径
- 启动类: `RuoYi-Vue/ruoyi-admin/src/main/java/com/ruoyi/RuoYiApplication.java`
- 配置文件: `RuoYi-Vue/ruoyi-admin/src/main/resources/application.yml`
- 系统管理: `RuoYi-Vue/ruoyi-system/`
- 业务服务: `RuoYi-Vue/lf-base-service/`
- OpenAPI: `RuoYi-Vue/lf-base-service/src/main/java/cn/lf/base_service/controller/open_api/`
- 代码生成: `RuoYi-Vue/ruoyi-generator/`
- SQL脚本: `RuoYi-Vue/sql/`

### 前端关键路径
- 主入口: `RuoYi-Vue/ruoyi-ui/src/main.js`
- 路由配置: `RuoYi-Vue/ruoyi-ui/src/router/index.js`
- API接口: `RuoYi-Vue/ruoyi-ui/src/api/`
- 页面视图: `RuoYi-Vue/ruoyi-ui/src/views/`
- 公共组件: `RuoYi-Vue/ruoyi-ui/src/components/`

## 多端扩展

### 已支持的端

1. **管理端**: 后台管理系统
   - 路径前缀: 无（默认）
   - 认证方式: JWT Token (`Authorization` header)
   - 权限控制: 基于角色的菜单权限

2. **OpenAPI前台**: 小程序/H5前台接口
   - 路径前缀: `/open-api/`
   - 认证方式: 独立JWT Token (`OPEN-API-TOKEN` header)
   - 权限控制: 基于用户的简单认证
   - 接口示例:
     - `/open-api/mini-program-user/login` - 登录
     - `/open-api/mini-program-user/getInfo` - 获取用户信息

### 扩展新端

创建新端步骤：
1. 创建新Maven模块（如 `lf-merchant`）
2. 配置独立的Token认证
3. 创建Controller接口
4. 在父pom.xml中添加模块
5. 在ruoyi-admin中添加依赖

## 开发流程

### 使用代码生成器快速开发

1. **创建数据库表**: 设计表结构
2. **导入表结构**: 登录系统 -> 系统工具 -> 代码生成 -> 导入
3. **配置生成信息**: 编辑基本信息、字段信息
4. **生成代码**: 点击"生成代码"下载ZIP
5. **部署代码**: 将生成的代码放入对应目录
6. **配置菜单**: 执行菜单SQL，配置权限

### 手动开发新功能

1. **创建数据表**: 编写建表SQL
2. **创建实体类**: 继承 `LBaseEntity` 或 `BaseEntity`
3. **创建Mapper**: 继承 `BaseMapper<Entity>`
4. **创建Service**: 继承 `IService<Entity>`
5. **创建Controller**: 添加权限注解
6. **创建前端API**: 定义接口方法
7. **创建前端页面**: 使用Element Plus组件
8. **配置菜单权限**: 添加菜单和按钮权限

## Agent使用建议

### 按任务类型选择Agent

| 任务类型 | 推荐Agent |
|---------|----------|
| 代码生成 | ruoyi-code-generator |
| 系统管理功能 | backend-developer + frontend-developer |
| OpenAPI接口 | ruoyi-backend-interface-engineer |
| 微信功能 | ruoyi-backend-interface-engineer + ruoyi-tool-developer |
| 工具库扩展 | ruoyi-tool-developer |
| 数据库设计 | ruoyi-data-engineer |
| 测试 | test-engineer |

### Agent协同模式

**新功能开发协同**:
```
需求分析 → 数据库设计 → 代码生成 → 后端调整 → 前端开发 → 测试验证
   ↓         ↓         ↓         ↓         ↓         ↓
PRA.md → data-engineer → code-gen → backend → frontend → testing
```

## 项目约束

### 不可改动的模块
- ruoyi-framework（框架核心）
- ruoyi-common（通用工具）
- ruoyi-system（系统模块）
- ruoyi-generator（代码生成器）

### 可扩展的位置
- 业务模块: `lf-base-service/` 或创建新模块
- 控制层接口: `ruoyi-admin/web/controller/`
- 前端页面: `ruoyi-ui/src/views/`
- OpenAPI接口: `lf-base-service/controller/open_api/`

## 配置说明

### 后端配置

**主配置** (`application.yml`):
- 服务器端口: 8080
- 数据库: MySQL (Druid连接池)
- Redis: localhost:6379
- Token配置: JWT有效期30天
- OpenAPI Token: 独立配置

**数据源配置** (`application-druid.yml`):
- 主数据库: ruoyi
- 从数据库: 可配置
- Druid监控: /druid/

### 前端配置

**开发环境** (`.env.development`):
- API地址: /dev-api
- 代理目标: http://localhost:8080

**Vite配置** (`vite.config.js`):
- 开发服务器端口: 8111
- 代理配置: /dev-api -> http://localhost:8080
