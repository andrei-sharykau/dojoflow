/**
 * Утилиты для работы с локальным хранилищем
 */

/**
 * Безопасное сохранение в localStorage
 */
export function setLocalStorage<T>(key: string, value: T): void {
  try {
    const serializedValue = JSON.stringify(value)
    localStorage.setItem(key, serializedValue)
  } catch (error) {
    console.error('Ошибка сохранения в localStorage:', error)
  }
}

/**
 * Безопасное получение из localStorage
 */
export function getLocalStorage<T>(key: string, defaultValue?: T): T | null {
  try {
    const item = localStorage.getItem(key)
    return item ? JSON.parse(item) : defaultValue || null
  } catch (error) {
    console.error('Ошибка чтения из localStorage:', error)
    return defaultValue || null
  }
}

/**
 * Удаление из localStorage
 */
export function removeLocalStorage(key: string): void {
  try {
    localStorage.removeItem(key)
  } catch (error) {
    console.error('Ошибка удаления из localStorage:', error)
  }
}

/**
 * Очистка localStorage
 */
export function clearLocalStorage(): void {
  try {
    localStorage.clear()
  } catch (error) {
    console.error('Ошибка очистки localStorage:', error)
  }
}

/**
 * Проверка поддержки localStorage
 */
export function isLocalStorageAvailable(): boolean {
  try {
    const test = '__localStorage_test__'
    localStorage.setItem(test, test)
    localStorage.removeItem(test)
    return true
  } catch {
    return false
  }
}

/**
 * Безопасное сохранение в sessionStorage
 */
export function setSessionStorage<T>(key: string, value: T): void {
  try {
    const serializedValue = JSON.stringify(value)
    sessionStorage.setItem(key, serializedValue)
  } catch (error) {
    console.error('Ошибка сохранения в sessionStorage:', error)
  }
}

/**
 * Безопасное получение из sessionStorage
 */
export function getSessionStorage<T>(key: string, defaultValue?: T): T | null {
  try {
    const item = sessionStorage.getItem(key)
    return item ? JSON.parse(item) : defaultValue || null
  } catch (error) {
    console.error('Ошибка чтения из sessionStorage:', error)
    return defaultValue || null
  }
}

/**
 * Удаление из sessionStorage
 */
export function removeSessionStorage(key: string): void {
  try {
    sessionStorage.removeItem(key)
  } catch (error) {
    console.error('Ошибка удаления из sessionStorage:', error)
  }
}

/**
 * Ключи для хранения данных приложения
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'dojoflow_auth_token',
  REFRESH_TOKEN: 'dojoflow_refresh_token',
  USER_DATA: 'dojoflow_user_data',
  USER_PREFERENCES: 'dojoflow_user_preferences',
  LAST_SELECTED_CLUB: 'dojoflow_last_club',
  TABLE_SETTINGS: 'dojoflow_table_settings',
  THEME: 'dojoflow_theme',
} as const

/**
 * Специализированные функции для токенов
 */
export const tokenStorage = {
  setToken: (token: string) => setLocalStorage(STORAGE_KEYS.AUTH_TOKEN, token),
  getToken: () => getLocalStorage<string>(STORAGE_KEYS.AUTH_TOKEN),
  removeToken: () => removeLocalStorage(STORAGE_KEYS.AUTH_TOKEN),
  
  setRefreshToken: (token: string) => setLocalStorage(STORAGE_KEYS.REFRESH_TOKEN, token),
  getRefreshToken: () => getLocalStorage<string>(STORAGE_KEYS.REFRESH_TOKEN),
  removeRefreshToken: () => removeLocalStorage(STORAGE_KEYS.REFRESH_TOKEN),
  
  clearAllTokens: () => {
    removeLocalStorage(STORAGE_KEYS.AUTH_TOKEN)
    removeLocalStorage(STORAGE_KEYS.REFRESH_TOKEN)
  }
}

/**
 * Специализированные функции для пользователя
 */
export const userStorage = {
  setUserData: (user: any) => setLocalStorage(STORAGE_KEYS.USER_DATA, user),
  getUserData: () => getLocalStorage(STORAGE_KEYS.USER_DATA),
  removeUserData: () => removeLocalStorage(STORAGE_KEYS.USER_DATA),
  
  setLastSelectedClub: (clubId: number) => setLocalStorage(STORAGE_KEYS.LAST_SELECTED_CLUB, clubId),
  getLastSelectedClub: () => getLocalStorage<number>(STORAGE_KEYS.LAST_SELECTED_CLUB),
  
  setPreferences: (preferences: any) => setLocalStorage(STORAGE_KEYS.USER_PREFERENCES, preferences),
  getPreferences: () => getLocalStorage(STORAGE_KEYS.USER_PREFERENCES, {}),
} 