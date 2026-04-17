import request from '../utils/request'

export const register = (data) => {
  return request.post('/user/register', data)
}

export const login = (data) => {
  return request.post('/user/login', data)
}

export const getUserInfo = () => {
  return request.get('/user/info')
}

export const updateUserInfo = (data) => {
  return request.put('/user/update', data)
}

export const changePassword = (data) => {
  return request.put('/user/password', data)
}
