import request from '../utils/request'

export const getFavorites = (page = 1, pageSize = 10) => {
  return request.get('/favorite/list', { params: { page, pageSize } })
}

export const addFavorite = (newsId) => {
  return request.post('/favorite/add', { newsId: newsId })
}

export const removeFavorite = (newsId) => {
  return request.delete('/favorite/remove', { params: { newsId } })
}

export const clearFavorites = () => {
  return request.delete('/favorite/clear')
}
