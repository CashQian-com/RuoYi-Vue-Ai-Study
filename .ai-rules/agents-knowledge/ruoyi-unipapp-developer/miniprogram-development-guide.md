# UniApp小程序开发规范

## 项目结构

```
RuoYi-Vue/
├── src/
│   ├── pages/            # 页面
│   ├── components/       # 组件
│   ├── service/          # 服务层
│   │   ├── api/          # API接口
│   │   └── request/      # 请求封装
│   ├── store/            # 状态管理
│   ├── hooks/            # 自定义Hooks
│   ├── compositionApi/   # 组合式API
│   ├── static/           # 静态资源
│   └── uni_modules/      # UniApp模块
├── pages.json            # 页面配置
├── manifest.json         # 应用配置
└── uni.scss              # 全局样式
```

## 页面开发

### 1. 页面模板

```vue
<template>
  <view class="page-container">
    <!-- 自定义导航栏 -->
    <uv-navbar
      :title="pageTitle"
      :safeAreaInsetTop="true"
      :placeholder="true"
    />

    <!-- 页面内容 -->
    <view class="page-content">
      <!-- 内容区域 -->
    </view>

    <!-- 自定义TabBar -->
    <uv-tabbar
      :value="tabBarValue"
      :list="tabBarList"
      @change="onTabBarChange"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 页面标题
const pageTitle = ref('首页')

// TabBar
const tabBarValue = ref(0)
const tabBarList = [
  { key: 'home', text: '首页', icon: 'home' },
  { key: 'order', text: '订单', icon: 'list' },
  { key: 'mine', text: '我的', icon: 'account' }
]

const onTabBarChange = (e: any) => {
  tabBarValue.value = e.value
}

onMounted(() => {
  // 页面加载完成
})
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.page-content {
  padding: 30rpx;
}
</style>
```

### 2. API调用

```typescript
// service/api/user.ts
import { request } from '../request'

export interface UserInfo {
  id: number
  nickname: string
  avatar: string
}

export const userApi = {
  // 获取用户信息
  getUserInfo: () => {
    return request.get<UserInfo>('/user/info')
  },

  // 更新用户信息
  updateUserInfo: (data: Partial<UserInfo>) => {
    return request.post('/user/update', data)
  }
}
```

### 3. 请求封装

```typescript
// service/request/index.ts
import instance from './instance'

// 普通请求（带loading和错误提示）
export const request = instance()

// 静默请求（无loading和错误提示）
export const silentRequest = instance(false)
```

### 4. 状态管理

```typescript
// store/modules/user.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref<UserInfo | null>(null)
  const token = ref('')

  // 计算属性
  const isLogin = computed(() => !!token.value)

  // 方法
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    uni.setStorageSync('userInfo', info)
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    uni.setStorageSync('token', newToken)
  }

  const logout = () => {
    userInfo.value = null
    token.value = ''
    uni.removeStorageSync('token')
    uni.removeStorageSync('userInfo')
  }

  return {
    userInfo,
    token,
    isLogin,
    setUserInfo,
    setToken,
    logout
  }
})
```

## 组件开发

### 1. 组件模板

```vue
<template>
  <view class="custom-component" @click="handleClick">
    <slot name="header">
      <!-- 默认header -->
      <view class="default-header">默认标题</view>
    </slot>

    <slot>
      <!-- 默认内容 -->
      <view class="default-content">默认内容</view>
    </slot>

    <slot name="footer">
      <!-- 默认footer -->
      <view class="default-footer">默认底部</view>
    </slot>
  </view>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  disabled?: boolean
}

// 定义props
const props = withDefaults(defineProps<Props>(), {
  title: '默认标题',
  disabled: false
})

// 定义emits
const emit = defineEmits<{
  click: []
  change: [value: string]
}>()

// 方法
const handleClick = () => {
  if (props.disabled) return
  emit('click')
}
</script>

<style lang="scss" scoped>
.custom-component {
  padding: 30rpx;
}
</style>
```

### 2. 使用组件

```vue
<template>
  <view>
    <custom-component
      title="自定义组件"
      :disabled="false"
      @click="handleClick"
    >
      <template #header>
        <view class="custom-header">自定义标题</view>
      </template>

      <view>自定义内容</view>

      <template #footer>
        <view class="custom-footer">自定义底部</view>
      </template>
    </custom-component>
  </view>
</template>
```

## 常用功能

### 1. 微信登录

```typescript
// 微信登录
const wechatLogin = () => {
  uni.login({
    provider: 'weixin',
    success: (res) => {
      const code = res.code
      // 调用后端登录接口
      authApi.postLogin({ code }).then(result => {
        // 保存Token
        authStore.setToken(result.token)
        // 获取用户信息
        getUserInfo()
      })
    },
    fail: (err) => {
      console.error('登录失败', err)
      uni.showToast({
        title: '登录失败',
        icon: 'none'
      })
    }
  })
}
```

### 2. 获取用户手机号

```vue
<template>
  <button
    open-type="getPhoneNumber"
    @getphonenumber="getPhoneNumber"
  >
    获取手机号
  </button>
</template>

<script setup lang="ts">
const getPhoneNumber = (e: any) => {
  const { code } = e.detail
  authApi.getPhoneNumber({ code }).then(result => {
    console.log('手机号', result.phoneNumber)
  })
}
</script>
```

