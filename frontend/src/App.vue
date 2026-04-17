<template>
  <div id="app">
    <div class="container" v-if="isLoggedIn">
      <el-header>
        <div class="header-content">
          <h1 class="title">掘金头条</h1>
          <div class="header-actions">
            <el-dropdown @command="handleCommand">
              <el-avatar :size="32" :src="userInfo?.avatar" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <div class="footer-content">
          <el-button 
            :type="currentPage === 'news' ? 'primary' : 'default'" 
            @click="$router.push('/news')"
            size="large"
            :icon="Document"
          >
            新闻
          </el-button>
          <el-button 
            :type="currentPage === 'ai' ? 'primary' : 'default'" 
            @click="$router.push('/ai')"
            size="large"
            :icon="ChatDotRound"
          >
            AI问答
          </el-button>
          <el-button 
            :type="currentPage === 'user' ? 'primary' : 'default'" 
            @click="$router.push('/user')"
            size="large"
            :icon="User"
          >
            我的
          </el-button>
        </div>
      </el-footer>
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from './store/user'
import { Document, ChatDotRound, User } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const currentPage = computed(() => {
  if (route.path.startsWith('/news')) return 'news'
  if (route.path.startsWith('/ai')) return 'ai'
  if (route.path.startsWith('/user')) return 'user'
  return 'news'
})

const isLoggedIn = computed(() => !!userStore.token)
const userInfo = computed(() => userStore.userInfo)

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/user')
  } else if (command === 'logout') {
    userStore.logout()
    router.push('/user')
  }
}
</script>

<style scoped>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.title {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.el-main {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f7fa;
}

.el-footer {
  background: white;
  padding: 12px 16px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
}

.footer-content {
  display: flex;
  justify-content: space-around;
  gap: 8px;
}

.footer-content .el-button {
  flex: 1;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .el-main {
    padding: 12px;
  }

  .title {
    font-size: 18px;
  }

  .footer-content .el-button {
    font-size: 12px;
  }
}
</style>
