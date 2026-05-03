<template>
  <div class="layout-wrapper">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="leaf leaf-1"></div>
      <div class="leaf leaf-2"></div>
      <div class="leaf leaf-3"></div>
    </div>
    
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <!-- Logo区域 -->
      <div class="logo-section">
        <div class="logo-icon">🌱</div>
        <transition name="fade">
          <div v-if="!isCollapsed" class="logo-text">
            <h1>种植周期管理</h1>
            <p class="logo-subtitle">Planting Cycle</p>
          </div>
        </transition>
      </div>
      
      <!-- 折叠按钮 -->
      <button class="collapse-btn" @click="toggleCollapse">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M15 18l-6-6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      
      <!-- 导航菜单 -->
      <nav class="nav-menu">
        <div v-for="item in menuItems" :key="item.key" class="menu-section">
          <div v-if="item.children" class="menu-group">
            <div 
              class="menu-title" 
              :class="{ expanded: expandedMenus.includes(item.key) }"
              @click="toggleMenu(item.key)"
            >
              <span class="menu-icon">{{ item.icon }}</span>
              <transition name="fade">
                <span v-if="!isCollapsed" class="menu-text">{{ item.title }}</span>
              </transition>
              <transition name="fade">
                <svg 
                  v-if="!isCollapsed" 
                  class="arrow-icon"
                  width="16" 
                  height="16" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor"
                >
                  <path d="M6 9l6 6 6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </transition>
            </div>
            
            <transition name="slide">
              <div v-if="!isCollapsed && expandedMenus.includes(item.key)" class="submenu">
                <router-link 
                  v-for="child in item.children" 
                  :key="child.path"
                  :to="child.path"
                  class="submenu-item"
                  :class="{ active: $route.path === child.path }"
                >
                  <span class="dot"></span>
                  <span>{{ child.title }}</span>
                </router-link>
              </div>
            </transition>
          </div>
          
          <router-link 
            v-else
            :to="item.path"
            class="menu-item"
            :class="{ active: $route.path === item.path }"
          >
            <span class="menu-icon">{{ item.icon }}</span>
            <transition name="fade">
              <span v-if="!isCollapsed" class="menu-text">{{ item.title }}</span>
            </transition>
          </router-link>
        </div>
      </nav>
      
      <!-- 底部版本信息 -->
      <transition name="fade">
        <div v-if="!isCollapsed" class="sidebar-footer">
          <p>v2.0.0</p>
          <p class="copyright">© 2024 Agriculture</p>
        </div>
      </transition>
    </aside>
    
    <!-- 主内容区 -->
    <main class="main-content" :class="{ expanded: isCollapsed }">
      <!-- 顶部栏 -->
      <header class="top-bar">
        <div class="breadcrumb">
          <span class="breadcrumb-icon">📍</span>
          <h2 class="page-title">{{ currentTitle }}</h2>
        </div>
        
        <div class="top-actions">
          <!-- 用户头像 -->
          <div class="user-avatar">
            <div class="avatar-circle">
              <span>👨‍🌾</span>
            </div>
          </div>
          
          <!-- 退出按钮 -->
          <button class="logout-btn" @click="logout">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke-width="2"/>
              <polyline points="16 17 21 12 16 7" stroke-width="2"/>
              <line x1="21" y1="12" x2="9" y2="12" stroke-width="2"/>
            </svg>
            <span>退出</span>
          </button>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <div class="page-content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)
const expandedMenus = ref(['resource', 'planning', 'phenology'])

const menuItems = [
  {
    key: 'resource',
    title: '资源信息管理',
    icon: '🌿',
    children: [
      { title: '作物管理', path: '/resource/crops' },
      { title: '地块管理', path: '/resource/plots' }
    ]
  },
  {
    key: 'planning',
    title: '种植规划',
    icon: '📅',
    children: [
      { title: '种植计划', path: '/planning/plans' },
      { title: '种植日历', path: '/planning/calendar' }
    ]
  },
  {
    key: 'phenology',
    title: '物候期监测',
    icon: '🔬',
    children: [
      { title: '物候期记录', path: '/phenology/records' },
      { title: '病虫害识别', path: '/phenology/pests' }
    ]
  },
  {
    key: 'material',
    title: '农资需求',
    icon: '📦',
    children: [
      { title: '农资库存', path: '/material/list' }
    ]
  },
  { title: '采收品质', icon: '🌾', path: '/harvest/records' },
  { title: '产量预估', icon: '📊', path: '/yield/predictions' },
  { title: '智能问答', icon: '🤖', path: '/ai/chat' }
]

const currentTitle = computed(() => {
  const titles = {
    '/resource/crops': '作物管理',
    '/resource/plots': '地块管理',
    '/planning/plans': '种植计划',
    '/planning/calendar': '种植日历',
    '/phenology/records': '物候期记录',
    '/phenology/pests': '病虫害图片识别',
    '/material/list': '农资库存',
    '/harvest/records': '采收记录',
    '/yield/predictions': '产量预估',
    '/ai/chat': '智能问答'
  }
  return titles[route.path] || '种植周期管理系统'
})

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

