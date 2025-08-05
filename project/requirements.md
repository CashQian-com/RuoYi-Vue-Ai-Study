我需要查阅RuoYi-Vue项目框架源码以及java-spring-tools工具源码，根据代码结构帮我创建专门为这套框架开发的agent
agent可细分为：
  后台后端：ruoyi接口开发工程师(项目接口+forest对接第三方接口)，ruoyi数据开发工程师，ruoyi系统架构师，ruoyi-tool开发工程师
  后台前段：ruoyi-UI/UE工程师，ruoyi前段开发工程师，ruoyi组件开发工程师

框架结构：
  java-spring-toos：后端开发工具包
  RuoYi-Vue：后台框架（包含后台后端，后台前端）
    lf-base：基础服务
    lf-merchant: 门店端服务（控制层）
    lf-module：所有业务模块（新建业务也是在这里新建模块）实际业务实现
    lf-open-api： 前台服务（控制车层）
    lf-wechat: 微信相关服务
    ruoyi-admin: 管理平台服务（控制层）
    ruoyi-common: 公共服务
    ruoyi-framework：框架实现
    ruoyi-generator：代码生成器
    ruoyi-quartz：定时任务
    ruoyi-ui：后台管理平台前端
    ruoyi-ui-merchant：后台门店平台前端
    sql：初始化sql

- 注意：框架业务而开时ruoyi-common，ruoyi-framework，ruoyi-generator，ruoyi-system，lf-base基本不能改动（除特殊情况必须修改）
  - 所有新业务实现都按模块在lf-module中新建模块实现
  - 各个端的接口在各个端控制层实现，如ruoyi-admin，lf-open-api，lf-merchant