/**
 * Утилиты валидации
 */

/**
 * Проверяет email
 */
export function isValidEmail(email: string): boolean {
  if (!email) return false
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Проверяет телефон
 */
export function isValidPhone(phone: string): boolean {
  if (!phone) return false
  
  // Убираем все нецифровые символы кроме +
  const cleaned = phone.replace(/[^\d+]/g, '')
  
  // Проверяем формат
  return /^\+?\d{10,15}$/.test(cleaned)
}

/**
 * Проверяет пароль
 */
export function isValidPassword(password: string): boolean {
  if (!password) return false
  
  // Минимум 8 символов, хотя бы одна буква и одна цифра
  return password.length >= 8 && /[a-zA-Z]/.test(password) && /\d/.test(password)
}

/**
 * Проверяет дату рождения
 */
export function isValidBirthDate(birthDate: string | Date): boolean {
  if (!birthDate) return false
  
  const date = new Date(birthDate)
  const today = new Date()
  
  // Дата должна быть в прошлом
  if (date >= today) return false
  
  // Возраст не должен быть больше 150 лет
  const age = today.getFullYear() - date.getFullYear()
  if (age > 150) return false
  
  // Минимальный возраст 3 года
  if (age < 3) return false
  
  return true
}

/**
 * Проверяет дату в будущем
 */
export function isDateNotInFuture(date: string | Date): boolean {
  if (!date) return true
  
  const target = new Date(date)
  const today = new Date()
  
  return target <= today
}

/**
 * Проверяет обязательное поле
 */
export function isRequired(value: any): boolean {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  
  return true
}

/**
 * Проверяет минимальную длину
 */
export function hasMinLength(value: string, minLength: number): boolean {
  if (!value) return false
  
  return value.length >= minLength
}

/**
 * Проверяет максимальную длину
 */
export function hasMaxLength(value: string, maxLength: number): boolean {
  if (!value) return true
  
  return value.length <= maxLength
}

/**
 * Проверяет числовое значение в диапазоне
 */
export function isInRange(value: number, min: number, max: number): boolean {
  return value >= min && value <= max
}

/**
 * Проверяет URL
 */
export function isValidUrl(url: string): boolean {
  if (!url) return false
  
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Создает правила валидации для формы
 */
export const validationRules = {
  required: (message = 'Поле обязательно для заполнения') => 
    (value: any) => isRequired(value) || message,
  
  email: (message = 'Некорректный email') => 
    (value: string) => !value || isValidEmail(value) || message,
  
  phone: (message = 'Некорректный номер телефона') => 
    (value: string) => !value || isValidPhone(value) || message,
  
  minLength: (min: number, message?: string) => 
    (value: string) => {
      const msg = message || `Минимальная длина ${min} символов`
      return !value || hasMinLength(value, min) || msg
    },
  
  maxLength: (max: number, message?: string) => 
    (value: string) => {
      const msg = message || `Максимальная длина ${max} символов`
      return !value || hasMaxLength(value, max) || msg
    },
  
  birthDate: (message = 'Некорректная дата рождения') => 
    (value: string) => !value || isValidBirthDate(value) || message,
  
  pastDate: (message = 'Дата не может быть в будущем') => 
    (value: string) => !value || isDateNotInFuture(value) || message,
} 