function toggleMenu(key) {
  const index = expandedMenus.value.indexOf(key)
  if (index > -1) {
    expandedMenus.value.splice(index, 1)
  } else {
    expandedMenus.value.push(key)
  }
}

function logout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
@import '@/assets/styles/design-system.css';

/* ========================================
   布局容器
   ======================================== */
.layout-wrapper {
  display: flex;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
  width: 100%;
}

/* ========================================
   背景装饰
   ======================================== */
.background-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.leaf {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 8s ease-in-out infinite;
}

.leaf-1 {
  top: -100px;
  right: -100px;
  background: linear-gradient(135deg, var(--primary-300), var(--primary-500));
  animation-delay: 0s;
}

.leaf-2 {
  bottom: 20%;
  left: -150px;
  background: linear-gradient(135deg, var(--earth-200), var(--earth-400));
  animation-delay: 2s;
}

.leaf-3 {
  bottom: -100px;
  right: 20%;
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, var(--primary-200), var(--primary-400));
  animation-delay: 4s;
}

/* ========================================
   侧边栏
   ======================================== */
.sidebar {
  width: 280px;
  min-width: 280px;
  min-height: 100vh;
  background: linear-gradient(180deg, var(--soil-900) 0%, var(--soil-800) 100%);
  position: relative;
  z-index: 100;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-2xl);
}

.sidebar.collapsed {
  width: 80px;
  min-width: 80px;
}

/* Logo区域 */
.logo-section {
  padding: var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 80px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
  flex-shrink: 0;
}

.logo-text h1 {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
  color: white;
  margin: 0;
  letter-spacing: -0.02em;
}

.logo-subtitle {
  font-size: var(--text-xs);
  color: var(--primary-400);
  margin-top: var(--space-1);
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* 折叠按钮 */
.collapse-btn {
  position: absolute;
  top: var(--space-4);
  right: -14px;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  background: var(--primary-500);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.collapse-btn:hover {
  background: var(--primary-600);
  transform: scale(1.1);
}

.sidebar.collapsed .collapse-btn svg {
  transform: rotate(180deg);
}

/* ========================================
   导航菜单
   ======================================== */
.nav-menu {
  flex: 1;
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
  overflow-x: hidden;
}

.menu-section {
  margin-bottom: var(--space-2);
}

/* 菜单组 */
.menu-group {
  margin-bottom: var(--space-2);
}

.menu-title {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  color: var(--soil-400);
  cursor: pointer;
  transition: all var(--transition-base);
  font-size: var(--text-sm);
  font-weight: 500;
}

.menu-title:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.menu-title.expanded {
  color: var(--primary-400);
}

.menu-icon {
  font-size: 20px;
  width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.menu-text {
  flex: 1;
  white-space: nowrap;
}

.arrow-icon {
  transition: transform var(--transition-base);
}

.menu-title.expanded .arrow-icon {
  transform: rotate(180deg);
}

/* 子菜单 */
.submenu {
  margin-left: var(--space-6);
  margin-top: var(--space-2);
  overflow: hidden;
}

.submenu-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  color: var(--soil-500);
  text-decoration: none;
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  margin-bottom: var(--space-1);
}

.submenu-item .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--soil-600);
  transition: all var(--transition-base);
}

.submenu-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.05);
}

.submenu-item:hover .dot {
  background: var(--primary-400);
}

.submenu-item.active {
  color: var(--primary-400);
  background: rgba(34, 197, 94, 0.1);
}

.submenu-item.active .dot {
  background: var(--primary-500);
  box-shadow: 0 0 8px var(--primary-500);
}

/* 单个菜单项 */
.menu-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  color: var(--soil-400);
  text-decoration: none;
  transition: all var(--transition-base);
  font-size: var(--text-sm);
  font-weight: 500;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.menu-item.active {
  background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
  color: white;
  box-shadow: var(--shadow-glow);
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.sidebar-footer p {
  font-size: var(--text-xs);
  color: var(--soil-600);
  margin: var(--space-1) 0;
}

.sidebar-footer .copyright {
  font-size: 10px;
}

/* ========================================
   主内容区
   ======================================== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  width: 100%;
  position: relative;
  z-index: 1;
  transition: all var(--transition-base);
}

.main-content.expanded {
  margin-left: 0;
  width: calc(100% - 80px);
}

/* 顶部栏 */
.top-bar {
  height: 70px;
  background: white;
  border-bottom: 1px solid var(--soil-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-8);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 50;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.breadcrumb-icon {
  font-size: 24px;
}

.page-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--soil-800);
  margin: 0;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.user-avatar {
  cursor: pointer;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-400), var(--primary-600));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
}

.avatar-circle:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-lg);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: 1px solid var(--soil-300);
  border-radius: var(--radius-md);
  color: var(--soil-600);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all var(--transition-base);
}

.logout-btn:hover {
  background: var(--danger);
  border-color: var(--danger);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 页面内容 */
.page-content {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
}

/* ========================================
   过渡动画
   ======================================== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-fast);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all var(--transition-base);
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
