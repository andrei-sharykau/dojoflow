/**
 * Основной файл API сервисов
 * Экспортирует все API сервисы для удобного импорта
 */

// Экспорт всех API сервисов
export { authAPI } from './api/auth'
export { clubsAPI } from './api/clubs'
export { studentsAPI } from './api/students'
export { attestationsAPI } from './api/attestations'
export { attestationLevelsAPI } from './api/attestation-levels'

// Экспорт базового сервиса для расширения
export { BaseApiService } from './api/base' 