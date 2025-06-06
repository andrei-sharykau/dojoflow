/**
 * Типы для студентов
 */

import type { AttestationLevel, Attestation } from './attestation'

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
  years_of_practice: number
  city: string
  address?: string
  phone?: string
  workplace?: string
  start_date: string
  current_level: number | null
  current_level_display: string | null
  last_attestation_date: string | null
  created_at: string
  updated_at?: string
}

export interface StudentDetail extends Student {
  attestations: Attestation[]
  next_attestation_eligible: {
    eligible: boolean
    next_level: string | null
    reason: string
  }
}

export interface StudentCreateUpdate {
  club: number
  last_name: string
  first_name: string
  middle_name: string
  birth_date: string
  city: string
  address?: string
  phone?: string
  workplace?: string
  start_date: string
  current_level?: number
}

export interface StudentFilters {
  search?: string
  club?: number
  city?: string
  level?: number
  min_age?: number
  max_age?: number
  start_date_after?: string
  start_date_before?: string
  page?: number
  page_size?: number
  [key: string]: string | number | boolean | undefined
}

export interface StudentStatistics {
  total_students: number
  by_level: Record<string, number>
  by_age_group: Record<string, number>
  by_city: Record<string, number>
  avg_age: number
  avg_years_practice: number
  recent_joiners: number
  need_attestation: number
} 