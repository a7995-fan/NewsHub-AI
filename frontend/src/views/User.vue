<template>
  <div class="user-page">
    <div v-if="!isLoggedIn" class="auth-container">
      <el-card class="auth-card">
        <el-tabs v-model="activeTab" stretch>
          <el-tab-pane label="登录" name="login">
            <el-form 
              ref="loginFormRef" 
              :model="loginForm" 
              :rules="loginRules"
              label-width="0"
              @submit.prevent="handleLogin"
            >
              <el-form-item prop="username">
                <el-input 
                  v-model="loginForm.username" 
                  placeholder="用户名"
                  prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="密码"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  style="width: 100%"
                  :loading="loading"
                  @click="handleLogin"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="注册" name="register">
            <el-form 
              ref="registerFormRef" 
              :model="registerForm" 
              :rules="registerRules"
              label-width="0"
              @submit.prevent="handleRegister"
            >
              <el-form-item prop="username">
                <el-input 
                  v-model="registerForm.username" 
                  placeholder="用户名（3-50字符）"
                  prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="registerForm.password" 
                  type="password" 
                  placeholder="密码（6-100字符）"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  size="large" 
                  style="width: 100%"
                  :loading="loading"
                  @click="handleRegister"
                >
                  注册
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

    <div v-else class="profile-container">
      <el-card class="profile-card">
        <div class="profile-header">
          <el-avatar :size="80" :src="userInfo?.avatar" />
          <h2>{{ userInfo?.username }}</h2>
        </div>

        <el-tabs v-model="activeProfileTab">
          <el-tab-pane label="个人信息" name="profile">
            <el-form 
              ref="profileFormRef" 
              :model="profileForm" 
              label-width="80px"
            >
              <el-form-item label="昵称">
                <el-input v-model="profileForm.nickname" />
              </el-form-item>
              <el-form-item label="头像">
                <el-input v-model="profileForm.avatar" placeholder="头像URL" />
              </el-form-item>
              <el-form-item label="性别">
                <el-radio-group v-model="profileForm.gender">
                  <el-radio label="male">男</el-radio>
                  <el-radio label="female">女</el-radio>
                  <el-radio label="unknown">保密</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input 
                  v-model="profileForm.bio" 
                  type="textarea" 
                  :rows="3"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="profileForm.phone" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleUpdateProfile" :loading="loading">
                  保存
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="我的收藏" name="favorites">
            <div class="favorites-section">
              <el-empty v-if="favorites.length === 0 && !loading" description="暂无收藏" />
              <el-table v-else :data="favorites" style="width: 100%" v-loading="loading">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="title" label="标题">
                  <template #default="scope">
                    <el-link :href="`/news/${scope.row.id}`" target="_blank">
                      {{ scope.row.title }}
                    </el-link>
                  </template>
                </el-table-column>
                <el-table-column prop="categoryName" label="分类" width="120" />
                <el-table-column label="收藏时间" width="180">
                  <template #default="scope">
                    {{ formatTime(scope.row.favoriteTime) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="scope">
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="handleRemoveFavorite(scope.row.id)"
                    >
                      取消收藏
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div v-if="favorites.length > 0" class="favorites-actions">
                <el-button 
                  type="danger" 
                  @click="handleClearFavorites"
                  :loading="loading"
                >
                  清空收藏
                </el-button>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="浏览记录" name="history">
            <div class="history-section">
              <el-empty v-if="history.length === 0 && !loading" description="暂无浏览记录" />
              <el-table v-else :data="history" style="width: 100%" v-loading="loading">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="title" label="标题">
                  <template #default="scope">
                    <el-link :href="`/news/${scope.row.id}`" target="_blank">
                      {{ scope.row.title }}
                    </el-link>
                  </template>
                </el-table-column>
                <el-table-column prop="categoryName" label="分类" width="120" />
                <el-table-column prop="viewCount" label="浏览次数" width="100" />
                <el-table-column label="最近浏览" width="180">
                  <template #default="scope">
                    {{ formatTime(scope.row.viewTime) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                  <template #default="scope">
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="handleRemoveHistory(scope.row.historyId)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div v-if="history.length > 0" class="history-actions">
                <el-button 
                  type="danger" 
                  @click="handleClearHistory"
                  :loading="loading"
                >
                  清空记录
                </el-button>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="修改密码" name="password">
            <el-form 
              ref="passwordFormRef" 
              :model="passwordForm" 
              :rules="passwordRules"
              label-width="80px"
            >
              <el-form-item label="旧密码" prop="oldPassword">
                <el-input 
                  v-model="passwordForm.oldPassword" 
                  type="password" 
                  show-password
                />
              </el-form-item>
              <el-form-item label="新密码" prop="newPassword">
                <el-input 
                  v-model="passwordForm.newPassword" 
                  type="password" 
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleChangePassword" :loading="loading">
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="退出登录" name="logout">
            <div class="logout-section">
              <el-button type="danger" @click="handleLogout" :icon="SwitchButton">
                退出登录
              </el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { login, register, getUserInfo, updateUserInfo, changePassword } from '../api/user'
import { getFavorites, removeFavorite, clearFavorites } from '../api/favorite'
import { getHistory, removeHistory, clearHistory } from '../api/history'
import { SwitchButton } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => !!userStore.token)
const userInfo = computed(() => userStore.userInfo)

const activeTab = ref('login')
const activeProfileTab = ref('profile')
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: ''
})

const profileForm = ref({
  nickname: '',
  avatar: '',
  gender: 'unknown',
  bio: '',
  phone: ''
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: ''
})

const favorites = ref([])
const history = ref([])

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度在 6 到 100 个字符', trigger: 'blur' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度在 6 到 100 个字符', trigger: 'blur' }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度在 6 到 100 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await login(loginForm.value)
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUserInfo(res.data.userInfo || res.data.user_info)
      ElMessage.success('登录成功')
      router.push('/news')
    }
  } catch (error) {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  try {
    const res = await register(registerForm.value)
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUserInfo(res.data.userInfo || res.data.user_info)
      ElMessage.success('注册成功')
      router.push('/news')
    }
  } catch (error) {
    ElMessage.error('注册失败')
  } finally {
    loading.value = false
  }
}

