/**
 * Типы для аттестаций и уровней
 */

export interface AttestationLevel {
  id: number
  level: string
  display_name: string
  order: number
  students_count: number
  next_level: AttestationLevel | null
  previous_level: AttestationLevel | null
}

export interface Attestation {
  id: number
  student: number
  student_name: string
  level: number
  level_display: string
  club_name: string
  date: string
  city: string
  created_at: string
}

export interface AttestationDetail extends Attestation {
  student_info: {
    id: number
    full_name: string
    age: number
    club: string
    start_date: string
    phone: string
    city: string
  }
  level_info: {
    id: number
    level: string
    display_name: string
    order: number
  }
  attestation_context: {
    time_since_start_days: number | null
    time_since_previous_days: number | null
    previous_attestations: Array<{
      date: string
      level: string
      city: string
    }>
    next_attestations: Array<{
      date: string
      level: string
      city: string
    }>
  }
}

export interface AttestationCreateUpdate {
  student: number
  level: number
  date: string
  city: string
}

export interface AttestationFilters {
  search?: string
  student?: number
  club?: number
  level?: number
  date_after?: string
  date_before?: string
  city?: string
  page?: number
  page_size?: number
  [key: string]: string | number | boolean | undefined
}

export interface AttestationHistory {
  id: number
  date: string
  level: {
    id: number
    name: string
    order: number
  }
  city: string
  time_since_previous_days: number | null
  level_progress: 'new' | 'up' | 'same' | 'down'
  created_at: string
} 