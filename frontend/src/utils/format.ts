/**
 * Утилиты форматирования
 */

/**
 * Форматирует номер телефона
 */
export function formatPhoneNumber(phone: string): string {
  if (!phone) return ''
  
  // Убираем все нецифровые символы кроме +
  const cleaned = phone.replace(/[^\d+]/g, '')
  
  // Если номер начинается с 8, заменяем на +7
  if (cleaned.startsWith('8')) {
    return '+7' + cleaned.slice(1)
  }
  
  // Если номер не начинается с +, добавляем +7
  if (!cleaned.startsWith('+')) {
    return '+7' + cleaned
  }
  
  return cleaned
}

/**
 * Форматирует ФИО
 */
export function formatFullName(
  lastName: string, 
  firstName: string, 
  middleName?: string
): string {
  const parts = [lastName, firstName, middleName].filter(Boolean)
  return parts.join(' ')
}

/**
 * Получает инициалы
 */
export function getInitials(
  lastName: string, 
  firstName: string, 
  middleName?: string
): string {
  const parts = [firstName, middleName, lastName].filter(Boolean)
  return parts.map(part => part && part.charAt(0).toUpperCase()).filter(Boolean).join('')
}

/**
 * Форматирует размер файла
 */
export function formatFileSize(bytes: number): string {
  if (!bytes) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Обрезает текст до указанной длины
 */
export function truncateText(text: string, maxLength: number): string {
  if (!text || text.length <= maxLength) return text
  
  return text.slice(0, maxLength) + '...'
}

/**
 * Капитализирует первую букву
 */
export function capitalize(text: string): string {
  if (!text) return ''
  
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase()
}

/**
 * Преобразует строку в camelCase
 */
export function toCamelCase(str: string): string {
  return str
    .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
      return index === 0 ? word.toLowerCase() : word.toUpperCase()
    })
    .replace(/\s+/g, '')
}

/**
 * Преобразует строку в kebab-case
 */
export function toKebabCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase()
}

/**
 * Удаляет HTML теги из строки
 */
export function stripHtml(html: string): string {
  if (!html) return ''
  
  return html.replace(/<[^>]*>/g, '')
}

/**
 * Экранирует HTML символы
 */
export function escapeHtml(text: string): string {
  if (!text) return ''
  
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
} 