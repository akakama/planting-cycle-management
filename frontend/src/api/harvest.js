import request from './request'

export const harvestApi = {
  getList(params) {
    return request({ url: '/harvest-records', method: 'get', params })
  },
  add(data) {
    return request({ url: '/harvest-records', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/harvest-records/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/harvest-records/${id}`, method: 'delete' })
  }
}
