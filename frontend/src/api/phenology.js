import request from './request'

export const phenologyApi = {
  getList(params) {
    return request({ url: '/phenology-records', method: 'get', params })
  },
  add(data) {
    return request({ url: '/phenology-records', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/phenology-records/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/phenology-records/${id}`, method: 'delete' })
  }
}
