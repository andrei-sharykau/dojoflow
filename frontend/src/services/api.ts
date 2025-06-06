/**
 * Основной файл API сервисов
 * Экспортирует все API сервисы для удобного импорта
 */

// Импортируем сервисы
import { authAPI } from './api/auth'
import { clubsAPI } from './api/clubs'
import { attestationsAPI } from './api/attestations'
import { attestationLevelsAPI } from './api/attestation-levels'
import { studentsService, StudentsService } from './api/students'
import { BaseApiService, apiClient, isApiError, getErrorMessage } from './api/base'

// Экспортируем новые сервисы
export { studentsService, StudentsService }
export { BaseApiService, apiClient, isApiError, getErrorMessage }
export type { ApiResponse, ApiError } from './api/base'

// Экспортируем старые сервисы для обратной совместимости
export { authAPI } from './api/auth'
export { clubsAPI } from './api/clubs'
export { attestationsAPI } from './api/attestations'
export { attestationLevelsAPI } from './api/attestation-levels'

// Псевдоним для обратной совместимости
export { studentsService as studentsAPI }

// Основной объект API для удобного использования
export const api = {
  auth: authAPI,
  students: studentsService,
  clubs: clubsAPI,
  attestations: attestationsAPI,
  attestationLevels: attestationLevelsAPI
} 