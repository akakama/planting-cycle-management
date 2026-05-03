import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),
  actions: {
    async login(username, password) {
      const res = await authApi.login({ username, password })
      const { token, userInfo } = res.data
      this.token = token
      this.userInfo = userInfo
      localStorage.setItem('token', token)
      return res
    },
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
    async fetchUser() {
      const res = await authApi.getCurrentUser()
      this.userInfo = res.data
      return res
    }
  }
})
