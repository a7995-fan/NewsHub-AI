<template>
  <div class="news-page">
    <div class="category-tabs">
      <el-tabs v-model="activeCategory" @tab-change="handleCategoryChange">
        <el-tab-pane 
          v-for="category in categories" 
          :key="category.id" 
          :label="category.name" 
          :name="category.id"
        />
      </el-tabs>
    </div>

    <div class="news-list">
      <el-card 
        v-for="news in newsList" 
        :key="news.id" 
        class="news-card"
        @click="goToDetail(news.id)"
      >
        <div class="news-content">
          <div class="news-info">
            <h3 class="news-title">{{ news.title }}</h3>
            <p class="news-description">{{ news.description }}</p>
            <div class="news-meta">
              <span class="author">{{ news.author }}</span>
              <span class="views">{{ news.views }} 浏览</span>
            </div>
          </div>
          <div class="news-image" v-if="news.image">
            <el-image :src="news.image" fit="cover" />
          </div>
        </div>
      </el-card>
    </div>

    <div class="load-more" v-if="hasMore">
      <el-button 
        type="primary" 
        @click="loadMore" 
        :loading="loading"
        style="width: 100%"
      >
        加载更多
      </el-button>
    </div>

    <div class="no-more" v-else-if="newsList.length > 0">
      没有更多了
    </div>

    <el-empty v-if="newsList.length === 0 && !loading" description="暂无新闻" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories, getNewsList } from '../api/news'
import { ElMessage } from 'element-plus'

const router = useRouter()

const categories = ref([])
const activeCategory = ref(null)
const newsList = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const hasMore = ref(false)
const loading = ref(false)

const loadCategories = async () => {
  try {
    const res = await getCategories()
    if (res.code === 200) {
      categories.value = res.data
      if (categories.value.length > 0) {
        activeCategory.value = categories.value[0].id
        loadNews()
      }
    }
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const loadNews = async () => {
  if (loading.value) return
  
  loading.value = true
  try {
    const res = await getNewsList({
      categoryId: activeCategory.value,
      page: page.value,
      pageSize: pageSize.value
    })
    
    if (res.code === 200) {
      if (page.value === 1) {
        newsList.value = res.data.list
      } else {
        newsList.value = [...newsList.value, ...res.data.list]
      }
      total.value = res.data.total
      hasMore.value = res.data.hasMore
    }
  } catch (error) {
    ElMessage.error('加载新闻失败')
  } finally {
    loading.value = false
  }
}

const handleCategoryChange = () => {
  page.value = 1
  newsList.value = []
  loadNews()
}

const loadMore = () => {
  page.value++
  loadNews()
}

const goToDetail = (id) => {
  router.push(`/news/${id}`)
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.news-page {
  max-width: 800px;
  margin: 0 auto;
}

.category-tabs {
  background: white;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.category-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
}

.news-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.news-content {
  display: flex;
  gap: 12px;
}

.news-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.news-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.news-description {
  font-size: 14px;
  color: #666;
  margin: 0 0 8px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #999;
  margin-top: auto;
}

.news-image {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
}

.news-image :deep(.el-image) {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.load-more,
.no-more {
  padding: 16px 0;
  text-align: center;
  color: #999;
  font-size: 14px;
}

@media (max-width: 768px) {
  .news-content {
    flex-direction: column;
  }

  .news-image {
    width: 100%;
    height: 160px;
  }

  .news-title {
    font-size: 15px;
  }

  .news-description {
    font-size: 13px;
  }
}
</style>
