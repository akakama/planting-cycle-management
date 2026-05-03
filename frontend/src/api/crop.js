import request from './request'

export const cropApi = {
  getList(params) {
    return request({ url: '/crops', method: 'get', params })
  },
  getDetail(id) {
    return request({ url: `/crops/${id}`, method: 'get' })
  },
  add(data) {
    return request({ url: '/crops', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/crops/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/crops/${id}`, method: 'delete' })
  }
}
