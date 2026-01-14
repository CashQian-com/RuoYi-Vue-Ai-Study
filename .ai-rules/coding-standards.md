# 编码规范

## Java后端编码规范

### 1. 命名规范

#### 1.1 包名规范
```
com.ruoyi.module.[模块名]
├── domain/         # 实体类
├── mapper/         # Mapper接口
│   └── xml/        # Mapper XML
├── service/        # Service接口
│   └── impl/       # Service实现
└── controller/     # Controller（在控制层模块）
```

#### 1.2 类名规范
- **实体类**: 使用业务名称，如 `AiModel`, `User`
- **Mapper接口**: 实体名 + Mapper，如 `AiModelMapper`
- **Service接口**: I + 实体名 + Service，如 `IAiModelService`
- **Service实现**: 实体名 + ServiceImpl，如 `AiModelServiceImpl`
- **Controller**: 实体名 + Controller，如 `AiModelController`

#### 1.3 方法名规范
```java
// 查询
select[Entity]List(Query)        # 查询列表
select[Entity]ById(id)           # 根据ID查询
select[Entity]By[Field](value)   # 根据字段查询

// 新增
insert[Entity](entity)           # 新增

// 修改
update[Entity](entity)           # 修改

// 删除
delete[Entity]ById(id)           # 根据ID删除
delete[Entity]ByIds(ids[])       # 批量删除
```

#### 1.4 变量名规范
```java
// 布尔变量使用is/has/can前缀
boolean isActive;
boolean hasPermission;
boolean canDelete;

// 集合变量使用复数
List<User> users;
Map<String, Object> dataMap;

// 常量使用全大写下划线分隔
public static final String MAX_SIZE = "100";
public static final String DEFAULT_PAGE_SIZE = "10";
```

### 2. 注解规范

#### 2.1 Controller注解
```java
@RestController
@RequestMapping("/module/entity")
public class EntityController extends BaseController {

    @Autowired
    private IEntityService entityService;

    @PreAuthorize("@ss.hasPermi('module:entity:list')")
    @GetMapping("/list")
    public TableDataInfo list(Entity entity) {
        // ...
    }

    @PreAuthorize("@ss.hasPermi('module:entity:add')")
    @Log(title = "实体", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@Validated @RequestBody Entity entity) {
        // ...
    }
}
```

#### 2.2 Service注解
```java
@Service
public class EntityServiceImpl implements IEntityService {

    @Autowired
    private EntityMapper entityMapper;

    @Override
    public Entity selectEntityById(Long id) {
        return entityMapper.selectEntityById(id);
    }

    @RedisLock(
        value = "entity:lock",
        param = "#id",
        waitTime = "10",
        autoReleaseTime = "30"
    )
    @Override
    public int updateEntity(Entity entity) {
        return entityMapper.updateEntity(entity);
    }
}
```

#### 2.3 Entity注解
```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("ai_model")
public class AiModel extends BaseEntity {

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    @TableField("model_name")
    @NotBlank(message = "模型名称不能为空")
    private String modelName;

    @TableField("model_key")
    @JsonIgnore  // JSON序列化时忽略
    private String modelKey;

    @TableField("expire_time")
    private Date expireTime;

    @TableField("status")
    private String status;
}
```

### 3. 异常处理规范

#### 3.1 业务异常
```java
// 抛出业务异常
throw new ServiceException("用户名已存在");
throw new ServiceException("余额不足");

// 带错误码
throw new ServiceException("USER_EXISTS", "用户名已存在");
```

