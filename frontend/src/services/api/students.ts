/**
 * API сервис для работы со студентами
 */

import { BaseApiService } from './base'
import type { 
  Student, 
  StudentDetail, 
  StudentCreateUpdate, 
  StudentFilters,
  StudentStatistics,
  PaginatedResponse 
} from '@/types'

export class StudentsService extends BaseApiService {
  constructor() {
    super('http://localhost:8000/api', '/students/')
  }

  // Получение списка студентов с фильтрацией
  async getStudents(filters?: StudentFilters): Promise<PaginatedResponse<Student>> {
    return this.get<PaginatedResponse<Student>>('/students/', filters)
  }

  // Получение детальной информации о студенте
  async getDetail(id: number): Promise<StudentDetail> {
    return this.get<StudentDetail>(`/students/${id}/`)
  }

  // Создание нового студента
  async createStudent(data: StudentCreateUpdate): Promise<StudentDetail> {
    return this.post<StudentDetail>('/students/', data)
  }

  // Обновление студента
  async updateStudent(id: number, data: Partial<StudentCreateUpdate>): Promise<StudentDetail> {
    return this.patch<StudentDetail>(`/students/${id}/`, data)
  }

  // Удаление студента
  async deleteStudent(id: number): Promise<void> {
    return this.deleteRequest<void>(`/students/${id}/`)
  }

  // Получение статистики по студентам
  async getStatistics(filters?: StudentFilters): Promise<StudentStatistics> {
    return this.get<StudentStatistics>('/students/statistics/', filters)
  }

  // Проверка права на следующую аттестацию
  async checkAttestationEligibility(id: number): Promise<{
    eligible: boolean
    next_level: string | null
    reason: string
  }> {
    return this.get(`/students/${id}/attestation-eligibility/`)
  }

  // Поиск студентов
  async searchStudents(query: string, filters?: Partial<StudentFilters>): Promise<PaginatedResponse<Student>> {
    return this.get<PaginatedResponse<Student>>('/students/search/', {
      q: query,
      ...filters
    })
  }

  // Получение истории аттестаций студента
  async getAttestationHistory(id: number): Promise<StudentDetail['attestations']> {
    return this.get(`/students/${id}/attestations/`)
  }

  // Перевод студента в другой клуб
  async transferStudent(id: number, newClubId: number): Promise<StudentDetail> {
    return this.post<StudentDetail>(`/students/${id}/transfer/`, {
      club: newClubId
    })
  }

  // Экспорт данных студентов
  async exportStudents(filters?: StudentFilters, format: 'csv' | 'xlsx' = 'csv'): Promise<Blob> {
    const params = { ...filters, format }
    const response = await this.client.get('/students/export/', {
      params,
      responseType: 'blob'
    })
    return response.data
  }

  // Импорт студентов из файла
  async importStudents(
    file: File, 
    onProgress?: (progress: number) => void
  ): Promise<{ 
    success: number
    errors: string[]
    total: number 
  }> {
    return this.uploadFile('/students/import/', file, onProgress)
  }

  // Массовые операции
  async bulkDelete(ids: number[]): Promise<{ deleted: number; errors: string[] }> {
    return this.post('/students/bulk-delete/', { ids })
  }

  async bulkUpdate(
    ids: number[], 
    data: Partial<StudentCreateUpdate>
  ): Promise<{ updated: number; errors: string[] }> {
    return this.post('/students/bulk-update/', { ids, data })
  }

  // Получение студентов по клубу
  async getByClub(clubId: number, filters?: Partial<StudentFilters>): Promise<PaginatedResponse<Student>> {
    return this.get<PaginatedResponse<Student>>('/students/', {
      club: clubId,
      ...filters
    })
  }

  // Получение недавно добавленных студентов
  async getRecent(limit = 10): Promise<Student[]> {
    const response = await this.get<PaginatedResponse<Student>>('/students/', {
      ordering: '-created_at',
      limit
    })
    return response.results
  }

  // Получение студентов с днем рождения сегодня
  async getBirthdayToday(): Promise<Student[]> {
    return this.get('/students/birthday-today/')
  }

  // Получение студентов готовых к аттестации
  async getReadyForAttestation(): Promise<Student[]> {
    return this.get('/students/ready-for-attestation/')
  }
}

// Экспортируем экземпляр сервиса
export const studentsService = new StudentsService()

// Экспортируем класс для возможности создания других экземпляров
export default StudentsService 