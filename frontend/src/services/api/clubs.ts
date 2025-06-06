/**
 * API сервис для клубов
 */

import { BaseApiService } from './base'
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
    super(API_ENDPOINTS.CLUBS)
  }

  async getAllClubs(): Promise<Club[]> {
    const response = await super.getAll<Club>()
    return response.results || []
  }

  async getDetail(id: number): Promise<ClubDetail> {
    return await this.getById<ClubDetail>(id)
  }

  async getStudentsByClub(search?: string): Promise<ClubWithStudents[]> {
    const api = this.getApi()
    const params = search ? { search } : {}
    return await api.get<ClubWithStudents[]>(API_ENDPOINTS.CLUBS_STUDENTS, params)
  }

  async getStatistics(id: number): Promise<ClubStatistics> {
    const api = this.getApi()
    return await api.get<ClubStatistics>(`${this.endpoint}${id}/statistics/`)
  }

  async getPermissions(id: number): Promise<ClubPermissions> {
    const api = this.getApi()
    return await api.get<ClubPermissions>(`${this.endpoint}${id}/permissions/`)
  }

  async createClub(data: ClubCreateUpdate): Promise<Club> {
    return await this.create<Club, ClubCreateUpdate>(data)
  }

  async updateClub(id: number, data: Partial<ClubCreateUpdate>): Promise<Club> {
    return await this.update<Club, ClubCreateUpdate>(id, data)
  }

  async deleteClub(id: number): Promise<void> {
    await this.delete(id)
  }
}

export const clubsAPI = new ClubsApiService() 