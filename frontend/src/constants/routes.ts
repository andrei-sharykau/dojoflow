/**
 * Константы маршрутов
 */

export const ROUTE_NAMES = {
  // Auth
  LOGIN: 'login',
  
  // Main
  DASHBOARD: 'dashboard',
  
  // Students
  STUDENTS: 'students',
  STUDENTS_BY_CLUB: 'students-by-club',
  STUDENT_DETAIL: 'student-detail',
  STUDENT_CREATE: 'student-create',
  STUDENT_EDIT: 'student-edit',
  
  // Attestations
  ATTESTATIONS: 'attestations',
  ATTESTATION_DETAIL: 'attestation-detail',
  ATTESTATION_CREATE: 'attestation-create',
  ATTESTATION_EDIT: 'attestation-edit',
  
  // Clubs
  CLUBS: 'clubs',
  CLUB_DETAIL: 'club-detail',
} as const

export const ROUTE_PATHS = {
  // Auth
  LOGIN: '/login',
  
  // Main
  DASHBOARD: '/dashboard',
  HOME: '/',
  
  // Students
  STUDENTS: '/students',
  STUDENTS_BY_CLUB: '/students-by-club',
  STUDENT_DETAIL: '/students/:id',
  STUDENT_CREATE: '/students/create',
  STUDENT_EDIT: '/students/:id/edit',
  
  // Attestations
  ATTESTATIONS: '/attestations',
  ATTESTATION_DETAIL: '/attestations/:id',
  ATTESTATION_CREATE: '/attestations/create',
  ATTESTATION_EDIT: '/attestations/:id/edit',
  
  // Clubs
  CLUBS: '/clubs',
  CLUB_DETAIL: '/clubs/:id',
} as const

// Защищенные маршруты (требуют авторизации)
export const PROTECTED_ROUTES = [
  ROUTE_NAMES.DASHBOARD,
  ROUTE_NAMES.STUDENTS,
  ROUTE_NAMES.STUDENTS_BY_CLUB,
  ROUTE_NAMES.STUDENT_DETAIL,
  ROUTE_NAMES.STUDENT_CREATE,
  ROUTE_NAMES.STUDENT_EDIT,
  ROUTE_NAMES.ATTESTATIONS,
  ROUTE_NAMES.ATTESTATION_DETAIL,
  ROUTE_NAMES.ATTESTATION_CREATE,
  ROUTE_NAMES.ATTESTATION_EDIT,
  ROUTE_NAMES.CLUBS,
  ROUTE_NAMES.CLUB_DETAIL,
] as const

// Публичные маршруты (не требуют авторизации)
export const PUBLIC_ROUTES = [
  ROUTE_NAMES.LOGIN,
] as const 