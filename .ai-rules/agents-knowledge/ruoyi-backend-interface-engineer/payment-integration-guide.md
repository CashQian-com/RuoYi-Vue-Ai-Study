# 支付接口对接流程

## 支付方式概述

项目支持的支付方式：
- 微信支付: JSAPI、Native、H5、APP
- 支付宝支付: APP、网页、WAP、交易

## java-spring-tools支付集成

### Maven依赖

```xml
<dependency>
    <groupId>cn.lf</groupId>
    <artifactId>payment</artifactId>
    <version>1.1.0</version>
</dependency>
```

### 配置

#### 微信支付配置

```java
@Configuration
public class WechatPayConfig {

    @Bean
    public WechatPlugin wechatPlugin() {
        WechatPayConfig config = new WechatPayConfig();
        config.setAppId("wx1234567890");
        config.setApiV3Key("your_api_v3_key");
        config.setMchId("1234567890");
        config.setPrivateKeyFromPath("/path/to/apiclient_key.pem");
        config.setMerchantSerialNumber("your_serial_no");
        config.setNotifyUrl("https://your-domain.com/api/pay/notify/wechat");

        return PaymentUtil.createWechatPlugin(config);
    }
}
```

#### 支付宝配置

```java
@Configuration
public class AlipayConfig {

    @Bean
    public AliPlugin aliPlugin() {
        AlipayConfig config = new AlipayConfig();
        config.setAppId("your_app_id");
        config.setPrivateKey("your_private_key");
        config.setAlipayPublicKey("alipay_public_key");
        config.setServerUrl("https://openapi.alipay.com/gateway.do");
        config.setNotifyUrl("https://your-domain.com/api/pay/notify/alipay");

        return PaymentUtil.createAliPlugin(config);
    }
}
```

## 微信支付对接

### 1. JSAPI支付（公众号/小程序）

```java
@Service
public class PaymentService {

    @Autowired
    private WechatPlugin wechatPlugin;

    /**
     * 创建JSAPI支付订单
     */
    public Map<String, Object> createJsapiPay(OrderDTO orderDTO) {
        // 创建支付参数
        WechatPayParam param = new WechatPayParam();
        param.setOutTradeNo(orderDTO.getOrderNo());
        param.setDescription(orderDTO.getDescription());
        param.setTotalAmount(orderDTO.getAmount().multiply(new BigDecimal("100")).longValue());  // 转为分
        param.setOpenid(orderDTO.getOpenid());

        // 调用支付接口
        PrepayWithRequestPaymentResponse response = wechatPlugin.jsapi().createOrder(param);

        // 返回前端支付参数
        Map<String, Object> result = new HashMap<>();
        result.put("appId", response.getAppid());
        result.put("timeStamp", response.getTimeStamp());
        result.put("nonceStr", response.getNonceStr());
        result.put("package", response.getPackage());
        result.put("signType", response.getSignType());
        result.put("paySign", response.getSign());
        result.put("prepayId", response.getPrepayId());

        return result;
    }
}
```

### 2. Native支付（扫码）

```java
/**
 * 创建Native支付订单
 */
public String createNativePay(OrderDTO orderDTO) {
    WechatPayParam param = new WechatPayParam();
    param.setOutTradeNo(orderDTO.getOrderNo());
    param.setDescription(orderDTO.getDescription());
    param.setTotalAmount(orderDTO.getAmount().multiply(new BigDecimal("100")).longValue());

    PrepayResponse response = wechatPlugin.nativePay().createOrder(param);

    return response.getCodeUrl();  // 返回二维码URL
}
```

### 3. H5支付

