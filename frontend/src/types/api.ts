/**
 * Базовые типы для API
 */

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  results: T[]
  pagination: {
    count: number
    page: number
    pages: number
    page_size: number
    next: string | null
    previous: string | null
    has_next: boolean
    has_previous: boolean
  }
}

export interface SearchParams {
  search?: string
  page?: number
  page_size?: number
}

export interface FilterParams {
  [key: string]: string | number | boolean | undefined
} 