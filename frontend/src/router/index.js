import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  {
    path: '/',
    redirect: '/user' // 默认重定向到登录/注册页面
  },
  {
    path: '/news',
    name: 'News',
    component: () => import('../views/News.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/news/:id',
    name: 'NewsDetail',
    component: () => import('../views/NewsDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai',
    name: 'AI',
    component: () => import('../views/AI.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('../views/User.vue'),
    meta: { requiresAuth: false } // 登录/注册页面不需要认证
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token
  
  console.log('路由守卫检查:', { to: to.path, from: from.path, isAuthenticated })
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 未登录，重定向到登录页面
    console.log('未登录，重定向到登录页面')
    next('/user')
  } else {
    next()
  }
})

export default router
