import request from './request'

export const pestRecordApi = {
  getList(params) {
    return request({ url: '/pest-records', method: 'get', params })
  },
  add(data) {
    return request({ url: '/pest-records', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/pest-records/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/pest-records/${id}`, method: 'delete' })
  },
  diagnose(formData) {
    return request({
      url: '/pest-records/diagnose',
      method: 'post',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
