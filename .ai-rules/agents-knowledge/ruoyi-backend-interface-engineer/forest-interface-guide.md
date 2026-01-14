# Forest接口定义指南

## Forest简介

Forest是一个声明式HTTP客户端框架，比RestTemplate更简洁，支持自定义拦截器和自动JSON转换。

## 项目集成

### Maven依赖

```xml
<dependency>
    <groupId>com.dtflys.forest</groupId>
    <artifactId>forest-spring-boot-starter</artifactId>
    <version>1.5.30</version>
</dependency>

<!-- 如果使用java-spring-tools -->
<dependency>
    <groupId>cn.lf</groupId>
    <artifactId>base-forest</artifactId>
    <version>1.0.0</version>
</dependency>
```

### 配置

```yaml
forest:
  # 最大连接数
  max-connections: 500
  # 每个路由的最大连接数
  max-route-connections: 500
  # 超时时间(毫秒)
  timeout: 5000
  # 连接超时(毫秒)
  connect-timeout: 3000
  # 请求重试次数
  retry-count: 0
```

## 接口定义

### 基础接口

```java
@BaseRequest(
    baseURL = "${api.domain}",  # 从配置文件读取
    contentType = "application/json"
)
@BodyType(type = "json", encoder = ForestJacksonConverter.class)
public interface ApiClient {

    // GET请求
    @Get("/api/data")
    @QueryParamsJackson  # GET参数使用Jackson序列化
    Result getData(@Query Param param);

    // POST请求
    @Post("/api/create")
    Result create(@Body CreateParam param);

    // PUT请求
    @Put("/api/update")
    Result update(@Body UpdateParam param);

    // DELETE请求
    @Delete("/api/delete/{id}")
    Result delete(@PathVariable("id") Long id);
}
```

### 微信接口示例

```java
@BaseRequest(baseURL = "${wechat.apiDomain}")
public interface MiniProgramInterface {

    /**
     * 小程序登录
     */
    @Get("/sns/jscode2session")
    @QueryParamsJackson
    MiniProgramLoginVO jsCodeToSession(@Query MiniProgramLoginDTO dto);

    /**
     * 获取用户手机号
     */
    @Post("/wxa/business/getuserphonenumber")
    @AccessToken(AppTypeEnum.MINI_PROGRAM)  # 自动注入AccessToken
    MiniProgramPhone getPhoneNumber(
        AccessTokenBaseRequestDTO dto,
        @Body String code
    );

    /**
     * 发送订阅消息
     */
    @Post("/cgi-bin/message/subscribe/send")
    BaseVO sendSubscribeMessage(@Body MiniProgramMessageSubscribeSendDTO message);
}
```

### 支付接口示例

```java
@BaseRequest(baseURL = "${payment.domain}")
public interface PaymentInterface {

    /**
     * 创建支付订单
     */
    @Post("/api/payment/create")
    PaymentResponse createOrder(@Body PaymentParam param);

    /**
     * 查询订单
     */
    @Get("/api/payment/query")
    PaymentQueryResponse queryOrder(@Query("orderNo") String orderNo);

    /**
     * 申请退款
     */
    @Post("/api/payment/refund")
    RefundResponse refund(@Body RefundParam param);
}
```

## 高级用法

### 拦截器

```java
/**
 * GET参数拦截器
 */
public class GetParamsInterceptor implements Interceptor<Object> {

    @Override
    public void onInvoke(Method method, ForestRequest request, ForestResponse response) {
        // 获取@QueryParamsJackson注解
        QueryParamsJackson annotation = method.getAnnotation(QueryParamsJackson.class);

        if (annotation != null) {
            // 处理参数
            Object queryParam = request.getQueryArguments()[0];
            Map<String, Object> map = JacksonUtil.toMap(queryParam);

            // 设置查询参数
            request.addQuery(map);
        }
    }
}
```

### AccessToken拦截器

```java
/**
 * AccessToken获取拦截器
 */
public class WechatAccessTokenGetInterceptor implements Interceptor<Object> {

    @Override
    public void onInvoke(Method method, ForestRequest request, ForestResponse response) {
        // 获取@AccessToken注解
        AccessToken accessToken = method.getAnnotation(AccessToken.class);

        if (accessToken != null) {
            // 从缓存获取AccessToken
            String token = redisCache.getCacheObject("wechat:access_token");

            // 添加到请求头
            request.addHeader("Authorization", "Bearer " + token);
        }
    }
}
```

### 超时配置

