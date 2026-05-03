import request from './request'

export const yieldPredictionApi = {
  getList(params) {
    return request({ url: '/yield-predictions', method: 'get', params })
  },
  add(data) {
    return request({ url: '/yield-predictions', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/yield-predictions/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/yield-predictions/${id}`, method: 'delete' })
  }
}
