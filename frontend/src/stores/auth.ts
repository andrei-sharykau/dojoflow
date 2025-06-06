import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Club, LoginCredentials, UserPermissions } from '../types'
import { authAPI } from '../services/api'
import { tokenStorage } from '../utils/storage'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const userClubs = ref<Club[]>([])
  const permissions = ref<UserPermissions | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const initialized = ref(false)

  const isAuthenticated = computed(() => {
    return !!tokenStorage.getToken() && !!user.value
  })

  const isSuperuser = computed(() => {
    return permissions.value?.is_superuser ?? false
  })

  const isStaff = computed(() => {
    return permissions.value?.is_staff ?? false
  })

  async function login(credentials: LoginCredentials) {
    try {
      loading.value = true
      error.value = null
      
      console.log('Auth: попытка логина для пользователя:', credentials.username)
      const tokens = await authAPI.login(credentials)
      console.log('Auth: получен токен, сохраняем...')
      
      tokenStorage.setToken(tokens.access)
      tokenStorage.setRefreshToken(tokens.refresh)
      
      console.log('Auth: загружаем данные пользователя...')
      await loadUser()
      
      console.log('Auth: логин успешен!')
      return true
    } catch (err: any) {
      console.error('Auth: ошибка логина:', err)
      error.value = err.response?.data?.detail || err.message || 'Ошибка входа в систему'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      console.log('Auth: попытка выхода...')
      await authAPI.logout()
    } catch (err) {
      console.error('Auth: ошибка при выходе:', err)
    } finally {
      console.log('Auth: очищаем локальные данные...')
      user.value = null
      userClubs.value = []
      permissions.value = null
      initialized.value = false
      tokenStorage.clearAllTokens()
    }
  }

  async function loadUser() {
    try {
      const token = tokenStorage.getToken()
      if (!token) {
        console.log('Auth: нет токена для загрузки пользователя')
        return false
      }

      console.log('Auth: есть токен, загружаем данные пользователя...')
      loading.value = true
      
      const [userData, clubsData, permissionsData] = await Promise.all([
        authAPI.getCurrentUser(),
        authAPI.getUserClubs(),
        authAPI.getUserPermissions(),
      ])

      console.log('Auth: данные пользователя загружены:', userData.username)
      user.value = userData
      userClubs.value = clubsData
      permissions.value = permissionsData
      initialized.value = true

      return true
    } catch (err) {
      console.error('Auth: ошибка загрузки пользователя:', err)
      await logout()
      return false
    } finally {
      loading.value = false
    }
  }

  async function checkAuth() {
    // Если уже инициализирован, возвращаем текущее состояние
    if (initialized.value) {
      console.log('Auth: уже инициализирован, возвращаем:', isAuthenticated.value)
      return isAuthenticated.value
    }

    const token = tokenStorage.getToken()
    console.log('Auth: проверяем токен:', token ? 'есть' : 'нет')
    
    if (!token) {
      initialized.value = true
      return false
    }

    // Если есть токен, но нет данных пользователя, загружаем их
    if (!user.value) {
      console.log('Auth: есть токен, но нет данных пользователя, загружаем...')
      const success = await loadUser()
      return success
    }

    console.log('Auth: есть токен и данные пользователя')
    initialized.value = true
    return true
  }

  async function initialize() {
    if (initialized.value) {
      return isAuthenticated.value
    }
    
    return await checkAuth()
  }

  function clearError() {
    error.value = null
  }

  return {
    user,
    userClubs,
    permissions,
    loading,
    error,
    initialized,
    isAuthenticated,
    isSuperuser,
    isStaff,
    login,
    logout,
    loadUser,
    checkAuth,
    initialize,
    clearError,
  }
}) 