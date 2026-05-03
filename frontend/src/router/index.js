import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/login/Login.vue'), meta: { guest: true } },
  {
    path: '/',
    component: () => import('@/views/layout/Layout.vue'),
    redirect: '/resource/crops',
    children: [
      { path: 'resource/crops', name: 'Crops', component: () => import('@/views/resource/CropList.vue') },
      { path: 'resource/plots', name: 'Plots', component: () => import('@/views/resource/PlotList.vue') },
      { path: 'planning/plans', name: 'Plans', component: () => import('@/views/planning/PlanList.vue') },
      { path: 'planning/calendar', name: 'Calendar', component: () => import('@/views/planning/Calendar.vue') },
      { path: 'phenology/records', name: 'Phenology', component: () => import('@/views/phenology/PhenologyList.vue') },
      { path: 'phenology/pests', name: 'Pests', component: () => import('@/views/phenology/PestList.vue') },
      { path: 'material/list', name: 'Material', component: () => import('@/views/material/MaterialList.vue') },
      { path: 'harvest/records', name: 'Harvest', component: () => import('@/views/harvest/HarvestList.vue') },
      { path: 'yield/predictions', name: 'Yield', component: () => import('@/views/yield/YieldList.vue') },
      { path: 'ai/chat', name: 'AiChat', component: () => import('@/views/ai-chat/Chat.vue') }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.guest) {
    if (token) next({ path: '/' })
    else next()
  } else {
    if (!token && to.path !== '/login') next({ path: '/login' })
    else next()
  }
})

export default router
