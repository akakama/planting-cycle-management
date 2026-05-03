import request from './request'

export const plantingPlanApi = {
  getList(params) {
    return request({ url: '/planting-plans', method: 'get', params })
  },
  getDetail(id) {
    return request({ url: `/planting-plans/${id}`, method: 'get' })
  },
  add(data) {
    return request({ url: '/planting-plans', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/planting-plans/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/planting-plans/${id}`, method: 'delete' })
  },
  updateStatus(id, data) {
    return request({ url: `/planting-plans/${id}/status`, method: 'put', data })
  }
}

export const plantingCalendarApi = {
  getCalendar(params) {
    return request({ url: '/planting-calendar', method: 'get', params })
  }
}
