/**
 * Composable для работы с API
 */
import { ref, computed } from 'vue'
import { API_BASE_URL } from '@/constants/api'
import { 
  handleApiResponse, 
  createFetchOptions, 
  createQueryString, 
  handleApiError 
} from '@/utils/api'
import { tokenStorage } from '@/utils/storage'

export function useApi() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Создает полный URL для API запроса
   */
  const createApiUrl = (endpoint: string, params?: Record<string, any>): string => {
    const baseUrl = `${API_BASE_URL}${endpoint}`
    return params ? `${baseUrl}${createQueryString(params)}` : baseUrl
  }

  /**
   * Обновляет токен через refresh token
   */
  const refreshToken = async (): Promise<string | null> => {
    try {
      const refreshTokenValue = tokenStorage.getRefreshToken()
      if (!refreshTokenValue) {
        console.warn('useApi: нет refresh token для обновления')
        return null
      }

      console.log('useApi: пытаемся обновить токен...')
      const response = await fetch(`${API_BASE_URL}/api/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshTokenValue })
      })

      if (!response.ok) {
        console.error('useApi: не удалось обновить токен:', response.status)
        return null
      }

      const data = await response.json()
      const newToken = data.access
      
      if (newToken) {
        console.log('useApi: токен успешно обновлен')
        tokenStorage.setToken(newToken)
        return newToken
      }

      return null
    } catch (error) {
      console.error('useApi: ошибка при обновлении токена:', error)
      return null
    }
  }

  /**
   * Выполняет API запрос
   */
  const request = async <T>(
    endpoint: string,
    options: {
      method?: string
      body?: any
      params?: Record<string, any>
      headers?: Record<string, string>
      skipAuth?: boolean
      skipTokenRefresh?: boolean
    } = {}
  ): Promise<T> => {
    const { method = 'GET', body, params, headers = {}, skipAuth = false, skipTokenRefresh = false } = options

    loading.value = true
    error.value = null

    try {
      const url = createApiUrl(endpoint, params)
      let token = skipAuth ? undefined : tokenStorage.getToken()
      
      // Логирование для отладки
      console.log(`useApi: ${method} ${endpoint}`, {
        hasToken: !!token,
        tokenLength: token?.length,
        skipAuth,
        body: method !== 'GET' ? body : undefined
      })
      
      const fetchOptions = createFetchOptions({
        method,
        body,
        headers,
        token: token || undefined,
      })

      let response = await fetch(url, fetchOptions)

      // Если получили 401 и не скипаем обновление токена, пытаемся обновить токен
      if (response.status === 401 && !skipAuth && !skipTokenRefresh) {
        console.log('useApi: получен 401, пытаемся обновить токен...')
        const newToken = await refreshToken()
        
        if (newToken) {
          console.log('useApi: повторяем запрос с новым токеном...')
          const newFetchOptions = createFetchOptions({
            method,
            body,
            headers,
            token: newToken,
          })
          response = await fetch(url, newFetchOptions)
        } else {
          console.error('useApi: не удалось обновить токен, перенаправляем на логин')
          // Очищаем токены и перенаправляем на логин
          tokenStorage.clearAllTokens()
          if (typeof window !== 'undefined') {
            window.location.href = '/login'
          }
          throw new Error('Сессия истекла, необходимо войти заново')
        }
      }

      const data = await handleApiResponse<T>(response)
      
      return data
    } catch (err) {
      const errorMessage = handleApiError(err)
      error.value = errorMessage
      console.error(`useApi: ошибка ${method} ${endpoint}:`, err)
      throw new Error(errorMessage)
    } finally {
      loading.value = false
    }
  }

  /**
   * GET запрос
   */
  const get = <T>(endpoint: string, params?: Record<string, any>): Promise<T> => {
    return request<T>(endpoint, { method: 'GET', params })
  }

  /**
   * POST запрос
   */
  const post = <T>(endpoint: string, body?: any): Promise<T> => {
    return request<T>(endpoint, { method: 'POST', body })
  }

  /**
   * PUT запрос
   */
  const put = <T>(endpoint: string, body?: any): Promise<T> => {
    return request<T>(endpoint, { method: 'PUT', body })
  }

  /**
   * PATCH запрос
   */
  const patch = <T>(endpoint: string, body?: any): Promise<T> => {
    return request<T>(endpoint, { method: 'PATCH', body })
  }

  /**
   * DELETE запрос
   */
  const del = <T>(endpoint: string): Promise<T> => {
    return request<T>(endpoint, { method: 'DELETE' })
  }

  /**
   * Сброс состояния
   */
  const reset = () => {
    loading.value = false
    error.value = null
  }

  return {
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    request,
    get,
    post,
    put,
    patch,
    delete: del,
    reset,
  }
} 