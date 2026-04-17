<template>
  <div class="news-detail-page">
    <el-button 
      class="back-btn" 
      @click="$router.back()" 
      :icon="ArrowLeft"
      circle
    />
    
    <el-card v-if="newsDetail" class="detail-card">
      <h1 class="detail-title">{{ newsDetail.title }}</h1>
      
      <div class="detail-meta">
        <span class="author">{{ newsDetail.author }}</span>
        <span class="views">{{ newsDetail.views }} 浏览</span>
        <span class="time">{{ formatTime(newsDetail.publishTime) }}</span>
      </div>

      <div class="detail-content" v-html="newsDetail.content"></div>

      <div class="detail-actions">
        <el-button type="primary" @click="toggleFavorite" :icon="isFavorited ? StarFilled : Star">
          {{ isFavorited ? '已收藏' : '收藏' }}
        </el-button>
        <el-button @click="shareNews" :icon="Share">分享</el-button>
      </div>

      <div class="related-news" v-if="relatedNews.length > 0">
        <h3>相关新闻</h3>
        <div class="related-list">
          <div 
            v-for="news in relatedNews" 
            :key="news.id" 
            class="related-item"
            @click="goToDetail(news.id)"
          >
            <h4>{{ news.title }}</h4>
            <span class="views">{{ news.views }} 浏览</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNewsDetail, checkFavorite } from '../api/news'
import { addHistory } from '../api/history'
import { addFavorite, removeFavorite } from '../api/favorite'
import { ArrowLeft, Star, StarFilled, Share } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const newsDetail = ref(null)
const relatedNews = ref([])
const isFavorited = ref(false)
const loading = ref(false)

const loadNewsDetail = async () => {
  try {
    const res = await getNewsDetail(route.params.id)
    if (res.code === 200) {
      newsDetail.value = res.data
      relatedNews.value = res.data.relatedNews || []
      console.log('相关新闻数据:', relatedNews.value)
      // 添加浏览记录
      await addHistory(route.params.id)
      // 检查收藏状态
      await checkFavoriteStatus()
    }
  } catch (error) {
    ElMessage.error('加载新闻详情失败')
  }
}

const checkFavoriteStatus = async () => {
  try {
    const res = await checkFavorite(route.params.id)
    if (res.code === 200) {
      isFavorited.value = res.data.isFavorite
    }
  } catch (error) {
    console.error('检查收藏状态失败', error)
  }
}

const toggleFavorite = async () => {
  loading.value = true
  try {
    if (isFavorited.value) {
      const res = await removeFavorite(route.params.id)
      if (res.code === 200) {
        isFavorited.value = false
        ElMessage.success('取消收藏成功')
      }
    } else {
      const res = await addFavorite(route.params.id)
      if (res.code === 200) {
        isFavorited.value = true
        ElMessage.success('收藏成功')
      }
    }
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    loading.value = false
  }
}

const shareNews = () => {
  if (navigator.share) {
    navigator.share({
      title: newsDetail.value.title,
      url: window.location.href
    })
  } else {
    ElMessage.info('复制链接成功')
  }
}

const goToDetail = (id) => {
  console.log('点击了相关新闻，id:', id)
  console.log('当前token:', localStorage.getItem('token'))
  console.log('router对象:', router)
  ElMessage.info(`正在跳转到新闻 ${id}`)
  try {
    window.location.href = `/news/${id}`
  } catch (error) {
    console.error('路由跳转失败:', error)
    ElMessage.error('跳转失败')
  }
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadNewsDetail()
})
</script>

<style scoped>
.news-detail-page {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.back-btn {
  position: fixed;
  top: 80px;
  left: 16px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.detail-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.detail-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.detail-meta {
  display: flex;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
  font-size: 14px;
  color: #666;
}

.detail-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 24px;
}

.detail-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 12px 0;
}

.detail-actions {
  display: flex;
  gap: 12px;
  padding: 20px 0;
  border-top: 1px solid #eee;
}

.related-news {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
  position: relative;
  z-index: 1;
}

.related-news h3 {
  font-size: 18px;
  margin: 0 0 16px 0;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: block;
  color: inherit;
  pointer-events: auto;
  user-select: none;
}

.related-item:hover {
  background: #e6e8eb;
}

.related-item h4 {
  font-size: 15px;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.related-item .views {
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .back-btn {
    top: 70px;
    left: 12px;
  }

  .detail-title {
    font-size: 20px;
  }

  .detail-content {
    font-size: 15px;
  }

  .detail-actions {
    flex-direction: column;
  }

  .detail-actions .el-button {
    width: 100%;
  }
}
</style>
