<template>
  <div class="login-wrapper">
    <!-- 动态背景 -->
    <div class="animated-background">
      <div class="gradient-layer"></div>
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="wave"></div>
    </div>
    
    <!-- 装饰元素 -->
    <div class="decorations">
      <div class="plant plant-1">🌱</div>
      <div class="plant plant-2">🌿</div>
      <div class="plant plant-3">🌾</div>
      <div class="plant plant-4">🍃</div>
    </div>
    
    <!-- 登录卡片 -->
    <div class="login-container">
      <div class="login-card">
        <!-- Logo区域 -->
        <div class="logo-area">
          <div class="logo-circle">
            <span class="logo-emoji">🌱</span>
          </div>
          <h1 class="system-title">种植周期管理</h1>
          <p class="system-subtitle">Planting Cycle Management System</p>
        </div>
        
        <!-- 标签切换 -->
        <div class="tab-switcher">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'login' }"
            @click="activeTab = 'login'"
          >
            登录
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'register' }"
            @click="activeTab = 'register'"
          >
            注册
          </button>
          <div class="tab-indicator" :class="{ right: activeTab === 'register' }"></div>
        </div>
        
        <!-- 登录表单 -->
        <transition name="slide-fade" mode="out-in">
          <div v-if="activeTab === 'login'" key="login" class="form-container">
            <form @submit.prevent="onLogin" class="auth-form">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">👤</span>
                  用户名
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="loginForm.username"
                    type="text"
                    class="form-input"
                    placeholder="请输入用户名"
                    autocomplete="username"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔒</span>
                  密码
                </label>
                <div class="input-wrapper">
                  <input 
                    v-model="loginForm.password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-input"
                    placeholder="请输入密码"
                    autocomplete="current-password"
                  />
                  <button 
                    type="button"
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                  >
                    {{ showPassword ? '🙈' : '👁️' }}
                  </button>
                </div>
              </div>
              
              <button 
                type="submit" 
                class="submit-btn"
                :disabled="loading"
              >
                <span v-if="loading" class="loading-spinner"></span>
                <span v-else>立即登录</span>
              </button>
            </form>
          </div>
          
          <!-- 注册表单 -->
          <div v-else key="register" class="form-container">
            <form @submit.prevent="onRegister" class="auth-form">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">👤</span>
                  用户名
                </label>
                <input 
                  v-model="registerForm.username"
                  type="text"
                  class="form-input"
                  placeholder="3-20位字符"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔒</span>
                  密码
                </label>
                <input 
                  v-model="registerForm.password"
                  type="password"
                  class="form-input"
                  placeholder="6-20位字符"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔐</span>
                  确认密码
                </label>
                <input 
                  v-model="registerForm.confirmPassword"
                  type="password"
                  class="form-input"
                  placeholder="请再次输入密码"
                />
              </div>
              
              <div class="form-row">
                <div class="form-group half">
                  <label class="form-label">
                    <span class="label-icon">📧</span>
                    邮箱
                  </label>
                  <input 
                    v-model="registerForm.email"
                    type="email"
                    class="form-input"
                    placeholder="选填"
                  />
                </div>
                
                <div class="form-group half">
                  <label class="form-label">
                    <span class="label-icon">📱</span>
                    手机
                  </label>
                  <input 
                    v-model="registerForm.phone"
                    type="tel"
                    class="form-input"
                    placeholder="选填"
                  />
                </div>
              </div>
              
              <button 
                type="submit" 
                class="submit-btn"
                :disabled="registering"
              >
                <span v-if="registering" class="loading-spinner"></span>
                <span v-else>立即注册</span>
              </button>
            </form>
          </div>
        </transition>
        
        <!-- 底部装饰 -->
        <div class="card-footer">
          <p>🌱 让农业管理更智能</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const registering = ref(false)
const activeTab = ref('login')
const showPassword = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  phone: ''
})

async function onLogin() {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(loginForm.username, loginForm.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    ElMessage.error(e.response?.data?.message || '登录失败')
  } finally {
    loading.value = false
  }
}

async function onRegister() {
  if (!registerForm.username || !registerForm.password || !registerForm.confirmPassword) {
    ElMessage.warning('请填写所有必填项')
    return
  }

  if (registerForm.username.length < 3 || registerForm.username.length > 20) {
    ElMessage.warning('用户名长度必须在3-20个字符之间')
    return
  }

  if (registerForm.password.length < 6 || registerForm.password.length > 20) {
    ElMessage.warning('密码长度必须在6-20个字符之间')
    return
  }

  if (registerForm.password !== registerForm.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  if (registerForm.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
    ElMessage.warning('邮箱格式不正确')
    return
  }

  registering.value = true
  try {
    const response = await axios.post('/api/auth/register', {
      username: registerForm.username,
      password: registerForm.password,
      email: registerForm.email,
      phone: registerForm.phone
    })

    if (response.data.code === 200) {
      ElMessage.success('注册成功，请登录')
      activeTab.value = 'login'
      Object.assign(registerForm, {
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        phone: ''
      })
    } else {
      ElMessage.error(response.data.message || '注册失败')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.message || '注册失败')
  } finally {
    registering.value = false
  }
}
</script>

<style scoped>
@import '@/assets/styles/design-system.css';

/* ========================================
   登录页面容器
   ======================================== */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  font-family: var(--font-body);
}

