/**
 * Базовый API сервис
 */

import { useApi } from '@/composables/useApi'
import type { PaginatedResponse, SearchParams, FilterParams } from '@/types'

export class BaseApiService {
  protected endpoint: string

  constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  protected getApi() {
    return useApi()
  }

  async getAll<T>(params?: SearchParams & FilterParams): Promise<PaginatedResponse<T>> {
    const api = this.getApi()
    return await api.get<PaginatedResponse<T>>(this.endpoint, params)
  }

  async getById<T>(id: number): Promise<T> {
    const api = this.getApi()
    return await api.get<T>(`${this.endpoint}${id}/`)
  }

  async create<T, U>(data: U): Promise<T> {
    const api = this.getApi()
    return await api.post<T>(this.endpoint, data)
  }

  async update<T, U>(id: number, data: Partial<U>): Promise<T> {
    const api = this.getApi()
    return await api.patch<T>(`${this.endpoint}${id}/`, data)
  }

  async delete(id: number): Promise<void> {
    const api = this.getApi()
    await api.delete(`${this.endpoint}${id}/`)
  }
} 