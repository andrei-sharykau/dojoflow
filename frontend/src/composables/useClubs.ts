/**
 * Composable для работы с клубами
 */
import { ref, computed } from 'vue'
import { useApi } from './useApi'
import { API_ENDPOINTS } from '@/constants/api'

export interface Club {
  id: number
  name: string
  city: string
  created_at: string
  students_count: number
}

export interface ClubsStudentsData {
  id: number
  name: string
  city: string
  students_count: number
  students: any[]
}

export function useClubs() {
  const api = useApi()
  
  const clubs = ref<Club[]>([])
  const clubsWithStudents = ref<ClubsStudentsData[]>([])
  const currentClub = ref<Club | null>(null)

  const loading = computed(() => api.loading.value)
  const error = computed(() => api.error.value)

  /**
   * Получает клубы пользователя
   */
  const fetchUserClubs = async (): Promise<Club[]> => {
    const userClubs = await api.get<Club[]>(API_ENDPOINTS.CLUBS)
    clubs.value = userClubs
    return userClubs
  }

  /**
   * Получает студентов по клубам
   */
  const fetchStudentsByClub = async (search?: string): Promise<ClubsStudentsData[]> => {
    const params = search ? { search } : {}
    const data = await api.get<ClubsStudentsData[]>(API_ENDPOINTS.CLUBS_STUDENTS, params)
    clubsWithStudents.value = data
    return data
  }

  /**
   * Получает клуб по ID
   */
  const fetchClub = async (id: number): Promise<Club> => {
    const club = await api.get<Club>(`${API_ENDPOINTS.CLUBS}${id}/`)
    currentClub.value = club
    return club
  }

  /**
   * Устанавливает текущий клуб
   */
  const setCurrentClub = (club: Club | null) => {
    currentClub.value = club
  }

  /**
   * Найти клуб по ID
   */
  const findClubById = (id: number): Club | undefined => {
    return clubs.value.find(club => club.id === id)
  }

  /**
   * Сброс состояния
   */
  const reset = () => {
    clubs.value = []
    clubsWithStudents.value = []
    currentClub.value = null
    api.reset()
  }

  return {
    // State
    clubs: computed(() => clubs.value),
    clubsWithStudents: computed(() => clubsWithStudents.value),
    currentClub: computed(() => currentClub.value),
    loading,
    error,
    
    // Actions
    fetchUserClubs,
    fetchStudentsByClub,
    fetchClub,
    setCurrentClub,
    findClubById,
    reset,
  }
} 