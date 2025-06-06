/**
 * Утилиты для работы с API
 */

/**
 * Обрабатывает ответы API
 */
export async function handleApiResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `HTTP Error: ${response.status}`
    let errorDetails: any = null
    
    try {
      const errorData = await response.json()
      errorDetails = errorData
      
      // Специальная обработка для разных типов ошибок
      if (response.status === 401) {
        errorMessage = errorData.detail || 'Не авторизован. Войдите в систему.'
      } else if (response.status === 403) {
        errorMessage = errorData.detail || 'Недостаточно прав для выполнения операции'
      } else if (response.status === 400) {
        if (errorData.detail) {
          errorMessage = errorData.detail
        } else if (typeof errorData === 'object') {
          // Обработка ошибок валидации
          const validationErrors = []
          for (const [field, messages] of Object.entries(errorData)) {
            if (Array.isArray(messages)) {
              validationErrors.push(`${field}: ${messages.join(', ')}`)
            } else if (typeof messages === 'string') {
              validationErrors.push(`${field}: ${messages}`)
            }
          }
          if (validationErrors.length > 0) {
            errorMessage = `Ошибка валидации: ${validationErrors.join('; ')}`
          }
        } else {
          errorMessage = 'Некорректный запрос'
        }
      } else {
        errorMessage = errorData.message || errorData.error || errorMessage
      }
    } catch {
      // Если не удалось распарсить JSON, используем статус
      if (response.status === 401) {
        errorMessage = 'Не авторизован. Войдите в систему.'
      } else if (response.status === 403) {
        errorMessage = 'Недостаточно прав для выполнения операции'
      } else if (response.status === 404) {
        errorMessage = 'Ресурс не найден'
      } else if (response.status >= 500) {
        errorMessage = 'Ошибка сервера. Попробуйте позже.'
      }
    }
    
    console.error('API Error:', {
      status: response.status,
      statusText: response.statusText,
      url: response.url,
      details: errorDetails,
      message: errorMessage
    })
    
    throw new Error(errorMessage)
  }
  
  // Если ответ пустой (например, 204 No Content)
  if (response.status === 204) {
    return null as T
  }
  
  return await response.json()
}

/**
 * Создает параметры для fetch запроса
 */
export function createFetchOptions(options: {
  method?: string
  body?: any
  headers?: Record<string, string>
  token?: string
}): RequestInit {
  const { method = 'GET', body, headers = {}, token } = options
  
  const fetchOptions: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  }
  
  // Добавляем токен авторизации
  if (token) {
    fetchOptions.headers = {
      ...fetchOptions.headers,
      Authorization: `Bearer ${token}`,
    }
  }
  
  // Добавляем body для POST/PUT/PATCH запросов
  if (body && method !== 'GET' && method !== 'DELETE') {
    if (body instanceof FormData) {
      // Для FormData удаляем Content-Type, браузер установит его автоматически
      delete (fetchOptions.headers as Record<string, string>)['Content-Type']
      fetchOptions.body = body
    } else {
      fetchOptions.body = JSON.stringify(body)
    }
  }
  
  return fetchOptions
}

/**
 * Создает query string из объекта параметров
 */
export function createQueryString(params: Record<string, any>): string {
  const searchParams = new URLSearchParams()
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(item => searchParams.append(key, String(item)))
      } else {
        searchParams.append(key, String(value))
      }
    }
  })
  
  const queryString = searchParams.toString()
  return queryString ? `?${queryString}` : ''
}

/**
 * Обрабатывает ошибки API
 */
export function handleApiError(error: any): string {
  if (error instanceof Error) {
    return error.message
  }
  
  if (typeof error === 'string') {
    return error
  }
  
  if (error?.response?.data?.message) {
    return error.response.data.message
  }
  
  if (error?.response?.data?.error) {
    return error.response.data.error
  }
  
  return 'Произошла неизвестная ошибка'
}

/**
 * Задержка для имитации загрузки (для разработки)
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Retry функция для повторных запросов
 */
export async function retryRequest<T>(
  requestFn: () => Promise<T>,
  maxRetries = 3,
  retryDelay = 1000
): Promise<T> {
  let lastError: Error
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await requestFn()
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error))
      
      if (i === maxRetries) {
        throw lastError
      }
      
      // Экспоненциальная задержка
      await delay(retryDelay * Math.pow(2, i))
    }
  }
  
  throw lastError!
}

/**
 * Проверяет доступность сети
 */
export function isOnline(): boolean {
  return navigator.onLine
}

/**
 * Отменяемый fetch
 */
export class CancellableRequest {
  private controller = new AbortController()
  
  async fetch<T>(url: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(url, {
      ...options,
      signal: this.controller.signal,
    })
    
    return handleApiResponse<T>(response)
  }
  
  cancel(): void {
    this.controller.abort()
  }
} 