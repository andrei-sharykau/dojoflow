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
      path: '/students/create',
      name: 'student-create',
      component: () => import('../views/StudentCreateView.vue'),
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
      path: '/students/:id/edit',
      name: 'student-edit',
      component: () => import('../views/StudentCreateView.vue'),
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
  
  console.log(`Router: переход с ${from.path} на ${to.path}`)
  console.log(`Router: требуется авторизация: ${to.meta.requiresAuth !== false}`)
  
  // Для страницы логина просто пропускаем
  if (to.name === 'login') {
    console.log('Router: переход на страницу логина, пропускаем')
    next()
    return
  }
  
  // Инициализируем auth store если еще не инициализирован
  try {
    const isAuthenticated = await authStore.initialize()
    console.log(`Router: результат инициализации auth store: ${isAuthenticated}`)
    
    // Если маршрут требует аутентификации и пользователь не авторизован
    if (to.meta.requiresAuth !== false && !isAuthenticated) {
      console.log('Router: пользователь не авторизован, перенаправляем на логин')
      next({ name: 'login' })
      return
    }
    
    console.log('Router: пользователь авторизован, продолжаем')
    next()
  } catch (error) {
    console.error('Router: ошибка при инициализации auth store:', error)
    next({ name: 'login' })
  }
})

export default router
