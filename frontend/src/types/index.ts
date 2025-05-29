export interface User {
  id: number
  username: string
  first_name: string
  last_name: string
  email: string
}

export interface Club {
  id: number
  name: string
  city: string
  created_at: string
  students_count: number
}

export interface ClubWithStudents {
  id: number
  name: string
  city: string
  students_count: number
  students: Student[]
}

export interface AttestationLevel {
  id: number
  level: string
  display_name: string
  order: number
}

export interface Student {
  id: number
  club: number
  club_name: string
  last_name: string
  first_name: string
  middle_name: string
  full_name: string
  birth_date: string
  age: number
  city: string
  address: string
  phone: string
  workplace: string
  start_date: string
  current_level: number
  current_level_display: string
  last_attestation_date: string | null
  attestations?: Attestation[]
  created_at: string
  updated_at: string
}

export interface StudentCreate {
  club: number
  last_name: string
  first_name: string
  middle_name: string
  birth_date: string
  city: string
  address: string
  phone: string
  workplace: string
  start_date: string
  current_level: number
  last_attestation_date: string | null
}

export interface Attestation {
  id: number
  student: number
  student_name: string
  level: number
  level_display: string
  date: string
  city: string
  notes: string
  created_at: string
}

export interface AttestationCreate {
  student: number
  level: number
  date: string
  city: string
  notes?: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface TokenResponse {
  access: string
  refresh: string
}

export interface PaginatedResponse<T> {
  results: T[]
  count: number
  next: string | null
  previous: string | null
}

export interface UserPermissions {
  is_superuser: boolean
  is_staff: boolean
  clubs_count: number
} 