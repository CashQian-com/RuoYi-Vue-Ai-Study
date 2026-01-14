# RuoYi-Vue 模块包结构规范（正确版本）

## 核心架构

基于实际项目的正确模块组织方式：

```
项目结构
├── lf-base              # 基础模块（通用基础类）
├── lf-modules           # 业务模块容器（新增）
│   └── 按业务领域划分子模块
├── lf-admin             # 后台管理Controller模块
├── lf-open-api          # 开放API模块（前台接口）
└── ruoyi-*              # 若依框架模块
```

## 模块职责划分

### 1. lf-base 模块（基础模块）

**包路径**: `cn.lf.base.*`

**职责**: 存放跨业务模块共享的基础类

**包结构**:
```
lf-base/
└── src/main/java/cn/lf/base/
    ├── annotation/          # 注解定义
    ├── common/              # 通用工具类
    ├── config/              # 配置类
    ├── domain/              # 基础实体类（LBaseEntity等）
    └── security/            # 安全相关
```

### 2. lf-modules 模块（业务模块容器）

**包路径**: `cn.lf.modules.*` 或 `cn.ynlky.modules.*`

**职责**: 存放所有业务逻辑的domain、mapper、service（**不包含Controller**）

**重要**: Controller不在lf-modules中，Controller在独立的lf-admin模块中

#### 子模块组织方式

按业务领域划分，每个子模块是独立的业务单元：

```
lf-modules/
└── src/main/java/
    ├── cn/lf/modules/base/              # 基础业务模块
    │   ├── domain/                      # 实体类
    │   ├── dto/                         # 数据传输对象
    │   ├── mapper/                      # Mapper接口
    │   ├── service/                     # Service接口
    │   │   └── impl/                    # Service实现
    │   ├── validation/                  # 验证器
    │   ├── config/                      # 配置
    │   └── common/                      # 通用类
    │
    └── cn/ynlky/modules/                # 具体业务模块
        ├── ydcx_user/                   # 用户业务
        │   ├── domain/
        │   │   ├── entity/              # 实体类
        │   │   ├── dto/                 # 数据传输对象
        │   │   └── vo/                  # 视图对象
        │   ├── mapper/
        │   ├── service/
        │   │   └── impl/
        │   └── support/                 # 支撑类
        │
        ├── ydcx_order/                  # 订单业务
        ├── ydcx_product/                # 产品业务
        ├── ydcx_finance/                # 财务业务
        ├── payment/                     # 支付业务
        ├── wechat/                      # 微信业务
        └── ...                          # 其他业务模块
```

### 3. lf-admin 模块（后台管理Controller模块）

**包路径**: `cn.lf.base.controller.*` 或按业务划分

**职责**: 存放所有后台管理的Controller

**包结构**:
```
lf-admin/
└── src/main/java/cn/lf/base/controller/
    ├── AttachController.java
    ├── SysAgreementController.java
    ├── SysCarouselController.java
    ├── SysOssController.java
    └── ...                             # 其他Controller
```

**Controller示例**:
```java
package cn.lf.base.controller;

import cn.lf.modules.base.domain.SysCarousel;           // ✅ 引用lf-modules的domain
import cn.lf.modules.base.service.ISysCarouselService;  // ✅ 引用lf-modules的service
import com.ruoyi.common.core.controller.BaseController;

@RestController
@RequestMapping("/service/carousel")
public class SysCarouselController extends BaseController {

    @Resource
    private ISysCarouselService sysCarouselService;      // ✅ 注入lf-modules的service
}
```

### 4. lf-open-api 模块（开放API模块）

**包路径**: `cn.lf.open_api.controller.*` 和 `cn.ynlky.open_api.controller.*`

**职责**: 存放小程序/H5前台的API接口

**包结构**:
```
lf-open-api/
└── src/main/java/
    ├── cn/lf/open_api/controller/           # 基础OpenAPI
    │   ├── CarouselController.java
    │   ├── MiniProgamUserController.java
    │   └── ...
    └── cn/ynlky/open_api/controller/        # 业务OpenAPI
        ├── OpenApiAccountController.java
        ├── OpenApiAuthController.java
        └── ...
```

## 跨模块引用规则

### 引用关系图

```
┌─────────────────────────────────────────────────────────┐
│                    lf-admin                             │
│                  (后台管理Controller)                    │
│            依赖: lf-modules, ruoyi-common              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ 依赖
                        ↓
┌─────────────────────────────────────────────────────────┐
│                  lf-modules                             │
│                (业务模块容器)                             │
│         依赖: lf-base, ruoyi-common                    │
│                                                           │
│  cn.lf.modules.base (domain + mapper + service)         │
│  cn.ynlky.modules.* (各业务子模块)                       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ 依赖
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    lf-base                              │
│                  (基础模块)                              │
│         依赖: ruoyi-common, java-spring-tools          │
│                                                           │
│  cn.lf.base.domain (基础实体类)                          │
│  cn.lf.base.config (配置类)                              │
└─────────────────────────────────────────────────────────┘
```

### 正确的import示例

#### Controller层（lf-admin模块）

```java
package cn.lf.base.controller;  // ✅ 在lf-admin模块

import cn.lf.modules.base.domain.SysCarousel;           // ✅ 引用lf-modules的domain
import cn.lf.modules.base.service.ISysCarouselService;  // ✅ 引用lf-modules的service
import com.ruoyi.common.core.controller.BaseController;  // ✅ 引用ruoyi-common

@RestController
@RequestMapping("/service/carousel")
public class SysCarouselController extends BaseController {

    @Resource
    private ISysCarouselService sysCarouselService;  // ✅ lf-modules的service
}
```

