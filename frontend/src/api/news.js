import request from '../utils/request'

export const getCategories = () => {
  return request.get('/news/categories')
}

export const getNewsList = (params) => {
  return request.get('/news/list', { params })
}

export const getNewsDetail = (id) => {
  return request.get('/news/detail', { params: { id } })
}

export const checkFavorite = (newsId) => {
  return request.get('/favorite/check', { params: { newsId } })
}