```java
@BaseRequest(
    baseURL = "${api.domain}",
    timeout = 3000,  # 请求超时3秒
    connectTimeout = 2000  # 连接超时2秒
)
public interface TimeoutClient {

    @Get("/api/data")
    Result getData(@Query Param param);

    # 覆盖全局超时配置
    @Get(
        value = "/api/slow",
        timeout = 10000
    )
    Result getSlowData(@Query Param param);
}
```

### 重试配置

```java
@BaseRequest(
    baseURL = "${api.domain}",
    retryCount = 3,  # 重试3次
    retryInterval = 1000  # 重试间隔1秒
)
public interface RetryClient {

    @Get("/api/data")
    Result getData(@Query Param param);
}
```

## 常见场景

### 1. 文件上传

```java
@Post("/api/upload")
String uploadFile(@DataFile("file") File file);

@Post("/api/upload")
String uploadFile(@DataFile("file") byte[] bytes);

@Post("/api/upload")
String uploadFile(@DataFile("file") InputStream inputStream);
```

### 2. 文件下载

```java
@Get("/api/download")
File downloadFile(@Query("fileName") String fileName);
```

### 3. 表单提交

```java
@Post(
    value = "/api/form",
    contentType = "application/x-www-form-urlencoded"
)
Result submitForm(@Form("username") String username, @Form("password") String password);
```

### 4. URL编码

```java
@Get("/api/search")
Result search(@Query("keyword") String keyword);

// Forest会自动进行URL编码
```

## 错误处理

### 全局异常处理

```java
@Configuration
public classForestExceptionConfig {

    @Bean
    public ForestErrorHandler forestErrorHandler() {
        return new ForestErrorHandler() {
            @Override
            public void onError(ForestRuntimeException e, ForestRequest request, ForestResponse response) {
                logger.error("Forest请求失败: {}", e.getMessage());
                throw new ServiceException("接口调用失败");
            }
        };
    }
}
```

### 接口级错误处理

```java
@Get("/api/data")
Result getData(@Query Param param) {
    // Forest会自动处理HTTP错误
    // 4xx/5xx会抛出ForestRuntimeException
}
```

## 测试

### 单元测试

```java
@SpringBootTest
class ForestInterfaceTest {

    @Autowired
    private ApiClient apiClient;

    @Test
    void testGetData() {
        Param param = new Param();
        param.setId(1L);

        Result result = apiClient.getData(param);

        assertNotNull(result);
        assertEquals(200, result.getCode());
    }
}
```

### Mock测试

```java
@Test
void testMockForest() {
    // Mock Forest接口
    ApiClient mockClient = Forest.mock(ApiClient.class);

    when(mockClient.getData(any()))
        .thenReturn(new Result(200, "success"));

    Result result = mockClient.getData(new Param());

    assertEquals(200, result.getCode());
}
```

## 最佳实践

### 1. 接口设计

```java
// ✅ 推荐: 明确的接口定义
@BaseRequest(baseURL = "${api.domain}")
public interface UserClient {

    @Get("/api/user/{id}")
    User getUser(@PathVariable("id") Long id);

    @Post("/api/user")
    User createUser(@Body CreateUserParam param);
}

// ❌ 不推荐: 模糊的接口定义
@BaseRequest(baseURL = "${api.domain}")
public interface UserClient {

    @Get("/api/user")
    Object getUser(@Query Map<String, Object> params);
}
```

### 2. 参数验证

```java
// 在调用前验证参数
public void createOrder(OrderParam param) {
    // 验证参数
    if (StringUtils.isBlank(param.getOrderNo())) {
        throw new ServiceException("订单号不能为空");
    }

    // 调用接口
    orderClient.createOrder(param);
}
```

### 3. 日志记录

```java
// 使用拦截器记录日志
public class LoggingInterceptor implements Interceptor<Object> {

    @Override
    public void onInvoke(Method method, ForestRequest request, ForestResponse response) {
        logger.info("Forest请求: {} {}", request.getType(), request.getUrl());
    }
}
```

### 4. 超时处理

```java
// 设置合理的超时时间
@BaseRequest(
    baseURL = "${api.domain}",
    timeout = 5000,  # 5秒超时
    retryCount = 2  # 重试2次
)
public interface ApiClient {
    // ...
}
```

## 项目位置

- Forest配置: `java-spring-tools/base-forest`
- 拦截器: `cn.lf.base_forest.interceptor`
- 注解: `cn.lf.base_forest.annotation`

## 相关文档

- [Forest官方文档](https://forest.dtflyx.com/)
- [Spring Boot集成](https://forest.dtflyx.com/docs/Start)
