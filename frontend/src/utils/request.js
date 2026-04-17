import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('请求错误:', error)
    console.error('错误响应:', error.response)
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || '请求失败'
    
    // 处理401错误
    if (error.response?.status === 401) {
      // 清除本地存储的token和用户信息
      const userStore = useUserStore()
      userStore.logout()
      
      // 跳转到登录页面
      const router = useRouter()
      router.push('/user')
      
      ElMessage.error('登录已过期，请重新登录')
    } else {
      ElMessage.error(message)
    }
    
    return Promise.reject(error)
  }
)

export default request
