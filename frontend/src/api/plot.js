import request from './request'

export const plotApi = {
  getList(params) {
    return request({ url: '/plots', method: 'get', params })
  },
  getDetail(id) {
    return request({ url: `/plots/${id}`, method: 'get' })
  },
  add(data) {
    return request({ url: '/plots', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/plots/${id}`, method: 'put', data })
  }
}