#### Service实现层（lf-modules模块）

```java
package cn.lf.modules.base.service.impl;  // ✅ 在lf-modules模块

import cn.lf.modules.base.domain.SysCarousel;           // ✅ 同模块domain
import cn.lf.modules.base.mapper.SysCarouselMapper;     // ✅ 同模块mapper
import cn.lf.modules.base.service.ISysCarouselService;  // ✅ 同模块service接口
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

@Service
public class SysCarouselServiceImpl
    extends ServiceImpl<SysCarouselMapper, SysCarousel>
    implements ISysCarouselService {

    @Resource
    private SysCarouselMapper sysCarouselMapper;
}
```

#### Mapper层（lf-modules模块）

```java
package cn.lf.modules.base.mapper;  // ✅ 在lf-modules模块

import cn.lf.modules.base.domain.SysCarousel;  // ✅ 同模块domain
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

public interface SysCarouselMapper extends BaseMapper<SysCarousel> {
}
```

#### Domain层（lf-modules模块）

```java
package cn.lf.modules.base.domain;  // ✅ 在lf-modules模块

import cn.lf.base.domain.LBaseEntity;  // ✅ 引用lf-base的基础实体
import com.baomidou.mybatisplus.annotation.*;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_carousel")
public class SysCarousel extends LBaseEntity {

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    @TableField("title")
    private String title;
}
```

## 创建新业务模块的步骤

### 场景：开发AI模型管理功能

### 1. 创建Domain（在lf-modules）

**文件路径**: `lf-modules/src/main/java/cn/lf/modules/ai/domain/AiModel.java`

```java
package cn.lf.modules.ai.domain;

import cn.lf.base.domain.LBaseEntity;
import com.baomidou.mybatisplus.annotation.*;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("ai_model")
public class AiModel extends LBaseEntity {
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    @TableField("model_name")
    private String modelName;
}
```

### 2. 创建Mapper（在lf-modules）

**文件路径**: `lf-modules/src/main/java/cn/lf/modules/ai/mapper/AiModelMapper.java`

```java
package cn.lf.modules.ai.mapper;

import cn.lf.modules.ai.domain.AiModel;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

public interface AiModelMapper extends BaseMapper<AiModel> {
}
```

### 3. 创建Service接口（在lf-modules）

**文件路径**: `lf-modules/src/main/java/cn/lf/modules/ai/service/IAiModelService.java`

```java
package cn.lf.modules.ai.service;

import cn.lf.modules.ai.domain.AiModel;
import com.baomidou.mybatisplus.extension.service.IService;
import java.util.List;

public interface IAiModelService extends IService<AiModel> {
    List<AiModel> selectAiModelList(AiModel aiModel);
}
```

### 4. 创建Service实现（在lf-modules）

**文件路径**: `lf-modules/src/main/java/cn/lf/modules/ai/service/impl/AiModelServiceImpl.java`

```java
package cn.lf.modules.ai.service.impl;

import cn.lf.modules.ai.domain.AiModel;
import cn.lf.modules.ai.mapper.AiModelMapper;
import cn.lf.modules.ai.service.IAiModelService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class AiModelServiceImpl
    extends ServiceImpl<AiModelMapper, AiModel>
    implements IAiModelService {

    @Override
    public List<AiModel> selectAiModelList(AiModel aiModel) {
        return baseMapper.selectList(null);
    }
}
```

### 5. 创建Controller（在lf-admin）

**文件路径**: `lf-admin/src/main/java/cn/lf/base/controller/AiModelController.java`

```java
package cn.lf.base.controller;

import cn.lf.modules.ai.domain.AiModel;           // ✅ 引用lf-modules
import cn.lf.modules.ai.service.IAiModelService;  // ✅ 引用lf-modules
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

@RestController
@RequestMapping("/service/aiModel")
public class AiModelController extends BaseController {

    @Resource
    private IAiModelService aiModelService;  // ✅ 注入lf-modules的service

    @GetMapping("/list")
    public TableDataInfo list(AiModel aiModel) {
        startPage();
        List<AiModel> list = aiModelService.selectAiModelList(aiModel);
        return getDataTable(list);
    }

    @GetMapping("/{id}")
    public AjaxResult getInfo(@PathVariable Long id) {
        return success(aiModelService.getById(id));
    }
}
```

### 6. 配置模块依赖

**lf-admin的pom.xml**:
```xml
<dependency>
    <groupId>cn.lf</groupId>
    <artifactId>lf-modules</artifactId>
</dependency>
```

**lf-modules的pom.xml**:
```xml
<dependency>
    <groupId>cn.lf</groupId>
    <artifactId>lf-base</artifactId>
</dependency>
```

## 常见错误对照表

| 错误类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| **Controller位置错误** | 放在lf-modules | 放在lf-admin |
| **Domain位置错误** | 放在lf-admin或lf-base | 放在lf-modules |
| **Service位置错误** | 放在lf-admin | 放在lf-modules |
| **包名与路径不匹配** | 文件在com/xxx/，包名cn.xxx | 文件路径与包名严格一致 |
| **import路径错误** | import lf-module.domain | import cn.lf.modules.xxx.domain |

## 关键要点

1. **Controller必须在lf-admin模块**，不在lf-modules中
2. **lf-modules是纯业务模块**，只包含domain、mapper、service
3. **按业务领域划分子模块**，如cn.lf.modules.ai、cn.ynlky.modules.ydcx_user
4. **包名必须与文件路径严格匹配**
5. **lf-admin引用lf-modules**，lf-modules引用lf-base
