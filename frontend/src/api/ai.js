import request from './request'

export const aiApi = {
  sendChatMessage(data) {
    return request({ url: '/ai/chat', method: 'post', data })
  },
  getHistory(params) {
    return request({ url: '/ai/history', method: 'get', params })
  },
  searchKnowledge(params) {
    return request({ url: '/ai/knowledge/search', method: 'get', params })
  },
  pesticideInfo(name) {
    return request({ url: '/ai/tools/pesticide-info', method: 'get', params: { name } })
  },
  weather(location, days) {
    return request({ url: '/ai/tools/weather', method: 'get', params: { location, days } })
  }
}
