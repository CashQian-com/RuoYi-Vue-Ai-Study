# RuoYi-Vue-Ai-Study AI开发使用手册

## 目录

1. [快速开始](#快速开始)
2. [项目概述](#项目概述)
3. [Agent使用指南](#agent使用指南)
4. [开发流程](#开发流程)
5. [常见场景](#常见场景)
6. [最佳实践](#最佳实践)
7. [问题排查](#问题排查)

---

## 快速开始

### 前置要求

- **Claude Code**: 已安装并配置
- **JDK**: 1.8+
- **Node.js**: 16+
- **MySQL**: 5.7+
- **Redis**: 6.0+

### 环境准备

1. **克隆项目**
```bash
git clone https://gitee.com/myaccountl/RuoYi-Vue.git
git clone https://gitee.com/myaccountl/java-spring-tools.git
```

2. **配置数据库**
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE ruoyi CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

# 导入SQL脚本
mysql -u root -p ruoyi < sql/ry_20230223.sql
mysql -u root -p ruoyi < sql/lf_service.sql
```

3. **配置后端**
```yaml
# RuoYi-Vue/ruoyi-admin/src/main/resources/application-druid.yml
spring:
  datasource:
    druid:
      master:
        url: jdbc:mysql://localhost:3306/ruoyi?useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
        username: root
        password: your_password
```

4. **配置前端**
```bash
cd RuoYi-Vue/ruoyi-ui
npm install
npm run dev
```

5. **启动项目**
```bash
# 后端
cd RuoYi-Vue
mvn clean install
mvn spring-boot:run -pl ruoyi-admin

# 前端（新终端）
cd RuoYi-Vue/ruoyi-ui
npm run dev
```

6. **访问系统**
- 前端地址: http://localhost:8111
- 默认账号: admin
- 默认密码: admin123

---

## 项目概述

### 技术架构

**后端技术栈**:
- Spring Boot 2.7.10
- MyBatis-Plus 3.5.3
- Spring Security + JWT
- Redis + Caffeine
- Forest 1.5.30
- Swagger 3.0

**前端技术栈**:
- Vue 3.2.45
- Element Plus 2.2.27
- Pinia 2.0.22
- Vite 3.2.3

**工具库**:
- java-spring-tools 1.0.0
  - common: 通用工具和分布式锁
  - base-forest: Forest HTTP客户端封装
  - validator: 自定义验证器
  - wechat: 微信SDK封装
  - payment: 支付服务（微信+支付宝）
  - message: 消息服务（短信+推送+微信）

### 项目结构

```
RuoYi-Vue/
├── ruoyi-admin/          # 管理端入口
├── ruoyi-framework/      # 框架核心（不可改动）
├── ruoyi-common/         # 通用工具（不可改动）
├── ruoyi-system/         # 系统管理（不可改动）
├── ruoyi-generator/      # 代码生成器
├── ruoyi-quartz/         # 定时任务
├── lf-wechat/            # 微信服务
├── lf-base-service/      # 业务服务（OpenAPI前台）
├── lf-base/              # 基础服务
├── ruoyi-ui/             # Vue 3管理端
└── sql/                  # 数据库脚本
```

### 多端支持

1. **管理端**: 后台管理系统（默认端口8080）
2. **OpenAPI前台**: 小程序/H5前台接口（路径前缀 `/open-api/`）

---

## Agent使用指南

### Agent列表

| Agent | 用途 | 适用场景 |
|-------|------|---------|
| `ruoyi-code-generator` | 代码生成 | 使用RuoYi代码生成器生成CRUD代码 |
| `ruoyi-backend-interface-engineer` | 接口开发 | OpenAPI接口、Forest接口、支付接口 |
| `ruoyi-frontend-developer` | 前端开发 | ruoyi-ui页面开发 |
| `ruoyi-tool-developer` | 工具开发 | java-spring-tools工具库扩展 |
| `ruoyi-data-engineer` | 数据库设计 | 表结构设计、数据层开发 |
| `ruoyi-unipapp-developer` | 小程序开发 | UniApp小程序开发 |
| `ruoyi-integration-tester` | 集成测试 | 接口测试、前后端联调 |
| `ruoyi-system-architect` | 架构设计 | 系统架构设计、技术选型 |
| `backend-developer` | 后端开发 | 通用后端开发 |
| `frontend-developer` | 前端开发 | 通用前端开发 |
| `test-engineer` | 测试 | 单元测试、集成测试 |

### 使用示例

#### 1. 使用代码生成器

```bash
# 调用代码生成Agent
请使用 ruoyi-code-generator Agent 为AI模型管理功能生成代码。

功能需求:
- 模型名称
- 模型地址
- API密钥
- 到期时间
- 状态（0正常 1停用）

数据库表名: ai_model
生成位置: lf-base-service
```

#### 2. OpenAPI接口开发

```bash
# 调用接口开发Agent
请使用 ruoyi-backend-interface-engineer Agent 开发用户信息查询接口。

接口路径: /open-api/user/info
请求方式: GET
返回字段: 用户ID、昵称、头像、手机号

需要使用 @Anonymous 注解允许匿名访问
```

#### 3. 前端页面开发

```bash
# 调用前端开发Agent
请使用 ruoyi-frontend-developer Agent 开发AI模型管理页面。

功能需求:
- 列表展示（模型名称、状态、到期时间）
- 新增/编辑对话框
- 删除确认
- 状态切换

使用Element Plus组件，遵循RuoYi前端规范
```

---

## 开发流程

### 标准开发流程

#### 阶段1: 需求分析

使用 `product-requirements-analyst` Agent:
```markdown
请分析以下需求并生成PRD文档:

需求: AI模型管理功能
- 管理AI模型的配置信息
- 包括模型名称、地址、密钥、到期时间
- 支持新增、编辑、删除、查询
- 需要记录操作日志
```

#### 阶段2: 数据库设计

使用 `ruoyi-data-engineer` Agent:
```markdown
请为AI模型管理功能设计数据库表。

功能需求:
- 模型名称（varchar 100）
- 模型地址（varchar 500）
- API密钥（varchar 200）
- 到期时间（datetime）
- 状态（char 1，0正常1停用）

遵循RuoYi数据库设计规范，包含基础字段
```

#### 阶段3: 代码生成

使用 `ruoyi-code-generator` Agent:
```markdown
请使用RuoYi代码生成器为AI模型管理功能生成代码。

表名: ai_model
模块名: ai-model
包名: cn.lf.base_service
业务名: aiModel
功能名: AI模型管理

生成类型: 单表（crud）
```

#### 阶段4: 后端开发

使用 `backend-developer` 或 `ruoyi-backend-interface-engineer` Agent:
```markdown
请调整AI模型管理的后端代码。

需要调整:
1. Service层业务逻辑
2. 添加数据验证
3. 添加操作日志记录
4. 实现状态切换功能
```

#### 阶段5: 前端开发

使用 `frontend-developer` 或 `ruoyi-frontend-developer` Agent:
```markdown
请调整AI模型管理的前端页面。

需要调整:
1. 页面布局优化
2. 添加表单验证
3. 实现状态切换按钮
4. 添加操作权限控制
```

#### 阶段6: 测试验证

使用 `test-engineer` 或 `ruoyi-integration-tester` Agent:
```markdown
请对AI模型管理功能进行集成测试。

测试内容:
- 接口功能测试
- 前后端联调测试
- 权限控制测试
- 数据验证测试
```

### 快速开发流程（使用代码生成器）

```
数据库设计 → 导入表结构 → 配置生成信息 → 生成代码 → 部署代码 → 配置菜单
     ↓             ↓              ↓            ↓          ↓          ↓
  设计SQL      代码生成器      编辑配置      下载ZIP     放入项目    执行SQL
```

**详细步骤**:

1. **设计数据库表**
```sql
CREATE TABLE `ai_model` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `model_name` varchar(100) NOT NULL COMMENT '模型名称',
  `model_address` varchar(500) NOT NULL COMMENT '模型地址',
  `model_key` varchar(200) NOT NULL COMMENT 'API密钥',
  `expire_time` datetime DEFAULT NULL COMMENT '到期时间',
  `status` char(1) DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI模型管理表';
```

2. **登录系统导入表**
- 访问: http://localhost:8111
- 导航: 系统工具 -> 代码生成 -> 导入
- 选择: ai_model 表

3. **配置生成信息**
```
基本信息:
- 表名称: ai_model
- 表描述: AI模型管理表
- 功能名称: AI模型
- 功能作者: YourName
- 包名: cn.lf.base_service
- 模块名: base-service
- 业务名: aiModel
- 生成路径: /lf-base-service

字段信息:
- model_name: 列表、查询、必填
- model_address: 列表、必填
- model_key: 列表、密码类型
- expire_time: 列表、日期范围
- status: 列表、查询、下拉框
```

4. **生成代码**
- 点击"生成代码"
- 下载ZIP包
- 解压得到前后端代码

5. **部署代码**
```bash
# 后端代码
cd RuoYi-Vue
# Java文件放入对应目录
# Mapper.xml放入 lf-base-service/src/main/resources/mapper/

# 前端代码
cd ruoyi-ui
# Vue文件放入 src/views/service/ai-model/
# API文件放入 src/api/service/
```

6. **配置菜单权限**
```sql
-- 执行生成的menu.sql
-- 或者手动添加菜单: 系统管理 -> 菜单管理 -> 新增
```

---

## 常见场景

### 场景1: 开发OpenAPI接口

**需求**: 开发一个获取轮播图的OpenAPI接口

**步骤**:

1. **创建数据库表**
```sql
CREATE TABLE `sys_carousel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '标题',
  `image_url` varchar(512) NOT NULL COMMENT '图片URL',
  `link_url` varchar(512) DEFAULT NULL COMMENT '链接URL',
  `sort` int(11) DEFAULT '0' NOT NULL COMMENT '排序',
  `status` char(1) DEFAULT '0' COMMENT '状态（0正常 1关闭）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='轮播图表';
```

2. **创建Controller**
```java
package cn.lf.base_service.controller.open_api;

@Api(tags = "OpenAPI-轮播图")
@RestController
@RequestMapping(Constants.OPEN_API + "/carousel")
public class CarouselController {

    @Autowired
    private ISysCarouselService carouselService;

    @ApiOperation(value = "轮播图列表")
    @GetMapping("/list")
    @Anonymous  // 允许匿名访问
    public AjaxResult list() {
        List<SysCarousel> list = carouselService.selectCarouselList(new SysCarousel());
        return AjaxResult.success(list);
    }
}
```

3. **测试接口**
```bash
curl http://localhost:8080/open-api/carousel/list
```

### 场景2: 使用Forest对接微信接口

**需求**: 对接微信小程序登录接口

**步骤**:

1. **配置Forest**
```java
@Configuration
public class WechatForestConfiguration {

    @Bean
    public MiniProgramInterface miniProgramInterface() {
        return ForestClient.client(MiniProgramInterface.class);
    }
}
```

2. **定义接口**
```java
@BaseRequest(baseURL = "${wechat.apiDomain}")
public interface MiniProgramInterface {

    @Get("/sns/jscode2session")
    @QueryParamsJackson
    MiniProgramLoginVO jsCodeToSession(@Query MiniProgramLoginDTO dto);
}
```

3. **调用接口**
```java
@Service
public class WechatLoginService {

    @Autowired
    private MiniProgramInterface miniProgramInterface;

    public UserVO login(String code) {
        MiniProgramLoginDTO dto = new MiniProgramLoginDTO();
        dto.setAppId(appid);
        dto.setSecret(secret);
        dto.setJsCode(code);

        MiniProgramLoginVO result = miniProgramInterface.jsCodeToSession(dto);

        // 处理登录逻辑
        return userLogin(result);
    }
}
```

### 场景3: 添加数据权限

**需求**: 某个查询只能查看本部门的数据

**步骤**:

1. **在Mapper方法上添加注解**
```java
@DataScope(deptAlias = "d", userAlias = "u")
public List<SysUser> selectUserList(SysUser user);
```

2. **数据权限自动生效**
- 管理员: 查看全部数据
- 部门领导: 查看本部门及下级部门数据
- 普通用户: 只查看本人数据

### 场景4: 添加操作日志

**步骤**:

1. **在Controller方法上添加注解**
```java
@Log(title = "用户管理", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@RequestBody SysUser user) {
    return toAjax(userService.insertUser(user));
}
```

2. **日志自动记录**
- 操作人
- 操作时间
- 操作类型
- 请求参数
- 返回结果

### 场景5: 添加Excel导出

**步骤**:

1. **在实体类上添加注解**
```java
@Excel(name = "用户表")
public class SysUser extends BaseEntity {

    @Excel(name = "用户编号", cellType = ColumnType.NUMERIC)
    private Long userId;

    @Excel(name = "用户名称")
    private String userName;

    @Excel(name = "手机号码")
    private String phonenumber;
}
```

2. **在Controller添加导出方法**
```java
@Log(title = "用户管理", businessType = BusinessType.EXPORT)
@PreAuthorize("@ss.hasPermi('system:user:export')")
@PostMapping("/export")
public void export(HttpServletResponse response, SysUser user) {
    List<SysUser> list = userService.selectUserList(user);
    ExcelUtil<SysUser> util = new ExcelUtil<SysUser>(SysUser.class);
    util.exportExcel(response, list, "用户数据");
}
```

---

## 最佳实践

### 1. 命名规范

**包命名**:
```
com.ruoyi.模块名
├── controller       # 控制器
├── service          # 服务接口
├── service/impl     # 服务实现
├── mapper           # MyBatis Mapper
└── domain           # 实体类
```

**类命名**:
- Controller: `XxxController`
- Service接口: `IXxxService`
- Service实现: `XxxServiceImpl`
- Mapper: `XxxMapper`
- 实体类: `Xxx` 或 `SysXxx`

**方法命名**:
- 查询列表: `selectXxxList`
- 根据ID查询: `selectXxxById`
- 新增: `insertXxx`
- 修改: `updateXxx`
- 删除: `deleteXxxById`

### 2. 权限标识规范

```
系统:模块:操作

示例:
- system:user:list        # 用户列表
- system:user:add         # 新增用户
- system:user:edit        # 修改用户
- system:user:remove      # 删除用户
- system:user:export      # 导出用户
- system:user:import      # 导入用户
```

### 3. 前后端分离规范

**后端返回格式**:
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

**前端调用规范**:
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

### 4. 代码注释规范

**类注释**:
```java
/**
 * 用户信息
 *
 * @author ruoyi
 */
public class SysUser extends BaseEntity {
    // ...
}
```

**方法注释**:
```java
/**
 * 查询用户列表
 *
 * @param user 用户信息
 * @return 用户集合
 */
public List<SysUser> selectUserList(SysUser user) {
    // ...
}
```

### 5. 异常处理规范

**业务异常**:
```java
// 抛出业务异常
throw new ServiceException("用户名已存在");

// 带错误码
throw new ServiceException("USER_NOT_EXIST", "用户不存在");
```

**全局异常处理**:
- 已在 `ruoyi-framework` 中配置
- 自动捕获并返回友好提示

---

## 问题排查

### 常见问题

#### 1. 启动失败

**问题**: `Failed to configure a DataSource`

**解决**:
```yaml
# 检查 application-druid.yml 配置
spring:
  datasource:
    druid:
      master:
        url: jdbc:mysql://localhost:3306/ruoyi
        username: root
        password: your_password
```

#### 2. 前端跨域问题

**问题**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**解决**:
```javascript
// vite.config.js 已配置代理
server: {
  proxy: {
    '/dev-api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
      rewrite: (p) => p.replace(/^\/dev-api/, '')
    }
  }
}
```

#### 3. 权限不生效

**问题**: 添加了 `@PreAuthorize` 但权限不生效

**解决**:
1. 确认菜单权限已配置
2. 确认角色已分配菜单权限
3. 刷新Token重新登录

#### 4. 代码生成后404

**问题**: 生成的Controller访问404

**解决**:
1. 检查 `@RequestMapping` 路径
2. 确认类已在启动类扫描包下
3. 检查父pom.xml是否引入模块

#### 5. 前端页面空白

**问题**: 访问页面后空白

**解决**:
1. 打开浏览器控制台查看错误
2. 检查API接口是否返回数据
3. 检查路由配置是否正确

### 调试技巧

#### 1. 后端调试

**启用日志**:
```yaml
# application.yml
logging:
  level:
    com.ruoyi: debug
    cn.lf: debug
```

**Druid监控**:
- 访问: http://localhost:8080/druid/
- 用户名: ruoyi
- 密码: 123456

#### 2. 前端调试

**Vue DevTools**:
- 安装Vue DevTools浏览器扩展
- 查看组件状态
- 查看Pinia状态

**Network**:
- 查看API请求
- 查看请求参数
- 查看响应数据

---

## 附录

### A. 快捷命令

```bash
# 后端启动
mvn clean install
mvn spring-boot:run -pl ruoyi-admin

# 前端启动
cd ruoyi-ui
npm install
npm run dev
npm run build

# 代码格式化
mvn spotless:apply

# 跳过测试
mvn clean install -DskipTests
```

### B. 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端 | 8080 | Spring Boot |
| 前端 | 8111 | Vite开发服务器 |
| MySQL | 3306 | 数据库 |
| Redis | 6379 | 缓存 |
| Druid | 8080/druid | 数据源监控 |

### C. 相关资源

- [RuoYi-Vue官方文档](http://doc.ruoyi.vip/)
- [Vue 3文档](https://cn.vuejs.org/)
- [Element Plus文档](https://element-plus.org/)
- [MyBatis-Plus文档](https://baomidou.com/)
- [Spring Boot文档](https://spring.io/projects/spring-boot)

---

**手册版本**: 1.0.0
**更新日期**: 2024-01-14
**维护者**: AI Agent Team
