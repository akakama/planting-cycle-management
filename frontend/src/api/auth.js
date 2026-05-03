import request from './request'

export const authApi = {
  login(data) {
    return request({ url: '/auth/login', method: 'post', data })
  },
  logout() {
    return request({ url: '/auth/logout', method: 'post' })
  },
  getCurrentUser() {
    return request({ url: '/auth/current-user', method: 'get' })
  }
}
