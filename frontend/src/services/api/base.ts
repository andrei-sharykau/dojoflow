/**
 * Базовый API сервис
 */

import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import type { PaginatedResponse, SearchParams, FilterParams } from '@/types'
import { tokenStorage } from '@/utils/storage'

// Типы для ответов API
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status: number
}

export interface ApiError {
  message: string
  status: number
  details?: Record<string, any>
}

// Базовый класс для API сервисов
export class BaseApiService {
  protected client: AxiosInstance
  protected baseURL: string
  protected endpoint: string

  constructor(baseURL = 'http://localhost:8000/api', endpoint = '') {
    this.baseURL = baseURL
    this.endpoint = endpoint
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor для добавления токена
    this.client.interceptors.request.use(
      (config) => {
        const token = tokenStorage.getToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor для обработки ошибок
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config

        // Автоматическое обновление токена при 401 ошибке
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          
          try {
            const refreshToken = tokenStorage.getRefreshToken()
            if (refreshToken) {
              const response = await axios.post('http://localhost:8000/api/auth/refresh/', {
                refresh: refreshToken
              })
              
              const newToken = response.data.access
              tokenStorage.setToken(newToken)
              
              originalRequest.headers.Authorization = `Bearer ${newToken}`
              return this.client(originalRequest)
            }
          } catch (refreshError) {
            // Очищаем токены и перенаправляем на страницу входа
            tokenStorage.clearAllTokens()
            window.location.href = '/login'
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(this.formatError(error))
      }
    )
  }

  private formatError(error: any): ApiError {
    if (error.response) {
      return {
        message: error.response.data?.message || error.response.data?.detail || 'Server error',
        status: error.response.status,
        details: error.response.data
      }
    } else if (error.request) {
      return {
        message: 'Network error',
        status: 0,
        details: error.request
      }
    } else {
      return {
        message: error.message || 'Unknown error',
        status: 0
      }
    }
  }

  // Базовые HTTP методы
  protected async get<T = any>(
    url: string, 
    params?: Record<string, any>
  ): Promise<T> {
    const response = await this.client.get<T>(url, { params })
    return response.data
  }

  protected async post<T = any>(
    url: string, 
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  protected async put<T = any>(
    url: string, 
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  protected async patch<T = any>(
    url: string, 
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  protected async deleteRequest<T = any>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }

  // Утилиты для работы с параметрами
  protected buildQueryParams(params: Record<string, any>): URLSearchParams {
    const searchParams = new URLSearchParams()
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        if (Array.isArray(value)) {
          value.forEach(item => searchParams.append(key, String(item)))
        } else {
          searchParams.append(key, String(value))
        }
      }
    })
    
    return searchParams
  }

  // Метод для загрузки файлов
  protected async uploadFile<T = any>(
    url: string,
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<T> {
    const formData = new FormData()
    formData.append('file', file)

    const config: AxiosRequestConfig = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      },
    }

    const response = await this.client.post<T>(url, formData, config)
    return response.data
  }

  // CRUD операции для совместимости со старым кодом
  async getAll<T>(params?: SearchParams & FilterParams): Promise<PaginatedResponse<T>> {
    return await this.get<PaginatedResponse<T>>(this.endpoint, params)
  }

  async getById<T>(id: number): Promise<T> {
    return await this.get<T>(`${this.endpoint}${id}/`)
  }

  async create<T, U>(data: U): Promise<T> {
    return await this.post<T>(this.endpoint, data)
  }

  async update<T, U>(id: number, data: Partial<U>): Promise<T> {
    return await this.put<T>(`${this.endpoint}${id}/`, data)
  }

  async delete(id: number): Promise<void> {
    await this.deleteRequest(`${this.endpoint}${id}/`)
  }
}

// Создаем экземпляр базового сервиса для использования в других сервисах
export const apiClient = new BaseApiService()

// Хелперы для обработки ошибок
export const isApiError = (error: any): error is ApiError => {
  return error && typeof error.message === 'string' && typeof error.status === 'number'
}

export const getErrorMessage = (error: any): string => {
  if (isApiError(error)) {
    return error.message
  }
  return error?.message || 'Неизвестная ошибка'
} 