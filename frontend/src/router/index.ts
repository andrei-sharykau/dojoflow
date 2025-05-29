import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/students',
      name: 'students',
      component: () => import('../views/StudentsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/students-by-club',
      name: 'students-by-club',
      component: () => import('../views/StudentsByClubView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/students/:id',
      name: 'student-detail',
      component: () => import('../views/StudentDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/attestations',
      name: 'attestations',
      component: () => import('../views/AttestationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/dashboard'
    }
  ]
})

// Проверка аутентификации перед каждым переходом
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Инициализируем auth store если еще не инициализирован
  const isAuthenticated = await authStore.initialize()
  
  // Если пользователь авторизован и идет на страницу логина, перенаправляем на дашборд
  if (to.name === 'login' && isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }
  
  // Если маршрут требует аутентификации и пользователь не авторизован
  if (to.meta.requiresAuth !== false && !isAuthenticated) {
    next({ name: 'login' })
    return
  }
  
  next()
})

export default router
