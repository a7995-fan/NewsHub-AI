import request from '../utils/request'

export const getHistory = (page = 1, pageSize = 10) => {
  return request.get('/history/list', { params: { page, pageSize } })
}

export const addHistory = (newsId) => {
  return request.post('/history/add', { newsId: newsId })
}

export const removeHistory = (historyId) => {
  return request.delete('/history/remove', { params: { historyId } })
}

export const clearHistory = () => {
  return request.delete('/history/clear')
}
