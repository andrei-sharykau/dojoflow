/**
 * API сервис для аутентификации
 */

import { useApi } from '@/composables/useApi'
import { API_ENDPOINTS } from '@/constants/api'
import type { 
  User, 
  LoginCredentials, 
  TokenResponse, 
  UserPermissions,
  Club
} from '@/types'

export class AuthApiService {
  private getApi() {
    return useApi()
  }

  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const api = this.getApi()
    return await api.post<TokenResponse>(API_ENDPOINTS.LOGIN, credentials)
  }

  async logout(): Promise<void> {
    const api = this.getApi()
    await api.post(API_ENDPOINTS.LOGOUT)
  }

  async getCurrentUser(): Promise<User> {
    const api = this.getApi()
    return await api.get<User>(API_ENDPOINTS.ME)
  }

  async getUserClubs(): Promise<Club[]> {
    const api = this.getApi()
    return await api.get<Club[]>(API_ENDPOINTS.MY_CLUBS)
  }

  async getUserPermissions(): Promise<UserPermissions> {
    const api = this.getApi()
    return await api.get<UserPermissions>(API_ENDPOINTS.PERMISSIONS)
  }

  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const api = this.getApi()
    return await api.post<TokenResponse>(API_ENDPOINTS.REFRESH, {
      refresh: refreshToken
    })
  }
}

export const authAPI = new AuthApiService() 