const handleUpdateProfile = async () => {
  loading.value = true
  try {
    const res = await updateUserInfo(profileForm.value)
    if (res.code === 200) {
      await loadUserInfo()
      ElMessage.success('更新成功')
    }
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

const handleChangePassword = async () => {
  loading.value = true
  try {
    const res = await changePassword(passwordForm.value)
    if (res.code === 200) {
      ElMessage.success('密码修改成功')
      passwordForm.value = {
        oldPassword: '',
        newPassword: ''
      }
    }
  } catch (error) {
    ElMessage.error('密码修改失败')
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('退出登录成功')
  router.push('/news')
}

const loadUserInfo = async () => {
  try {
    const res = await getUserInfo()
    if (res.code === 200) {
      userStore.setUserInfo(res.data)
    }
  } catch (error) {
    console.error('加载用户信息失败', error)
  }
}

const loadFavorites = async () => {
  try {
    const res = await getFavorites()
    if (res.code === 200) {
      favorites.value = res.data.list
    }
  } catch (error) {
    console.error('加载收藏失败', error)
  }
}

const loadHistory = async () => {
  try {
    const res = await getHistory()
    if (res.code === 200) {
      history.value = res.data.list
    }
  } catch (error) {
    console.error('加载浏览记录失败', error)
  }
}

const handleRemoveFavorite = async (newsId) => {
  loading.value = true
  try {
    const res = await removeFavorite(newsId)
    if (res.code === 200) {
      ElMessage.success('取消收藏成功')
      await loadFavorites()
    }
  } catch (error) {
    ElMessage.error('取消收藏失败')
  } finally {
    loading.value = false
  }
}

const handleClearFavorites = async () => {
  loading.value = true
  try {
    const res = await clearFavorites()
    if (res.code === 200) {
      ElMessage.success('清空收藏成功')
      favorites.value = []
    }
  } catch (error) {
    ElMessage.error('清空收藏失败')
  } finally {
    loading.value = false
  }
}

const handleRemoveHistory = async (historyId) => {
  loading.value = true
  try {
    const res = await removeHistory(historyId)
    if (res.code === 200) {
      ElMessage.success('删除记录成功')
      await loadHistory()
    }
  } catch (error) {
    ElMessage.error('删除记录失败')
  } finally {
    loading.value = false
  }
}

const handleClearHistory = async () => {
  loading.value = true
  try {
    const res = await clearHistory()
    if (res.code === 200) {
      ElMessage.success('清空记录成功')
      history.value = []
    }
  } catch (error) {
    ElMessage.error('清空记录失败')
  } finally {
    loading.value = false
  }
}

const formatTime = (time) => {
  if (!time) return ''
  // 确保正确解析UTC时间
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour
  
  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)}分钟前`
  } else if (diff < day) {
    return `${Math.floor(diff / hour)}小时前`
  } else {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}

onMounted(() => {
  if (isLoggedIn.value) {
    loadUserInfo()
    loadFavorites()
    loadHistory()
    profileForm.value = {
      nickname: userInfo.value?.nickname || '',
      avatar: userInfo.value?.avatar || '',
      gender: userInfo.value?.gender || 'unknown',
      bio: userInfo.value?.bio || '',
      phone: userInfo.value?.phone || ''
    }
  }
})

// 监听标签页变化，加载对应数据
watch(activeProfileTab, (newTab) => {
  if (isLoggedIn.value) {
    if (newTab === 'favorites') {
      loadFavorites()
    } else if (newTab === 'history') {
      loadHistory()
    }
  }
})
</script>

<style scoped>
.user-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.auth-container,
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.auth-card,
.profile-card {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.profile-header {
  text-align: center;
  padding: 24px 0;
}

.profile-header h2 {
  margin: 12px 0 0 0;
  font-size: 20px;
}

.logout-section {
  text-align: center;
  padding: 40px 0;
}

@media (max-width: 768px) {
  .user-page {
    padding: 12px;
  }

  .profile-header h2 {
    font-size: 18px;
  }
}
</style>