```java
/**
 * 创建H5支付订单
 */
public String createH5Pay(OrderDTO orderDTO) {
    WechatPayParam param = new WechatPayParam();
    param.setOutTradeNo(orderDTO.getOrderNo());
    param.setDescription(orderDTO.getDescription());
    param.setTotalAmount(orderDTO.getAmount().multiply(new BigDecimal("100")).longValue());

    // 设置H5场景信息
    H5Info h5Info = new H5Info();
    h5Info.setType("Wap");
    SceneInfo sceneInfo = new SceneInfo();
    sceneInfo.setPayerClientIp(orderDTO.getClientIp());
    sceneInfo.setH5Info(h5Info);
    param.setSceneInfo(sceneInfo);

    PrepayResponse response = wechatPlugin.h5().createOrder(param);

    return response.getH5Url();  // 返回H5支付URL
}
```

### 4. 支付回调处理

```java
@RestController
@RequestMapping("/api/pay/notify")
public class PaymentNotifyController {

    @Autowired
    private WechatPlugin wechatPlugin;

    /**
     * 微信支付回调
     */
    @PostMapping("/wechat")
    public String wechatNotify(@RequestBody String notifyData) {
        try {
            // 验签并解析回调数据
            Transaction transaction = wechatPlugin.verifyNotify(notifyData);

            // 处理支付成功逻辑
            if ("TRANSACTION.SUCCESS".equals(transaction.getTradeState())) {
                String orderNo = transaction.getOutTradeNo();
                String transactionId = transaction.getTransactionId();

                // 更新订单状态
                orderService.paymentSuccess(orderNo, transactionId);

                return successResponse();
            }

            return failResponse("支付状态异常");
        } catch (Exception e) {
            logger.error("微信支付回调处理失败", e);
            return failResponse("处理失败");
        }
    }

    private String successResponse() {
        Map<String, String> data = new HashMap<>();
        data.put("code", "SUCCESS");
        data.put("message", "成功");
        return JacksonUtil.toJson(data);
    }

    private String failResponse(String message) {
        Map<String, String> data = new HashMap<>();
        data.put("code", "FAIL");
        data.put("message", message);
        return JacksonUtil.toJson(data);
    }
}
```

### 5. 退款

```java
/**
 * 微信退款
 */
public RefundResult refund(String orderNo, BigDecimal amount) {
    // 查询订单信息
    Order order = orderService.getByOrderNo(orderNo);

    // 创建退款参数
    WechatRefund refund = new WechatRefund();
    refund.setOutTradeNo(orderNo);
    refund.setOutRefundNo("REFUND_" + orderNo);
    refund.setReason("用户申请退款");

    // 退款金额
    Refund.Amount refundAmount = new Refund.Amount();
    refundAmount.setRefund(amount.multiply(new BigDecimal("100")).longValue());
    refundAmount.setTotal(order.getTotalAmount().multiply(new BigDecimal("100")).longValue());
    refundAmount.setCurrency("CNY");
    refund.setAmount(refundAmount);

    // 调用退款接口
    Refund response = wechatPlugin.refund(refund);

    return RefundResult.builder()
        .refundId(response.getRefundId())
        .status(response.getStatus())
        .build();
}
```

## 支付宝支付对接

### 1. APP支付

```java
/**
 * 创建支付宝APP支付订单
 */
public String createAlipayAppPay(OrderDTO orderDTO) {
    AliAppPayParam param = new AliAppPayParam();
    param.setOutTradeNo(orderDTO.getOrderNo());
    param.setTotalAmount(orderDTO.getAmount().toString());
    param.setSubject(orderDTO.getSubject());

    // 调用支付接口
    String orderString = aliPlugin.app().createOrder(param);

    return orderString;  // 返回SDK执行字符串
}
```

### 2. 网页支付

```java
/**
 * 创建支付宝网页支付订单
 */
public String createAlipayPagePay(OrderDTO orderDTO) {
    AliPagePayParam param = new AliPagePayParam();
    param.setOutTradeNo(orderDTO.getOrderNo());
    param.setTotalAmount(orderDTO.getAmount().toString());
    param.setSubject(orderDTO.getSubject());
    param.setReturnUrl("https://your-domain.com/return");
    param.setNotifyUrl("https://your-domain.com/api/pay/notify/alipay");

    // 调用支付接口
    String form = aliPlugin.page().createOrder(param);

    return form;  // 返回自动提交表单
}
```