### 3. 微信支付

```typescript
const wechatPay = (payParams: any) => {
  uni.requestPayment({
    provider: 'wxpay',
    timeStamp: payParams.timeStamp,
    nonceStr: payParams.nonceStr,
    package: payParams.package,
    signType: payParams.signType,
    paySign: payParams.paySign,
    success: () => {
      uni.showToast({
        title: '支付成功'
      })
      // 刷新订单状态
      checkOrderStatus()
    },
    fail: (err) => {
      console.error('支付失败', err)
      if (err.errMsg.includes('cancel')) {
        uni.showToast({
          title: '已取消支付',
          icon: 'none'
        })
      } else {
        uni.showToast({
          title: '支付失败',
          icon: 'none'
        })
      }
    }
  })
}
```

### 4. 分享功能

```typescript
// 分享给朋友
uni.share({
  provider: 'weixin',
  scene: 'WXSceneSession',
  type: 0,
  title: '分享标题',
  summary: '分享描述',
  href: 'https://example.com',
  imageUrl: 'https://example.com/share.png',
  success: () => {
    console.log('分享成功')
  },
  fail: (err) => {
    console.error('分享失败', err)
  }
})

// 分享到朋友圈
uni.share({
  provider: 'weixin',
  scene: 'WXSenceTimeline',
  type: 0,
  title: '分享标题',
  imageUrl: 'https://example.com/share.png'
})
```

### 5. 图片上传

```typescript
const uploadImage = () => {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      const tempFilePaths = res.tempFilePaths
      uni.uploadFile({
        url: 'https://api.example.com/upload',
        filePath: tempFilePaths[0],
        name: 'file',
        header: {
          'Authorization': 'Bearer ' + token.value
        },
        success: (uploadRes) => {
          const data = JSON.parse(uploadRes.data)
          console.log('上传成功', data)
        },
        fail: (err) => {
          console.error('上传失败', err)
        }
      })
    }
  })
}
```

## 条件编译

### 1. 平台判断

```vue
<!-- #ifdef MP-WEIXIN -->
<view>仅在微信小程序显示</view>
<!-- #endif -->

<!-- #ifdef H5 -->
<view>仅在H5显示</view>
<!-- #endif -->

<!-- #ifndef MP-WEIXIN -->
<view>除了微信小程序都显示</view>
<!-- #endif -->
```

### 2. 代码条件编译

```typescript
// #ifdef MP-WEIXIN
console.log('微信小程序')
// #endif

// #ifdef H5
console.log('H5')
// #endif

// #ifdef MP-WEIXIN || H5
console.log('微信小程序或H5')
// #endif
```

### 3. 样式条件编译

```scss
/* #ifdef MP-WEIXIN */
.container {
  padding-top: 0;
}
/* #endif */

/* #ifdef H5 */
.container {
  padding-top: 44px;
}
/* #endif */
```

## 性能优化

### 1. 分包加载

```json
{
  "subPackages": [
    {
      "root": "pages/mine",
      "pages": [
        {
          "path": "wx-login",
          "style": {
            "navigationBarTitleText": "微信登录"
          }
        }
      ]
    }
  ]
}
```

### 2. 图片懒加载

```vue
<image
  :src="imageSrc"
  lazy-load
  mode="aspectFill"
/>
```

### 3. 自定义组件按需引入

```javascript
// 按需引入uv-ui组件
import { UvButton } from '@climblee/uv-ui'
```

### 4. 长列表优化

```vue
<template>
  <scroll-view
    scroll-y
    @scrolltolower="onScrollToLower"
  >
    <view v-for="item in list" :key="item.id">
      {{ item.name }}
    </view>
  </scroll-view>
</template>

<script setup lang="ts">
const list = ref([])
const page = ref(1)
const loading = ref(false)
const finished = ref(false)

const loadData = () => {
  if (loading.value || finished.value) return

  loading.value = true
  api.getList({ page: page.value }).then(res => {
    list.value.push(...res.data)
    page.value++
    loading.value = false

    if (res.data.length === 0) {
      finished.value = true
    }
  })
}

const onScrollToLower = () => {
  loadData()
}
</script>
```

## 调试

### 1. 微信开发者工具

1. 打开微信开发者工具
2. 导入项目（选择项目目录）
3. 选择小程序项目
4. 点击编译

### 2. 真机调试

1. 微信开发者工具 → 预览 → 生成二维码
2. 微信扫码预览
3. 打开调试模式

### 3. vconsole调试H5

```typescript
// main.ts
import VConsole from 'vconsole'

// #ifdef H5
new VConsole()
// #endif
```

## 注意事项

### 1. 小程序审核

- 确保所有功能可正常使用
- 避免使用测试数据
- 检查隐私政策
- 验证支付功能
- 内容符合规范

### 2. 性能优化

- 使用分包加载
- 图片压缩
- 减少包体积
- 避免频繁setData

### 3. 兼容性

- 使用条件编译
- 测试不同平台
- 处理平台差异

## 项目位置

- 小程序项目: `RuoYi-Vue/`
- API接口: `src/service/api/`
- 状态管理: `src/store/modules/`
- 组件: `src/components/`