#### 3.2 全局异常处理
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ServiceException.class)
    public AjaxResult handleServiceException(ServiceException e) {
        logger.error("业务异常: {}", e.getMessage());
        return AjaxResult.error(e.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public AjaxResult handleException(Exception e) {
        logger.error("系统异常: {}", e.getMessage(), e);
        return AjaxResult.error("系统错误，请联系管理员");
    }
}
```

### 4. 日志规范

#### 4.1 日志级别
```java
// DEBUG: 调试信息
logger.debug("查询参数: {}", param);

// INFO: 重要信息
logger.info("用户登录成功: {}", username);

// WARN: 警告信息
logger.warn("接口调用频率过高: {}", ip);

// ERROR: 错误信息
logger.error("接口调用失败: {}", e.getMessage(), e);
```

#### 4.2 日志格式
```java
// 使用占位符，不要用字符串拼接
logger.info("用户{}执行了{}操作", username, operation);

// 记录异常堆栈
logger.error("处理失败", e);

// 关键业务操作记录
@Log(title = "用户管理", businessType = BusinessType.INSERT)
public AjaxResult add(User user) {
    // ...
}
```

### 5. 数据验证规范

#### 5.1 实体验证
```java
@Data
public class UserDTO {

    @Null(message = "新增时ID必须为空", groups = Add.class)
    @NotNull(message = "修改时ID不能为空", groups = Update.class)
    private Long id;

    @NotBlank(message = "用户名不能为空")
    @Length(min = 2, max = 20, message = "用户名长度2-20字符")
    private String username;

    @Phone(checkType = Phone.CheckType.ONLY_MOBILE, message = "手机号格式错误")
    private String phone;

    @IdCard(isNull = true, message = "身份证号格式错误")
    private String idCard;

    @Email(message = "邮箱格式错误")
    private String email;

    @Past(message = "出生日期必须是过去时间")
    private Date birthday;
}
```

#### 5.2 Controller验证
```java
@PostMapping
public AjaxResult add(@Validated(Add.class) @RequestBody UserDTO userDTO) {
    // ...
}

@PutMapping
public AjaxResult edit(@Validated(Update.class) @RequestBody UserDTO userDTO) {
    // ...
}
```

### 6. SQL编写规范

#### 6.1 Mapper XML规范
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.ruoyi.module.ai.mapper.AiModelMapper">

    <!-- 结果映射 -->
    <resultMap type="AiModel" id="AiModelResult">
        <result property="id" column="id" />
        <result property="modelName" column="model_name" />
        <result property="modelKey" column="model_key" />
    </resultMap>

    <!-- 查询列 -->
    <sql id="selectAiModelVo">
        select id, model_name, model_key, expire_time, status
        from ai_model
    </sql>

    <!-- 查询列表 -->
    <select id="selectAiModelList" parameterType="AiModel" resultMap="AiModelResult">
        <include refid="selectAiModelVo"/>
        <where>
            <if test="modelName != null and modelName != ''">
                AND model_name like concat('%', #{modelName}, '%')
            </if>
            <if test="status != null and status != ''">
                AND status = #{status}
            </if>
        </where>
        order by id desc
    </select>

    <!-- 新增 -->
    <insert id="insertAiModel" parameterType="AiModel" useGeneratedKeys="true" keyProperty="id">
        insert into ai_model
        <trim prefix="(" suffix=")" suffixOverrides=",">
            <if test="modelName != null">model_name,</if>
            <if test="modelKey != null">model_key,</if>
            <if test="expireTime != null">expire_time,</if>
            <if test="status != null">status,</if>
            create_by,
            create_time
        </trim>
        <trim prefix="values (" suffix=")" suffixOverrides=",">
            <if test="modelName != null">#{modelName},</if>
            <if test="modelKey != null">#{modelKey},</if>
            <if test="expireTime != null">#{expireTime},</if>
            <if test="status != null">#{status},</if>
            #{createBy},
            sysdate()
        </trim>
    </insert>

    <!-- 修改 -->
    <update id="updateAiModel" parameterType="AiModel">
        update ai_model
        <trim prefix="SET" suffixOverrides=",">
            <if test="modelName != null">model_name = #{modelName},</if>
            <if test="modelKey != null">model_key = #{modelKey},</if>
            <if test="expireTime != null">expire_time = #{expireTime},</if>
            <if test="status != null">status = #{status},</if>
            update_by = #{updateBy},
            update_time = sysdate()
        </trim>
        where id = #{id}
    </update>

    <!-- 删除 -->
    <delete id="deleteAiModelByIds" parameterType="Long">
        update ai_model set del_flag = '2' where id in
        <foreach item="id" collection="array" open="(" separator="," close=")">
            #{id}
        </foreach>
    </delete>
</mapper>
```

#### 6.2 动态SQL规范
```xml
<!-- 使用where标签自动处理AND -->
<select id="selectList" parameterType="Entity" resultMap="Result">
    select * from table
    <where>
        <if test="name != null and name != ''">
            and name = #{name}
        </if>
        <if test="status != null">
            and status = #{status}
        </if>
    </where>
</select>

<!-- 使用trim处理逗号 -->
<insert id="insert" parameterType="Entity">
    insert into table
    <trim prefix="(" suffix=")" suffixOverrides=",">
        <if test="name != null">name,</if>
        <if test="value != null">value,</if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
        <if test="name != null">#{name},</if>
        <if test="value != null">#{value},</if>
    </trim>
</insert>
```

### 7. 注释规范

#### 7.1 类注释
```java
/**
 * AI模型管理Controller
 *
 * @author AI Agent
 * @date 2024-01-01
 */
@RestController
@RequestMapping("/ai/model")
public class AiModelController extends BaseController {
    // ...
}
```

#### 7.2 方法注释
```java
/**
 * 查询AI模型列表
 *
 * @param aiModel AI模型
 * @return AI模型集合
 */
@PreAuthorize("@ss.hasPermi('ai:model:list')")
@GetMapping("/list")
public TableDataInfo list(AiModel aiModel) {
    // ...
}

/**
 * 新增AI模型
 *
 * @param aiModel AI模型
 * @return 结果
 */
@PreAuthorize("@ss.hasPermi('ai:model:add')")
@Log(title = "AI模型", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@Validated @RequestBody AiModel aiModel) {
    // ...
}
```

#### 7.3 字段注释
```java
public class AiModel extends BaseEntity {

    /** 模型ID */
    private Long id;

    /** 模型名称 */
    private String modelName;

    /** 模型密钥 */
    private String modelKey;

    /** 到期时间 */
    private Date expireTime;

    /** 状态（0正常 1停用） */
    private String status;
}
```

## Vue前端编码规范

### 1. 组件命名规范

```
// 文件名: kebab-case
user-info.vue
user-list.vue

// 组件名: PascalCase
export default {
  name: 'UserInfo'
}

// 使用: kebab-case
<user-info />
```

### 2. API定义规范

```javascript
// api/user.js
import request from '@/utils/request'

// 查询用户列表
export function listUser(query) {
  return request({
    url: '/system/user/list',
    method: 'get',
    params: query
  })
}

// 查询用户详细
export function getUser(userId) {
  return request({
    url: '/system/user/' + userId,
    method: 'get'
  })
}

// 新增用户
export function addUser(data) {
  return request({
    url: '/system/user',
    method: 'post',
    data: data
  })
}

// 修改用户
export function updateUser(data) {
  return request({
    url: '/system/user',
    method: 'put',
    data: data
  })
}

// 删除用户
export function delUser(userId) {
  return request({
    url: '/system/user/' + userId,
    method: 'delete'
  })
}
```

### 3. 组件结构规范

```vue
<template>
  <div class="user-container">
    <!-- 模板内容 -->
  </div>
</template>

<script>
export default {
  name: 'User',
  components: {},
  props: {},
  data() {
    return {
      // 数据
    }
  },
  computed: {
    // 计算属性
  },
  watch: {
    // 监听器
  },
  created() {},
  mounted() {},
  methods: {
    // 方法
  }
}
</script>

<style lang="scss" scoped>
.user-container {
  // 样式
}
</style>
```

### 4. Vuex/Pinia规范

```javascript
// store/modules/user.js
const state = {
  token: '',
  userInfo: null
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USER_INFO: (state, userInfo) => {
    state.userInfo = userInfo
  }
}

const actions = {
  // 登录
  login({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      login(userInfo).then(res => {
        commit('SET_TOKEN', res.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
```

## UniApp编码规范

### 1. 页面结构规范

```vue
<template>
  <view class="page-container">
    <!-- 页面内容 -->
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const data = ref('')

// 计算属性
const computedData = computed(() => {
  return data.value.toUpperCase()
})

// 生命周期
onMounted(() => {
  // 初始化
})

// 方法
const handleClick = () => {
  // 处理逻辑
}
</script>

<style lang="scss" scoped>
.page-container {
  padding: 30rpx;
}
</style>
```

### 2. API调用规范

```typescript
// service/api/user.ts
import { request } from '../request'

export const userApi = {
  // 获取用户信息
  getUserInfo: () => {
    return request.get<UserInfo>('/user/info')
  },

  // 更新用户信息
  updateUserInfo: (data: UpdateUserInfoDTO) => {
    return request.post('/user/update', data)
  }
}
```

### 3. 条件编译规范

```vue
<template>
  <!-- 微信小程序 -->
  <!-- #ifdef MP-WEIXIN -->
  <button open-type="getUserInfo">微信登录</button>
  <!-- #endif -->

  <!-- H5 -->
  <!-- #ifdef H5 -->
  <button @click="h5Login">H5登录</button>
  <!-- #endif -->
</template>

<script>
// #ifdef MP-WEIXIN
console.log('微信小程序')
// #endif

// #ifdef H5
console.log('H5')
// #endif
</script>
```

## 通用规范

### 1. Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
perf: 性能优化
test: 测试相关
chore: 构建/工具链相关

示例:
feat: 添加AI模型管理功能
fix: 修复支付回调验签问题
docs: 更新README文档
```

### 2. 代码审查要点

- [ ] 代码符合命名规范
- [ ] 有必要的注释和文档
- [ ] 异常处理完善
- [ ] 日志记录合理
- [ ] 数据验证充分
- [ ] 无安全漏洞
- [ ] 无性能问题
- [ ] 测试覆盖充分
