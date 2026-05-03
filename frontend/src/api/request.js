import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const service = axios.create({
  baseURL: import.meta.env.VITE_BASE_API || '/api',
  timeout: 30000
})

service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code === 200) {
      return res
    }
    // 业务错误处理
    const errorMessage = res.message || '请求失败'
    ElMessage.error(errorMessage)
    console.error('业务错误:', errorMessage, res)
    return Promise.reject(new Error(errorMessage))
  },
  error => {
    // HTTP错误处理
    let errorMessage = '网络错误'
    let errorDetail = error.message

    if (error.response) {
      // 服务器返回了响应，但状态码不在2xx范围内
      const { status, data } = error.response

      switch (status) {
        case 400:
          errorMessage = '请求参数错误'
          errorDetail = data?.message || '参数格式不正确'
          break
        case 401:
          errorMessage = '登录已过期，请重新登录'
          errorDetail = 'Token无效或已过期'
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          errorMessage = '无权限访问'
          errorDetail = '您没有权限执行此操作'
          break
        case 404:
          errorMessage = '资源不存在'
          errorDetail = '请求的资源未找到'
          break
        case 500:
          errorMessage = '服务器内部错误'
          errorDetail = data?.message || '服务器处理请求时发生错误'
          break
        case 503:
          errorMessage = '服务不可用'
          errorDetail = '服务暂时不可用，请稍后重试'
          break
        default:
          errorMessage = `请求失败 (${status})`
          errorDetail = data?.message || error.message
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      errorMessage = '网络连接失败'
      errorDetail = '无法连接到服务器，请检查网络连接'
    } else {
      // 请求配置出错
      errorMessage = '请求配置错误'
      errorDetail = error.message
    }

    ElMessage.error(errorMessage)
    console.error('HTTP错误:', {
      message: errorMessage,
      detail: errorDetail,
      error: error
    })

    return Promise.reject(new Error(errorMessage))
  }
)

export default service
