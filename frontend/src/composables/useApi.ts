/**
 * Composable для работы с API
 */
import { ref, computed } from 'vue'
import { API_BASE_URL, API_PREFIX } from '@/constants/api'
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
    const baseUrl = `${API_BASE_URL}${API_PREFIX}${endpoint}`
    return params ? `${baseUrl}${createQueryString(params)}` : baseUrl
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
    } = {}
  ): Promise<T> => {
    const { method = 'GET', body, params, headers = {}, skipAuth = false } = options

    loading.value = true
    error.value = null

    try {
      const url = createApiUrl(endpoint, params)
      const token = skipAuth ? undefined : tokenStorage.getToken()
      
      const fetchOptions = createFetchOptions({
        method,
        body,
        headers,
        token: token || undefined,
      })

      const response = await fetch(url, fetchOptions)
      const data = await handleApiResponse<T>(response)
      
      return data
    } catch (err) {
      const errorMessage = handleApiError(err)
      error.value = errorMessage
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