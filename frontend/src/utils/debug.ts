/**
 * Утилиты для отладки
 */

import { tokenStorage } from './storage'

export function debugAuthTokens() {
  const token = tokenStorage.getToken()
  const refreshToken = tokenStorage.getRefreshToken()
  
  console.log('=== DEBUG: Проверка токенов ===')
  console.log('Access token:', token ? `${token.substring(0, 20)}...` : 'НЕТ')
  console.log('Refresh token:', refreshToken ? `${refreshToken.substring(0, 20)}...` : 'НЕТ')
  console.log('Token length:', token?.length || 0)
  console.log('Refresh token length:', refreshToken?.length || 0)
  
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const now = Math.floor(Date.now() / 1000)
      const isExpired = payload.exp < now
      
      console.log('Token payload:', payload)
      console.log('Token expires:', new Date(payload.exp * 1000).toLocaleString())
      console.log('Token is expired:', isExpired)
      console.log('Current time:', new Date().toLocaleString())
    } catch (e) {
      console.error('Ошибка при разборе токена:', e)
    }
  }
  
  console.log('=== Конец отладки токенов ===')
}

// Глобальная функция для отладки в консоли браузера
if (typeof window !== 'undefined') {
  (window as any).debugAuthTokens = debugAuthTokens
} 