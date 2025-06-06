/**
 * Типы для пользователей и аутентификации
 */

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  is_superuser: boolean
  is_staff: boolean
  date_joined: string
  last_login: string | null
  clubs_count: number
  is_club_admin: boolean
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface TokenResponse {
  access: string
  refresh: string
}

export interface UserPermissions {
  is_superuser: boolean
  is_staff: boolean
  clubs_count: number
} 