/* ========================================
   动态背景
   ======================================== */
.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.gradient-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 30% 20%, rgba(134, 239, 172, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(254, 243, 199, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(187, 247, 208, 0.3) 0%, transparent 60%),
    linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #fef3c7 100%);
  animation: gradient-shift 15s ease infinite;
  background-size: 200% 200%;
}

.particle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
  animation: float 8s ease-in-out infinite;
}

.particle-1 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -200px;
  background: linear-gradient(135deg, var(--primary-300), var(--primary-500));
  animation-delay: 0s;
}

.particle-2 {
  width: 350px;
  height: 350px;
  top: 50%;
  right: -150px;
  background: linear-gradient(135deg, var(--earth-200), var(--earth-400));
  animation-delay: 2s;
}

.particle-3 {
  width: 300px;
  height: 300px;
  bottom: -100px;
  left: 30%;
  background: linear-gradient(135deg, var(--primary-200), var(--primary-400));
  animation-delay: 4s;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 200px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M321.39,56.44c58-10.79,114.43-21.34,168.71-21.34,67.73,0,117.57,21.34,184.77,21.34,46.35,0,90.11-10.79,136.05-21.34,58-10.79,114.43-21.34,168.71-21.34,67.73,0,117.57,21.34,184.77,21.34,46.35,0,90.11-10.79,136.05-21.34' fill='none' stroke='%2322c55e' stroke-width='3' opacity='0.2'/%3E%3C/svg%3E") repeat-x;
  animation: wave 10s linear infinite;
}

@keyframes wave {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ========================================
   装饰元素
   ======================================== */
.decorations {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.plant {
  position: absolute;
  font-size: 60px;
  opacity: 0.15;
  animation: float 6s ease-in-out infinite;
}

.plant-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.plant-2 {
  top: 20%;
  right: 15%;
  font-size: 50px;
  animation-delay: 1.5s;
}

.plant-3 {
  bottom: 15%;
  left: 20%;
  font-size: 55px;
  animation-delay: 3s;
}

.plant-4 {
  bottom: 25%;
  right: 10%;
  animation-delay: 4.5s;
}

/* ========================================
   登录卡片容器
   ======================================== */
.login-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 480px;
  padding: var(--space-4);
}

.login-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-2xl);
  padding: var(--space-10);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.5);
  animation: grow 0.6s var(--transition-bounce);
}

/* ========================================
   Logo区域
   ======================================== */
.logo-area {
  text-align: center;
  margin-bottom: var(--space-8);
}

.logo-circle {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-4);
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-400), var(--primary-600));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 10px 30px rgba(34, 197, 94, 0.3),
    inset 0 -5px 15px rgba(0, 0, 0, 0.1);
  animation: pulse-glow 3s ease-in-out infinite;
}

.logo-emoji {
  font-size: 48px;
  animation: float 3s ease-in-out infinite;
}

.system-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--soil-800);
  margin: 0 0 var(--space-2);
  letter-spacing: -0.02em;
}

.system-subtitle {
  font-size: var(--text-sm);
  color: var(--soil-500);
  margin: 0;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 500;
}

/* ========================================
   标签切换
   ======================================== */
.tab-switcher {
  position: relative;
  display: flex;
  background: var(--soil-100);
  border-radius: var(--radius-lg);
  padding: var(--space-1);
  margin-bottom: var(--space-6);
}

.tab-btn {
  flex: 1;
  padding: var(--space-3);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--soil-600);
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  z-index: 2;
}

.tab-btn.active {
  color: white;
}

.tab-indicator {
  position: absolute;
  top: var(--space-1);
  left: var(--space-1);
  width: calc(50% - var(--space-1));
  height: calc(100% - var(--space-2));
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  border-radius: var(--radius-md);
  transition: transform var(--transition-base);
  z-index: 1;
  box-shadow: var(--shadow-md);
}

.tab-indicator.right {
  transform: translateX(100%);
}

/* ========================================
   表单样式
   ======================================== */
.form-container {
  overflow: hidden;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-group.half {
  flex: 1;
}

.form-row {
  display: flex;
  gap: var(--space-4);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--soil-700);
}

.label-icon {
  font-size: 16px;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: white;
  border: 2px solid var(--soil-200);
  border-radius: var(--radius-lg);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--soil-800);
  transition: all var(--transition-base);
}

.form-input::placeholder {
  color: var(--soil-400);
}

.form-input:hover {
  border-color: var(--soil-300);
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

.password-toggle {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
  transition: transform var(--transition-fast);
}

.password-toggle:hover {
  transform: translateY(-50%) scale(1.1);
}

/* ========================================
   提交按钮
   ======================================== */
.submit-btn {
  width: 100%;
  padding: var(--space-4);
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  border: none;
  border-radius: var(--radius-lg);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: 
    0 4px 15px rgba(34, 197, 94, 0.3),
    inset 0 -2px 5px rgba(0, 0, 0, 0.1);
  margin-top: var(--space-4);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.submit-btn:hover::before {
  left: 100%;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(34, 197, 94, 0.4),
    inset 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========================================
   卡片底部
   ======================================== */
.card-footer {
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid var(--soil-200);
  text-align: center;
}

.card-footer p {
  font-size: var(--text-sm);
  color: var(--soil-500);
  margin: 0;
}

/* ========================================
   过渡动画
   ======================================== */
.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
