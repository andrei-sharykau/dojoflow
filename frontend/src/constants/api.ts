/**
 * API константы
 */

export const API_BASE_URL = 'http://localhost:8000'
export const API_VERSION = 'v1'
export const API_PREFIX = `/api/${API_VERSION}`

// API endpoints
export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login/',
  LOGOUT: '/auth/logout/',
  ME: '/auth/me/',
  
  // Clubs
  CLUBS: '/clubs/',
  CLUBS_STUDENTS: '/clubs/students_by_club/',
  
  // Students
  STUDENTS: '/students/',
  
  // Attestations
  ATTESTATIONS: '/attestations/',
  
  // Attestation Levels
  ATTESTATION_LEVELS: '/attestation_levels/',
} as const

// HTTP статусы
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
} as const

// Заголовки
export const HTTP_HEADERS = {
  CONTENT_TYPE: 'Content-Type',
  AUTHORIZATION: 'Authorization',
  ACCEPT: 'Accept',
} as const

// Типы контента
export const CONTENT_TYPES = {
  JSON: 'application/json',
  FORM_DATA: 'multipart/form-data',
  URL_ENCODED: 'application/x-www-form-urlencoded',
} as const 