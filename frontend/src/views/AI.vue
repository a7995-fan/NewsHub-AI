<template>
  <div class="ai-page">
    <div class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message', message.role]"
        >
          <div class="message-content">
            <div class="message-avatar">
              <el-avatar v-if="message.role === 'user'" :src="userAvatar" />
              <el-icon v-else :size="24" color="#667eea">
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="message-text">
              <div v-html="formatMessage(message.content)"></div>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="message assistant">
          <div class="message-content">
            <div class="message-avatar">
              <el-icon :size="24" color="#667eea">
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="message-text loading">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keydown.enter.prevent="handleEnter"
          :disabled="loading"
        />
        <el-button 
          type="primary" 
          @click="sendMessage" 
          :loading="loading"
          :icon="Promotion"
        >
          发送
        </el-button>
      </div>
    </div>

    <el-empty v-if="messages.length === 0 && !loading" description="开始与 AI 对话吧" />
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import { ChatDotRound, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store/user'
import { chat } from '../api/ai'

const userStore = useUserStore()
const userAvatar = computed(() => userStore.userInfo?.avatar || '')

const messages = ref([
  {
    role: 'assistant',
    content: '您好！我是掘金头条的 AI 助手，可以帮您查询新闻、推荐内容、回答问题。请问有什么可以帮助您的？'
  }
])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)
const conversationId = ref('')

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleEnter = (e) => {
  if (!e.shiftKey) {
    sendMessage()
  }
}

const formatMessage = (content) => {
  // 简单的格式化，处理换行和特殊字符
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) {
    ElMessage.warning('请输入内容')
    return
  }

  messages.value.push({
    role: 'user',
    content: inputMessage.value
  })
  
  const userMessage = inputMessage.value
  inputMessage.value = ''
  scrollToBottom()

  loading.value = true

  try {
    const res = await chat({
      message: userMessage,
      conversation_id: conversationId.value
    })
    
    if (res.code === 200) {
      conversationId.value = res.data.conversation_id
      
      messages.value.push({
        role: 'assistant',
        content: res.data.message
      })
    } else {
      ElMessage.error(res.message || 'AI回复失败')
    }
  } catch (error) {
    console.error('AI问答错误:', error)
    ElMessage.error('发送失败，请重试')
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.ai-page {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  display: flex;
  gap: 8px;
  max-width: 80%;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
  border-radius: 50%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
  word-wrap: break-word;
  background: #f0f2f5;
  color: #333;
}

.message.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-text.loading {
  display: flex;
  gap: 4px;
  padding: 12px 20px;
}

.message-text.loading span {
  width: 6px;
  height: 6px;
  background: #999;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.message-text.loading span:nth-child(1) {
  animation-delay: -0.32s;
}

.message-text.loading span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-input {
  padding: 12px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.chat-input :deep(.el-textarea__inner) {
  border-radius: 8px;
  resize: none;
}

.chat-input .el-button {
  height: 74px;
  border-radius: 8px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .message-content {
    max-width: 90%;
  }

  .chat-input .el-button {
    height: 60px;
  }
}
</style>
