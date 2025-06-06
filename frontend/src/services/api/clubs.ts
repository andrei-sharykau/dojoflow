/**
 * API сервис для клубов
 */

import { BaseApiService } from './base'
import { useApi } from '@/composables/useApi'
import { API_ENDPOINTS } from '@/constants/api'
import type { 
  Club, 
  ClubDetail, 
  ClubWithStudents, 
  ClubStatistics,
  ClubPermissions,
  ClubCreateUpdate
} from '@/types'

export class ClubsApiService extends BaseApiService {
  constructor() {
    super('http://localhost:8000/api', '/clubs/')
  }

  private getApi() {
    return useApi()
  }

  async getAllClubs(): Promise<Club[]> {
    const response = await this.get<{ results: Club[] }>('/clubs/')
    return response.results || []
  }

  async getDetail(id: number): Promise<ClubDetail> {
    return await this.get<ClubDetail>(`/clubs/${id}/`)
  }

  async getStudentsByClub(search?: string): Promise<ClubWithStudents[]> {
    const api = this.getApi()
    const params = search ? { search } : {}
    return await api.get<ClubWithStudents[]>(API_ENDPOINTS.CLUBS_STUDENTS, params)
  }

  async getStatistics(id: number): Promise<ClubStatistics> {
    return await this.get<ClubStatistics>(`/clubs/${id}/statistics/`)
  }

  async getPermissions(id: number): Promise<ClubPermissions> {
    return await this.get<ClubPermissions>(`/clubs/${id}/permissions/`)
  }

  async createClub(data: ClubCreateUpdate): Promise<Club> {
    return await this.post<Club>('/clubs/', data)
  }

  async updateClub(id: number, data: Partial<ClubCreateUpdate>): Promise<Club> {
    return await this.patch<Club>(`/clubs/${id}/`, data)
  }

  async deleteClub(id: number): Promise<void> {
    await this.deleteRequest(`/clubs/${id}/`)
  }
}

export const clubsAPI = new ClubsApiService() 