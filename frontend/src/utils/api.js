/**
 * API适配工具
 * 用于适配新的统一API接口格式
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    
    // 检查响应码
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      
      // 处理401未授权
      if (res.code === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    return res.data
  },
  error => {
    console.error('响应错误:', error)
    
    // 处理网络错误
    if (error.message.includes('timeout')) {
      ElMessage.error('请求超时，请重试')
    } else if (error.message.includes('Network Error')) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error(error.message || '请求失败')
    }
    
    return Promise.reject(error)
  }
)

/**
 * 分页查询参数
 */
export class PageParam {
  constructor(page = 1, size = 10) {
    this.page = page
    this.size = size
    this.sort = null
    this.order = null
    this.keyword = null
  }
}

/**
 * 种植计划API
 */
export const planApi = {
  /**
   * 分页查询种植计划
   */
  page: (param) => {
    return request({
      url: '/plans',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 查询种植计划详情
   */
  getDetail: (id) => {
    return request({
      url: `/plans/${id}`,
      method: 'get'
    })
  },
  
  /**
   * 根据状态查询种植计划
   */
  pageByStatus: (status, param) => {
    return request({
      url: `/plans/status/${status}`,
      method: 'get',
      params: param
    })
  },
  
  /**
   * 创建种植计划
   */
  add: (data) => {
    return request({
      url: '/plans',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新种植计划
   */
  update: (id, data) => {
    return request({
      url: `/plans/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除种植计划
   */
  delete: (id) => {
    return request({
      url: `/plans/${id}`,
      method: 'delete'
    })
  },
  
  /**
   * 更新种植计划状态
   */
  updateStatus: (id, status, actualEndDate, actualYield) => {
    return request({
      url: `/plans/${id}/status`,
      method: 'put',
      params: {
        status,
        actualEndDate,
        actualYield
      }
    })
  }
}

/**
 * 作物API
 */
export const cropApi = {
  /**
   * 分页查询作物
   */
  page: (param) => {
    return request({
      url: '/crops',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 查询所有启用的作物
   */
  listEnabled: () => {
    return request({
      url: '/crops/enabled',
      method: 'get'
    })
  },
  
  /**
   * 查询推荐的作物
   */
  listRecommended: () => {
    return request({
      url: '/crops/recommended',
      method: 'get'
    })
  },
  
  /**
   * 根据类别查询作物
   */
  listByCategory: (category) => {
    return request({
      url: `/crops/category/${category}`,
      method: 'get'
    })
  },
  
  /**
   * 查询作物详情
   */
  getDetail: (id) => {
    return request({
      url: `/crops/${id}`,
      method: 'get'
    })
  },
  
  /**
   * 创建作物
   */
  add: (data) => {
    return request({
      url: '/crops',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新作物
   */
  update: (id, data) => {
    return request({
      url: `/crops/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除作物
   */
  delete: (id) => {
    return request({
      url: `/crops/${id}`,
      method: 'delete'
    })
  }
}

/**
 * 病虫害记录API
 */
export const pestApi = {
  /**
   * 分页查询病虫害记录
   */
  page: (param) => {
    return request({
      url: '/pests',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 根据种植计划查询病虫害记录
   */
  pageByPlanId: (planId, param) => {
    return request({
      url: `/pests/plan/${planId}`,
      method: 'get',
      params: param
    })
  },
  
  /**
   * 创建病虫害记录
   */
  add: (data) => {
    return request({
      url: '/pests',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新病虫害记录
   */
  update: (id, data) => {
    return request({
      url: `/pests/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除病虫害记录
   */
  delete: (id) => {
    return request({
      url: `/pests/${id}`,
      method: 'delete'
    })
  },
  
  /**
   * 病虫害图片识别
   */
  identify: (imageUrl) => {
    return request({
      url: '/pests/identify',
      method: 'post',
      data: { imageUrl }
    })
  },
  
  /**
   * 保存识别结果并创建记录
   */
  saveWithIdentify: (data) => {
    return request({
      url: '/pests/save-with-identify',
      method: 'post',
      data
    })
  }
}

/**
 * 物候期记录API
 */
export const phenologyApi = {
  /**
   * 分页查询物候期记录
   */
  page: (param) => {
    return request({
      url: '/phenology',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 根据种植计划查询物候期记录
   */
  pageByPlanId: (planId, param) => {
    return request({
      url: `/phenology/plan/${planId}`,
      method: 'get',
      params: param
    })
  },
  
  /**
   * 创建物候期记录
   */
  add: (data) => {
    return request({
      url: '/phenology',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新物候期记录
   */
  update: (id, data) => {
    return request({
      url: `/phenology/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除物候期记录
   */
  delete: (id) => {
    return request({
      url: `/phenology/${id}`,
      method: 'delete'
    })
  }
}

/**
 * 农资使用记录API
 */
export const materialUsageApi = {
  /**
   * 分页查询农资使用记录
   */
  page: (param) => {
    return request({
      url: '/materials/usage',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 根据种植计划查询农资使用记录
   */
  pageByPlanId: (planId, param) => {
    return request({
      url: `/materials/usage/plan/${planId}`,
      method: 'get',
      params: param
    })
  },
  
  /**
   * 统计农资总成本
   */
  getTotalCost: (planId) => {
    return request({
      url: `/materials/usage/plan/${planId}/total-cost`,
      method: 'get'
    })
  },
  
  /**
   * 创建农资使用记录
   */
  add: (data) => {
    return request({
      url: '/materials/usage',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新农资使用记录
   */
  update: (id, data) => {
    return request({
      url: `/materials/usage/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除农资使用记录
   */
  delete: (id) => {
    return request({
      url: `/materials/usage/${id}`,
      method: 'delete'
    })
  }
}

/**
 * 农资API
 */
export const materialApi = {
  /**
   * 分页查询农资
   */
  page: (param) => {
    return request({
      url: '/materials',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 查询所有启用的农资
   */
  listEnabled: () => {
    return request({
      url: '/materials/enabled',
      method: 'get'
    })
  },
  
  /**
   * 查询推荐的农资
   */
  listRecommended: () => {
    return request({
      url: '/materials/recommended',
      method: 'get'
    })
  },
  
  /**
   * 根据类型查询农资
   */
  listByType: (materialType) => {
    return request({
      url: `/materials/type/${materialType}`,
      method: 'get'
    })
  },
  
  /**
   * 查询农资详情
   */
  getDetail: (id) => {
    return request({
      url: `/materials/${id}`,
      method: 'get'
    })
  },
  
  /**
   * 创建农资
   */
  add: (data) => {
    return request({
      url: '/materials',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新农资
   */
  update: (id, data) => {
    return request({
      url: `/materials/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除农资
   */
  delete: (id) => {
    return request({
      url: `/materials/${id}`,
      method: 'delete'
    })
  }
}

/**
 * 采收记录API
 */
export const harvestApi = {
  /**
   * 分页查询采收记录
   */
  page: (param) => {
    return request({
      url: '/harvests',
      method: 'get',
      params: param
    })
  },
  
  /**
   * 根据种植计划查询采收记录
   */
  pageByPlanId: (planId, param) => {
    return request({
      url: `/harvests/plan/${planId}`,
      method: 'get',
      params: param
    })
  },
  
  /**
   * 统计总产量
   */
  getTotalYield: (planId) => {
    return request({
      url: `/harvests/plan/${planId}/total-yield`,
      method: 'get'
    })
  },
  
  /**
   * 统计总销售额
   */
  getTotalSaleAmount: (planId) => {
    return request({
      url: `/harvests/plan/${planId}/total-sale-amount`,
      method: 'get'
    })
  },
  
  /**
   * 创建采收记录
   */
  add: (data) => {
    return request({
      url: '/harvests',
      method: 'post',
      data
    })
  },
  
  /**
   * 更新采收记录
   */
  update: (id, data) => {
    return request({
      url: `/harvests/${id}`,
      method: 'put',
      data
    })
  },
  
  /**
   * 删除采收记录
   */
  delete: (id) => {
    return request({
      url: `/harvests/${id}`,
      method: 'delete'
    })
  }
}

export default request
