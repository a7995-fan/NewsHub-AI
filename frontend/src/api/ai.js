import request from '../utils/request'

export const chat = (data) => {
  return request.post('/ai/chat', data)
}

export const chatWithSearch = (data) => {
  return request.post('/ai/chat/search', data)
}

export const getAICategories = () => {
  return request.get('/ai/categories')
}

export const getAINews = (limit = 20) => {
  return request.get('/ai/news', { params: { limit } })
}
