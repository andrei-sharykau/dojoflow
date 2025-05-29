/**
 * Утилиты для работы с датами
 */

/**
 * Вычисляет возраст по дате рождения
 */
export function calculateAge(birthDate: string | Date): number | null {
  if (!birthDate) return null
  
  const birth = new Date(birthDate)
  const today = new Date()
  
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  
  return age
}

/**
 * Вычисляет количество лет практики
 */
export function calculateYearsOfPractice(startDate: string | Date): number | null {
  if (!startDate) return null
  
  const start = new Date(startDate)
  const today = new Date()
  
  let years = today.getFullYear() - start.getFullYear()
  const monthDiff = today.getMonth() - start.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < start.getDate())) {
    years--
  }
  
  return Math.max(0, years)
}

/**
 * Форматирует дату в локальном формате
 */
export function formatDate(date: string | Date, locale = 'ru-RU'): string {
  if (!date) return ''
  
  return new Date(date).toLocaleDateString(locale)
}

/**
 * Форматирует дату с временем
 */
export function formatDateTime(date: string | Date, locale = 'ru-RU'): string {
  if (!date) return ''
  
  return new Date(date).toLocaleString(locale)
}

/**
 * Получает относительное время (например, "2 дня назад")
 */
export function getRelativeTime(date: string | Date, locale = 'ru'): string {
  if (!date) return ''
  
  const now = new Date()
  const target = new Date(date)
  const diffInSeconds = Math.floor((now.getTime() - target.getTime()) / 1000)
  
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' })
  
  if (diffInSeconds < 60) {
    return rtf.format(-diffInSeconds, 'second')
  } else if (diffInSeconds < 3600) {
    return rtf.format(-Math.floor(diffInSeconds / 60), 'minute')
  } else if (diffInSeconds < 86400) {
    return rtf.format(-Math.floor(diffInSeconds / 3600), 'hour')
  } else if (diffInSeconds < 2592000) {
    return rtf.format(-Math.floor(diffInSeconds / 86400), 'day')
  } else if (diffInSeconds < 31536000) {
    return rtf.format(-Math.floor(diffInSeconds / 2592000), 'month')
  } else {
    return rtf.format(-Math.floor(diffInSeconds / 31536000), 'year')
  }
}

/**
 * Проверяет, является ли дата сегодняшней
 */
export function isToday(date: string | Date): boolean {
  if (!date) return false
  
  const target = new Date(date)
  const today = new Date()
  
  return (
    target.getDate() === today.getDate() &&
    target.getMonth() === today.getMonth() &&
    target.getFullYear() === today.getFullYear()
  )
}

/**
 * Получает начало дня
 */
export function startOfDay(date: string | Date = new Date()): Date {
  const result = new Date(date)
  result.setHours(0, 0, 0, 0)
  return result
}

/**
 * Получает конец дня
 */
export function endOfDay(date: string | Date = new Date()): Date {
  const result = new Date(date)
  result.setHours(23, 59, 59, 999)
  return result
}