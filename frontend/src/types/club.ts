/**
 * Типы для клубов
 */

import type { User } from './user'
import type { Student } from './student'

export interface Club {
  id: number
  name: string
  city: string
  address?: string
  phone?: string
  email?: string
  created_at: string
  updated_at: string
  students_count: number
  admins_count: number
}

export interface ClubDetail extends Club {
  admins: ClubAdmin[]
  recent_students: Student[]
  statistics: ClubStatistics
}

export interface ClubAdmin {
  id: number
  user: User
  created_at: string
}

export interface ClubWithStudents {
  id: number
  name: string
  city: string
  students_count: number
  students: Student[]
}

export interface ClubStatistics {
  total_students: number
  by_level: Record<string, number>
  by_age_group: Record<string, number>
  avg_age: number
}

export interface ClubPermissions {
  can_view: boolean
  can_edit: boolean
  can_delete: boolean
  can_manage_students: boolean
  can_manage_admins: boolean
  role: 'superuser' | 'admin' | 'none'
}

export interface ClubCreateUpdate {
  name: string
  city: string
  address?: string
  phone?: string
  email?: string
} 