### 3. 支付宝回调处理

```java
/**
 * 支付宝支付回调
 */
@PostMapping("/alipay")
public String alipayNotify(HttpServletRequest request) {
    try {
        // 获取回调参数
        Map<String, String> params = new HashMap<>();
        Map<String, String[]> requestParams = request.getParameterMap();
        for (String name : requestParams.keySet()) {
            params.put(name, request.getParameter(name));
        }

        // 验签
        AlipayAsyncNotifyParam notify = aliPlugin.verifyNotify(params);

        if ("TRADE_SUCCESS".equals(notify.getTradeStatus())) {
            String orderNo = notify.getOutTradeNo();
            String tradeNo = notify.getTradeNo();

            // 更新订单状态
            orderService.paymentSuccess(orderNo, tradeNo);

            return "success";
        }

        return "fail";
    } catch (Exception e) {
        logger.error("支付宝支付回调处理失败", e);
        return "fail";
    }
}
```

## 前端集成

### 微信小程序支付

```javascript
// 小程序支付
function wechatPay(payParams) {
  uni.requestPayment({
    provider: 'wxpay',
    timeStamp: payParams.timeStamp,
    nonceStr: payParams.nonceStr,
    package: payParams.package,
    signType: payParams.signType,
    paySign: payParams.paySign,
    success: (res) => {
      console.log('支付成功', res)
      uni.showToast({ title: '支付成功' })
    },
    fail: (err) => {
      console.error('支付失败', err)
      uni.showToast({ title: '支付失败', icon: 'none' })
    }
  })
}
```

### H5支付

```javascript
// 跳转到微信H5支付
function h5Pay(payUrl) {
  window.location.href = payUrl
}
```

### 支付宝支付

```javascript
// APP支付
function alipayPay(orderString) {
  // 调用支付宝SDK
  Alipay.pay(orderString)
    .then(result => {
      console.log('支付成功', result)
    })
    .catch(error => {
      console.error('支付失败', error)
    })
}
```

## 注意事项

### 1. 幂等性处理

支付回调可能会重复发送，需要保证幂等性：

```java
@RedisLock(
    value = "pay:notify",
    param = "#orderNo",
    waitTime = "5",
    autoReleaseTime = "30"
)
public void paymentSuccess(String orderNo, String transactionId) {
    // 检查订单是否已处理
    Order order = orderService.getByOrderNo(orderNo);
    if (order.getStatus() == OrderStatus.PAID) {
        return;  // 已处理，直接返回
    }

    // 处理支付成功逻辑
    orderService.updatePaymentStatus(orderNo, transactionId);
}
```

### 2. 异步处理

支付回调处理应该快速响应，复杂业务异步处理：

```java
@PostMapping("/wechat")
public String wechatNotify(@RequestBody String notifyData) {
    // 验签
    Transaction transaction = wechatPlugin.verifyNotify(notifyData);

    // 快速返回成功
    asyncService.processPaymentSuccess(transaction);

    return successResponse();
}

@Async
public void processPaymentSuccess(Transaction transaction) {
    // 异步处理业务逻辑
}
```

### 3. 安全考虑

- 使用HTTPS
- 验证回调签名
- 使用Redis分布式锁
- 记录支付日志
- 异常情况告警

### 4. 测试

使用沙箱环境进行测试：
- 微信支付沙箱: https://pay.weixin.qq.com/wiki/doc/api/index.html
- 支付宝沙箱: https://opendocs.alipay.com/open/200/105314

## 项目位置

- 支付模块: `java-spring-tools/payment`
- 支付配置: `cn.lf.payment.config`
- 支付插件: `cn.lf.payment.plugin.*`

## 相关文档

- [微信支付文档](https://pay.weixin.qq.com/wiki/doc/api/index.html)
- [支付宝支付文档](https://opendocs.alipay.com/open)
