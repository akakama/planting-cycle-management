import request from './request'

export const materialApi = {
  getList(params) {
    return request({ url: '/materials', method: 'get', params })
  },
  getDetail(id) {
    return request({ url: `/materials/${id}`, method: 'get' })
  },
  stockIn(id, data) {
    return request({ url: `/materials/${id}/stock-in`, method: 'put', data })
  }
}

export const materialUsageApi = {
  getList(params) {
    return request({ url: '/material-usage', method: 'get', params })
  },
  add(data) {
    return request({ url: '/material-usage', method: 'post', data })
  }
}
