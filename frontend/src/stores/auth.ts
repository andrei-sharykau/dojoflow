import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Club, LoginCredentials, UserPermissions } from '../types'
import { authAPI } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const userClubs = ref<Club[]>([])
  const permissions = ref<UserPermissions | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const initialized = ref(false)

  const isAuthenticated = computed(() => {
    return !!localStorage.getItem('access_token') && !!user.value
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
      
      const tokens = await authAPI.login(credentials)
      
      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)
      
      await loadUser()
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ошибка входа в систему'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authAPI.logout()
    } catch (err) {
      console.error('Ошибка при выходе:', err)
    } finally {
      user.value = null
      userClubs.value = []
      permissions.value = null
      initialized.value = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  async function loadUser() {
    try {
      if (!localStorage.getItem('access_token')) {
        return false
      }

      loading.value = true
      
      const [userData, clubsData, permissionsData] = await Promise.all([
        authAPI.getCurrentUser(),
        authAPI.getUserClubs(),
        authAPI.getUserPermissions(),
      ])

      user.value = userData
      userClubs.value = clubsData
      permissions.value = permissionsData
      initialized.value = true

      return true
    } catch (err) {
      console.error('Ошибка загрузки пользователя:', err)
      await logout()
      return false
    } finally {
      loading.value = false
    }
  }

  async function checkAuth() {
    // Если уже инициализирован, возвращаем текущее состояние
    if (initialized.value) {
      return isAuthenticated.value
    }

    const token = localStorage.getItem('access_token')
    if (!token) {
      initialized.value = true
      return false
    }

    // Если есть токен, но нет данных пользователя, загружаем их
    if (!user.value) {
      const success = await loadUser()
      return success
    }

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