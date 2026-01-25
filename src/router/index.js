import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

// Lazy-load pages for better performance
const HomePage = () => import('@/pages/HomePage.vue')
const PlatformPage = () => import('@/pages/PlatformPage.vue')
const ContactPage = () => import('@/pages/ContactPage.vue')

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: HomePage,
      },
      {
        path: 'platform',
        name: 'platform',
        component: PlatformPage,
      },
      {
        path: 'contact',
        name: 'contact',
        component: ContactPage,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  },
})

export default router
